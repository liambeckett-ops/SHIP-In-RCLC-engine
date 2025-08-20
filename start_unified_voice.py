#!/usr/bin/env python3
"""
Unified Voice Chat Launcher
Start talking to your Solvine System with one unified voice
"""

import asyncio
import sys
import os
from pathlib import Path

# Ensure we can import our modules
sys.path.append(str(Path(__file__).parent))

try:
    from unified_voice_system import UnifiedVoiceSystem
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure unified_voice_system.py is in the same directory.")
    sys.exit(1)

def main():
    """Main launcher function"""
    print("🧠 Solvine Systems - Unified Voice Interface")
    print("=" * 50)
    print("🎭 One voice, seven specialized agents working together")
    print("🗣️ Real-time voice conversation")
    print("🧠 Intelligent agent coordination")
    print()
    print("Available agent specializations:")
    print("🧭 Solvine - Coordination & Strategy")
    print("🤗 Aiven - Emotional Intelligence") 
    print("💰 Midas - Financial Analysis")
    print("⚖️ Jasper - Ethics & Philosophy")
    print("🎨 VeilSynth - Creativity & Analysis")
    print("🛡️ Halcyon - Safety & Security")
    print("🔢 Quanta - Logic & Computation")
    print("=" * 50)
    print()
    
    try:
        # Start unified voice system
        system = UnifiedVoiceSystem()
        asyncio.run(system.start_conversation())
        
    except KeyboardInterrupt:
        print("\n👋 Unified voice system shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Ensure microphone is connected and working")
        print("2. Check that speech recognition libraries are installed")
        print("3. Try: python unified_voice_system.py")

if __name__ == "__main__":
    main()
