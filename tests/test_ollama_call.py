import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ollama_model import OllamaModel

def run_test():
    model = OllamaModel(model_name="llama3")  # or "mistral" if that’s what’s loaded
    prompt = "What is Project Phoenix and how does it support human-machine autonomy?"

    try:
        result = model.generate(prompt)
        print("✅ RESPONSE:")
        if hasattr(result, '__iter__') and not isinstance(result, str):
            # Streaming/generator output
            for chunk in result:
                print(chunk, end='', flush=True)
            print()
        else:
            print(result)
    except Exception as e:
        print("❌ ERROR:")
        print(e)

if __name__ == "__main__":
    run_test()
