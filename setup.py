#!/usr/bin/env python3
"""
Solvine Systems Setup Script
Automated installation and configuration
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def setup_environment():
    """Set up environment file"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        print("📝 Creating .env file from example...")
        shutil.copy(env_example, env_file)
        print("✅ .env file created")
        print("💡 Please edit .env with your API keys and settings")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️ No .env.example found")

def install_dependencies():
    """Install Python dependencies"""
    if Path("requirements_unified.txt").exists():
        return run_command(
            f"{sys.executable} -m pip install -r requirements_unified.txt",
            "Installing dependencies"
        )
    else:
        print("❌ requirements_unified.txt not found")
        return None

def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    # Test configuration validation
    result = run_command(
        f"{sys.executable} main_unified.py --validate-config",
        "Validating configuration"
    )
    if result is None:
        return False
    
    # Test Jasper head agent
    result = run_command(
        f"{sys.executable} main_unified.py --jasper-test",
        "Testing Jasper head agent"
    )
    if result is None:
        return False
    
    # Test system status
    result = run_command(
        f"{sys.executable} main_unified.py --status",
        "Checking system status"
    )
    if result is None:
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Solvine Systems Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if install_dependencies() is None:
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    # Set up environment
    setup_environment()
    
    # Test installation
    if test_installation():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit .env file with your API keys")
        print("2. Run: python main_unified.py --cli")
        print("3. Check out the documentation in docs/")
    else:
        print("\n❌ Setup completed with errors")
        print("💡 Check the error messages above and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
