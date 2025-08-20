#!/usr/bin/env python3
"""
Solvine Loader (LangChain/Ollama-ready)
- Prioritizes mission_core + environment_profile for retrieval
- Loads agent tone files as system prompts
- Provides a minimal AgentRouter you can plug into LangChain or use directly
"""
import os, json, glob
from pathlib import Path

# Optional imports: only required if you wire into LangChain/Ollama
try:
    from langchain_community.chat_models import ChatOllama  # pip install langchain-community
    from langchain.schema import SystemMessage, HumanMessage
    HAVE_LANGCHAIN = True
except Exception:
    HAVE_LANGCHAIN = False

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT
AGENTS_DIR = ROOT / "agents"

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def load_core():
    mission = read_text(DATA_DIR / "mission_core.yaml")
    env = read_text(DATA_DIR / "environment_profile.yaml")
    baseline = read_text(ROOT / "baselines" / "post_upgrade_baseline.yaml")
    return {"mission_core": mission, "environment_profile": env, "baseline": baseline}

def load_agents():
    tones = {}
    for p in sorted(AGENTS_DIR.glob("*_tone.txt")):
        name = p.stem.replace("_tone", "")
        tones[name.lower()] = read_text(p).strip()
    return tones

class AgentRouter:
    def __init__(self, model_name: str = "llama3:instruct", temperature: float = 0.3):
        self.model_name = model_name
        self.temperature = temperature
        self.tones = load_agents()
        self.core = load_core()
        self._llm = None
        if HAVE_LANGCHAIN:
            try:
                self._llm = ChatOllama(model=self.model_name, temperature=self.temperature)
            except Exception:
                self._llm = None  # Let users wire their own LLM

    def system_prompt_for(self, agent: str) -> str:
        agent = agent.lower()
        tone = self.tones.get(agent, "")
        core_bits = [
            "# Solvine Mission Core",
            self.core["mission_core"],
            "# Environment Profile",
            self.core["environment_profile"],
            "# Baseline Note",
            self.core["baseline"],
            "# Tone Anchor",
            tone,
            "# Context Integrity Protocols",
            "- Use [FLAG] when memory is uncertain or suggestions are generic.",
            "- Respect environment constraints (no porch suggestions; patio ok).",
            "- Reload last stored tone if drift is detected (panic button).",
        ]
        return "\n".join([b for b in core_bits if b])

    def reply(self, agent: str, user_text: str) -> str:
        sys_prompt = self.system_prompt_for(agent)
        # If LangChain/Ollama is available, use it; otherwise return the assembled prompt for inspection
        if HAVE_LANGCHAIN and self._llm is not None:
            msgs = [SystemMessage(content=sys_prompt), HumanMessage(content=user_text)]
            return self._llm.invoke(msgs).content
        else:
            return f"[DRY RUN]\nSystem Prompt for {agent}:\n{sys_prompt}\n\nUser:\n{user_text}\n"

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Solvine Agent Router")
    ap.add_argument("--agent", default="solvine", help="Agent name (solvine, jasper, aiven, veilsynth, halcyon, midas, quanta)")
    ap.add_argument("--model", default="llama3:instruct", help="Ollama model name")
    ap.add_argument("--temp", type=float, default=0.3)
    ap.add_argument("prompt", nargs="*", help="User prompt")
    args = ap.parse_args()

    router = AgentRouter(model_name=args.model, temperature=args.temp)
    text = " ".join(args.prompt) if args.prompt else "Give me a quick mission summary."
    out = router.reply(args.agent, text)
    print(out)
