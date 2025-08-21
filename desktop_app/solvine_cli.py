import argparse
import sys
import os
from chat_memory import ChatMemory
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

def get_agent_response(user_input):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": user_input,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "[Ollama error: No response]")
    except Exception as e:
        return f"[Ollama error: {e}]"

def main():
    parser = argparse.ArgumentParser(description="Solvine CLI Agent")
    parser.add_argument('--prompt', type=str, help='Prompt to send to the agent')
    parser.add_argument('--history', action='store_true', help='Show conversation history')
    parser.add_argument('--search', type=str, help='Search conversation history')
    args = parser.parse_args()

    memory = ChatMemory()

    if args.history:
        history = memory.get_history(limit=100)
        for timestamp, sender, message in history:
            print(f"{timestamp} | {sender}: {message}")
        sys.exit(0)

    if args.search:
        results = memory.search_messages(args.search, limit=100)
        print(f"Search results for '{args.search}':\n")
        for timestamp, sender, message in results:
            print(f"{timestamp} | {sender}: {message}")
        sys.exit(0)

    if args.prompt:
        print(f"You: {args.prompt}")
        memory.add_message("You", args.prompt)
        response = get_agent_response(args.prompt)
        print(f"Solvine: {response}")
        memory.add_message("Solvine", response)
        sys.exit(0)

    # Interactive mode
    print("Welcome to Solvine CLI. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"): break
        memory.add_message("You", user_input)
        response = get_agent_response(user_input)
        print(f"Solvine: {response}")
        memory.add_message("Solvine", response)

if __name__ == "__main__":
    main()
