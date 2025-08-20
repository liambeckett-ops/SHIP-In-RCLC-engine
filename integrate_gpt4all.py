#!/usr/bin/env python3
"""
Simple GPT4All Integration Script for Solvine Systems
Safely adds GPT4All local models to your existing system
"""

import asyncio
import sys
import os
from pathlib import Path

# Add Solvine Systems to path
solvine_path = Path(__file__).parent
sys.path.insert(0, str(solvine_path))

try:
    # Import the GPT4All provider we just created
    from model_providers.gpt4all_provider import initialize_gpt4all_for_solvine, solvine_gpt4all_integration
    
    # Try to import your existing Solvine system
    # (Adjust these imports based on your actual system structure)
    try:
        from agents import jasper, midas, aiven  # Adjust based on your structure
        SOLVINE_AGENTS_AVAILABLE = True
    except ImportError:
        SOLVINE_AGENTS_AVAILABLE = False
        print("ℹ️ Solvine agents not found - that's okay, we'll set up GPT4All standalone")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the Solvine_Systems directory and have installed gpt4all:")
    print("   pip install gpt4all")
    sys.exit(1)

class SolvineGPT4AllManager:
    """Simple manager to integrate GPT4All with your Solvine system"""
    
    def __init__(self):
        self.integration = None
        self.agents = {}
        
    async def setup_gpt4all(self):
        """Set up GPT4All integration"""
        print("🚀 Setting up GPT4All for Solvine Systems...")
        print("=" * 50)
        
        # Initialize GPT4All integration
        self.integration = await initialize_gpt4all_for_solvine()
        
        if self.integration:
            print("✅ GPT4All integration successful!")
            
            # Show what models are available
            status = self.integration.get_integration_status()
            print(f"📊 Available models: {len(status['available_models'])}")
            print(f"📥 Downloaded models: {len(status['downloaded_models'])}")
            
            return True
        else:
            print("❌ GPT4All integration failed")
            return False
    
    async def chat_with_agent(self, agent_name: str, message: str):
        """Chat with a specific agent using GPT4All"""
        if not self.integration:
            print("❌ GPT4All not initialized. Run setup_gpt4all() first.")
            return None
        
        try:
            print(f"💭 {agent_name.title()} is thinking...")
            response = await self.integration.enhance_agent_with_gpt4all(agent_name, message)
            print(f"🤖 {agent_name.title()}: {response}")
            return response
        except Exception as e:
            print(f"❌ Error with {agent_name}: {e}")
            return None
    
    async def demo_all_agents(self):
        """Demonstrate all agents with GPT4All"""
        if not self.integration:
            print("❌ GPT4All not initialized")
            return
        
        agents = ["solvine", "aiven", "midas", "jasper", "veilsynth", "halcyon", "quanta"]
        demo_messages = {
            "solvine": "As the primary orchestrator, please coordinate a project status update across all agents.",
            "aiven": "I'm feeling overwhelmed with work. Can you help me feel better?",
            "midas": "What are the current trends in AI investment and market opportunities?",
            "jasper": "Test my ethical framework with an edge case about AI decision-making boundaries.",
            "veilsynth": "Tell me a symbolic myth about the recursive nature of consciousness.",
            "halcyon": "Assess the safety protocols for our AI agent system and recommend safeguards.",
            "quanta": "Calculate the probability and statistical implications of AI agent coordination."
        }
        
        print("🎭 Demonstrating all Solvine agents with GPT4All...")
        print("=" * 60)
        
        for agent in agents:
            message = demo_messages.get(agent, "Hello, please introduce yourself.")
            print(f"\\n👤 User → {agent.title()}: {message}")
            await self.chat_with_agent(agent, message)
            print("-" * 40)
    
    def show_model_recommendations(self):
        """Show model recommendations for each agent"""
        if not self.integration:
            print("❌ GPT4All not initialized")
            return
        
        status = self.integration.get_integration_status()
        recommendations = status.get('agent_recommendations', {})
        
        print("🎯 Model Recommendations for Each Agent:")
        print("=" * 45)
        
        for agent_name, rec in recommendations.items():
            model_name = rec['recommended_model']
            model_info = rec['model_info']
            is_downloaded = rec['is_downloaded']
            
            status_icon = "✅" if is_downloaded else "📥"
            size_info = f"({model_info.get('size_mb', 0)}MB)"
            
            print(f"{status_icon} {agent_name.title()}: {model_info.get('name', model_name)} {size_info}")
            print(f"   └─ {model_info.get('description', 'No description')}")
            
            if not is_downloaded:
                print(f"   💡 Download with: await download_model_for_agent('{agent_name}')")
            print()
    
    async def download_model_for_agent(self, agent_name: str):
        """Download the recommended model for a specific agent"""
        if not self.integration:
            print("❌ GPT4All not initialized")
            return False
        
        try:
            rec = await self.integration.get_recommendations_for_agent(agent_name)
            model_id = rec['recommended_model']
            
            print(f"📥 Downloading {rec['model_info']['name']} for {agent_name.title()}...")
            success = await self.integration.gpt4all_provider.download_model(model_id)
            
            if success:
                print(f"✅ Model downloaded successfully!")
            else:
                print(f"❌ Download failed")
            
            return success
            
        except Exception as e:
            print(f"❌ Download error: {e}")
            return False
    
    async def interactive_chat(self):
        """Start an interactive chat session"""
        if not self.integration:
            print("❌ GPT4All not initialized")
            return
        
        print("🗣️ Interactive Chat with Solvine Agents (GPT4All)")
        print("=" * 50)
        print("Available agents: solvine, aiven, midas, jasper, veilsynth, halcyon, quanta")
        print("Commands: 'quit' to exit, 'switch <agent>' to change agent")
        print("=" * 50)
        
        current_agent = "solvine"
        print(f"💬 Chatting with {current_agent.title()} (powered by GPT4All)")
        
        while True:
            try:
                user_input = input(f"\\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower().startswith('switch '):
                    new_agent = user_input[7:].strip().lower()
                    if new_agent in ["solvine", "aiven", "midas", "jasper", "veilsynth", "halcyon", "quanta"]:
                        current_agent = new_agent
                        print(f"🔄 Switched to {current_agent.title()}")
                    else:
                        print("❌ Unknown agent. Available: solvine, aiven, midas, jasper, veilsynth, halcyon, quanta")
                    continue
                
                if user_input:
                    await self.chat_with_agent(current_agent, user_input)
                
            except KeyboardInterrupt:
                print("\\n👋 Chat ended by user")
                break
            except Exception as e:
                print(f"❌ Chat error: {e}")

async def main():
    """Main function to demonstrate GPT4All integration"""
    print("🤖 Solvine Systems + GPT4All Integration")
    print("=" * 40)
    print("🔒 100% Local AI - Your data never leaves your computer")
    print("💰 100% Free - No API costs ever")
    print("⚡ Enhanced Performance - Better reasoning and creativity")
    print("=" * 40)
    
    manager = SolvineGPT4AllManager()
    
    # Set up GPT4All
    success = await manager.setup_gpt4all()
    if not success:
        print("❌ Setup failed. Please check the error messages above.")
        return
    
    # Show recommendations
    print("\\n" + "="*50)
    manager.show_model_recommendations()
    
    # Ask what the user wants to do
    print("\\nWhat would you like to do?")
    print("1. 🎭 Demo all agents")
    print("2. 💬 Interactive chat")
    print("3. 📥 Download models for agents")
    print("4. 🔍 Show system status")
    
    try:
        choice = input("\\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            await manager.demo_all_agents()
        elif choice == "2":
            await manager.interactive_chat()
        elif choice == "3":
            agents = ["solvine", "aiven", "midas", "jasper", "veilsynth", "halcyon", "quanta"]
            print("\\nWhich agent's model would you like to download?")
            for i, agent in enumerate(agents, 1):
                print(f"{i}. {agent.title()}")
            
            agent_choice = input("Enter agent number: ").strip()
            try:
                agent_index = int(agent_choice) - 1
                if 0 <= agent_index < len(agents):
                    agent_name = agents[agent_index]
                    await manager.download_model_for_agent(agent_name)
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a number")
        elif choice == "4":
            status = manager.integration.get_integration_status()
            print("\\n📊 System Status:")
            print(f"Enabled: {status['enabled']}")
            print(f"Models Available: {len(status['available_models'])}")
            print(f"Models Downloaded: {len(status['downloaded_models'])}")
            print(f"Current Model: {status['provider_info']['current_model']}")
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")

if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("model_providers").exists():
        print("❌ Please run this script from the Solvine_Systems directory")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    # Run the main function
    asyncio.run(main())
