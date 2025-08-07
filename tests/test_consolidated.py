#!/usr/bin/env python3
"""
Quick Test Script for Consolidated Solvine Systems
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_jasper():
    """Test Jasper head agent functionality"""
    print("🧪 Testing Jasper Head Agent")
    print("=" * 40)
    
    try:
        from agents.jasper.jasper_agent import JasperAgent
        
        # Create and initialize Jasper
        jasper = JasperAgent()
        jasper.initialize()
        
        print("✅ Jasper successfully initialized")
        
        # Test autonomy status
        autonomy = jasper.get_autonomy_status()
        print(f"\n🛡️ Autonomy Status:")
        for key, value in autonomy.items():
            print(f"   {key}: {value}")
        
        # Test workshop response
        print(f"\n🔧 Testing Workshop Response:")
        response = jasper.respond("Analyze the consolidated Solvine Systems architecture")
        print(f"Jasper: {response[:200]}...")
        
        # Test clarification mode
        print(f"\n🤔 Testing Clarification Mode:")
        clarification = jasper.respond("help")
        print(f"Jasper: {clarification}")
        
        print(f"\n✅ All Jasper tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Jasper test failed: {e}")
        return False

def test_config():
    """Test configuration system"""
    print("\n🔧 Testing Configuration System")
    print("=" * 40)
    
    try:
        from unified_config.config_loader import SolvineConfigLoader
        
        loader = SolvineConfigLoader()
        
        # Test system config loading
        system_config = loader.load_system_config()
        print(f"✅ System config loaded: {system_config['system']['name']}")
        
        # Test agent config loading
        jasper_config = loader.load_agent_config('jasper')
        print(f"✅ Jasper config loaded: {jasper_config['agent_info']['type']}")
        
        # Test validation
        if loader.validate_config():
            print("✅ Configuration validation passed")
            return True
        else:
            print("❌ Configuration validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 Solvine Systems - Consolidated Test Suite")
    print("=" * 50)
    
    results = []
    
    # Test Jasper
    results.append(test_jasper())
    
    # Test Configuration
    results.append(test_config())
    
    # Summary
    print(f"\n📊 Test Summary:")
    print(f"   Jasper Head Agent: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"   Configuration: {'✅ PASS' if results[1] else '❌ FAIL'}")
    
    if all(results):
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"🚀 Solvine Systems consolidation successful!")
        print(f"\n💡 Next steps:")
        print(f"   • Run: python interfaces/unified_cli.py --local")
        print(f"   • Or: python main_unified.py --cli --local")
        return 0
    else:
        print(f"\n❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
