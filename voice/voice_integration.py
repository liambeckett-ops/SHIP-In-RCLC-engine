#!/usr/bin/env python3
"""
Voice Integration System for Solvine Systems
Enables voice input/output for Aiven & Solvine agents
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
    import openai_whisper as whisper  # Advanced speech recognition
except ImportError:
    whisper = None

class VoiceIntegrationManager:
    def __init__(self, config_path: str = "voice_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
        # Audio settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.record_seconds = 30  # Max recording time
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = self._initialize_tts()
        self.whisper_model = self._initialize_whisper()
        
        # Voice profiles for agents
        self.voice_profiles = {
            "aiven": {
                "voice_id": 0,  # Female voice for emotional intelligence
                "rate": 180,    # Speaking rate
                "volume": 0.8,
                "pitch": 150,
                "personality": "warm, empathetic, caring"
            },
            "solvine": {
                "voice_id": 1,  # Male voice for coordination
                "rate": 160,    # Slightly slower, more authoritative
                "volume": 0.9,
                "pitch": 120,
                "personality": "confident, clear, strategic"
            }
        }
        
        # Audio queue for real-time processing
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.current_agent = None
        
        print("🎤 Voice Integration System initialized")
        print(f"📊 Available voices: {len(self.voice_profiles)}")
        if self.whisper_model:
            print("🧠 Whisper model loaded for advanced speech recognition")
        
    def _load_config(self) -> dict:
        """Load voice configuration"""
        default_config = {
            "enabled_agents": ["aiven", "solvine"],
            "speech_recognition": {
                "engine": "google",  # Can be "google", "whisper", or "sphinx"
                "language": "en-US",
                "timeout": 10,
                "phrase_timeout": 2
            },
            "text_to_speech": {
                "engine": "pyttsx3",  # Can be "pyttsx3" or "gtts"
                "rate": 170,
                "volume": 0.8
            },
            "voice_commands": {
                "wake_words": ["hey aiven", "aiven", "hey solvine", "solvine"],
                "stop_words": ["stop", "end conversation", "goodbye"]
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
        """Initialize text-to-speech engine"""
        if pyttsx3:
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', self.config['text_to_speech']['rate'])
                engine.setProperty('volume', self.config['text_to_speech']['volume'])
                return engine
            except Exception as e:
                print(f"⚠️ TTS initialization failed: {e}")
        return None
    
    def _initialize_whisper(self):
        """Initialize Whisper model for advanced speech recognition"""
        if whisper:
            try:
                model = whisper.load_model("base")
                return model
            except Exception as e:
                print(f"⚠️ Whisper initialization failed: {e}")
        return None
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        print("🎙️ Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Microphone calibrated")
    
    def set_voice_for_agent(self, agent_name: str):
        """Set TTS voice characteristics for specific agent"""
        if agent_name not in self.voice_profiles:
            print(f"⚠️ Unknown agent: {agent_name}")
            return
        
        if not self.tts_engine:
            return
        
        profile = self.voice_profiles[agent_name]
        
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices and len(voices) > profile['voice_id']:
                self.tts_engine.setProperty('voice', voices[profile['voice_id']].id)
            
            self.tts_engine.setProperty('rate', profile['rate'])
            self.tts_engine.setProperty('volume', profile['volume'])
            
            self.current_agent = agent_name
            print(f"🎭 Voice set for {agent_name}: {profile['personality']}")
            
        except Exception as e:
            print(f"⚠️ Error setting voice for {agent_name}: {e}")
    
    def listen_for_speech(self, timeout: int = 10) -> str:
        """Listen for speech input and convert to text"""
        try:
            print("👂 Listening for speech...")
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=self.config['speech_recognition']['phrase_timeout']
                )
            
            print("🔄 Processing speech...")
            
            # Try Whisper first if available
            if self.whisper_model:
                try:
                    # Save audio to temporary file for Whisper
                    temp_file = "temp_audio.wav"
                    with wave.open(temp_file, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
                        wf.setframerate(16000)
                        wf.writeframes(audio.get_wav_data())
                    
                    result = self.whisper_model.transcribe(temp_file)
                    os.remove(temp_file)
                    
                    text = result["text"].strip()
                    print(f"💬 Whisper recognized: '{text}'")
                    return text
                    
                except Exception as e:
                    print(f"⚠️ Whisper failed, falling back to Google: {e}")
            
            # Fallback to Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(
                    audio, 
                    language=self.config['speech_recognition']['language']
                )
                print(f"💬 Google recognized: '{text}'")
                return text
                
            except sr.UnknownValueError:
                print("❓ Could not understand speech")
                return ""
            except sr.RequestError as e:
                print(f"⚠️ Speech recognition error: {e}")
                return ""
                
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            return ""
        except Exception as e:
            print(f"⚠️ Error during speech recognition: {e}")
            return ""
    
    def speak_text(self, text: str, agent_name: str = None):
        """Convert text to speech with agent-specific voice"""
        if not text or not self.tts_engine:
            return
        
        if agent_name:
            self.set_voice_for_agent(agent_name)
        
        try:
            print(f"🗣️ {agent_name or 'Agent'} speaking: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"⚠️ Error during speech synthesis: {e}")
    
    def detect_wake_word(self, text: str) -> str:
        """Detect which agent is being called"""
        text_lower = text.lower()
        
        for word in self.config['voice_commands']['wake_words']:
            if word.lower() in text_lower:
                if 'aiven' in word.lower():
                    return 'aiven'
                elif 'solvine' in word.lower():
                    return 'solvine'
        
        return None
    
    def is_stop_command(self, text: str) -> bool:
        """Check if user wants to stop conversation"""
        text_lower = text.lower()
        return any(stop_word in text_lower for stop_word in self.config['voice_commands']['stop_words'])
    
    async def voice_conversation_loop(self, agent_handler=None):
        """Main voice conversation loop"""
        print("🎤 Starting voice conversation mode")
        print("💡 Say 'Hey Aiven' or 'Hey Solvine' to start")
        print("💡 Say 'stop' or 'goodbye' to end")
        
        self.calibrate_microphone()
        
        while True:
            try:
                # Listen for wake word
                user_input = self.listen_for_speech(timeout=30)
                
                if not user_input:
                    continue
                
                # Check for stop command
                if self.is_stop_command(user_input):
                    print("👋 Ending voice conversation")
                    break
                
                # Detect which agent is being called
                target_agent = self.detect_wake_word(user_input)
                
                if target_agent:
                    print(f"🎯 Agent {target_agent} activated")
                    
                    # Remove wake word from input
                    for wake_word in self.config['voice_commands']['wake_words']:
                        if wake_word.lower() in user_input.lower():
                            user_input = user_input.lower().replace(wake_word.lower(), "").strip()
                            break
                    
                    # If there's remaining text, process it
                    if user_input:
                        response = await self._process_agent_request(target_agent, user_input, agent_handler)
                        if response:
                            self.speak_text(response, target_agent)
                    else:
                        # Agent acknowledged, wait for actual query
                        greeting = self._get_agent_greeting(target_agent)
                        self.speak_text(greeting, target_agent)
                        
                        # Listen for the actual query
                        query = self.listen_for_speech(timeout=15)
                        if query and not self.is_stop_command(query):
                            response = await self._process_agent_request(target_agent, query, agent_handler)
                            if response:
                                self.speak_text(response, target_agent)
                
            except KeyboardInterrupt:
                print("\n🛑 Voice conversation interrupted")
                break
            except Exception as e:
                print(f"⚠️ Error in conversation loop: {e}")
                continue
    
    def _get_agent_greeting(self, agent_name: str) -> str:
        """Get personalized greeting for agent"""
        greetings = {
            "aiven": "Hi there! I'm Aiven. How can I help you today?",
            "solvine": "Hello! Solvine here. What can I coordinate for you?"
        }
        return greetings.get(agent_name, "Hello! How can I assist you?")
    
    async def _process_agent_request(self, agent_name: str, query: str, agent_handler=None):
        """Process request through appropriate agent"""
        if agent_handler and hasattr(agent_handler, 'process_request'):
            try:
                response = await agent_handler.process_request(agent_name, query)
                return response
            except Exception as e:
                print(f"⚠️ Error processing request: {e}")
        
        # Fallback response
        responses = {
            "aiven": f"I understand you're asking about '{query}'. As your emotional intelligence agent, I'm here to provide support and understanding.",
            "solvine": f"I've noted your request about '{query}'. As your coordination agent, I'll help organize and strategize the best approach."
        }
        
        return responses.get(agent_name, "I'm processing your request.")
    
    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"💾 Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"⚠️ Error saving config: {e}")

def install_voice_dependencies():
    """Install required voice processing libraries"""
    print("📦 Installing voice integration dependencies...")
    
    dependencies = [
        "pyaudio",
        "SpeechRecognition", 
        "pyttsx3",
        "openai-whisper"
    ]
    
    import subprocess
    import sys
    
    for package in dependencies:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to install {package}: {e}")
            if package == "pyaudio":
                print("💡 Try: pip install pipwin && pipwin install pyaudio")

async def test_voice_integration():
    """Test voice integration system"""
    print("🧪 Testing voice integration...")
    
    voice_manager = VoiceIntegrationManager()
    
    # Test TTS for both agents
    print("\n🎭 Testing text-to-speech for Aiven...")
    voice_manager.speak_text(
        "Hello! I'm Aiven, your emotional intelligence agent. I'm here to provide support and understanding.",
        "aiven"
    )
    
    print("\n🎭 Testing text-to-speech for Solvine...")
    voice_manager.speak_text(
        "Greetings! I'm Solvine, your coordination agent. I help organize and strategize solutions.",
        "solvine"
    )
    
    # Test speech recognition
    print("\n👂 Testing speech recognition...")
    print("Please say something...")
    
    text = voice_manager.listen_for_speech(timeout=10)
    if text:
        print(f"✅ Speech recognition successful: '{text}'")
        
        # Test wake word detection
        agent = voice_manager.detect_wake_word(text)
        if agent:
            print(f"🎯 Wake word detected for agent: {agent}")
        else:
            print("💡 No wake word detected. Try saying 'Hey Aiven' or 'Hey Solvine'")
    else:
        print("❌ No speech detected")
    
    print("\n✅ Voice integration test completed")

if __name__ == "__main__":
    import asyncio
    
    print("🎤 Solvine Systems Voice Integration")
    print("=" * 50)
    
    # Check if dependencies need to be installed
    try:
        import pyaudio
        import speech_recognition
        import pyttsx3
    except ImportError:
        print("📦 Installing missing dependencies...")
        install_voice_dependencies()
    
    # Run test
    asyncio.run(test_voice_integration())
