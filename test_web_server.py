#!/usr/bin/env python3
"""
Quick test script to verify web server routing
"""

import requests
import sys

def test_web_server():
    """Test the web server endpoints"""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Solvine Web Server...")
    
    # Test health endpoint first
    try:
        print("\n0. Testing health check endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Server healthy: {health_data.get('service', 'Unknown')}")
        else:
            print(f"   ❌ Health check failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Server not running or not accessible")
        print("\n💡 To start the server:")
        print("   1. Run: start_web_interface.bat")
        print("   2. Or: python web_api_server.py --port 8080")
        return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test root endpoint
    try:
        print("\n1. Testing root endpoint (/)...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'Not set')}")
        
        if response.status_code == 200:
            if "text/html" in response.headers.get('content-type', ''):
                print("   ✅ HTML content served successfully")
            else:
                print(f"   ⚠️ JSON response: {response.json()}")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test direct web interface endpoint
    try:
        print("\n2. Testing direct web interface (/solvine_web_ui.html)...")
        response = requests.get(f"{base_url}/solvine_web_ui.html", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'Not set')}")
        
        if response.status_code == 200:
            print("   ✅ Direct access works")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test API endpoints
    try:
        print("\n3. Testing API endpoints...")
        
        # Test agents endpoint
        response = requests.get(f"{base_url}/agents", timeout=5)
        print(f"   /agents Status: {response.status_code}")
        if response.status_code == 200:
            agents_data = response.json()
            print(f"   ✅ Found {agents_data.get('total_count', 0)} agents")
        else:
            print(f"   ❌ Agents endpoint error: {response.text}")
        
        # Test status endpoint
        response = requests.get(f"{base_url}/status", timeout=5)
        print(f"   /status Status: {response.status_code}")
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ System uptime: {status_data.get('uptime', 'Unknown')}")
        else:
            print(f"   ❌ Status endpoint error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ API Error: {e}")
    
    print("\n🎯 Test complete!")
    return True

if __name__ == "__main__":
    if not test_web_server():
        print("\n💡 Make sure to start the server first:")
        print("   python web_api_server.py --port 8080")
        sys.exit(1)
