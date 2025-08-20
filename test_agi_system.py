#!/usr/bin/env python3
"""
Test script to verify the AGI system is working properly
"""

import sys
from pathlib import Path

print("🧪 Testing AGI System Components...")
print("="*50)

# Test 1: Fixed Jasper Agent
print("\n1️⃣ Testing Fixed Jasper Agent...")
try:
    import importlib.util
    jasper_path = Path(__file__).parent / "agents" / "jasper" / "jasper_agent_fixed.py"
    jasper_spec = importlib.util.spec_from_file_location("jasper_agent_fixed", jasper_path)
    jasper_module = importlib.util.module_from_spec(jasper_spec)
    jasper_spec.loader.exec_module(jasper_module)
    
    jasper = jasper_module.JasperAgent()
    jasper.initialize()
    response = jasper.respond("Test message")
    print(f"✅ Jasper Agent: WORKING")
    print(f"   Sample response: {response[:100]}...")
except Exception as e:
    print(f"❌ Jasper Agent: FAILED - {e}")

# Test 2: AGI Integration Manager
print("\n2️⃣ Testing AGI Integration Manager...")
try:
    from agi_integration_manager import AGIIntegrationManager
    manager = AGIIntegrationManager()
    manager.start()
    print("✅ AGI Integration Manager: WORKING")
except Exception as e:
    print(f"❌ AGI Integration Manager: FAILED - {e}")

# Test 3: Web API Server
print("\n3️⃣ Testing Web API Server imports...")
try:
    import web_api_server
    print("✅ Web API Server: IMPORTS SUCCESSFULLY")
except Exception as e:
    print(f"❌ Web API Server: IMPORT FAILED - {e}")

print("\n" + "="*50)
print("🎯 AGI System Test Complete!")
print("\nIf all tests pass, you can run:")
print("   python web_api_server.py")
print("   or")
print("   launch_agi_web.bat")
