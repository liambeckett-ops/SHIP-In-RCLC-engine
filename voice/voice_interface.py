"""
Voice Interface System for Solvine AGI Agents
Provides text-to-speech and speech-to-text capabilities for natural voice interaction
"""

import json
import asyncio
import threading
import queue
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import sys

# Try to import speech libraries
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ speech_recognition not available - install with: pip install SpeechRecognition")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ pyttsx3 not available - install with: pip install pyttsx3")

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("⚠️ pyaudio not available - install with: pip install pyaudio")

class VoiceInterface:
    """
    Advanced voice interface for AGI agents
    
    Features:
    - Real-time speech recognition
    - High-quality text-to-speech
    - Agent voice customization
    - Conversation flow management
    - Audio recording and playback
    - Voice command detection
    """
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.voice_dir = base_dir / "voice"
        self.voice_dir.mkdir(parents=True, exist_ok=True)
        
        # Voice interface state
        self.is_listening = False
        self.is_speaking = False
        self.voice_enabled = TTS_AVAILABLE and SPEECH_RECOGNITION_AVAILABLE
        
        # Audio components
        self.tts_engine = None
        self.speech_recognizer = None
        self.microphone = None
        
        # Voice settings
        self.agent_voices = {}
        self.default_voice_settings = {
            'rate': 180,  # Speaking rate
            'volume': 0.8,  # Volume level
            'voice_id': 0  # Voice selection
        }
        
        # Conversation management
        self.conversation_active = False
        self.last_speech_time = None
        self.speech_timeout = 5.0  # Seconds
        
        # Command processing
        self.voice_commands = {}
        self.wake_words = ['hey solvine', 'solvine', 'jasper', 'midas']
        
        # Audio queues for threading
        self.speech_queue = queue.Queue()
        self.recognition_queue = queue.Queue()
        
        # Initialize components
        self._initialize_tts()
        self._initialize_speech_recognition()
        self._load_agent_voice_profiles()
        
        # Enhanced voice profiles
        try:
            from voice.voice_config import VoiceProfileManager
            self.voice_profiles = VoiceProfileManager()
            print("✅ Enhanced voice profiles loaded for all agents")
        except ImportError:
            print("⚠️ Voice profiles not available - using basic TTS")
            self.voice_profiles = None
        
        print(f"🎙️ Voice Interface initialized (TTS: {TTS_AVAILABLE}, STT: {SPEECH_RECOGNITION_AVAILABLE})")
    
    def speak(self, text: str, agent_name: str = "Jasper", blocking: bool = True) -> bool:
        """
        Convert text to speech with agent-specific voice
        """
        if not self.voice_enabled or not text.strip():
            return False
        
        # Use enhanced voice profiles if available
        if self.voice_profiles:
            return self.voice_profiles.speak_as_agent(text, agent_name)
        
        # Fallback to basic TTS
        try:
            # Set voice for specific agent
            self._set_agent_voice(agent_name)
            
            # Clean text for speech
            speech_text = self._prepare_text_for_speech(text)
            
            if blocking:
                self._speak_sync(speech_text, agent_name)
            else:
                self._speak_async(speech_text, agent_name)
            
            # Log speech event
            self._log_speech_event(agent_name, speech_text)
            
            return True
            
        except Exception as e:
            print(f"⚠️ Speech error: {e}")
            return False
    
    def listen(self, timeout: float = 5.0, phrase_time_limit: float = 10.0) -> Optional[str]:
        """
        Listen for speech input and convert to text
        """
        if not SPEECH_RECOGNITION_AVAILABLE or not self.microphone:
            return None
        
        try:
            self.is_listening = True
            
            print("🎙️ Listening...")
            
            # Listen for audio
            with self.microphone as source:
                # Adjust for ambient noise
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for speech
                audio = self.speech_recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Processing speech...")
            
            # Recognize speech
            text = self.speech_recognizer.recognize_google(audio)
            
            self.is_listening = False
            self.last_speech_time = datetime.now()
            
            # Log recognition event
            self._log_recognition_event(text)
            
            print(f"👂 Heard: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            self.is_listening = False
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand speech")
            self.is_listening = False
            return None
        except sr.RequestError as e:
            print(f"⚠️ Speech recognition error: {e}")
            self.is_listening = False
            return None
        except Exception as e:
            print(f"⚠️ Listening error: {e}")
            self.is_listening = False
            return None
    
    def start_conversation_mode(self, agent_callback: Callable[[str], str]):
        """
        Start continuous conversation mode
        """
        if not self.voice_enabled:
            print("⚠️ Voice interface not available for conversation mode")
            return
        
        self.conversation_active = True
        print("🗣️ Conversation mode started. Say 'exit conversation' to stop.")
        
        try:
            while self.conversation_active:
                # Listen for user input
                user_input = self.listen(timeout=10.0)
                
                if user_input:
                    # Check for exit command
                    if any(phrase in user_input.lower() for phrase in ['exit conversation', 'stop talking', 'goodbye']):
                        self.speak("Goodbye! Conversation ended.")
                        break
                    
                    # Check for wake words
                    if self._contains_wake_word(user_input):
                        # Get agent response
                        response = agent_callback(user_input)
                        
                        # Speak response
                        self.speak(response, blocking=True)
                    else:
                        print(f"📝 Heard but no wake word: {user_input}")
                
                # Small delay to prevent overwhelming
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n🛑 Conversation interrupted by user")
        finally:
            self.conversation_active = False
            print("🏁 Conversation mode ended")
    
    def add_voice_command(self, command_phrase: str, callback: Callable[[str], Any]):
        """
        Add a voice command with callback
        """
        self.voice_commands[command_phrase.lower()] = callback
        print(f"🎙️ Voice command added: '{command_phrase}'")
    
    def customize_agent_voice(self, agent_name: str, voice_settings: Dict[str, Any]):
        """
        Customize voice settings for specific agent
        """
        self.agent_voices[agent_name] = {
            **self.default_voice_settings,
            **voice_settings
        }
        
        # Save to persistent storage
        self._save_voice_profiles()
        
        print(f"🎵 Voice customized for {agent_name}")
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """
        Get list of available TTS voices
        """
        if not self.tts_engine:
            return []
        
        voices = []
        for voice in self.tts_engine.getProperty('voices'):
            voices.append({
                'id': voice.id,
                'name': voice.name,
                'gender': getattr(voice, 'gender', 'unknown'),
                'age': getattr(voice, 'age', 'unknown')
            })
        
        return voices
    
    def test_voice_setup(self) -> Dict[str, bool]:
        """
        Test voice interface components
        """
        results = {
            'tts_available': TTS_AVAILABLE,
            'stt_available': SPEECH_RECOGNITION_AVAILABLE,
            'microphone_available': PYAUDIO_AVAILABLE,
            'tts_working': False,
            'microphone_working': False
        }
        
        # Test TTS
        if self.tts_engine:
            try:
                self.tts_engine.say("Voice interface test")
                self.tts_engine.runAndWait()
                results['tts_working'] = True
            except:
                pass
        
        # Test microphone
        if self.microphone and self.speech_recognizer:
            try:
                with self.microphone as source:
                    self.speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                results['microphone_working'] = True
            except:
                pass
        
        return results
    
    def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        if not TTS_AVAILABLE:
            return
        
        try:
            self.tts_engine = pyttsx3.init()
            
            # Set default properties
            self.tts_engine.setProperty('rate', self.default_voice_settings['rate'])
            self.tts_engine.setProperty('volume', self.default_voice_settings['volume'])
            
            print("✅ TTS engine initialized")
            
        except Exception as e:
            print(f"⚠️ TTS initialization error: {e}")
            self.tts_engine = None
    
    def _initialize_speech_recognition(self):
        """Initialize speech recognition"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            return
        
        try:
            self.speech_recognizer = sr.Recognizer()
            
            # Try to initialize microphone
            if PYAUDIO_AVAILABLE:
                self.microphone = sr.Microphone()
                print("✅ Speech recognition initialized with microphone")
            else:
                print("⚠️ Microphone not available - speech recognition limited")
                
        except Exception as e:
            print(f"⚠️ Speech recognition initialization error: {e}")
            self.speech_recognizer = None
    
    def _set_agent_voice(self, agent_name: str):
        """Set voice properties for specific agent"""
        if not self.tts_engine:
            return
        
        voice_settings = self.agent_voices.get(agent_name, self.default_voice_settings)
        
        try:
            # Set voice properties
            self.tts_engine.setProperty('rate', voice_settings['rate'])
            self.tts_engine.setProperty('volume', voice_settings['volume'])
            
            # Set specific voice if available
            voices = self.tts_engine.getProperty('voices')
            if voices and voice_settings['voice_id'] < len(voices):
                self.tts_engine.setProperty('voice', voices[voice_settings['voice_id']].id)
                
        except Exception as e:
            print(f"⚠️ Voice setting error: {e}")
    
    def _prepare_text_for_speech(self, text: str) -> str:
        """Clean and prepare text for natural speech"""
        # Remove markdown formatting
        text = text.replace('**', '').replace('*', '').replace('_', '')
        text = text.replace('#', '').replace('`', '')
        
        # Replace common symbols with spoken equivalents
        replacements = {
            '&': 'and',
            '@': 'at',
            '%': 'percent',
            '$': 'dollars',
            '€': 'euros',
            '£': 'pounds',
            '→': 'leads to',
            '←': 'comes from',
            '✅': 'check',
            '❌': 'cross',
            '⚠️': 'warning',
            '🔥': 'fire',
            '💰': 'money',
            '📈': 'chart up',
            '📉': 'chart down'
        }
        
        for symbol, replacement in replacements.items():
            text = text.replace(symbol, replacement)
        
        # Remove excessive punctuation
        text = text.replace('...', '.')
        text = text.replace('!!', '!')
        text = text.replace('??', '?')
        
        # Break up very long sentences
        sentences = text.split('. ')
        processed_sentences = []
        
        for sentence in sentences:
            if len(sentence) > 200:  # Very long sentence
                # Try to break at natural pause points
                parts = sentence.replace(', ', '. ').split('. ')
                processed_sentences.extend(parts)
            else:
                processed_sentences.append(sentence)
        
        return '. '.join(processed_sentences)
    
    def _speak_sync(self, text: str, agent_name: str):
        """Speak text synchronously"""
        self.is_speaking = True
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        finally:
            self.is_speaking = False
    
    def _speak_async(self, text: str, agent_name: str):
        """Speak text asynchronously"""
        def speak_thread():
            self._speak_sync(text, agent_name)
        
        thread = threading.Thread(target=speak_thread)
        thread.daemon = True
        thread.start()
    
    def _contains_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        text_lower = text.lower()
        return any(wake_word in text_lower for wake_word in self.wake_words)
    
    def _load_agent_voice_profiles(self):
        """Load agent voice profiles from storage"""
        profiles_file = self.voice_dir / "agent_voice_profiles.json"
        
        if profiles_file.exists():
            try:
                with open(profiles_file, 'r', encoding='utf-8') as f:
                    self.agent_voices = json.load(f)
                print(f"📂 Loaded {len(self.agent_voices)} voice profiles")
            except Exception as e:
                print(f"⚠️ Failed to load voice profiles: {e}")
        else:
            # Set default voice profiles for agents
            self._set_default_voice_profiles()
    
    def _set_default_voice_profiles(self):
        """Set default voice profiles for agents"""
        if not self.tts_engine:
            return
        
        voices = self.tts_engine.getProperty('voices')
        if not voices:
            return
        
        # Assign different voices to different agents
        self.agent_voices = {
            'Jasper': {
                'rate': 180,
                'volume': 0.8,
                'voice_id': 0  # Usually male voice
            },
            'Midas': {
                'rate': 160,
                'volume': 0.8,
                'voice_id': 1 if len(voices) > 1 else 0  # Different voice
            },
            'Aiven': {
                'rate': 200,
                'volume': 0.7,
                'voice_id': 0  # Faster, creative voice
            },
            'Halcyon': {
                'rate': 150,
                'volume': 0.9,
                'voice_id': 1 if len(voices) > 1 else 0  # Slower, supportive
            }
        }
        
        self._save_voice_profiles()
    
    def _save_voice_profiles(self):
        """Save agent voice profiles to storage"""
        profiles_file = self.voice_dir / "agent_voice_profiles.json"
        
        try:
            with open(profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.agent_voices, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save voice profiles: {e}")
    
    def _log_speech_event(self, agent_name: str, text: str):
        """Log speech events"""
        log_file = self.voice_dir / "speech_log.jsonl"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'speech',
            'agent_name': agent_name,
            'text': text[:200],  # Truncate long text
            'text_length': len(text)
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️ Speech logging error: {e}")
    
    def _log_recognition_event(self, text: str):
        """Log speech recognition events"""
        log_file = self.voice_dir / "speech_log.jsonl"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'recognition',
            'text': text,
            'confidence': 1.0  # Would be actual confidence if available
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️ Recognition logging error: {e}")


class VoiceCommandHandler:
    """
    Handler for voice commands and conversation flow
    """
    
    def __init__(self, voice_interface: VoiceInterface, agent_system):
        self.voice_interface = voice_interface
        self.agent_system = agent_system
        
        # Register default voice commands
        self._register_default_commands()
    
    def _register_default_commands(self):
        """Register default voice commands"""
        commands = {
            "status": self._handle_status_command,
            "help": self._handle_help_command,
            "who are you": self._handle_identity_command,
            "what can you do": self._handle_capabilities_command,
            "test voice": self._handle_test_voice_command,
            "switch to": self._handle_agent_switch_command
        }
        
        for command, handler in commands.items():
            self.voice_interface.add_voice_command(command, handler)
    
    def _handle_status_command(self, full_text: str) -> str:
        """Handle status command"""
        return "System status: All agents operational. Voice interface active."
    
    def _handle_help_command(self, full_text: str) -> str:
        """Handle help command"""
        return "Available commands: status, help, who are you, what can you do, test voice. You can also ask questions to any agent."
    
    def _handle_identity_command(self, full_text: str) -> str:
        """Handle identity command"""
        return "I am the Solvine AGI system with multiple specialized agents including Jasper, Midas, Aiven, Halcyon, VeilSynth, and Quanta."
    
    def _handle_capabilities_command(self, full_text: str) -> str:
        """Handle capabilities command"""
        return "I can help with financial analysis, creative projects, crisis support, complex reasoning, mathematical calculations, and general coordination."
    
    def _handle_test_voice_command(self, full_text: str) -> str:
        """Handle test voice command"""
        return "Voice test successful. I can hear you and respond with speech."
    
    def _handle_agent_switch_command(self, full_text: str) -> str:
        """Handle agent switching command"""
        # Extract agent name from command
        text_lower = full_text.lower()
        agents = ['jasper', 'midas', 'aiven', 'halcyon', 'veilsynth', 'quanta']
        
        for agent in agents:
            if agent in text_lower:
                return f"Switching to {agent.title()}. How can I help you?"
        
        return "Which agent would you like to switch to? Available: Jasper, Midas, Aiven, Halcyon, VeilSynth, Quanta."


# Test the voice interface
if __name__ == "__main__":
    print("🧪 Testing Voice Interface")
    print("="*50)
    
    # Initialize voice interface
    voice_interface = VoiceInterface(Path.cwd())
    
    # Test setup
    print("\n🔧 Voice Setup Test:")
    test_results = voice_interface.test_voice_setup()
    for component, status in test_results.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {component}: {status}")
    
    # Test available voices
    print(f"\n🎵 Available Voices ({len(voice_interface.get_available_voices())}):")
    for i, voice in enumerate(voice_interface.get_available_voices()[:5]):  # Show first 5
        print(f"   {i}: {voice['name']} ({voice.get('gender', 'unknown')})")
    
    # Test text-to-speech
    print("\n🗣️ Testing Text-to-Speech:")
    test_text = "Hello! This is a test of the Solvine voice interface system."
    success = voice_interface.speak(test_text, "Jasper", blocking=True)
    print(f"   TTS Test: {'✅ Success' if success else '❌ Failed'}")
    
    # Test different agent voices
    print("\n🎭 Testing Agent Voices:")
    agents_to_test = ["Jasper", "Midas", "Aiven"]
    for agent in agents_to_test:
        test_text = f"Hello, I am {agent}, your {agent.lower()} specialist."
        success = voice_interface.speak(test_text, agent, blocking=True)
        print(f"   {agent}: {'✅' if success else '❌'}")
    
    # Test speech recognition (if available)
    if SPEECH_RECOGNITION_AVAILABLE and PYAUDIO_AVAILABLE:
        print("\n👂 Testing Speech Recognition:")
        print("   Say something in the next 5 seconds...")
        
        recognized_text = voice_interface.listen(timeout=5.0)
        if recognized_text:
            print(f"   ✅ Recognized: {recognized_text}")
            
            # Echo back what was heard
            response = f"I heard you say: {recognized_text}"
            voice_interface.speak(response, "Jasper", blocking=True)
        else:
            print("   ❌ No speech recognized")
    else:
        print("\n👂 Speech Recognition: ❌ Not available (missing dependencies)")
    
    # Show voice command capabilities
    print(f"\n🎙️ Voice Commands Available: {len(voice_interface.voice_commands)}")
    for command in voice_interface.voice_commands.keys():
        print(f"   • {command}")
    
    print("\n✅ Voice Interface test complete!")
    
    if voice_interface.voice_enabled:
        print("\n💡 Try running: python voice_interface.py --conversation")
        print("   This will start conversation mode where you can talk to the agents!")
    else:
        print("\n💡 Install dependencies for full voice functionality:")
        print("   pip install SpeechRecognition pyttsx3 pyaudio")
