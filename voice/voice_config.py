#!/usr/bin/env python3
"""
Voice Configuration for Solvine Systems Agents
Manages voice profiles for each agent with different characteristics
"""

import pyttsx3
import platform
from typing import Dict, Optional

class VoiceProfileManager:
    """Manages voice profiles for different agents"""
    
    def __init__(self):
        self.engine = None
        self.agent_profiles = {}
        
        self.initialize_engine()
    
    def initialize_engine(self):
        """Initialize the TTS engine and discover available voices"""
        try:
            self.engine = pyttsx3.init()
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            print(f"🎙️ Found {len(voices)} system voices:")
            
            for i, voice in enumerate(voices):
                print(f"   {i}: {voice.name} ({voice.id})")
                
            return True
            
        except Exception as e:
            print(f"❌ Voice engine initialization failed: {e}")
            return False
    
    def get_available_voices(self):
        """Get list of available system voices"""
        if not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [(i, voice.name, voice.id) for i, voice in enumerate(voices)]
        except:
            return []
    
    def set_agent_voice(self, agent_name: str, voice_id: Optional[int] = None, 
                       rate: Optional[int] = None, volume: Optional[float] = None):
        """Configure voice settings for specific agent"""
        agent_name = agent_name.lower()
        
        if agent_name not in self.agent_profiles:
            print(f"⚠️ Unknown agent: {agent_name}")
            return False
        
        profile = self.agent_profiles[agent_name]
        
        # Update profile with new settings
        if voice_id is not None:
            profile['voice_id'] = voice_id
        if rate is not None:
            profile['rate'] = rate
        if volume is not None:
            profile['volume'] = volume
            
        print(f"✅ Updated voice profile for {agent_name.title()}")
        return True
    
    def speak_as_agent(self, text: str, agent_name: str = 'system') -> bool:
        """Speak text using agent-specific voice profile"""
        if not self.engine:
            print("❌ Voice engine not available")
            return False
        
        agent_name = agent_name.lower()
        profile = self.agent_profiles.get(agent_name, self.agent_profiles['system'])
        
        try:
            # Apply voice settings
            voices = self.engine.getProperty('voices')
            if voices and len(voices) > profile.get('voice_id', 0):
                voice_id = profile.get('voice_id', 0)
                self.engine.setProperty('voice', voices[voice_id].id)
            
            self.engine.setProperty('rate', profile.get('rate', 170))
            self.engine.setProperty('volume', profile.get('volume', 0.8))
            
            # Speak the text
            print(f"🗣️ {agent_name.title()} speaking: {text[:50]}...")
            self.engine.say(text)
            self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"❌ Speech error for {agent_name}: {e}")
            return False
    
    def test_agent_voice(self, agent_name: str):
        """Test voice for specific agent"""
        test_messages = {
            'jasper': "Hello, I'm Jasper, your head agent and workshop coordinator. Ready for systematic analysis.",
            'midas': "Greetings! I'm Midas, your financial specialist. Let's discuss investment strategies.",
            'aiven': "Hi there! I'm Aiven, bringing creative insights and artistic perspectives to your projects.",
            'halcyon': "Hello, I'm Halcyon. I'm here to provide support and guidance through any challenges.",
            'veilsynth': "Greetings... I am VeilSynth, guardian of patterns and recursive analysis.",
            'quanta': "Hello. I am Quanta, computational specialist. Ready for mathematical analysis.",
            'system': "System voice test. All agents operational and ready for interaction."
        }
        
        message = test_messages.get(agent_name.lower(), f"Test voice for {agent_name}")
        return self.speak_as_agent(message, agent_name)
    
    def create_voice_menu(self):
        """Interactive voice configuration menu"""
        print("\n🎙️ SOLVINE VOICE CONFIGURATION")
        print("="*40)
        
        voices = self.get_available_voices()
        if not voices:
            print("❌ No voices available")
            return
        
        print("\nAvailable System Voices:")
        for i, name, voice_id in voices:
            print(f"   {i}: {name}")
        
        print(f"\nAgent Voice Profiles:")
        for agent, profile in self.agent_profiles.items():
            print(f"   {agent.title()}: Rate={profile['rate']}, Volume={profile['volume']}, Voice ID={profile.get('voice_id', 0)}")
        
        while True:
            print(f"\nOptions:")
            print("1. Test agent voice")
            print("2. Configure agent voice")
            print("3. Test all agents")
            print("4. Exit")
            
            choice = input("\nChoice (1-4): ").strip()
            
            if choice == '1':
                agent = input("Agent name: ").strip()
                self.test_agent_voice(agent)
            elif choice == '2':
                self.configure_agent_interactive()
            elif choice == '3':
                self.test_all_agents()
            elif choice == '4':
                break
    
    def configure_agent_interactive(self):
        """Interactive agent voice configuration"""
        agent = input("Agent name: ").strip().lower()
        if agent not in self.agent_profiles:
            print(f"❌ Unknown agent. Available: {', '.join(self.agent_profiles.keys())}")
            return
        
        try:
            voice_id = input(f"Voice ID (current: {self.agent_profiles[agent].get('voice_id', 0)}): ").strip()
            rate = input(f"Speaking rate (current: {self.agent_profiles[agent]['rate']}): ").strip()
            volume = input(f"Volume 0.0-1.0 (current: {self.agent_profiles[agent]['volume']}): ").strip()
            
            if voice_id:
                self.set_agent_voice(agent, voice_id=int(voice_id))
            if rate:
                self.set_agent_voice(agent, rate=int(rate))
            if volume:
                self.set_agent_voice(agent, volume=float(volume))
                
            print("✅ Voice profile updated!")
            self.test_agent_voice(agent)
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
    
    def test_all_agents(self):
        """Test voices for all agents"""
        print("🎙️ Testing all agent voices...")
        for agent in self.agent_profiles.keys():
            print(f"\n--- {agent.title()} ---")
            self.test_agent_voice(agent)
            input("Press Enter for next agent...")

def main():
    """Main voice configuration interface"""
    print("🎙️ Solvine Systems Voice Configuration")
    
    voice_manager = VoiceProfileManager()
    
    if not voice_manager.engine:
        print("❌ Voice system not available. Please install: pip install pyttsx3")
        return
    
    voice_manager.create_voice_menu()

if __name__ == "__main__":
    main()
