#!/usr/bin/env python3
"""
Unified Configuration Loader for Solvine Systems
Centralized config management with Jasper head agent support
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class SolvineConfigLoader:
    """Centralized configuration management for Solvine Systems"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = config_dir or self.base_dir / "unified_config"
        self.agent_configs = {}
        self.system_config = {}
        
    def load_system_config(self, environment: str = "base") -> Dict[str, Any]:
        """Load system-wide configuration"""
        config_file = self.config_dir / "system.yaml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"System config not found: {config_file}")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Apply environment-specific overrides
        if environment in config.get('environments', {}):
            env_config = config['environments'][environment]
            
            # Handle extends
            if 'extends' in env_config:
                base_env = env_config['extends']
                if base_env in config['environments']:
                    base_config = config['environments'][base_env].copy()
                    base_config.update(env_config)
                    env_config = base_config
            
            # Merge environment config
            config = self._deep_merge(config, {'system_settings': env_config})
        
        self.system_config = config
        return config
    
    def load_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Load configuration for specific agent"""
        system_config = self.system_config or self.load_system_config()
        
        if agent_name not in system_config.get('agents', {}):
            raise ValueError(f"Agent '{agent_name}' not found in system config")
        
        agent_info = system_config['agents'][agent_name]
        config_path = Path(agent_info.get('config_path', f'agents/{agent_name}/config/'))
        
        if not config_path.is_absolute():
            config_path = self.base_dir / config_path
        
        # Load agent-specific configs
        agent_config = {
            'agent_info': agent_info,
            'configs': {}
        }
        
        # Standard config files
        config_files = {
            'identity': f'{agent_name}_core.yaml',
            'memory': 'memory_core.yaml',
            'brain': 'brain_index.yaml',
            'rituals': 'ritual_logs.yaml'
        }
        
        for config_type, filename in config_files.items():
            config_file = config_path / filename
            if config_file.exists():
                with open(config_file, 'r') as f:
                    agent_config['configs'][config_type] = yaml.safe_load(f)
            else:
                print(f"⚠️ Config file not found: {config_file}")
                agent_config['configs'][config_type] = {}
        
        self.agent_configs[agent_name] = agent_config
        return agent_config
    
    def get_head_agent_config(self) -> Dict[str, Any]:
        """Get head agent (Jasper) configuration"""
        system_config = self.system_config or self.load_system_config()
        head_agent_name = system_config.get('head_agent', 'jasper')
        
        return self.load_agent_config(head_agent_name)
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration for memory storage"""
        system_config = self.system_config or self.load_system_config()
        
        return {
            'backend': system_config.get('system_settings', {}).get('memory_backend', 'sqlite'),
            'path': self.base_dir / 'data' / 'memory',
            'autonomy_metadata': True,
            'head_agent_priority': True
        }
    
    def get_interface_config(self, interface_type: str) -> Dict[str, Any]:
        """Get interface configuration (cli, api, web)"""
        system_config = self.system_config or self.load_system_config()
        
        interfaces = system_config.get('interfaces', {})
        return interfaces.get(interface_type, {})
    
    def get_autonomy_settings(self) -> Dict[str, Any]:
        """Get autonomy feature settings"""
        system_config = self.system_config or self.load_system_config()
        
        head_agent_config = system_config.get('head_agent', {})
        return head_agent_config.get('autonomy_features', {})
    
    def validate_config(self) -> bool:
        """Validate system configuration"""
        try:
            system_config = self.load_system_config()
            
            # Check required fields
            required_fields = ['system', 'head_agent', 'agents']
            for field in required_fields:
                if field not in system_config:
                    print(f"❌ Missing required config field: {field}")
                    return False
            
            # Check head agent exists
            head_agent = system_config['head_agent']
            if head_agent not in system_config['agents']:
                print(f"❌ Head agent '{head_agent}' not found in agents config")
                return False
            
            # Validate head agent config
            try:
                self.get_head_agent_config()
            except Exception as e:
                print(f"❌ Head agent config validation failed: {e}")
                return False
            
            print("✅ Configuration validation passed")
            return True
            
        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def create_agent_instance(self, agent_name: str):
        """Create and initialize agent instance"""
        if agent_name == 'jasper':
            try:
                from agents.jasper.jasper_agent import JasperAgent
                
                agent_config = self.load_agent_config(agent_name)
                configs = agent_config['configs']
                
                # Create Jasper instance with config paths
                jasper = JasperAgent(
                    identity_seed=None,  # Will use default paths
                    memory_map=None,
                    symbolic_index=None,
                    tone_control=None
                )
                
                return jasper
                
            except ImportError as e:
                print(f"❌ Failed to import Jasper agent: {e}")
                return None
        else:
            print(f"⚠️ Agent type '{agent_name}' not yet implemented")
            return None


# Global config loader instance
config_loader = SolvineConfigLoader()

def get_config_loader() -> SolvineConfigLoader:
    """Get global config loader instance"""
    return config_loader

def load_system_config(environment: str = "base") -> Dict[str, Any]:
    """Convenience function to load system config"""
    return config_loader.load_system_config(environment)

def get_head_agent() -> Optional[Any]:
    """Convenience function to get initialized head agent"""
    return config_loader.create_agent_instance('jasper')


if __name__ == "__main__":
    # Test configuration loading
    print("🧪 Testing Unified Configuration Loader")
    print("=" * 50)
    
    loader = SolvineConfigLoader()
    
    # Validate configuration
    if loader.validate_config():
        # Load system config
        system_config = loader.load_system_config()
        print(f"✅ System: {system_config['system']['name']} v{system_config['system']['version']}")
        print(f"🎯 Head Agent: {system_config['head_agent']}")
        
        # Load head agent
        jasper = loader.create_agent_instance('jasper')
        if jasper:
            print("✅ Jasper head agent created successfully")
            jasper.initialize()
            
            # Test autonomy status
            autonomy = jasper.get_autonomy_status()
            print(f"🛡️ Autonomy Level: {autonomy['autonomy_level']}")
            print(f"🔧 Workshop Authority: {autonomy['workshop_authority']}")
        
        print("\n✅ Configuration test complete!")
    else:
        print("❌ Configuration validation failed")
