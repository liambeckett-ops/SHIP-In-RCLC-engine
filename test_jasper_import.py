#!/usr/bin/env python3
"""
Test script for Jasper import
"""

import sys
import os
from pathlib import Path

print("🔍 Debugging Jasper Import")
print(f"Current working directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print()

# Check if agents directory exists
agents_dir = Path("agents")
print(f"Agents directory exists: {agents_dir.exists()}")
if agents_dir.exists():
    print(f"Agents directory contents: {list(agents_dir.iterdir())}")

# Check if jasper directory exists
jasper_dir = Path("agents/jasper")
print(f"Jasper directory exists: {jasper_dir.exists()}")
if jasper_dir.exists():
    print(f"Jasper directory contents: {list(jasper_dir.iterdir())}")

# Check if __init__.py files exist
agents_init = Path("agents/__init__.py")
jasper_init = Path("agents/jasper/__init__.py")
print(f"Agents __init__.py exists: {agents_init.exists()}")
print(f"Jasper __init__.py exists: {jasper_init.exists()}")

print()
print("📦 Testing imports...")

try:
    import agents
    print("✅ agents package imported successfully")
except Exception as e:
    print(f"❌ agents package import failed: {e}")

try:
    import agents.jasper
    print("✅ agents.jasper package imported successfully")
except Exception as e:
    print(f"❌ agents.jasper package import failed: {e}")

try:
    from agents.jasper.jasper_agent import JasperAgent
    print("✅ JasperAgent class imported successfully")
    
    # Try to create an instance
    jasper = JasperAgent()
    print("✅ JasperAgent instance created successfully")
    print(f"📋 Jasper base directory: {jasper.base_dir}")
    print(f"📋 Jasper config directory: {jasper.config_dir}")
    
except Exception as e:
    print(f"❌ JasperAgent import/creation failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("🎯 Test completed!")
