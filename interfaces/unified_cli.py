#!/usr/bin/env python3
"""
Solvine Systems - Unified CLI Interface
Enhanced with Jasper Head Agent Integration

Features consolidated from multiple CLI implementations:
- Interactive mode with Jasper voice-tone
- Agent-specific targeting 
- System status monitoring
- Memory and autonomy status
- Workshop mode integration
"""

import sys
import json
import argparse
import requests
from typing import Optional, Dict, List
from pathlib import Path

# Import Jasper head agent for local mode
try:
    from agents.jasper.jasper_agent import JasperAgent
    JASPER_AVAILABLE = True
except ImportError:
    JASPER_AVAILABLE = False
    print("⚠️ Jasper head agent not available for local mode")

class SolvineUnifiedCLI:
    """Unified command-line interface for Solvine Systems with Jasper integration"""
    
    def __init__(self, base_url: str = "http://localhost:8000", local_mode: bool = False):
        self.base_url = base_url
        self.local_mode = local_mode
        self.session = requests.Session()
        
        # Initialize Jasper head agent for local mode
        self.jasper = None
        if local_mode and JASPER_AVAILABLE:
            self.jasper = JasperAgent()
            try:
                self.jasper.initialize()
                print("🎯 Jasper Head Agent: LOCAL MODE ACTIVE")
            except Exception as e:
                print(f"⚠️ Jasper initialization error: {e}")
                self.jasper = None
    
    def query_agent(self, message: str, agent: Optional[str] = None, context: str = "") -> dict:
        """Send query to agent collective or local Jasper"""
        
        # Local mode with Jasper
        if self.local_mode and self.jasper:
            try:
                response = self.jasper.respond(message, {'context': context})
                return {
                    'responses': [{
                        'agent': 'jasper',
                        'role': 'head_agent',
                        'message': response,
                        'is_primary': True,
                        'stability_score': 0.95,
                        'autonomy_status': self.jasper.get_autonomy_status()
                    }]
                }
            except Exception as e:
                return {"error": f"Jasper local query failed: {str(e)}"}
        
        # API mode
        query_data = {
            "message": message,
            "agent": agent,
            "context": context
        }
        
        try:
            response = self.session.post(f"{self.base_url}/query", json=query_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to Solvine API. Is the server running?"}
        except Exception as e:
            return {"error": f"Query failed: {str(e)}"}
    
    def get_status(self) -> dict:
        """Get system status (API mode) or Jasper status (local mode)"""
        if self.local_mode and self.jasper:
            autonomy_status = self.jasper.get_autonomy_status()
            return {
                'status': 'active_local',
                'mode': 'local_jasper',
                'agents_count': 1,
                'system_stability': 0.95,
                'uptime': 'local_session',
                'head_agent': 'jasper',
                'autonomy_features': autonomy_status,
                'workshop_mode': True,
                'voice_tone_controller': True
            }
        
        try:
            response = self.session.get(f"{self.base_url}/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Status check failed: {str(e)}"}
    
    def list_agents(self) -> dict:
        """List available agents"""
        if self.local_mode and self.jasper:
            autonomy_status = self.jasper.get_autonomy_status()
            return {
                'agents': [{
                    'name': 'jasper',
                    'role': 'Head Agent / Voice-Tone Controller',
                    'status': 'active',
                    'stability': 0.95,
                    'domains': ['workshop_analysis', 'boundary_enforcement', 'voice_tone_control'],
                    'triggers': ['analytical_queries', 'system_analysis', 'technical_assessment'],
                    'autonomy_level': autonomy_status['autonomy_level'],
                    'workshop_authority': autonomy_status['workshop_authority'],
                    'boundary_enforcement': autonomy_status['boundary_enforcement']
                }]
            }
        
        try:
            response = self.session.get(f"{self.base_url}/agents")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Agent list failed: {str(e)}"}
    
    def get_memory_status(self) -> dict:
        """Get memory system status"""
        if self.local_mode and self.jasper:
            history = self.jasper.get_session_memory(5)
            autonomy_status = self.jasper.get_autonomy_status()
            
            return {
                'agent_memories': {
                    'jasper': {
                        'personal_details': len(self.jasper.identity),
                        'interactions': len(history),
                        'autonomy_metadata': True,
                        'workshop_authority': autonomy_status['workshop_authority']
                    }
                },
                'current_session': {
                    'session_id': 'local_jasper',
                    'message_count': autonomy_status['session_interactions'],
                    'agents_involved': ['jasper'],
                    'autonomy_features_active': True
                },
                'memory_backend': 'sqlite_with_autonomy_metadata'
            }
        
        try:
            response = self.session.get(f"{self.base_url}/memory/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Memory status failed: {str(e)}"}
    
    def get_jasper_autonomy_status(self) -> dict:
        """Get detailed Jasper autonomy status (local mode only)"""
        if self.local_mode and self.jasper:
            return {
                'jasper_autonomy': self.jasper.get_autonomy_status(),
                'identity': self.jasper.identity.get('agent_name', 'Unknown'),
                'authority_level': self.jasper.identity.get('core_identity', {}).get('personality_matrix', {}).get('authority_level', 'unknown'),
                'voice_tone_active': 'tone: sarcastic' in self.jasper.identity.get('persona_flags', []),
                'workshop_protocols': True
            }
        return {"error": "Jasper autonomy status only available in local mode"}
    
    def format_responses(self, responses: list) -> str:
        """Format agent responses for CLI display with autonomy info"""
        if not responses:
            return "No responses received."
        
        output = []
        for response in responses:
            primary_indicator = "🎯" if response.get('is_primary', False) else "💭"
            agent_name = response['agent'].title()
            role = response['role']
            message = response['message']
            stability = response.get('stability_score', 0.0)
            
            stability_icon = "🟢" if stability > 0.7 else "🟡" if stability > 0.4 else "🔴"
            
            # Add autonomy indicators for head agents
            autonomy_info = ""
            if 'autonomy_status' in response:
                autonomy = response['autonomy_status']
                if autonomy.get('autonomy_level') == 'high':
                    autonomy_info = " 🛡️"
                if autonomy.get('workshop_authority'):
                    autonomy_info += " 🔧"
                if autonomy.get('voice_tone_active'):
                    autonomy_info += " 🎭"
            
            output.append(f"{primary_indicator} {agent_name} ({role}){autonomy_info} {stability_icon}: {message}")
        
        return "\n\n".join(output)
    
    def interactive_mode(self):
        """Run interactive CLI session with Jasper integration"""
        mode_indicator = "🎯 LOCAL" if self.local_mode else "🌐 API"
        
        print(f"🤖 SOLVINE UNIFIED CLI - {mode_indicator} Mode")
        print("=" * 60)
        print("Commands:")
        print("  • Type your message to query agents")
        print("  • '@agent message' to target specific agent")
        print("  • '/status' for system status")
        print("  • '/agents' to list agents")
        print("  • '/memory' for memory status")
        print("  • '/jasper' for Jasper autonomy status (local mode)")
        print("  • '/workshop' to enable workshop mode emphasis")
        print("  • '/quit' to exit")
        print("=" * 60)
        
        # Check system status
        status = self.get_status()
        if 'error' in status:
            print(f"❌ {status['error']}")
            if not self.local_mode:
                print("💡 Try --local flag for Jasper head agent local mode")
            return
        
        if self.local_mode:
            print(f"✅ Jasper Head Agent Active - Local Mode")
            print(f"🎯 Workshop Authority: {status.get('autonomy_features', {}).get('workshop_authority', False)}")
            print(f"🛡️ Boundary Enforcement: {status.get('autonomy_features', {}).get('boundary_enforcement', False)}")
        else:
            print(f"✅ Connected to Solvine API")
            print(f"📊 {status.get('agents_count', 0)} agents active")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                
                elif user_input.lower() == '/status':
                    status = self.get_status()
                    if 'error' in status:
                        print(f"❌ {status['error']}")
                    else:
                        print(f"📊 System Status: {status['status']}")
                        if self.local_mode:
                            print(f"🎯 Head Agent: {status.get('head_agent', 'unknown')}")
                            print(f"🔧 Workshop Mode: {status.get('workshop_mode', False)}")
                            print(f"🎭 Voice-Tone Controller: {status.get('voice_tone_controller', False)}")
                        else:
                            print(f"🤖 Agents: {status['agents_count']} active")
                            print(f"📈 Stability: {status['system_stability']:.2f}")
                            print(f"⏰ Uptime: {status['uptime']}")
                
                elif user_input.lower() == '/agents':
                    agents_data = self.list_agents()
                    if 'error' in agents_data:
                        print(f"❌ {agents_data['error']}")
                    else:
                        print("🤖 Available Agents:")
                        for agent in agents_data['agents']:
                            status_icon = "🟢" if agent['status'] == 'active' else "🔴"
                            stability = agent['stability']
                            stability_icon = "🟢" if stability > 0.7 else "🟡" if stability > 0.4 else "🔴"
                            
                            autonomy_indicators = ""
                            if 'autonomy_level' in agent and agent['autonomy_level'] == 'high':
                                autonomy_indicators += " 🛡️"
                            if agent.get('workshop_authority'):
                                autonomy_indicators += " 🔧"
                            if agent.get('boundary_enforcement'):
                                autonomy_indicators += " ⚡"
                            
                            print(f"  {status_icon} {agent['name'].title()}: {agent['role']}{autonomy_indicators}")
                            print(f"     Stability: {stability:.2f} {stability_icon}")
                            if agent['domains']:
                                print(f"     Domains: {', '.join(agent['domains'])}")
                            if agent['triggers']:
                                print(f"     Triggers: {', '.join(agent['triggers'])}")
                
                elif user_input.lower() == '/memory':
                    memory_data = self.get_memory_status()
                    if 'error' in memory_data:
                        print(f"❌ {memory_data['error']}")
                    else:
                        print("🧠 Memory System Status:")
                        
                        agent_memories = memory_data.get('agent_memories', {})
                        for agent_name, stats in agent_memories.items():
                            memory_icon = "🧠" if stats['personal_details'] > 0 else "💭"
                            autonomy_icon = " 🛡️" if stats.get('autonomy_metadata') else ""
                            workshop_icon = " 🔧" if stats.get('workshop_authority') else ""
                            
                            print(f"  {memory_icon} {agent_name.title()}: {stats['personal_details']} details, {stats['interactions']} interactions{autonomy_icon}{workshop_icon}")
                        
                        session = memory_data.get('current_session', {})
                        if session:
                            print(f"\n💬 Current Session: {session.get('session_id', 'Unknown')}")
                            print(f"    Messages: {session.get('message_count', 0)}")
                            print(f"    Agents: {', '.join(session.get('agents_involved', []))}")
                            if session.get('autonomy_features_active'):
                                print(f"    Autonomy Features: ✅ Active")
                
                elif user_input.lower() == '/jasper':
                    jasper_status = self.get_jasper_autonomy_status()
                    if 'error' in jasper_status:
                        print(f"❌ {jasper_status['error']}")
                    else:
                        print("🎯 Jasper Head Agent - Autonomy Status:")
                        autonomy = jasper_status['jasper_autonomy']
                        
                        print(f"    Agent: {jasper_status['identity']}")
                        print(f"    Authority Level: {jasper_status['authority_level']}")
                        print(f"    Autonomy Level: {autonomy['autonomy_level']}")
                        print(f"    Workshop Authority: {'✅' if autonomy['workshop_authority'] else '❌'}")
                        print(f"    Boundary Enforcement: {'✅' if autonomy['boundary_enforcement'] else '❌'}")
                        print(f"    Independent Decisions: {'✅' if autonomy['independent_decision_making'] else '❌'}")
                        print(f"    Voice-Tone Active: {'✅' if autonomy['voice_tone_active'] else '❌'}")
                        print(f"    Session Interactions: {autonomy['session_interactions']}")
                        print(f"    Recursive Count: {autonomy['recursive_count']}")
                
                elif user_input.lower() == '/workshop':
                    if self.local_mode and self.jasper:
                        print("🔧 Workshop Mode Emphasis Activated")
                        workshop_response = self.jasper.respond("Activate enhanced workshop protocols for systematic analysis")
                        print(f"Jasper: {workshop_response}")
                    else:
                        print("⚠️ Workshop mode emphasis only available in local mode with Jasper")
                
                else:
                    # Regular query
                    agent = None
                    message = user_input
                    
                    # Check for agent targeting (@agent)
                    if user_input.startswith('@'):
                        parts = user_input.split(' ', 1)
                        if len(parts) > 1:
                            agent = parts[0][1:]  # Remove @
                            message = parts[1]
                        else:
                            print("❌ Invalid format. Use: @agent your message")
                            continue
                    
                    # Send query
                    response_data = self.query_agent(message, agent)
                    
                    if 'error' in response_data:
                        print(f"❌ {response_data['error']}")
                    elif 'responses' in response_data:
                        formatted = self.format_responses(response_data['responses'])
                        print(f"\n{formatted}\n")
                    else:
                        print(f"❌ Unexpected response format")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Solvine Unified CLI - Enhanced Agent Interface")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--local", action="store_true", help="Use local Jasper head agent mode")
    parser.add_argument("--message", "-m", help="Single message query")
    parser.add_argument("--agent", "-a", help="Target specific agent")
    parser.add_argument("--context", "-c", default="", help="Additional context")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run interactive mode")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--agents", action="store_true", help="List available agents")
    parser.add_argument("--jasper-status", action="store_true", help="Show Jasper autonomy status (local mode)")
    
    args = parser.parse_args()
    
    cli = SolvineUnifiedCLI(args.url, args.local)
    
    if args.interactive:
        cli.interactive_mode()
    elif args.status:
        status = cli.get_status()
        if 'error' in status:
            print(f"❌ {status['error']}")
            sys.exit(1)
        else:
            print(json.dumps(status, indent=2))
    elif args.agents:
        agents = cli.list_agents()
        if 'error' in agents:
            print(f"❌ {agents['error']}")
            sys.exit(1)
        else:
            print(json.dumps(agents, indent=2))
    elif args.jasper_status:
        jasper_status = cli.get_jasper_autonomy_status()
        if 'error' in jasper_status:
            print(f"❌ {jasper_status['error']}")
            sys.exit(1)
        else:
            print(json.dumps(jasper_status, indent=2))
    elif args.message:
        response_data = cli.query_agent(args.message, args.agent, args.context)
        if 'error' in response_data:
            print(f"❌ {response_data['error']}")
            sys.exit(1)
        elif 'responses' in response_data:
            formatted = cli.format_responses(response_data['responses'])
            print(formatted)
        else:
            print(json.dumps(response_data, indent=2))
    else:
        # Default to interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
