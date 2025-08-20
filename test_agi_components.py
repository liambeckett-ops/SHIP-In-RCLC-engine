"""
Simple test script for AGI components
"""

import sys
from pathlib import Path
import traceback

def test_component(component_name, test_function):
    """Test a component and report results"""
    print(f"\n🧪 Testing {component_name}...")
    try:
        result = test_function()
        print(f"✅ {component_name}: {result}")
        return True
    except Exception as e:
        print(f"❌ {component_name}: {str(e)}")
        print(f"   Traceback: {traceback.format_exc().splitlines()[-1]}")
        return False

def test_base_agent():
    """Test base agent import and creation"""
    try:
        sys.path.append(str(Path.cwd() / "agents"))
        from base_agent import BaseAgent
        return "Imported successfully"
    except ImportError as e:
        return f"Import failed: {e}"

def test_midas_agent():
    """Test Midas agent"""
    try:
        sys.path.append(str(Path.cwd() / "agents" / "midas"))
        from midas_agent import MidasAgent
        midas = MidasAgent()
        capabilities = midas.get_specialized_capabilities()
        return f"Created with {len(capabilities)} capabilities"
    except Exception as e:
        return f"Failed: {e}"

def test_collective_intelligence():
    """Test collective intelligence"""
    try:
        sys.path.append(str(Path.cwd() / "collective"))
        from collective_intelligence import CollectiveIntelligenceHub
        hub = CollectiveIntelligenceHub(Path.cwd())
        return "Hub created successfully"
    except Exception as e:
        return f"Failed: {e}"

def test_voice_interface():
    """Test voice interface"""
    try:
        sys.path.append(str(Path.cwd() / "voice"))
        from voice_interface import VoiceInterface
        voice = VoiceInterface(Path.cwd())
        return f"Voice interface created (enabled: {voice.voice_enabled})"
    except Exception as e:
        return f"Failed: {e}"

def test_agi_manager():
    """Test AGI integration manager"""
    try:
        from agi_integration_manager import AGIIntegrationManager
        manager = AGIIntegrationManager()
        return f"Manager created (active: {manager.system_active})"
    except Exception as e:
        return f"Failed: {e}"

if __name__ == "__main__":
    print("🚀 SOLVINE AGI COMPONENT TESTING")
    print("="*50)
    
    print(f"📁 Working directory: {Path.cwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    # Test each component
    tests = [
        ("Base Agent", test_base_agent),
        ("Midas Agent", test_midas_agent),
        ("Collective Intelligence", test_collective_intelligence), 
        ("Voice Interface", test_voice_interface),
        ("AGI Manager", test_agi_manager)
    ]
    
    results = []
    for name, test_func in tests:
        success = test_component(name, test_func)
        results.append((name, success))
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("="*30)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AGI system ready.")
    else:
        print("⚠️ Some tests failed. Check error messages above.")
    
    print("\n💡 Next steps:")
    print("   1. Run: python agi_integration_manager.py")
    print("   2. Try voice mode if voice interface works")
    print("   3. Test agent collaborations")
    print("   4. Implement remaining specialized agents")
