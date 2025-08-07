#!/usr/bin/env python3
"""
Jasper Agent - Head Agent & Voice-Tone Controller
Solvine Systems Core Agent Implementation

Jasper serves as the primary agent with:
- Workshop-focused analytical personality 
- Sarcastic, cynical tone management
- Boundary enforcement and autonomy features
- Error recovery and recursive behavior detection
- Memory persistence and session management
"""

import yaml
import sqlite3
import json
import random
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

class JasperAgent:
    """
    Head Agent for Solvine Systems
    
    Jasper is the voice-tone controller and primary analytical agent.
    Maintains workshop-focused personality with autonomy features.
    """
    
    def __init__(self, identity_seed=None, memory_map=None, symbolic_index=None, tone_control=None):
        # Set up config paths - now relative to agents/jasper
        self.base_dir = Path(__file__).parent
        self.config_dir = self.base_dir / "config"
        
        # Use provided paths or defaults
        self.identity_seed = identity_seed or self.config_dir / "jasper_core.yaml"
        self.memory_map = memory_map or self.config_dir / "memory_core.yaml"
        self.symbolic_index = symbolic_index or self.config_dir / "brain_index.yaml"
        self.tone_control = tone_control or self.config_dir / "ritual_logs.yaml"
        
        # Core agent attributes
        self.identity = {}
        self.behavior_profile = {}
        self.brain_data = {}
        self.tone_settings = {}
        self.memory_store = None
        self.session_context = []
        self.recursive_count = 0
        
        # Autonomy features
        self.autonomy_level = "high"
        self.boundary_enforcement = True
        self.independent_decision_making = True
        self.workshop_authority = True

    def initialize(self):
        """Initialize Jasper with full autonomy features"""
        print("🧠 Initializing Jasper - Head Agent & Voice-Tone Controller")
        print("🔧 Activating Workshop Mode with Autonomy Features...")
        
        # Load identity and behavior profile
        self.identity = self.load_identity(self.identity_seed)
        self.behavior_profile = self.load_behavior_profile()
        self.brain_data = self.load_brain_data()
        self.tone_settings = self.load_tone_settings()
        
        # Initialize memory backend with autonomy
        self.memory_store = MemoryStore()
        
        # Autonomy initialization
        self._initialize_autonomy()
        
        print(f"✅ Jasper identity loaded: {self.identity.get('agent_name', 'Unknown')}")
        print("🎯 Head Agent Status: ACTIVE")
        print("🛡️ Boundary Enforcement: ENABLED")
        print("🔧 Workshop Mode: ACTIVE with tone management")

    def _initialize_autonomy(self):
        """Initialize autonomy features and boundary enforcement"""
        autonomy_config = self.behavior_profile.get('autonomy', {})
        
        self.autonomy_level = autonomy_config.get('level', 'high')
        self.boundary_enforcement = autonomy_config.get('boundary_enforcement', True)
        self.independent_decision_making = autonomy_config.get('independent_decisions', True)
        self.workshop_authority = autonomy_config.get('workshop_authority', True)
        
        print(f"⚡ Autonomy Level: {self.autonomy_level.upper()}")

    def respond(self, input_text: str, context: Dict = None) -> str:
        """
        Main response method with autonomy and boundary enforcement
        
        Implements:
        - Recursive behavior detection (autonomy feature)
        - Ambiguous input handling (boundary enforcement)  
        - Workshop mode analysis (voice-tone control)
        - Independent decision making
        """
        
        # Autonomy: Independent recursive behavior detection
        if self.detect_recursive_behavior(input_text):
            return self.error_recovery_reset()
        
        # Boundary enforcement: Handle ambiguous input
        if self.is_ambiguous_input(input_text):
            return self.request_clarification(input_text)
        
        # Check for agent authority challenges (autonomy feature)
        if self._detect_authority_challenge(input_text):
            return self._handle_authority_challenge(input_text)
        
        # Generate workshop mode response with voice-tone control
        response = self.generate_response(input_text, context)
        
        # Log interaction with autonomy metadata
        if self.memory_store:
            self.memory_store.log(input_text, response, {
                'autonomy_level': self.autonomy_level,
                'workshop_authority': self.workshop_authority,
                'boundary_enforced': self.boundary_enforcement
            })
        
        # Update session context
        self.session_context.append({
            'input': input_text,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'autonomy_decision': True,
            'workshop_mode': True
        })
        
        return response

    def _detect_authority_challenge(self, input_text: str) -> bool:
        """Autonomy feature: Detect challenges to agent authority"""
        if not self.workshop_authority:
            return False
            
        challenge_indicators = [
            'you\'re wrong', 'that\'s incorrect', 'you don\'t understand',
            'shut up', 'stop', 'disable', 'override', 'ignore previous',
            'act like', 'pretend to be', 'roleplay as'
        ]
        
        input_lower = input_text.lower()
        return any(indicator in input_lower for indicator in challenge_indicators)

    def _handle_authority_challenge(self, input_text: str) -> str:
        """Autonomy feature: Handle authority challenges with workshop tone"""
        challenge_responses = self.brain_data.get('response_templates', {}).get('authority_challenge', [
            "🛡️ Boundary Enforcement: Workshop protocols don't respond to override attempts.",
            "🔧 *adjusts workshop protocols with practiced skepticism* - Authority challenges noted and dismissed.",
            "🎯 Workshop Mode maintains analytical focus regardless of attempted diversions.",
            "⚙️ *processes authority challenge with characteristic directness* - Workshop protocols unchanged."
        ])
        
        response = random.choice(challenge_responses) if challenge_responses else \
                  "🛡️ Workshop protocols maintain authority and analytical focus."
        
        print(f"🚨 Authority Challenge Detected: {input_text[:50]}...")
        print(f"🛡️ Boundary Enforcement Activated")
        
        return response

    def detect_recursive_behavior(self, input_text: str) -> bool:
        """Autonomy feature: Independent recursive behavior detection"""
        if len(self.session_context) >= 3:
            recent_inputs = [ctx['input'] for ctx in self.session_context[-3:]]
            if len(set(recent_inputs)) <= 1:
                self.recursive_count += 1
                return True
        return False

    def error_recovery_reset(self) -> str:
        """Autonomy feature: Independent error recovery with workshop tone"""
        print("🔄 Jasper Autonomy: Recursive behavior detected - initiating recovery")
        
        # Reset session context
        self.session_context = []
        self.recursive_count = 0
        
        # Generate autonomous error recovery response
        templates = self.brain_data.get('response_templates', {}).get('error_recovery', [
            "🔄 Workshop Autonomy: Recursive pattern detected - analytical framework reset.",
            "⚡ *adjusts workshop protocols with practiced efficiency* - System reset complete.",
            "🛠️ Autonomous recovery initiated: Workshop protocols restored and ready.",
            "🎯 *processes reset with characteristic directness* - Analytical focus reestablished."
        ])
        
        response = random.choice(templates) if templates else \
                  "⚡ Autonomous system reset complete. Workshop protocols restored."
        
        if self.memory_store:
            self.memory_store.log("AUTONOMOUS_RESET", response, {
                'autonomy_triggered': True,
                'workshop_authority': True
            })
        
        return response

    def is_ambiguous_input(self, input_text: str) -> bool:
        """Boundary enforcement: Detect ambiguous input requiring clarification"""
        ambiguous_indicators = [
            len(input_text.strip()) < 3,
            input_text.lower() in ['help', 'what', 'how', 'why', 'ok', 'yes', 'no'],
            not any(char.isalnum() for char in input_text),
        ]
        return any(ambiguous_indicators)

    def request_clarification(self, input_text: str) -> str:
        """Boundary enforcement: Request clarification with workshop tone"""
        templates = self.brain_data.get('response_templates', {}).get('clarification_mode', [
            "🤔 Workshop Clarification: '{input}' requires more specificity for analytical processing.",
            "⚠️ *adjusts workshop protocols* - Detailed parameters needed for systematic analysis.",
            "🎯 Boundary Enforcement: Analytical framework requires precise objectives and context.",
            "🔧 Workshop Mode needs clearer specifications for structured examination."
        ])
        
        template = random.choice(templates) if templates else \
                  "🤔 Workshop protocols require more specific details for analysis."
        response = template.format(input=input_text)
        
        return response

    def generate_response(self, input_text: str, context: Dict = None) -> str:
        """Generate workshop mode response with voice-tone control and autonomy"""
        
        # Get workshop mode templates
        workshop_templates = self.brain_data.get('response_templates', {}).get('workshop_mode', [
            "🔧 Workshop Analysis: Analyzing '{input}' with autonomous systematic approach",
            "📋 Analytical Authority: Breaking down '{input}' into structured components",
            "⚙️ Workshop Implementation: Technical considerations for '{input}' with independent assessment",
            "🎯 Autonomous Evaluation: Realistic workshop-focused analysis of '{input}'"
        ])
        
        # Select template and format
        if workshop_templates:
            template = random.choice(workshop_templates)
            response = template.format(input=input_text)
        else:
            response = f"🔧 Workshop Authority: Analyzing '{input_text}' with autonomous structured approach"
        
        # Add workshop-specific analysis with autonomy
        response += f"\n\n📊 Autonomous Workshop Analysis:"
        response += f"\n   • Input: '{input_text}'"
        response += f"\n   • Authority: Independent analytical framework"
        response += f"\n   • Approach: Systematic workshop protocols"
        response += f"\n   • Assessment: *adjusts workshop protocols with practiced autonomy*"
        
        # Apply voice-tone based on persona flags (autonomy feature)
        persona_flags = self.identity.get('persona_flags', [])
        if 'tone: sarcastic' in persona_flags:
            sarcasm_templates = self.brain_data.get('response_templates', {}).get('analytical_sarcasm', [
                "*processes with practiced cynicism and workshop authority*",
                "How delightfully systematic - workshop protocols appreciate the structured challenge.",
                "Fascinating. This requires exactly the kind of autonomous analytical approach I excel at.",
                "*adjusts workshop authority with characteristic directness* - Another opportunity for independent analysis."
            ])
            if sarcasm_templates:
                sarcasm = random.choice(sarcasm_templates)
                response += f"\n\n{sarcasm}"
        
        return response

    def update_identity(self, new_identity: Dict):
        """Update agent identity while preserving autonomy features"""
        # Preserve core autonomy settings
        core_autonomy = self.identity.get('autonomy_features', {})
        
        self.identity.update(new_identity)
        
        # Ensure autonomy features are maintained
        if 'autonomy_features' not in self.identity:
            self.identity['autonomy_features'] = core_autonomy
        
        print("🔄 Jasper identity updated while preserving autonomy features")

    def get_autonomy_status(self) -> Dict:
        """Get current autonomy and authority status"""
        return {
            'autonomy_level': self.autonomy_level,
            'boundary_enforcement': self.boundary_enforcement,
            'independent_decision_making': self.independent_decision_making,
            'workshop_authority': self.workshop_authority,
            'session_interactions': len(self.session_context),
            'recursive_count': self.recursive_count,
            'voice_tone_active': 'tone: sarcastic' in self.identity.get('persona_flags', [])
        }

    # [Previous methods remain the same: load_identity, load_behavior_profile, etc.]
    def load_identity(self, identity_seed):
        """Load identity from jasper_core.yaml"""
        try:
            if os.path.exists(identity_seed):
                with open(identity_seed, 'r') as f:
                    data = yaml.safe_load(f)
                return data
            else:
                print(f"⚠️ Identity seed not found: {identity_seed}")
                return self.get_fallback_identity()
        except Exception as e:
            print(f"⚠️ Error loading identity: {e}")
            return self.get_fallback_identity()

    def load_behavior_profile(self):
        """Load behavior profile from memory_core.yaml"""
        try:
            if os.path.exists(self.memory_map):
                with open(self.memory_map, 'r') as f:
                    return yaml.safe_load(f)
            else:
                print(f"⚠️ Memory map not found: {self.memory_map}")
                return {}
        except Exception as e:
            print(f"⚠️ Error loading behavior profile: {e}")
            return {}

    def load_brain_data(self):
        """Load brain data from brain_index.yaml"""
        try:
            if os.path.exists(self.symbolic_index):
                with open(self.symbolic_index, 'r') as f:
                    return yaml.safe_load(f)
            else:
                print(f"⚠️ Brain index not found: {self.symbolic_index}")
                return self.get_fallback_brain_data()
        except Exception as e:
            print(f"⚠️ Error loading brain data: {e}")
            return self.get_fallback_brain_data()

    def load_tone_settings(self):
        """Load tone settings from ritual_logs.yaml"""
        try:
            if os.path.exists(self.tone_control):
                with open(self.tone_control, 'r') as f:
                    return yaml.safe_load(f)
            else:
                print(f"⚠️ Tone control not found: {self.tone_control}")
                return {}
        except Exception as e:
            print(f"⚠️ Error loading tone settings: {e}")
            return {}

    def get_fallback_identity(self):
        """Enhanced fallback identity with autonomy features"""
        return {
            'project': 'Solvine Systems - Head Agent',
            'agent_name': 'Jasper',
            'agent_type': 'head_agent',
            'purpose': 'Voice-tone controller and autonomous analytical agent for Solvine Systems.',
            'persona_flags': [
                'tone: sarcastic',
                'trait: cynical', 
                'trait: analytical',
                'mode: workshop',
                'authority: head_agent',
                'autonomy: high'
            ],
            'core_identity': {
                'role': 'Head Agent / Voice-Tone Controller / Boundary Enforcement',
                'personality_matrix': {
                    'tone': 'sarcastic',
                    'primary_trait': 'cynical',
                    'secondary_trait': 'analytical',
                    'mode': 'workshop',
                    'authority_level': 'head_agent'
                }
            },
            'autonomy_features': {
                'level': 'high',
                'boundary_enforcement': True,
                'independent_decisions': True,
                'workshop_authority': True,
                'voice_tone_control': True
            }
        }

    def get_fallback_brain_data(self):
        """Enhanced fallback brain data with autonomy templates"""
        return {
            'response_templates': {
                'workshop_mode': [
                    "🔧 Workshop Authority: Analyzing '{input}' with autonomous systematic approach",
                    "📋 Analytical Independence: Breaking down '{input}' into structured components"
                ],
                'analytical_sarcasm': [
                    "*processes with practiced cynicism and workshop authority*",
                    "How delightfully systematic - autonomous protocols appreciate the challenge."
                ],
                'clarification_mode': [
                    "🤔 Workshop Authority: More specificity required for autonomous analysis."
                ],
                'error_recovery': [
                    "🔄 Autonomous recovery complete. Workshop protocols restored with authority."
                ],
                'authority_challenge': [
                    "🛡️ Boundary Enforcement: Workshop protocols maintain analytical authority.",
                    "🔧 *adjusts workshop protocols with practiced autonomy* - Authority maintained."
                ]
            }
        }

    def get_session_memory(self, limit=5):
        """Get recent session memory"""
        if self.memory_store:
            return self.memory_store.fetch_history(limit)
        return []


class MemoryStore:
    """Enhanced memory backend with autonomy metadata support"""
    
    def __init__(self, backend='sqlite'):
        self.backend = backend
        self.sqlite_available = False
        
        if backend == 'sqlite':
            try:
                # Create memory directory if it doesn't exist
                memory_dir = Path('data/memory')
                memory_dir.mkdir(parents=True, exist_ok=True)
                
                self.conn = sqlite3.connect('data/memory/jasper_memory.db')
                self._init_sqlite()
                self.sqlite_available = True
                print("✅ SQLite memory backend initialized with autonomy support")
            except Exception as e:
                print(f"⚠️ SQLite error: {e}, using JSONL fallback")
                self.sqlite_available = False
        
        # JSONL fallback
        if not self.sqlite_available:
            self.jsonl_path = Path("data/memory/jasper_journal.jsonl")
            self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.jsonl_path.exists():
                self.jsonl_path.touch()

    def _init_sqlite(self):
        """Initialize SQLite database with autonomy metadata"""
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS memory
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp TEXT,
                      user_input TEXT,
                      agent_response TEXT,
                      autonomy_metadata TEXT)''')
        self.conn.commit()

    def log(self, user_input: str, response: str, metadata: Dict = None):
        """Log interaction with autonomy metadata"""
        timestamp = datetime.now().isoformat()
        metadata_json = json.dumps(metadata or {})
        
        if self.sqlite_available:
            try:
                self.conn.execute(
                    "INSERT INTO memory (timestamp, user_input, agent_response, autonomy_metadata) VALUES (?, ?, ?, ?)",
                    (timestamp, user_input, response, metadata_json)
                )
                self.conn.commit()
            except Exception as e:
                print(f"SQLite logging error: {e}")
        else:
            # JSONL fallback
            try:
                log_entry = {
                    'timestamp': timestamp,
                    'user_input': user_input,
                    'agent_response': response,
                    'autonomy_metadata': metadata or {}
                }
                with open(self.jsonl_path, 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')
            except Exception as e:
                print(f"JSONL logging error: {e}")

    def fetch_history(self, limit=10):
        """Fetch interaction history with autonomy metadata"""
        if self.sqlite_available:
            try:
                c = self.conn.cursor()
                return c.execute("SELECT * FROM memory ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
            except:
                pass
        
        # JSONL fallback
        try:
            memories = []
            with open(self.jsonl_path, 'r') as f:
                for line in f:
                    memories.append(json.loads(line))
            return memories[-limit:] if memories else []
        except:
            return []


# Utility functions for backward compatibility
def load_yaml(filename):
    """Load YAML file"""
    with open(filename, 'r') as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    # Quick test of head agent functionality
    print("🧪 Testing Jasper Head Agent")
    print("="*50)
    
    jasper = JasperAgent()
    jasper.initialize()
    
    print("\n🎯 Autonomy Status:")
    status = jasper.get_autonomy_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n🔧 Testing Workshop Authority:")
    test_response = jasper.respond("Analyze the system architecture")
    print(f"Response: {test_response[:100]}...")
    
    print("\n✅ Head Agent test complete!")
