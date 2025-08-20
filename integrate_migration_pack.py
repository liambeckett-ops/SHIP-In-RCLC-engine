#!/usr/bin/env python3
"""
Solvine Migration Integration
Integrates the migration pack with existing Solvine Systems
"""
import os
import sys
import json
import shutil
from pathlib import Path

# Add the migration pack to the Python path
sys.path.insert(0, str(Path(__file__).parent / "migration_pack"))

try:
    from migration_pack.solvine_loader import AgentRouter, load_core, load_agents
    print("✅ Migration pack successfully imported")
except ImportError as e:
    print(f"❌ Failed to import migration pack: {e}")
    sys.exit(1)

class SolvineIntegration:
    """Integrates migration pack with existing Solvine Systems"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.migration_dir = self.root_dir / "migration_pack"
        self.voice_dir = self.root_dir / "voice"
        self.config_dir = self.root_dir / "config"
        
    def integrate_voice_profiles(self):
        """Integrate agent tone profiles with voice system"""
        print("🎙️ Integrating voice profiles...")
        
        # Load the voice config system
        voice_config_path = self.voice_dir / "voice_config.py"
        if voice_config_path.exists():
            # Read current voice config
            with open(voice_config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Load agent tones from migration pack
            agents = load_agents()
            
            # Update voice_config.py to include agent tone descriptions
            print(f"   Found {len(agents)} agent tone profiles")
            for agent_name, tone_content in agents.items():
                print(f"   - {agent_name}: Tone profile loaded")
        
        return True
    
    def integrate_mission_core(self):
        """Integrate mission core with existing config"""
        print("🎯 Integrating mission core...")
        
        core_data = load_core()
        
        # Save mission core to config directory
        mission_file = self.config_dir / "mission_core.yaml"
        env_file = self.config_dir / "environment_profile.yaml"
        
        if core_data['mission_core']:
            with open(mission_file, 'w', encoding='utf-8') as f:
                f.write(core_data['mission_core'])
            print(f"   ✅ Mission core saved to {mission_file}")
        
        if core_data['environment_profile']:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(core_data['environment_profile'])
            print(f"   ✅ Environment profile saved to {env_file}")
        
        return True
    
    def setup_agent_router(self):
        """Set up the agent router system"""
        print("🤖 Setting up agent router...")
        
        # Copy the loader to the main directory for easy access
        loader_dest = self.root_dir / "solvine_agent_router.py"
        loader_src = self.migration_dir / "solvine_loader.py"
        
        shutil.copy2(loader_src, loader_dest)
        print(f"   ✅ Agent router available at {loader_dest}")
        
        # Create a config file for the router
        config_dest = self.root_dir / "agent_router_config.json"
        config_src = self.migration_dir / "solvine_config.json"
        
        shutil.copy2(config_src, config_dest)
        print(f"   ✅ Router config available at {config_dest}")
        
        return True
    
    def verify_integration(self):
        """Verify the integration is working"""
        print("🔍 Verifying integration...")
        
        try:
            # Test agent router
            router = AgentRouter()
            available_agents = list(router.tones.keys())
            print(f"   ✅ Agent router working with {len(available_agents)} agents")
            print(f"   Available agents: {', '.join(available_agents)}")
            
            # Test system prompt generation
            test_prompt = router.system_prompt_for("jasper")
            if "mission_core" in test_prompt.lower():
                print("   ✅ Mission core integration working")
            if "environment_profile" in test_prompt.lower():
                print("   ✅ Environment profile integration working")
            
            return True
        except Exception as e:
            print(f"   ❌ Integration verification failed: {e}")
            return False
    
    def run_integration(self):
        """Run the complete integration process"""
        print("🚀 Starting Solvine Migration Integration...\n")
        
        try:
            self.integrate_voice_profiles()
            print()
            
            self.integrate_mission_core()
            print()
            
            self.setup_agent_router()
            print()
            
            if self.verify_integration():
                print("\n🎉 Integration completed successfully!")
                print("\nNext steps:")
                print("1. Test agent router: python solvine_agent_router.py --agent jasper 'Hello'")
                print("2. Update voice system to use new agent profiles")
                print("3. Replace placeholder files with your actual agent data")
                return True
            else:
                print("\n⚠️  Integration completed with warnings")
                return False
                
        except Exception as e:
            print(f"\n❌ Integration failed: {e}")
            return False

if __name__ == "__main__":
    integrator = SolvineIntegration()
    success = integrator.run_integration()
    sys.exit(0 if success else 1)
