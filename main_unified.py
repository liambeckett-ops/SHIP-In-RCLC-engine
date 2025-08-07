#!/usr/bin/env python3
"""
Solvine Systems - Unified Main Entry Point
Enhanced with Jasper Head Agent Integration

This is the primary entry point for the consolidated Solvine Systems
with Jasper as the head agent and voice-tone controller.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config.config_loader import get_config_loader, get_head_agent
    from interfaces.unified_cli import SolvineUnifiedCLI
    CONFIG_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    CONFIG_AVAILABLE = False

def main():
    """Main entry point for Solvine Systems"""
    parser = argparse.ArgumentParser(
        description="Solvine Systems - Autonomous Agent Collective with Jasper Head Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --cli                    # Interactive CLI with Jasper
  python main.py --cli --local           # Local Jasper mode only
  python main.py --status                # System status check
  python main.py --validate-config       # Validate configuration
  python main.py --jasper-test           # Test Jasper head agent
        """
    )
    
    # Mode selection
    parser.add_argument("--cli", action="store_true", help="Start interactive CLI interface")
    parser.add_argument("--api", action="store_true", help="Start API server (future)")
    parser.add_argument("--local", action="store_true", help="Use local Jasper head agent only")
    
    # System operations
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--validate-config", action="store_true", help="Validate configuration")
    parser.add_argument("--jasper-test", action="store_true", help="Test Jasper head agent")
    
    # Configuration
    parser.add_argument("--config-env", default="base", help="Configuration environment (base, dev, prod, sandbox)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # CLI options (passed through)
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--message", "-m", help="Single message query")
    parser.add_argument("--agent", "-a", help="Target specific agent")
    
    args = parser.parse_args()
    
    if not CONFIG_AVAILABLE:
        print("❌ Configuration system not available")
        print("💡 Make sure you're in the Solvine_Systems directory")
        sys.exit(1)
    
    # Load configuration
    config_loader = get_config_loader()
    
    try:
        system_config = config_loader.load_system_config(args.config_env)
        
        if args.debug:
            print(f"🔧 Debug mode enabled")
            print(f"📂 Base directory: {config_loader.base_dir}")
            print(f"⚙️ Environment: {args.config_env}")
        
        print(f"🤖 {system_config['system']['name']} v{system_config['system']['version']}")
        print(f"🎯 Head Agent: {system_config['head_agent'].title()}")
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        sys.exit(1)
    
    # Handle different modes
    if args.validate_config:
        print("\n🔍 Validating Configuration...")
        if config_loader.validate_config():
            print("✅ Configuration is valid")
            sys.exit(0)
        else:
            print("❌ Configuration validation failed")
            sys.exit(1)
    
    elif args.jasper_test:
        print("\n🧪 Testing Jasper Head Agent...")
        jasper = get_head_agent()
        
        if jasper:
            print("✅ Jasper instance created")
            
            try:
                jasper.initialize()
                print("✅ Jasper initialized successfully")
                
                # Test autonomy features
                autonomy_status = jasper.get_autonomy_status()
                print(f"\n🛡️ Autonomy Status:")
                for key, value in autonomy_status.items():
                    print(f"   {key}: {value}")
                
                # Test workshop response
                print(f"\n🔧 Testing Workshop Response:")
                test_response = jasper.respond("Test the workshop analytical framework")
                print(f"Jasper: {test_response[:150]}...")
                
                print("\n✅ Jasper head agent test complete!")
                
            except Exception as e:
                print(f"❌ Jasper test failed: {e}")
                sys.exit(1)
        else:
            print("❌ Failed to create Jasper instance")
            sys.exit(1)
    
    elif args.status:
        print("\n📊 System Status:")
        
        # System config status
        print(f"   System: {system_config['system']['name']} v{system_config['system']['version']}")
        print(f"   Head Agent: {system_config['head_agent']}")
        print(f"   Environment: {args.config_env}")
        
        # Head agent status
        try:
            jasper = get_head_agent()
            if jasper:
                jasper.initialize()
                autonomy_status = jasper.get_autonomy_status()
                print(f"   Jasper Status: ✅ Active")
                print(f"   Workshop Authority: {'✅' if autonomy_status['workshop_authority'] else '❌'}")
                print(f"   Boundary Enforcement: {'✅' if autonomy_status['boundary_enforcement'] else '❌'}")
                print(f"   Voice-Tone Control: {'✅' if autonomy_status['voice_tone_active'] else '❌'}")
            else:
                print(f"   Jasper Status: ❌ Not Available")
        except Exception as e:
            print(f"   Jasper Status: ❌ Error - {e}")
        
        # Configuration validation
        try:
            config_valid = config_loader.validate_config()
            print(f"   Configuration: {'✅ Valid' if config_valid else '❌ Invalid'}")
        except Exception as e:
            print(f"   Configuration: ❌ Error - {e}")
    
    elif args.cli:
        print(f"\n🚀 Starting CLI Interface...")
        
        # Determine mode
        local_mode = args.local
        if local_mode:
            print("🎯 Local Mode: Jasper Head Agent Only")
        else:
            print("🌐 Hybrid Mode: API + Local Jasper Fallback")
        
        # Start CLI
        try:
            cli = SolvineUnifiedCLI(args.url, local_mode)
            
            if args.message:
                # Single message mode
                response_data = cli.query_agent(args.message, args.agent)
                if 'error' in response_data:
                    print(f"❌ {response_data['error']}")
                    sys.exit(1)
                elif 'responses' in response_data:
                    formatted = cli.format_responses(response_data['responses'])
                    print(formatted)
                else:
                    print(f"❌ Unexpected response format")
                    sys.exit(1)
            else:
                # Interactive mode
                cli.interactive_mode()
                
        except Exception as e:
            print(f"❌ CLI startup failed: {e}")
            sys.exit(1)
    
    elif args.api:
        print("\n🌐 API Server mode not yet implemented")
        print("💡 Use --cli for interactive mode or --jasper-test for testing")
        sys.exit(1)
    
    else:
        # Default behavior - show help and status
        print("\n📋 Available Operations:")
        print("  --cli           Interactive CLI with Jasper head agent")
        print("  --cli --local   Local Jasper mode only")
        print("  --status        Show system status")
        print("  --jasper-test   Test Jasper head agent")
        print("  --validate-config  Validate configuration")
        print("\n💡 Use --help for full options")
        
        # Quick status check
        print(f"\n📊 Quick Status:")
        print(f"   System: {system_config['system']['name']} ✅")
        print(f"   Head Agent: {system_config['head_agent']} ✅")
        print(f"   Environment: {args.config_env} ✅")


if __name__ == "__main__":
    main()
