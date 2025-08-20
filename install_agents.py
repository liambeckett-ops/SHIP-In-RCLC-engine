#!/usr/bin/env python3
"""
Solvine Agent Installation Manager
Handles installation and integration of new agent zip files
"""

import zipfile
import os
import shutil
import json
from pathlib import Path
from typing import List, Dict, Optional

class AgentInstaller:
    """Manages installation of new agent packages"""
    
    def __init__(self, solvine_root: str = None):
        if solvine_root:
            self.solvine_root = Path(solvine_root)
        else:
            self.solvine_root = Path(__file__).parent
        
        self.agents_dir = self.solvine_root / "agents"
        self.memory_dir = self.solvine_root / "memory" / "agent_memories"
        self.config_dir = self.solvine_root / "config"
        
        # Ensure directories exist
        self.agents_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
    
    def discover_agent_zips(self, search_dir: str = None) -> List[Path]:
        """Find all agent zip files in directory"""
        if search_dir:
            search_path = Path(search_dir)
        else:
            search_path = self.solvine_root
        
        zip_files = list(search_path.glob("**/*.zip"))
        agent_zips = []
        
        for zip_file in zip_files:
            name = zip_file.stem.lower()
            if any(agent in name for agent in ['aiven', 'halcyon', 'veilsynth', 'quanta']):
                agent_zips.append(zip_file)
        
        return agent_zips
    
    def install_agent_zip(self, zip_path: Path) -> bool:
        """Install agent from zip file"""
        agent_name = self.extract_agent_name(zip_path)
        if not agent_name:
            print(f"❌ Could not determine agent name from {zip_path.name}")
            return False
        
        agent_dir = self.agents_dir / agent_name
        
        try:
            print(f"📦 Installing {agent_name.title()} from {zip_path.name}...")
            
            # Remove existing agent directory if it exists
            if agent_dir.exists():
                print(f"🗑️ Removing existing {agent_name} directory...")
                shutil.rmtree(agent_dir)
            
            # Extract zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract to temporary location first
                temp_dir = self.solvine_root / f"temp_{agent_name}"
                zip_ref.extractall(temp_dir)
                
                # Find the actual agent files (they might be in a subdirectory)
                agent_files = self.find_agent_files(temp_dir)
                if agent_files:
                    # Move agent files to proper location
                    shutil.move(str(agent_files), str(agent_dir))
                    print(f"✅ {agent_name.title()} installed to {agent_dir}")
                else:
                    print(f"❌ No agent files found in {zip_path.name}")
                    return False
                
                # Clean up temp directory
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
            
            # Initialize agent configuration
            self.initialize_agent_config(agent_name)
            
            return True
            
        except Exception as e:
            print(f"❌ Installation failed for {agent_name}: {e}")
            return False
    
    def extract_agent_name(self, zip_path: Path) -> Optional[str]:
        """Extract agent name from zip filename"""
        name = zip_path.stem.lower()
        
        for agent in ['aiven', 'halcyon', 'veilsynth', 'quanta']:
            if agent in name:
                return agent
        
        return None
    
    def find_agent_files(self, search_dir: Path) -> Optional[Path]:
        """Find the directory containing agent files"""
        # Look for Python files or directories that look like agent code
        for item in search_dir.rglob("*"):
            if item.is_dir():
                # Check if directory contains agent-like files
                py_files = list(item.glob("*.py"))
                if py_files:
                    # Check for agent-specific files
                    file_names = [f.name.lower() for f in py_files]
                    if any(name.endswith('_agent.py') or 'agent' in name for name in file_names):
                        return item
        
        # Fallback: return first directory with Python files
        for item in search_dir.rglob("*.py"):
            return item.parent
        
        return None
    
    def initialize_agent_config(self, agent_name: str):
        """Initialize configuration for newly installed agent"""
        try:
            # Create memory file
            memory_file = self.memory_dir / f"{agent_name}_memories.json"
            if not memory_file.exists():
                initial_memory = {
                    "agent_name": agent_name,
                    "memories": [],
                    "personality_traits": [],
                    "learned_patterns": [],
                    "created_at": "auto-generated",
                    "version": "1.0"
                }
                with open(memory_file, 'w') as f:
                    json.dump(initial_memory, f, indent=2)
                print(f"💾 Created memory file for {agent_name}")
            
            # Update agent registry (if it exists)
            self.update_agent_registry(agent_name)
            
        except Exception as e:
            print(f"⚠️ Config initialization warning for {agent_name}: {e}")
    
    def update_agent_registry(self, agent_name: str):
        """Update the agent registry with new agent"""
        registry_file = self.config_dir / "agent_registry.json"
        
        try:
            if registry_file.exists():
                with open(registry_file, 'r') as f:
                    registry = json.load(f)
            else:
                registry = {"agents": {}}
            
            # Add new agent to registry
            registry["agents"][agent_name] = {
                "name": agent_name.title(),
                "type": "specialized_agent",
                "status": "installed",
                "capabilities": [],
                "install_date": "auto-generated"
            }
            
            with open(registry_file, 'w') as f:
                json.dump(registry, f, indent=2)
            
            print(f"📋 Updated agent registry for {agent_name}")
            
        except Exception as e:
            print(f"⚠️ Registry update warning: {e}")
    
    def list_installed_agents(self):
        """List all currently installed agents"""
        print("\n🤖 INSTALLED AGENTS:")
        print("="*30)
        
        for agent_dir in self.agents_dir.iterdir():
            if agent_dir.is_dir() and not agent_dir.name.startswith('__'):
                status = "✅ Active" if (agent_dir / f"{agent_dir.name}_agent.py").exists() else "⚠️ Incomplete"
                print(f"   {agent_dir.name.title()}: {status}")
    
    def install_all_discovered_zips(self, search_dir: str = None):
        """Install all discovered agent zip files"""
        zip_files = self.discover_agent_zips(search_dir)
        
        if not zip_files:
            print("📦 No agent zip files found")
            return
        
        print(f"📦 Found {len(zip_files)} agent zip files:")
        for zip_file in zip_files:
            print(f"   {zip_file.name}")
        
        confirm = input(f"\nInstall all {len(zip_files)} agents? (y/n): ").lower().strip()
        if confirm == 'y':
            successful = 0
            for zip_file in zip_files:
                if self.install_agent_zip(zip_file):
                    successful += 1
            
            print(f"\n✅ Successfully installed {successful}/{len(zip_files)} agents")
            self.list_installed_agents()
        else:
            print("Installation cancelled")
    
    def interactive_install(self):
        """Interactive installation interface"""
        print("\n🤖 SOLVINE AGENT INSTALLER")
        print("="*40)
        
        while True:
            print("\nOptions:")
            print("1. Discover and install agent zips")
            print("2. Install specific zip file")
            print("3. List installed agents")
            print("4. Clean old agent data")
            print("5. Exit")
            
            choice = input("\nChoice (1-5): ").strip()
            
            if choice == '1':
                self.install_all_discovered_zips()
            elif choice == '2':
                zip_path = input("Path to zip file: ").strip()
                if os.path.exists(zip_path):
                    self.install_agent_zip(Path(zip_path))
                else:
                    print("❌ File not found")
            elif choice == '3':
                self.list_installed_agents()
            elif choice == '4':
                self.clean_old_data()
            elif choice == '5':
                break
            else:
                print("Invalid choice")
    
    def clean_old_data(self):
        """Clean old agent data"""
        print("🧹 Cleaning old agent data...")
        
        # Remove old memory files
        old_memories = self.memory_dir.glob("*_memories.json")
        removed = 0
        for memory_file in old_memories:
            agent_name = memory_file.stem.replace('_memories', '')
            if agent_name in ['aiven', 'halcyon', 'veilsynth', 'quanta']:
                memory_file.unlink()
                removed += 1
                print(f"🗑️ Removed old {agent_name} memory file")
        
        print(f"✅ Cleaned {removed} old memory files")

def main():
    """Main installer interface"""
    print("🤖 Solvine Systems Agent Installer")
    
    # Auto-detect Solvine root directory
    current_dir = Path(__file__).parent
    installer = AgentInstaller(current_dir)
    
    installer.interactive_install()

if __name__ == "__main__":
    main()
