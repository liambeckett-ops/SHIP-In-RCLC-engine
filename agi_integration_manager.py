"""
AGI Integration Manager
Integrates all advanced AGI systems: specialized agents, collective intelligence, voice interface
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import threading
import time

# Add paths for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "agents"))
sys.path.append(str(Path(__file__).parent / "collective"))
sys.path.append(str(Path(__file__).parent / "voice"))

# Import AGI systems
try:
    from agents.base_agent import BaseAgent
    from agents.midas.midas_agent import MidasAgent
    from collective.collective_intelligence import CollectiveIntelligenceHub
    from voice.voice_interface import VoiceInterface, VoiceCommandHandler
    ADVANCED_SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Advanced systems import error: {e}")
    ADVANCED_SYSTEMS_AVAILABLE = False

# Import existing Jasper (using fixed version)
try:
    import importlib.util
    jasper_path = Path(__file__).parent / "agents" / "jasper" / "jasper_agent_fixed.py"
    jasper_spec = importlib.util.spec_from_file_location("jasper_agent_fixed", jasper_path)
    jasper_module = importlib.util.module_from_spec(jasper_spec)
    jasper_spec.loader.exec_module(jasper_module)
    JasperAgent = jasper_module.JasperAgent
    JASPER_AVAILABLE = True
except ImportError:
    JASPER_AVAILABLE = False

class AGIIntegrationManager:
    """
    Main integration manager for the advanced AGI research system
    
    Coordinates:
    - Specialized agents with real capabilities
    - Cross-agent knowledge sharing
    - Voice interaction interfaces
    - Collective intelligence behaviors
    - Emergent behavior monitoring
    """
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).parent
        
        # Core systems
        self.collective_hub = None
        self.voice_interface = None
        self.voice_handler = None
        
        # Agent registry
        self.agents = {}
        self.agent_status = {}
        
        # System state
        self.system_active = False
        self.voice_mode_active = False
        self.conversation_mode_active = False
        
        # Statistics
        self.system_stats = {
            'startup_time': datetime.now(),
            'total_interactions': 0,
            'agent_communications': 0,
            'knowledge_shares': 0,
            'collaborations': 0,
            'voice_interactions': 0
        }
        
        # Initialize systems
        self._initialize_systems()
    
    def start(self):
        """Start the AGI system (alias for system initialization check)"""
        if self.system_active:
            print("✅ AGI system already initialized and running")
            return True
        else:
            print("❌ AGI system not properly initialized")
            return False
    
    def _initialize_systems(self):
        """Initialize all AGI systems"""
        print("🚀 Initializing Advanced AGI Research System")
        print("="*60)
        
        try:
            # Initialize collective intelligence hub
            print("\n🧠 Initializing Collective Intelligence...")
            self.collective_hub = CollectiveIntelligenceHub(self.base_dir)
            
            # Initialize voice interface
            print("\n🎙️ Initializing Voice Interface...")
            self.voice_interface = VoiceInterface(self.base_dir)
            
            # Initialize agents
            print("\n🤖 Initializing Specialized Agents...")
            self._initialize_agents()
            
            # Initialize voice command handler
            if self.voice_interface.voice_enabled:
                print("\n🗣️ Initializing Voice Commands...")
                self.voice_handler = VoiceCommandHandler(self.voice_interface, self)
            
            self.system_active = True
            print("\n✅ AGI Research System fully initialized!")
            
        except Exception as e:
            print(f"\n❌ System initialization failed: {e}")
            self.system_active = False
    
    def _initialize_agents(self):
        """Initialize specialized agents"""
        agent_init_results = {}
        
        # Initialize Jasper (head agent)
        if JASPER_AVAILABLE:
            try:
                jasper = JasperAgent()
                jasper.initialize()
                self.agents['Jasper'] = jasper
                self.collective_hub.register_agent('Jasper', jasper.get_specialized_capabilities() if hasattr(jasper, 'get_specialized_capabilities') else ['coordination', 'analysis'], jasper)
                agent_init_results['Jasper'] = '✅ Head Agent'
            except Exception as e:
                agent_init_results['Jasper'] = f'❌ {str(e)[:50]}'
        
        # Initialize Midas (financial agent)
        try:
            midas = MidasAgent()
            self.agents['Midas'] = midas
            self.collective_hub.register_agent('Midas', midas.get_specialized_capabilities(), midas)
            agent_init_results['Midas'] = '✅ Financial Specialist'
        except Exception as e:
            agent_init_results['Midas'] = f'❌ {str(e)[:50]}'
        
        # TODO: Initialize other specialized agents (Aiven, Halcyon, VeilSynth, Quanta)
        # For now, register placeholders
        placeholder_agents = {
            'Aiven': ['creative_analysis', 'symbolic_interpretation', 'artistic_generation'],
            'Halcyon': ['crisis_support', 'emotional_intelligence', 'mental_health'],
            'VeilSynth': ['pattern_analysis', 'recursive_simulation', 'philosophical_reasoning'],
            'Quanta': ['mathematical_computation', 'data_analysis', 'algorithmic_solving']
        }
        
        for agent_name, capabilities in placeholder_agents.items():
            self.collective_hub.register_agent(agent_name, capabilities)
            agent_init_results[agent_name] = '⏳ Placeholder (TODO: Implement)'
        
        # Display initialization results
        print("Agent Initialization Results:")
        for agent, result in agent_init_results.items():
            print(f"   {agent}: {result}")
    
    def query_agent(self, agent_name: str, query: str, context: Dict = None) -> str:
        """Query a specific agent"""
        if not self.system_active:
            return "❌ AGI system not active"
        
        if agent_name not in self.agents:
            return f"❌ Agent '{agent_name}' not available"
        
        try:
            # Get response from agent
            response = self.agents[agent_name].respond(query, context)
            
            # Update statistics
            self.system_stats['total_interactions'] += 1
            
            # Log interaction for research
            self._log_interaction(agent_name, query, response)
            
            return response
            
        except Exception as e:
            return f"❌ Error querying {agent_name}: {e}"
    
    def intelligent_query(self, query: str, context: Dict = None) -> Dict[str, str]:
        """
        Route query to most appropriate agent(s) using collective intelligence
        """
        if not self.system_active:
            return {"error": "AGI system not active"}
        
        # Use collective intelligence to determine best agent(s)
        # For now, simple routing logic
        query_lower = query.lower()
        
        responses = {}
        
        # Financial queries → Midas
        if any(word in query_lower for word in ['money', 'investment', 'financial', 'portfolio', 'market']):
            if 'Midas' in self.agents:
                responses['Midas'] = self.query_agent('Midas', query, context)
        
        # General/coordination queries → Jasper
        elif 'Jasper' in self.agents:
            responses['Jasper'] = self.query_agent('Jasper', query, context)
        
        # If no specific agent matched, use first available
        if not responses and self.agents:
            first_agent = list(self.agents.keys())[0]
            responses[first_agent] = self.query_agent(first_agent, query, context)
        
        return responses
    
    def start_agent_collaboration(self, task_description: str, required_capabilities: List[str] = None) -> str:
        """Start collaborative task between agents"""
        if not self.collective_hub:
            return "❌ Collective intelligence not available"
        
        task_id = self.collective_hub.start_collaboration(
            requesting_agent="AGI_Manager",
            task_description=task_description,
            required_capabilities=required_capabilities
        )
        
        self.system_stats['collaborations'] += 1
        return task_id
    
    def facilitate_agent_communication(self, from_agent: str, to_agent: str, message: str) -> str:
        """Facilitate communication between agents"""
        if not self.collective_hub:
            return "❌ Collective intelligence not available"
        
        message_id = self.collective_hub.send_message(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type="query",
            content=message
        )
        
        self.system_stats['agent_communications'] += 1
        return message_id
    
    def start_voice_conversation(self):
        """Start voice conversation mode"""
        if not self.voice_interface or not self.voice_interface.voice_enabled:
            print("❌ Voice interface not available")
            return
        
        print("🎙️ Starting voice conversation mode...")
        
        def agent_callback(user_input: str) -> str:
            """Callback for voice conversation"""
            self.system_stats['voice_interactions'] += 1
            
            # Route to appropriate agent
            responses = self.intelligent_query(user_input)
            
            if responses:
                # Return first response
                agent_name, response = list(responses.items())[0]
                return f"{response}"
            else:
                return "I didn't understand that. Could you please rephrase?"
        
        self.conversation_mode_active = True
        self.voice_interface.start_conversation_mode(agent_callback)
        self.conversation_mode_active = False
    
    def speak_response(self, text: str, agent_name: str = "Jasper") -> bool:
        """Speak a response using the voice interface"""
        if not self.voice_interface:
            return False
        
        return self.voice_interface.speak(text, agent_name)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'system_active': self.system_active,
            'voice_enabled': self.voice_interface.voice_enabled if self.voice_interface else False,
            'conversation_mode': self.conversation_mode_active,
            'agents_available': list(self.agents.keys()),
            'collective_intelligence': self.collective_hub is not None,
            'system_stats': self.system_stats.copy(),
            'uptime': str(datetime.now() - self.system_stats['startup_time']),
        }
        
        # Add collective behavior analysis
        if self.collective_hub:
            behavior_analysis = self.collective_hub.analyze_collective_behavior()
            status['collective_behavior'] = behavior_analysis
        
        # Add individual agent status
        agent_statuses = {}
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'get_agent_status'):
                agent_statuses[agent_name] = agent.get_agent_status()
            else:
                agent_statuses[agent_name] = {'status': 'active', 'type': 'basic'}
        
        status['agent_details'] = agent_statuses
        
        return status
    
    def get_agent(self, agent_name: str):
        """Get a specific agent by name"""
        # Handle case variations
        for name, agent in self.agents.items():
            if name.lower() == agent_name.lower():
                return agent
        return None
    
    def demonstrate_agi_capabilities(self):
        """Demonstrate advanced AGI capabilities"""
        print("\n🧪 AGI CAPABILITIES DEMONSTRATION")
        print("="*50)
        
        if not self.system_active:
            print("❌ System not active - cannot demonstrate")
            return
        
        # 1. Agent specialization
        print("\n1️⃣ SPECIALIZED AGENT RESPONSES:")
        test_queries = [
            ("Should I invest in Bitcoin?", "Financial Analysis"),
            ("How do I reduce portfolio risk?", "Risk Management"),
            ("What are the current market trends?", "Market Analysis")
        ]
        
        for query, category in test_queries:
            print(f"\n💬 Query ({category}): {query}")
            responses = self.intelligent_query(query)
            for agent, response in responses.items():
                print(f"🤖 {agent}: {response[:100]}...")
        
        # 2. Knowledge sharing
        print("\n\n2️⃣ KNOWLEDGE SHARING:")
        if 'Midas' in self.agents:
            # Midas shares financial knowledge
            knowledge_id = self.collective_hub.share_knowledge(
                source_agent="Midas",
                knowledge_type="market_insight",
                content="Market volatility increases during economic uncertainty periods",
                confidence=0.85,
                tags=["market", "volatility", "economics"]
            )
            print(f"📚 Midas shared knowledge: {knowledge_id}")
        
        # 3. Agent communication
        print("\n\n3️⃣ AGENT-TO-AGENT COMMUNICATION:")
        if len(self.agents) >= 2:
            agent_names = list(self.agents.keys())
            message_id = self.facilitate_agent_communication(
                from_agent=agent_names[0],
                to_agent=agent_names[1],
                message="What's your perspective on the current economic situation?"
            )
            print(f"💬 Communication initiated: {message_id}")
        
        # 4. Collaborative problem solving
        print("\n\n4️⃣ COLLABORATIVE PROBLEM SOLVING:")
        task_id = self.start_agent_collaboration(
            task_description="Analyze the impact of AI on financial markets",
            required_capabilities=["financial_analysis", "market_research", "pattern_analysis"]
        )
        print(f"🤝 Collaboration started: {task_id}")
        
        # 5. Voice interface (if available)
        print("\n\n5️⃣ VOICE INTERFACE:")
        if self.voice_interface and self.voice_interface.voice_enabled:
            test_speech = "This is a demonstration of the AGI voice interface system"
            success = self.speak_response(test_speech, "Jasper")
            print(f"🗣️ Voice synthesis: {'✅ Success' if success else '❌ Failed'}")
        else:
            print("🗣️ Voice interface: ❌ Not available")
        
        # 6. System analysis
        print("\n\n6️⃣ COLLECTIVE BEHAVIOR ANALYSIS:")
        status = self.get_system_status()
        behavior = status.get('collective_behavior', {})
        print(f"📊 Total agents: {behavior.get('registered_agents', 0)}")
        print(f"📚 Knowledge items: {behavior.get('total_knowledge_items', 0)}")
        print(f"💬 Communications: {behavior.get('total_communications', 0)}")
        print(f"🤝 Collaborations: {behavior.get('active_collaborations', 0)}")
        
        emergent_behaviors = behavior.get('emergent_behaviors', [])
        if emergent_behaviors:
            print(f"🌟 Emergent behaviors detected: {len(emergent_behaviors)}")
            for behavior_desc in emergent_behaviors:
                print(f"   • {behavior_desc}")
        else:
            print("🌟 No emergent behaviors detected yet")
        
        print("\n✅ AGI Capabilities demonstration complete!")
    
    def _log_interaction(self, agent_name: str, query: str, response: str):
        """Log interaction for research purposes"""
        log_dir = self.base_dir / "research" / "interaction_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"{datetime.now().strftime('%Y-%m')}_interactions.jsonl"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent_name': agent_name,
            'query': query,
            'response_length': len(response),
            'query_type': self._classify_query_type(query),
            'interaction_id': f"{agent_name}_{int(datetime.now().timestamp())}"
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️ Interaction logging error: {e}")
    
    def _classify_query_type(self, query: str) -> str:
        """Classify query type for research"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['money', 'invest', 'financial', 'portfolio']):
            return 'financial'
        elif any(word in query_lower for word in ['create', 'design', 'art', 'creative']):
            return 'creative'
        elif any(word in query_lower for word in ['help', 'support', 'problem', 'crisis']):
            return 'support'
        elif any(word in query_lower for word in ['analyze', 'pattern', 'complex', 'system']):
            return 'analytical'
        elif any(word in query_lower for word in ['calculate', 'math', 'compute', 'data']):
            return 'computational'
        else:
            return 'general'
    
    def shutdown(self):
        """Shutdown AGI system gracefully"""
        print("\n🛑 Shutting down AGI Research System...")
        
        # Save agent states
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'save_agent_state'):
                agent.save_agent_state()
                print(f"💾 Saved {agent_name} state")
        
        # Cleanup collective intelligence
        if self.collective_hub:
            self.collective_hub.cleanup_old_data(days_old=7)
        
        self.system_active = False
        print("✅ AGI system shutdown complete")


def main():
    """Main function for testing and demonstration"""
    print("🧠 ADVANCED AGI RESEARCH SYSTEM")
    print("Personal AGI experimentation sandbox for consciousness simulation")
    print("="*70)
    
    # Initialize AGI system
    agi_manager = AGIIntegrationManager()
    
    if not agi_manager.system_active:
        print("\n❌ Failed to initialize AGI system")
        return
    
    # Show system status
    print("\n📊 SYSTEM STATUS:")
    status = agi_manager.get_system_status()
    print(f"   🤖 Agents: {len(status['agents_available'])}")
    print(f"   🧠 Collective Intelligence: {'✅' if status['collective_intelligence'] else '❌'}")
    print(f"   🎙️ Voice Interface: {'✅' if status['voice_enabled'] else '❌'}")
    print(f"   ⏱️ Uptime: {status['uptime']}")
    
    # Demonstrate capabilities
    agi_manager.demonstrate_agi_capabilities()
    
    # Interactive mode
    print("\n\n🎮 INTERACTIVE MODE")
    print("Commands: 'query [agent] [question]', 'voice', 'status', 'quit'")
    print("Example: query Midas Should I invest in index funds?")
    
    try:
        while True:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            elif user_input.lower() == 'status':
                status = agi_manager.get_system_status()
                print(f"📊 System Status: {len(status['agents_available'])} agents, {status['system_stats']['total_interactions']} interactions")
            elif user_input.lower() == 'voice':
                agi_manager.start_voice_conversation()
            elif user_input.lower().startswith('query '):
                parts = user_input[6:].split(' ', 1)
                if len(parts) == 2:
                    agent_name, question = parts
                    response = agi_manager.query_agent(agent_name.title(), question)
                    print(f"\n🤖 {agent_name.title()}: {response}")
                else:
                    print("Usage: query [agent] [question]")
            elif user_input.strip():
                # Smart routing
                responses = agi_manager.intelligent_query(user_input)
                for agent, response in responses.items():
                    print(f"\n🤖 {agent}: {response}")
    
    except KeyboardInterrupt:
        print("\n\n⚡ Interrupted by user")
    
    finally:
        agi_manager.shutdown()


if __name__ == "__main__":
    main()
