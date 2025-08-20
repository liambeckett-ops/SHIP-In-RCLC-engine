#!/usr/bin/env python3
"""
Diagnostic script to check what's running on port 8080
"""

import socket
import requests
import json
from pathlib import Path

def check_port_8080():
    """Check if something is listening on port 8080"""
    print("🔍 Checking port 8080...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8080))
    sock.close()
    
    if result == 0:
        print("✅ Port 8080 is OPEN - something is listening")
        return True
    else:
        print("❌ Port 8080 is CLOSED - nothing is listening")
        return False

def check_server_type():
    """Check what type of server is running"""
    print("\n🔍 Checking server type...")
    
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8080/", timeout=5)
        print(f"📊 Root endpoint status: {response.status_code}")
        print(f"📊 Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"📊 Server header: {response.headers.get('server', 'Unknown')}")
        
        # Check if it's FastAPI
        if 'application/json' in response.headers.get('content-type', ''):
            print("🎯 Looks like FastAPI (JSON response)")
        elif 'text/html' in response.headers.get('content-type', ''):
            print("🌐 Looks like HTML server (not FastAPI)")
            
        # Test a known FastAPI endpoint
        try:
            health_response = requests.get("http://localhost:8080/health", timeout=5)
            if health_response.status_code == 200:
                print("✅ FastAPI health endpoint working!")
                data = health_response.json()
                print(f"📋 Health data: {data}")
            else:
                print(f"❌ Health endpoint failed: {health_response.status_code}")
        except:
            print("❌ Health endpoint not available")
            
        # Test docs endpoint
        try:
            docs_response = requests.get("http://localhost:8080/docs", timeout=5)
            if docs_response.status_code == 200:
                print("✅ FastAPI docs available!")
            else:
                print(f"❌ Docs endpoint failed: {docs_response.status_code}")
        except:
            print("❌ Docs endpoint not available")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
    except Exception as e:
        print(f"❌ Error checking server: {e}")

def check_file_structure():
    """Check if all required files exist"""
    print("\n🔍 Checking file structure...")
    
    base_path = Path(".")
    files_to_check = [
        "web_api_server.py",
        "web/solvine_web_ui.html",
        "web/diagnostic.html"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} MISSING")
            all_exist = False
    
    return all_exist

def check_python_imports():
    """Check if required Python packages are available"""
    print("\n🔍 Checking Python imports...")
    
    required_packages = {
        'fastapi': 'FastAPI web framework',
        'uvicorn': 'ASGI server',
        'pydantic': 'Data validation'
    }
    
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} available ({description})")
        except ImportError:
            print(f"❌ {package} MISSING ({description})")
            print(f"   Install with: pip install {package}")

def main():
    print("🚨 Solvine Server Diagnostic Tool\n")
    
    # Check if port is open
    port_open = check_port_8080()
    
    if port_open:
        # Check what type of server
        check_server_type()
    else:
        print("\n💡 The server is not running. To start it:")
        print("   1. Run: python web_api_server.py --port 8080")
        print("   2. Or: start_web_interface.bat")
    
    # Check file structure
    files_ok = check_file_structure()
    
    # Check Python packages
    check_python_imports()
    
    print("\n🎯 DIAGNOSIS SUMMARY:")
    if port_open:
        print("   ✅ Something is running on port 8080")
        print("   ❓ But it might not be the FastAPI server")
        print("   💡 Try stopping the current server and restarting:")
        print("      - Stop with Ctrl+C")
        print("      - Run: python web_api_server.py --port 8080")
    else:
        print("   ❌ No server running on port 8080")
        print("   💡 Start the server with:")
        print("      python web_api_server.py --port 8080")
    
    if not files_ok:
        print("   ❌ Some required files are missing")
        print("   💡 Make sure you're in the correct directory")
    
    print("\n🔧 Quick Fix Steps:")
    print("   1. Stop any running server (Ctrl+C)")
    print("   2. Verify you're in the Solvine_Systems directory")
    print("   3. Run: python web_api_server.py --port 8080")
    print("   4. Look for startup messages about FastAPI and uvicorn")
    print("   5. Test: http://localhost:8080/health")

if __name__ == "__main__":
    main()
