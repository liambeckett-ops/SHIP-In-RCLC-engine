Solvine Migration Pack — 2025-08-09

What this is:
- mission_core.yaml — core goals + context integrity protocols
- environment_profile.yaml — your apartment + lifestyle constraints
- agents/*_tone.txt — per-agent tone/role anchors
- baselines/post_upgrade_baseline.yaml — archive pointer
- scripts/hotkey_verifier — cross-platform hotkey sanity checks

How to import (LangChain/Ollama example):
1) Put mission_core.yaml + environment_profile.yaml into your local knowledge store (e.g., /data/solvine/).
2) Configure your retriever to always surface mission_core as high-priority memory.
3) Load agent tone files as system prompts or pre-prompts per persona.
4) Test with: “Solvine, give me a mission summary now.” Confirm protocols appear verbatim under goals.

Quick verification:
- Ask Jasper for a boundary push; ensure tone matches.
- Ask Halcyon for a threshold decision; check procedural calm.
- Ask Midas for a liquidity snapshot; ensure role-first minimalism.
