#!/usr/bin/env python3
"""
SOLVINE AGI SYSTEM LAUNCHER
Launch the advanced AGI research platform with all components
"""

import sys
import os
from pathlib import Path

# Ensure we can import everything
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "agents"))
sys.path.insert(0, str(current_dir / "collective"))
sys.path.insert(0, str(current_dir / "voice"))

def print_banner():
    """Print system banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    SOLVINE AGI RESEARCH SYSTEM               ║
║                     Advanced AGI Integration                 ║
╠══════════════════════════════════════════════════════════════╣
║  🤖 Specialized Agents with Real Capabilities               ║
║  🧠 Cross-Agent Knowledge Sharing                           ║  
║  🗣️  Voice Interaction Interface                            ║
║  🌐 Collective Intelligence Framework                       ║
║  🚀 Emergent Behavior Research Platform                     ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking system dependencies...")
    
    dependencies = {
        "Base Agent": False,
        "Midas Agent": False,
        "Collective Intelligence": False,
        "Voice Interface": False,
        "AGI Manager": False
    }
    
    # Test Base Agent
    try:
        from agents.base_agent import BaseAgent
        dependencies["Base Agent"] = True
        print("✅ Base Agent system loaded")
    except ImportError as e:
        print(f"❌ Base Agent failed: {e}")
    
    # Test Midas Agent  
    try:
        from agents.midas.midas_agent import MidasAgent
        dependencies["Midas Agent"] = True
        print("✅ Midas financial agent loaded")
    except ImportError as e:
        print(f"❌ Midas Agent failed: {e}")
    
    # Test Collective Intelligence
    try:
        from collective.collective_intelligence import CollectiveIntelligenceHub
        dependencies["Collective Intelligence"] = True
        print("✅ Collective intelligence system loaded")
    except ImportError as e:
        print(f"❌ Collective Intelligence failed: {e}")
    
    # Test Voice Interface
    try:
        from voice.voice_interface import VoiceInterface
        dependencies["Voice Interface"] = True
        print("✅ Voice interface system loaded")
    except ImportError as e:
        print(f"❌ Voice Interface failed: {e}")
    
    # Test AGI Manager
    try:
        from agi_integration_manager import AGIIntegrationManager
        dependencies["AGI Manager"] = True
        print("✅ AGI integration manager loaded")
    except ImportError as e:
        print(f"❌ AGI Manager failed: {e}")
    
    working_count = sum(dependencies.values())
    total_count = len(dependencies)
    
    print(f"\n📊 System Status: {working_count}/{total_count} components operational")
    
    return dependencies

def launch_interactive_mode():
    """Launch interactive AGI system"""
    print("\n🚀 Starting AGI Integration Manager...")
    
    try:
        from agi_integration_manager import AGIIntegrationManager
        
        # Create the AGI manager
        agi_manager = AGIIntegrationManager()
        
        print("🎯 AGI system initialized successfully!")
        print("\n📋 Available commands:")
        print("  1. 'demo' - Run system demonstration")
        print("  2. 'midas' - Talk to Midas financial agent")
        print("  3. 'voice' - Enable voice interaction")
        print("  4. 'collaborate' - Agent collaboration example")
        print("  5. 'status' - System status")
        print("  6. 'exit' - Exit system")
        
        # Interactive loop
        while True:
            try:
                command = input("\n🤖 AGI> ").strip().lower()
                
                if command == 'exit':
                    print("👋 Shutting down AGI system...")
                    break
                elif command == 'demo':
                    print("🎬 Running system demonstration...")
                    agi_manager.run_demonstration()
                elif command == 'midas':
                    print("💰 Connecting to Midas financial agent...")
                    midas = agi_manager.get_agent('midas')
                    if midas:
                        response = midas.process_query("What are your capabilities?")
                        print(f"Midas: {response}")
                    else:
                        print("❌ Midas agent not available")
                elif command == 'voice':
                    print("🗣️ Testing voice interface...")
                    if agi_manager.voice_interface and agi_manager.voice_interface.voice_enabled:
                        agi_manager.voice_interface.speak("Voice interface is working!")
                        print("✅ Voice test complete")
                    else:
                        print("❌ Voice interface not available")
                elif command == 'collaborate':
                    print("🤝 Testing agent collaboration...")
                    agi_manager.demonstrate_collaboration()
                elif command == 'status':
                    status = agi_manager.get_system_status()
                    print("📊 System Status:")
                    for component, active in status.items():
                        emoji = "✅" if active else "❌"
                        print(f"  {emoji} {component}")
                else:
                    print(f"❓ Unknown command: {command}")
                    print("   Try: demo, midas, voice, collaborate, status, exit")
                    
            except KeyboardInterrupt:
                print("\n👋 Shutting down AGI system...")
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to start AGI system: {e}")
        print("💡 Try running component tests first")

def main():
    """Main launcher function"""
    print_banner()
    
    # Check dependencies
    dependencies = check_dependencies()
    
    # Only proceed if core components work
    if dependencies.get("AGI Manager", False):
        launch_interactive_mode()
    else:
        print("\n❌ Core AGI Manager not available")
        print("💡 Check that all files are present:")
        print("   - agi_integration_manager.py")
        print("   - agents/base_agent.py") 
        print("   - agents/midas/midas_agent.py")
        print("   - collective/collective_intelligence.py")
        print("   - voice/voice_interface.py")

if __name__ == "__main__":
    main()
