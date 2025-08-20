#!/usr/bin/env python3
"""
Agent Voice Handler for Solvine Systems
Connects voice integration to Aiven & Solvine agents
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from voice_integration import VoiceIntegrationManager

# Add the models directory to path for GPT4All integration
sys.path.append(os.path.join(os.path.dirname(__file__), 'models', 'gpt4all'))

try:
    from gpt4all_provider import GPT4AllProvider
except ImportError:
    GPT4AllProvider = None

class AgentVoiceHandler:
    def __init__(self):
        self.voice_manager = VoiceIntegrationManager()
        self.gpt4all_provider = None
        self.agent_memory = {}
        
        # Initialize GPT4All if available
        if GPT4AllProvider:
            try:
                self.gpt4all_provider = GPT4AllProvider()
                print("🤖 GPT4All provider connected")
            except Exception as e:
                print(f"⚠️ GPT4All connection failed: {e}")
        
        # Agent personality traits for voice responses
        self.agent_personalities = {
            "aiven": {
                "role": "Emotional Intelligence Agent",
                "traits": ["empathetic", "supportive", "understanding", "warm"],
                "response_style": "caring and emotionally aware",
                "specialization": "emotional support and interpersonal guidance",
                "greeting_style": "warm and welcoming"
            },
            "solvine": {
                "role": "Coordination Agent", 
                "traits": ["strategic", "organized", "clear", "decisive"],
                "response_style": "structured and goal-oriented",
                "specialization": "planning, coordination, and strategic thinking",
                "greeting_style": "professional and confident"
            }
        }
    
    async def process_request(self, agent_name: str, user_input: str) -> str:
        """Process user request through specific agent"""
        try:
            print(f"🧠 Processing request for {agent_name}: '{user_input[:50]}...'")
            
            # Get agent personality
            personality = self.agent_personalities.get(agent_name, {})
            
            # Create context-aware prompt
            prompt = self._create_agent_prompt(agent_name, user_input, personality)
            
            # Get response from GPT4All if available
            if self.gpt4all_provider:
                try:
                    response = await self._get_gpt4all_response(agent_name, prompt)
                    if response:
                        # Store in memory for context
                        self._store_interaction(agent_name, user_input, response)
                        return self._format_voice_response(response, agent_name)
                except Exception as e:
                    print(f"⚠️ GPT4All error: {e}")
            
            # Fallback to rule-based responses
            return self._get_fallback_response(agent_name, user_input, personality)
            
        except Exception as e:
            print(f"⚠️ Error processing request: {e}")
            return f"I apologize, but I encountered an error while processing your request. Please try again."
    
    def _create_agent_prompt(self, agent_name: str, user_input: str, personality: dict) -> str:
        """Create personality-specific prompt for agent"""
        
        # Get conversation history for context
        history = self._get_recent_history(agent_name, limit=3)
        history_text = "\n".join([f"User: {h['input']}\n{agent_name}: {h['response']}" for h in history])
        
        base_prompt = f"""You are {agent_name.title()}, a {personality.get('role', 'AI assistant')} in the Solvine Systems.

Your personality traits: {', '.join(personality.get('traits', []))}
Your response style: {personality.get('response_style', 'helpful and informative')}
Your specialization: {personality.get('specialization', 'general assistance')}

This is a VOICE conversation, so:
- Keep responses concise and conversational (1-3 sentences max)
- Use natural speech patterns
- Be warm and engaging
- Avoid bullet points or complex formatting
- Speak as if talking directly to the person

Recent conversation history:
{history_text}

Current user message: {user_input}

Respond as {agent_name.title()} in a natural, conversational way suitable for voice interaction:"""

        return base_prompt
    
    async def _get_gpt4all_response(self, agent_name: str, prompt: str) -> str:
        """Get response from GPT4All model"""
        try:
            # Get the appropriate model for the agent
            model_name = self._get_agent_model(agent_name)
            
            response = await asyncio.to_thread(
                self.gpt4all_provider.generate_response,
                prompt,
                model_name=model_name,
                max_tokens=150,  # Keep voice responses concise
                temperature=0.7
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"⚠️ GPT4All generation error: {e}")
            return None
    
    def _get_agent_model(self, agent_name: str) -> str:
        """Get the preferred model for each agent"""
        model_mapping = {
            "aiven": "orca-mini-3b-q4_0",  # Good for emotional responses
            "solvine": "llama-3.2-3b-instruct-q4_0"  # Good for strategic thinking
        }
        return model_mapping.get(agent_name, "orca-mini-3b-q4_0")
    
    def _format_voice_response(self, response: str, agent_name: str) -> str:
        """Format response for natural voice delivery"""
        # Remove any markdown or formatting
        response = response.replace("*", "").replace("#", "").replace("`", "")
        
        # Split long responses into shorter segments
        sentences = response.split('. ')
        if len(sentences) > 3:
            response = '. '.join(sentences[:3]) + '.'
        
        # Add natural speech patterns
        if agent_name == "aiven":
            # Add empathetic language markers
            if not any(word in response.lower() for word in ['i understand', 'i hear', 'that sounds']):
                if '?' in response:
                    response = "I hear what you're asking. " + response
                else:
                    response = "I understand. " + response
        
        elif agent_name == "solvine":
            # Add strategic language markers
            if not any(word in response.lower() for word in ['let me', 'we can', 'the approach']):
                response = "Let me coordinate that for you. " + response
        
        return response
    
    def _get_fallback_response(self, agent_name: str, user_input: str, personality: dict) -> str:
        """Generate fallback response when GPT4All is unavailable"""
        
        responses = {
            "aiven": {
                "default": "I'm here to listen and support you. Could you tell me more about what you're feeling or experiencing?",
                "emotional": "That sounds like it might be emotionally challenging. I'm here to help you work through these feelings.",
                "support": "I want you to know that your feelings are valid. Let's explore this together.",
                "understanding": "I hear you, and I understand this is important to you. How can I best support you right now?"
            },
            "solvine": {
                "default": "I can help coordinate and organize a solution for you. What specific outcome are you looking to achieve?",
                "planning": "Let me help you structure an approach to this. What are the key priorities we need to address?",
                "strategy": "I can see this requires strategic thinking. Let's break this down into manageable steps.",
                "coordination": "This sounds like something I can help coordinate. What resources or support do you need?"
            }
        }
        
        agent_responses = responses.get(agent_name, {})
        
        # Simple keyword matching for appropriate response
        user_lower = user_input.lower()
        
        if agent_name == "aiven":
            if any(word in user_lower for word in ['feel', 'emotion', 'sad', 'happy', 'angry', 'frustrated']):
                return agent_responses.get("emotional", agent_responses["default"])
            elif any(word in user_lower for word in ['help', 'support', 'need', 'difficult']):
                return agent_responses.get("support", agent_responses["default"])
            elif any(word in user_lower for word in ['understand', 'listen', 'hear']):
                return agent_responses.get("understanding", agent_responses["default"])
        
        elif agent_name == "solvine":
            if any(word in user_lower for word in ['plan', 'organize', 'strategy', 'approach']):
                return agent_responses.get("planning", agent_responses["default"])
            elif any(word in user_lower for word in ['coordinate', 'manage', 'lead', 'direct']):
                return agent_responses.get("coordination", agent_responses["default"])
            elif any(word in user_lower for word in ['strategy', 'strategic', 'think', 'analyze']):
                return agent_responses.get("strategy", agent_responses["default"])
        
        return agent_responses.get("default", "I'm here to help. Could you tell me more about what you need?")
    
    def _store_interaction(self, agent_name: str, user_input: str, response: str):
        """Store interaction for context memory"""
        if agent_name not in self.agent_memory:
            self.agent_memory[agent_name] = []
        
        interaction = {
            "input": user_input,
            "response": response,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.agent_memory[agent_name].append(interaction)
        
        # Keep only recent interactions (last 10)
        if len(self.agent_memory[agent_name]) > 10:
            self.agent_memory[agent_name] = self.agent_memory[agent_name][-10:]
    
    def _get_recent_history(self, agent_name: str, limit: int = 3) -> list:
        """Get recent conversation history for context"""
        if agent_name not in self.agent_memory:
            return []
        
        return self.agent_memory[agent_name][-limit:]
    
    async def start_voice_conversation(self):
        """Start the voice conversation system"""
        print("🎤 Starting Solvine Systems Voice Interface")
        print("=" * 50)
        print("Available agents:")
        print("🤗 Aiven - Emotional Intelligence Agent")
        print("🧭 Solvine - Coordination Agent")
        print()
        print("Say 'Hey Aiven' or 'Hey Solvine' to start talking!")
        print("Say 'stop' or 'goodbye' to end the conversation.")
        print("=" * 50)
        
        await self.voice_manager.voice_conversation_loop(agent_handler=self)

async def main():
    """Main function to run voice-enabled agent system"""
    try:
        # Create and start the voice handler
        handler = AgentVoiceHandler()
        await handler.start_voice_conversation()
        
    except KeyboardInterrupt:
        print("\n👋 Voice system shutting down...")
    except Exception as e:
        print(f"❌ Error starting voice system: {e}")

if __name__ == "__main__":
    asyncio.run(main())
