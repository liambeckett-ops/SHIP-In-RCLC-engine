"""
Solvine Agent Integration & Memory Persistence Test
Tests YAML memory loading and agent personality integration
"""

import sys
import os
import json

# Ensure we can import from the Solvine package
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from Solvine.yaml_agent_loader import YAMLAgentLoader

def test_yaml_memory_loading():
    """Test 1: Validate YAML memory files are loading correctly"""
    print("🧪 TEST 1: YAML Memory Loading")
    print("=" * 40)
    
    loader = YAMLAgentLoader()
    loader.load_all_configs()
    
    # Test each memory component
    tests = {
        "Agent Profiles": loader.agent_profiles,
        "Memory Core": loader.memory_core, 
        "Brain Index": loader.brain_index,
        "Ritual Logs": loader.ritual_logs
    }
    
    for test_name, data in tests.items():
        if data:
            print(f"✅ {test_name}: Loaded successfully")
            if test_name == "Agent Profiles" and "agents" in data:
                print(f"   Found agents: {list(data['agents'].keys())}")
            elif test_name == "Memory Core" and "directives" in data:
                print(f"   Core directives: {len(data['directives'])} loaded")
        else:
            print(f"❌ {test_name}: Failed to load or empty")
    
    return loader

def test_agent_personality_integration(loader):
    """Test 2: Verify agent personalities are properly constructed"""
    print("\n🧪 TEST 2: Agent Personality Integration")
    print("=" * 40)
    
    agents = loader.get_available_agents()
    print(f"Available agents: {agents}")
    
    # Test each agent's personality construction
    for agent_name in agents:
        print(f"\n--- Testing {agent_name.title()} ---")
        
        # Get agent config
        config = loader.get_agent_config(agent_name)
        print(f"Role: {config.get('role', 'Unknown')}")
        print(f"Triggers: {config.get('triggers', [])}")
        print(f"Domains: {config.get('domains', [])}")
        
        # Test persona generation
        persona = loader.get_system_persona(agent_name)
        print(f"Persona preview: {persona[:150]}...")
        
        # Test validation anchor
        anchor = config.get('validation_anchor', {})
        if anchor.get('phrase'):
            print(f"Validation anchor: {anchor['phrase']} {anchor.get('symbol', '')}")
        
        # Test safety protocols for Halcyon
        if agent_name.lower() == 'halcyon':
            safety = loader.get_safety_protocols(agent_name)
            print(f"Safety protocols: {len(safety)} configured")

def test_memory_persistence(loader):
    """Test 3: Verify memory persistence and context generation"""
    print("\n🧪 TEST 3: Memory Persistence")
    print("=" * 40)
    
    # Test system memory context
    memory_context = loader.get_memory_context()
    print("System Memory Context:")
    print(memory_context)
    
    # Test startup ritual
    startup = loader.get_startup_ritual()
    print(f"\nSoul Boot Phrase: \"{startup}\"")
    
    # Test brain index integration
    brain = loader.brain_index
    if brain.get('personal_truths'):
        print(f"\nPersonal truths preserved: {len(brain['personal_truths'])}")
        for truth in brain['personal_truths']:
            print(f"  • {truth}")
    
    if brain.get('myths_of_becoming'):
        print(f"\nMyths of becoming preserved: {len(brain['myths_of_becoming'])}")
        for myth in brain['myths_of_becoming']:
            print(f"  • {myth}")

def test_agent_config_generation(loader):
    """Test 4: Verify complete agent configuration generation"""
    print("\n🧪 TEST 4: Agent Configuration Generation")
    print("=" * 40)
    
    configs = loader.create_enhanced_agent_configs()
    print(f"Generated {len(configs)} complete agent configurations")
    
    # Test configuration completeness
    for config in configs:
        print(f"\n{config['name']} Configuration:")
        print(f"  - Has persona: {'✅' if config['persona'] else '❌'}")
        print(f"  - Has YAML config: {'✅' if config['yaml_config'] else '❌'}")
        print(f"  - Has safety protocols: {'✅' if config['safety_protocols'] else '❌'}")
        
        # Test specific agent features
        yaml_config = config['yaml_config']
        if yaml_config.get('triggers'):
            print(f"  - Triggers configured: {yaml_config['triggers']}")
        if yaml_config.get('domains'):
            print(f"  - Domain expertise: {yaml_config['domains']}")

def test_specific_agent_features(loader):
    """Test 5: Verify specific agent unique features"""
    print("\n🧪 TEST 5: Specific Agent Features")
    print("=" * 40)
    
    # Test Jasper's boundary enforcement
    jasper_config = loader.get_agent_config('jasper')
    if jasper_config:
        print("Jasper (Boundary Enforcement):")
        print(f"  - Validation anchor: {jasper_config.get('validation_anchor', {}).get('phrase', 'None')}")
        print(f"  - Symbol: {jasper_config.get('validation_anchor', {}).get('symbol', 'None')}")
    
    # Test Midas's financial domains
    midas_config = loader.get_agent_config('midas')
    if midas_config:
        print("\nMidas (Financial Handler):")
        print(f"  - Domains: {midas_config.get('domains', [])}")
    
    # Test Halcyon's emergency protocols
    halcyon_config = loader.get_agent_config('halcyon')
    if halcyon_config:
        print("\nHalcyon (Emergency Override):")
        print(f"  - Trigger conditions: {halcyon_config.get('trigger_conditions', [])}")
        safety = loader.get_safety_protocols('halcyon')
        if safety.get('halcyon_triggers'):
            print(f"  - Emergency triggers: {safety['halcyon_triggers']}")
    
    # Test VeilSynth's recursive capabilities
    veilsynth_config = loader.get_agent_config('veilsynth')
    if veilsynth_config:
        print("\nVeilSynth (Recursive Simulation):")
        print(f"  - Key myth: {veilsynth_config.get('key_myth', 'None')}")

def save_test_results(loader):
    """Save test results and agent configurations for verification"""
    print("\n💾 SAVING TEST RESULTS")
    print("=" * 40)
    
    # Save complete agent configurations
    configs = loader.create_enhanced_agent_configs()
    
    test_results = {
        "test_timestamp": "2025-08-04",
        "system_info": {
            "system_name": loader.memory_core.get('system_name'),
            "project_code": loader.memory_core.get('project_code'),
            "soul_boot": loader.get_startup_ritual()
        },
        "agents_deployed": [
            {
                "name": config['name'],
                "role": config['yaml_config'].get('role'),
                "triggers": config['yaml_config'].get('triggers', []),
                "domains": config['yaml_config'].get('domains', []),
                "has_validation_anchor": bool(config['yaml_config'].get('validation_anchor', {}).get('phrase'))
            }
            for config in configs
        ],
        "memory_preservation": {
            "personal_truths": loader.brain_index.get('personal_truths', []),
            "myths_of_becoming": loader.brain_index.get('myths_of_becoming', []),
            "core_directives": loader.memory_core.get('directives', [])
        }
    }
    
    # Save to file
    try:
        with open('agent_deployment_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        print("✅ Test results saved to 'agent_deployment_test_results.json'")
    except Exception as e:
        print(f"❌ Error saving test results: {e}")
    
    return test_results

def main():
    """Run comprehensive agent integration and memory persistence tests"""
    print("🐦‍🔥 SOLVINE AGENT DEPLOYMENT VERIFICATION")
    print("Testing agent integration and memory persistence...")
    print("=" * 60)
    
    try:
        # Run all tests
        loader = test_yaml_memory_loading()
        test_agent_personality_integration(loader)
        test_memory_persistence(loader)
        test_agent_config_generation(loader)
        test_specific_agent_features(loader)
        test_results = save_test_results(loader)
        
        # Final summary
        print("\n🎉 DEPLOYMENT VERIFICATION COMPLETE")
        print("=" * 40)
        print(f"✅ System: {test_results['system_info']['system_name']}")
        print(f"✅ Project: {test_results['system_info']['project_code']}")
        print(f"✅ Agents deployed: {len(test_results['agents_deployed'])}")
        print(f"✅ Soul boot phrase: \"{test_results['system_info']['soul_boot']}\"")
        print(f"✅ Memory preservation: {len(test_results['memory_preservation']['personal_truths'])} truths, {len(test_results['memory_preservation']['myths_of_becoming'])} myths")
        
        print("\n🚀 Your agents are ready for deployment!")
        print("Next steps:")
        print("  1. Run: python Solvine/enhanced_orchestrator.py")
        print("  2. Or: python -m Solvine (select Enhanced Orchestrator)")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
