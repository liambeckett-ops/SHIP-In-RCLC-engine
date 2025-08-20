#!/usr/bin/env python3
"""
Unified Voice System for Solvine Systems
Single voice interface with multi-agent brain coordination
"""

import asyncio
import json
import os
import wave
import pyaudio
import speech_recognition as sr
from pathlib import Path
import threading
import queue
import time
from datetime import datetime

try:
    import pyttsx3  # Text-to-speech
except ImportError:
    pyttsx3 = None

try:
    import whisper  # Advanced speech recognition
except ImportError:
    whisper = None

class UnifiedVoiceSystem:
    def __init__(self, config_path: str = "unified_voice_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
        # Audio settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.record_seconds = 30
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = self._initialize_tts()
        self.whisper_model = self._initialize_whisper()
        
        # Unified voice profile (one voice for all agents)
        self.unified_voice_profile = {
            "voice_id": 0,  # Consistent voice across all responses
            "rate": 170,    # Balanced speaking rate
            "volume": 0.85,
            "pitch": 135,
            "personality": "intelligent, helpful, adaptive"
        }
        
        # Agent coordination system (brain-like operation)
        self.agent_roles = {
            "solvine": {
                "role": "Coordination & Strategy",
                "expertise": ["planning", "organization", "leadership", "strategy"],
                "activation_keywords": ["plan", "organize", "coordinate", "strategy", "manage", "lead"]
            },
            "aiven": {
                "role": "Emotional Intelligence",
                "expertise": ["emotions", "empathy", "support", "relationships", "understanding"],
                "activation_keywords": ["feel", "emotion", "support", "help", "understand", "care"]
            },
            "midas": {
                "role": "Financial Analysis", 
                "expertise": ["money", "finance", "investment", "economics", "budget", "market"],
                "activation_keywords": ["money", "finance", "invest", "budget", "cost", "profit", "market"]
            },
            "jasper": {
                "role": "Ethics & Philosophy",
                "expertise": ["ethics", "morality", "philosophy", "principles", "values"],
                "activation_keywords": ["ethics", "moral", "right", "wrong", "philosophy", "values", "principles"]
            },
            "veilsynth": {
                "role": "Creativity & Analysis",
                "expertise": ["creativity", "art", "design", "analysis", "innovation", "imagination"],
                "activation_keywords": ["creative", "art", "design", "imagine", "innovate", "analyze"]
            },
            "halcyon": {
                "role": "Safety & Security",
                "expertise": ["safety", "security", "risk", "protection", "monitoring"],
                "activation_keywords": ["safe", "secure", "risk", "protect", "danger", "monitor"]
            },
            "quanta": {
                "role": "Logic & Computation",
                "expertise": ["logic", "math", "computation", "analysis", "calculation", "reasoning"],
                "activation_keywords": ["calculate", "logic", "math", "compute", "analyze", "reason"]
            }
        }
        
        # Conversation memory
        self.conversation_history = []
        self.current_context = None
        
        print("🧠 Unified Solvine Systems Voice Interface initialized")
        print(f"👥 {len(self.agent_roles)} specialized agents coordinated")
        print("🎭 Single unified voice for seamless interaction")
        
    def _load_config(self) -> dict:
        """Load unified voice configuration"""
        default_config = {
            "unified_voice": True,
            "real_time_response": True,
            "speech_recognition": {
                "engine": "whisper",
                "language": "en-US", 
                "timeout": 8,
                "phrase_timeout": 2.5
            },
            "text_to_speech": {
                "engine": "pyttsx3",
                "rate": 170,
                "volume": 0.85
            },
            "conversation_settings": {
                "wake_phrase": "hey solvine",
                "alternative_wake": ["solvine", "system"],
                "end_phrases": ["goodbye", "end conversation", "stop", "exit"],
                "context_memory": 5  # Remember last 5 exchanges
            },
            "agent_coordination": {
                "auto_routing": True,  # Automatically route to best agent
                "multi_agent_responses": True,  # Allow multiple agents to contribute
                "unified_personality": True  # Single coherent personality
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"⚠️ Error loading config: {e}")
        
        return default_config
    
    def _initialize_tts(self):
        """Initialize unified text-to-speech engine"""
        if pyttsx3:
            try:
                engine = pyttsx3.init()
                
                # Apply unified voice settings
                profile = self.unified_voice_profile
                engine.setProperty('rate', profile['rate'])
                engine.setProperty('volume', profile['volume'])
                
                # Set consistent voice
                voices = engine.getProperty('voices')
                if voices and len(voices) > profile['voice_id']:
                    engine.setProperty('voice', voices[profile['voice_id']].id)
                
                return engine
            except Exception as e:
                print(f"⚠️ TTS initialization failed: {e}")
        return None
    
    def _initialize_whisper(self):
        """Initialize Whisper model for speech recognition"""
        if whisper:
            try:
                model = whisper.load_model("base")
                return model
            except Exception as e:
                print(f"⚠️ Whisper initialization failed: {e}")
        return None
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        print("🎙️ Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Microphone ready for conversation")
    
    def listen_for_speech(self, timeout: int = 8) -> str:
        """Listen for speech and convert to text"""
        try:
            print("👂 Listening...")
            
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=self.config['speech_recognition']['phrase_timeout']
                )
            
            print("🔄 Processing speech...")
            
            # Try Whisper first for better accuracy
            if self.whisper_model:
                try:
                    temp_file = "temp_audio.wav"
                    with wave.open(temp_file, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
                        wf.setframerate(16000)
                        wf.writeframes(audio.get_wav_data())
                    
                    result = self.whisper_model.transcribe(temp_file)
                    os.remove(temp_file)
                    
                    text = result["text"].strip()
                    print(f"💬 You said: '{text}'")
                    return text
                    
                except Exception as e:
                    print(f"⚠️ Whisper failed, using Google: {e}")
            
            # Fallback to Google
            try:
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.config['speech_recognition']['language']
                )
                print(f"💬 You said: '{text}'")
                return text
                
            except sr.UnknownValueError:
                print("❓ Could not understand speech - please try again")
                return ""
            except sr.RequestError as e:
                print(f"⚠️ Speech recognition error: {e}")
                return ""
                
        except sr.WaitTimeoutError:
            return ""  # Silent timeout, no error message
        except Exception as e:
            print(f"⚠️ Error during speech recognition: {e}")
            return ""
    
    def speak_response(self, text: str):
        """Speak response using unified voice"""
        if not text or not self.tts_engine:
            return
        
        try:
            # Clean text for natural speech
            clean_text = text.replace("*", "").replace("#", "").replace("`", "")
            
            print(f"🗣️ Solvine: {clean_text[:60]}{'...' if len(clean_text) > 60 else ''}")
            
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"⚠️ Error during speech synthesis: {e}")
    
    def detect_wake_phrase(self, text: str) -> bool:
        """Check if wake phrase was spoken"""
        text_lower = text.lower()
        
        # Check main wake phrase
        if self.config['conversation_settings']['wake_phrase'] in text_lower:
            return True
        
        # Check alternatives
        for alt_wake in self.config['conversation_settings']['alternative_wake']:
            if alt_wake.lower() in text_lower:
                return True
        
        return False
    
    def is_end_phrase(self, text: str) -> bool:
        """Check if conversation should end"""
        text_lower = text.lower()
        return any(end_phrase in text_lower for end_phrase in self.config['conversation_settings']['end_phrases'])
    
    def route_to_agents(self, user_input: str) -> list:
        """Intelligently route input to appropriate agent(s)"""
        user_lower = user_input.lower()
        activated_agents = []
        
        # Score each agent based on keyword matches
        agent_scores = {}
        for agent_name, agent_info in self.agent_roles.items():
            score = 0
            for keyword in agent_info['activation_keywords']:
                if keyword in user_lower:
                    score += 1
            
            if score > 0:
                agent_scores[agent_name] = score
        
        # Sort by relevance
        if agent_scores:
            # Get top scoring agents
            sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Primary agent (highest score)
            activated_agents.append(sorted_agents[0][0])
            
            # Add secondary agents if their scores are close
            if len(sorted_agents) > 1 and sorted_agents[1][1] >= sorted_agents[0][1] * 0.7:
                activated_agents.append(sorted_agents[1][0])
        else:
            # Default to Solvine for coordination if no specific match
            activated_agents = ["solvine"]
        
        return activated_agents
    
    async def generate_unified_response(self, user_input: str, activated_agents: list) -> str:
        """Generate unified response coordinating multiple agents"""
        
        # Build context from conversation history
        context = self._build_context()
        
        # Create agent-specific insights
        agent_insights = {}
        for agent in activated_agents:
            agent_info = self.agent_roles[agent]
            insight = self._generate_agent_insight(agent, agent_info, user_input, context)
            agent_insights[agent] = insight
        
        # Synthesize unified response
        unified_response = self._synthesize_response(user_input, agent_insights, activated_agents)
        
        # Store in conversation history
        self._store_interaction(user_input, unified_response, activated_agents)
        
        return unified_response
    
    def _generate_agent_insight(self, agent_name: str, agent_info: dict, user_input: str, context: str) -> str:
        """Generate insight from specific agent perspective"""
        
        insights = {
            "solvine": f"From a coordination perspective: I can help organize and structure an approach to '{user_input}'. Let me coordinate the best strategy.",
            
            "aiven": f"From an emotional intelligence perspective: I understand the feelings behind '{user_input}'. This seems to involve {self._detect_emotional_context(user_input)}.",
            
            "midas": f"From a financial perspective: Regarding '{user_input}', I can analyze the economic implications and resource requirements.",
            
            "jasper": f"From an ethical perspective: '{user_input}' raises important considerations about values and principles we should examine.",
            
            "veilsynth": f"From a creative perspective: '{user_input}' offers interesting possibilities for innovative approaches and creative solutions.",
            
            "halcyon": f"From a safety perspective: I want to ensure '{user_input}' is approached with appropriate risk assessment and safeguards.",
            
            "quanta": f"From a logical perspective: Let me analyze the computational and reasoning aspects of '{user_input}' systematically."
        }
        
        return insights.get(agent_name, f"I can provide expertise in {agent_info['role']} for your request.")
    
    def _detect_emotional_context(self, text: str) -> str:
        """Detect emotional context for Aiven"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['stress', 'anxious', 'worried', 'nervous']):
            return "stress and anxiety"
        elif any(word in text_lower for word in ['happy', 'excited', 'joy', 'great']):
            return "positive emotions"
        elif any(word in text_lower for word in ['sad', 'down', 'depressed', 'upset']):
            return "sadness or disappointment"
        elif any(word in text_lower for word in ['angry', 'frustrated', 'mad', 'annoyed']):
            return "frustration or anger"
        else:
            return "mixed emotions and needs"
    
    def _synthesize_response(self, user_input: str, agent_insights: dict, activated_agents: list) -> str:
        """Synthesize unified response from agent insights"""
        
        primary_agent = activated_agents[0]
        primary_role = self.agent_roles[primary_agent]['role']
        
        # Start with primary agent's perspective
        response_parts = []
        
        # Acknowledgment
        response_parts.append(f"I understand you're asking about {user_input.lower()}.")
        
        # Primary insight
        if primary_agent == "solvine":
            response_parts.append("Let me coordinate the best approach for you.")
        elif primary_agent == "aiven":
            response_parts.append("I can sense this is important to you emotionally.")
        elif primary_agent == "midas":
            response_parts.append("I'll analyze the financial and resource aspects.")
        elif primary_agent == "jasper":
            response_parts.append("This involves some important ethical considerations.")
        elif primary_agent == "veilsynth":
            response_parts.append("I see creative possibilities in this situation.")
        elif primary_agent == "halcyon":
            response_parts.append("Let me ensure we approach this safely.")
        elif primary_agent == "quanta":
            response_parts.append("I'll analyze this logically step by step.")
        
        # Add specific guidance based on input
        guidance = self._generate_specific_guidance(user_input, primary_agent)
        if guidance:
            response_parts.append(guidance)
        
        # Offer follow-up
        response_parts.append("What specific aspect would you like me to focus on?")
        
        return " ".join(response_parts)
    
    def _generate_specific_guidance(self, user_input: str, primary_agent: str) -> str:
        """Generate specific guidance based on input and primary agent"""
        
        user_lower = user_input.lower()
        
        if primary_agent == "solvine":
            if any(word in user_lower for word in ['project', 'plan', 'organize']):
                return "I can help break this into clear steps and coordinate the timeline."
            elif any(word in user_lower for word in ['team', 'group', 'manage']):
                return "I'll help coordinate team dynamics and resource allocation."
        
        elif primary_agent == "aiven":
            if any(word in user_lower for word in ['feel', 'emotion', 'stress']):
                return "I'm here to provide emotional support and help you process these feelings."
            elif any(word in user_lower for word in ['relationship', 'conflict']):
                return "I can help navigate the interpersonal aspects and communication strategies."
        
        # Add more specific guidance for other agents as needed
        
        return ""
    
    def _build_context(self) -> str:
        """Build context from recent conversation history"""
        if not self.conversation_history:
            return ""
        
        recent_history = self.conversation_history[-3:]  # Last 3 exchanges
        context_parts = []
        
        for exchange in recent_history:
            context_parts.append(f"User: {exchange['input']}")
            context_parts.append(f"Response: {exchange['response']}")
        
        return "\n".join(context_parts)
    
    def _store_interaction(self, user_input: str, response: str, activated_agents: list):
        """Store interaction in conversation history"""
        interaction = {
            "input": user_input,
            "response": response,
            "agents": activated_agents,
            "timestamp": time.time()
        }
        
        self.conversation_history.append(interaction)
        
        # Keep only recent history
        max_history = self.config['conversation_settings']['context_memory']
        if len(self.conversation_history) > max_history:
            self.conversation_history = self.conversation_history[-max_history:]
    
    async def start_conversation(self):
        """Start unified voice conversation"""
        print("🎤 Solvine Systems - Unified Voice Interface")
        print("=" * 55)
        print("🧠 Intelligent agent coordination with unified voice")
        print("🎭 Single voice, multiple specialized perspectives")
        print()
        print(f"💡 Say '{self.config['conversation_settings']['wake_phrase']}' to start")
        print("💡 Say 'goodbye' to end conversation")
        print("=" * 55)
        
        self.calibrate_microphone()
        
        conversation_active = False
        
        while True:
            try:
                # Listen for input
                user_input = self.listen_for_speech(timeout=30 if not conversation_active else 15)
                
                if not user_input:
                    if conversation_active:
                        print("💭 I'm still here if you need anything...")
                    continue
                
                # Check for end phrases
                if self.is_end_phrase(user_input):
                    if conversation_active:
                        self.speak_response("Goodbye! I'm here whenever you need me.")
                    break
                
                # Check for wake phrase or continue conversation
                if not conversation_active:
                    if self.detect_wake_phrase(user_input):
                        conversation_active = True
                        # Remove wake phrase from input
                        for wake in [self.config['conversation_settings']['wake_phrase']] + self.config['conversation_settings']['alternative_wake']:
                            user_input = user_input.lower().replace(wake.lower(), "").strip()
                        
                        if user_input:
                            # Process the request immediately
                            activated_agents = self.route_to_agents(user_input)
                            response = await self.generate_unified_response(user_input, activated_agents)
                            self.speak_response(response)
                        else:
                            # Just acknowledged, wait for actual request
                            self.speak_response("Hello! I'm here to help. What can I do for you?")
                    # If no wake phrase, ignore input when conversation not active
                    continue
                else:
                    # Conversation is active, process any input
                    activated_agents = self.route_to_agents(user_input)
                    response = await self.generate_unified_response(user_input, activated_agents)
                    self.speak_response(response)
                    
            except KeyboardInterrupt:
                print("\n👋 Voice conversation ended")
                break
            except Exception as e:
                print(f"⚠️ Error in conversation: {e}")
                continue

async def main():
    """Main function for unified voice system"""
    try:
        system = UnifiedVoiceSystem()
        await system.start_conversation()
    except Exception as e:
        print(f"❌ Error starting voice system: {e}")

if __name__ == "__main__":
    asyncio.run(main())
