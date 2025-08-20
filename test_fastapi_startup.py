#!/usr/bin/env python3
"""
Simple script to test if FastAPI server starts correctly
"""

import sys
import traceback
from pathlib import Path

def test_fastapi_import():
    """Test if we can import the FastAPI app"""
    print("🧪 Testing FastAPI app import...")
    
    try:
        # Add current directory to path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Try to import the app
        from web_api_server import app
        print("✅ FastAPI app imported successfully")
        
        # Check if app has routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append(f"{route.methods} {route.path}")
        
        print(f"✅ Found {len(routes)} routes:")
        for route in routes[:10]:  # Show first 10 routes
            print(f"   {route}")
        
        if len(routes) > 10:
            print(f"   ... and {len(routes) - 10} more")
            
        # Check for specific endpoints
        expected_endpoints = ['/health', '/agents', '/status', '/docs']
        for endpoint in expected_endpoints:
            found = any(endpoint in str(route) for route in app.routes)
            if found:
                print(f"✅ {endpoint} endpoint found")
            else:
                print(f"❌ {endpoint} endpoint MISSING")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import FastAPI app: {e}")
        print("💡 This usually means:")
        print("   - Missing dependencies (fastapi, uvicorn)")
        print("   - Syntax error in web_api_server.py")
        print("   - Wrong working directory")
        return False
    except Exception as e:
        print(f"❌ Error testing app: {e}")
        print("💡 Full traceback:")
        traceback.print_exc()
        return False

def test_server_startup():
    """Test if the server can start (dry run)"""
    print("\n🧪 Testing server startup (dry run)...")
    
    try:
        # Import uvicorn
        import uvicorn
        print("✅ uvicorn available")
        
        # Try to create the ASGI app
        from web_api_server import app
        print("✅ ASGI app created")
        
        # Check if we can get the app config
        config = uvicorn.Config(app, host="localhost", port=8080, log_level="info")
        print("✅ uvicorn config created")
        
        print("✅ Server should start successfully")
        print("💡 To actually start the server, run:")
        print("   python web_api_server.py --port 8080")
        
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        print("💡 This indicates a problem with the server configuration")
        traceback.print_exc()
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🧪 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    print("🔧 FastAPI Server Startup Test\n")
    
    # Check dependencies first
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Cannot continue - missing dependencies")
        return
    
    # Test app import
    app_ok = test_fastapi_import()
    
    if not app_ok:
        print("\n❌ Cannot continue - app import failed")
        return
    
    # Test server startup
    server_ok = test_server_startup()
    
    print("\n🎯 SUMMARY:")
    if deps_ok and app_ok and server_ok:
        print("✅ Everything looks good!")
        print("✅ The FastAPI server should start without issues")
        print("\n🚀 Ready to start server:")
        print("   python web_api_server.py --port 8080")
    else:
        print("❌ There are issues that need to be fixed")
        
    print("\n🔍 If the server still returns 404s after starting:")
    print("   1. Make sure you see 'Started server process' in the output")
    print("   2. Look for 'Application startup complete' message")
    print("   3. Check that uvicorn is running, not just Python's built-in server")
    print("   4. Test http://localhost:8080/health specifically")

if __name__ == "__main__":
    main()
