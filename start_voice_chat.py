#!/usr/bin/env python3
"""
Voice Chat Launcher for Solvine Systems
Quick launcher for voice conversations with Aiven & Solvine
"""

import asyncio
import sys
import os
from pathlib import Path

# Ensure we can import our modules
sys.path.append(str(Path(__file__).parent))

try:
    from agent_voice_handler import AgentVoiceHandler
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all voice integration files are in the same directory.")
    sys.exit(1)

def main():
    """Main launcher function"""
    print("🎤 Solvine Systems Voice Chat")
    print("=" * 40)
    print("🤗 Aiven - Your emotional support agent")
    print("🧭 Solvine - Your coordination agent")
    print("=" * 40)
    print()
    
    try:
        # Start voice conversation
        handler = AgentVoiceHandler()
        asyncio.run(handler.start_voice_conversation())
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Voice chat ended.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure your microphone is connected and working")
        print("2. Check that all required libraries are installed")
        print("3. Try running: python voice_integration.py")

if __name__ == "__main__":
    main()
