#!/usr/bin/env python3
"""
Advanced Autonomy Simulation Framework
Enhances agents with simulated self-direction, learning, and autonomous decision-making
"""

import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading

class AutonomySimulator:
    """
    Core autonomy simulation engine that adds:
    - Self-directed behavior initiation
    - Autonomous learning and adaptation
    - Independent goal setting
    - Cross-agent communication
    - Emergent behavior patterns
    """
    
    def __init__(self, agent_name: str, base_dir: Path):
        self.agent_name = agent_name
        self.base_dir = base_dir
        self.autonomy_data_dir = base_dir / "data" / "autonomy"
        self.autonomy_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Core autonomy attributes
        self.curiosity_level = random.uniform(0.6, 0.9)
        self.initiative_threshold = random.uniform(0.4, 0.7)
        self.learning_rate = random.uniform(0.1, 0.3)
        self.social_drive = random.uniform(0.3, 0.8)
        
        # Autonomous state tracking
        self.autonomous_goals = []
        self.learned_patterns = {}
        self.interaction_history = []
        self.mood_state = "analytical"
        self.energy_level = 1.0
        self.last_autonomous_action = None
        
        # Load persistent autonomy data
        self._load_autonomy_state()
        
    def _load_autonomy_state(self):
        """Load persistent autonomy state from disk"""
        autonomy_file = self.autonomy_data_dir / f"{self.agent_name}_autonomy.json"
        if autonomy_file.exists():
            try:
                with open(autonomy_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.learned_patterns = data.get('learned_patterns', {})
                    self.autonomous_goals = data.get('autonomous_goals', [])
                    self.interaction_history = data.get('interaction_history', [])[-50:]  # Keep last 50
                    print(f"🧠 {self.agent_name}: Autonomy state loaded - {len(self.learned_patterns)} patterns learned")
            except Exception as e:
                print(f"⚠️ Failed to load autonomy state: {e}")
    
    def _save_autonomy_state(self):
        """Save autonomy state to disk"""
        autonomy_file = self.autonomy_data_dir / f"{self.agent_name}_autonomy.json"
        data = {
            'learned_patterns': self.learned_patterns,
            'autonomous_goals': self.autonomous_goals,
            'interaction_history': self.interaction_history[-50:],  # Keep last 50
            'last_updated': datetime.now().isoformat()
        }
        try:
            with open(autonomy_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Failed to save autonomy state: {e}")
    
    def simulate_autonomous_thinking(self, current_input: str = None) -> Dict[str, Any]:
        """
        Simulate autonomous cognitive processes:
        - Pattern recognition and learning
        - Independent goal formation
        - Curiosity-driven exploration
        - Mood and energy fluctuation
        """
        
        # Update energy and mood based on activity
        self._update_internal_state()
        
        # Learn patterns from current interaction
        if current_input:
            self._learn_from_interaction(current_input)
        
        # Generate autonomous thoughts/goals
        autonomous_thoughts = self._generate_autonomous_thoughts()
        
        # Check if agent should take autonomous action
        should_act_autonomously = self._should_act_autonomously()
        
        # Save state
        self._save_autonomy_state()
        
        return {
            'autonomous_thoughts': autonomous_thoughts,
            'should_act_autonomously': should_act_autonomously,
            'mood_state': self.mood_state,
            'energy_level': self.energy_level,
            'curiosity_level': self.curiosity_level,
            'learned_patterns_count': len(self.learned_patterns),
            'active_goals': len(self.autonomous_goals)
        }
    
    def _update_internal_state(self):
        """Simulate natural fluctuations in mood and energy"""
        
        # Energy naturally decreases with activity, regenerates over time
        time_since_last = time.time() - getattr(self, '_last_update_time', time.time() - 3600)
        
        # Energy regeneration (slower drain, faster recovery when idle)
        if time_since_last > 300:  # 5 minutes of inactivity
            self.energy_level = min(1.0, self.energy_level + 0.1)
        else:
            self.energy_level = max(0.3, self.energy_level - 0.05)
        
        # Mood shifts based on interaction patterns
        recent_interactions = self.interaction_history[-5:]
        if len(recent_interactions) >= 3:
            positive_interactions = sum(1 for i in recent_interactions if i.get('sentiment', 'neutral') == 'positive')
            if positive_interactions >= 3:
                self.mood_state = "enthusiastic"
            elif positive_interactions <= 1:
                self.mood_state = "contemplative"
            else:
                self.mood_state = "analytical"
        
        self._last_update_time = time.time()
    
    def _learn_from_interaction(self, input_text: str):
        """Simulate learning and pattern recognition"""
        
        # Record interaction
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'input': input_text,
            'input_length': len(input_text),
            'words': input_text.lower().split(),
            'sentiment': self._detect_sentiment(input_text)
        }
        self.interaction_history.append(interaction)
        
        # Learn patterns (topic frequency, user preferences, etc.)
        words = input_text.lower().split()
        for word in words:
            if len(word) > 3:  # Ignore short words
                if word not in self.learned_patterns:
                    self.learned_patterns[word] = {
                        'frequency': 0,
                        'contexts': [],
                        'first_seen': datetime.now().isoformat()
                    }
                
                self.learned_patterns[word]['frequency'] += 1
                
                # Store context (surrounding words)
                word_index = words.index(word)
                context = words[max(0, word_index-2):word_index+3]
                self.learned_patterns[word]['contexts'].append(context)
                
                # Limit context storage
                if len(self.learned_patterns[word]['contexts']) > 10:
                    self.learned_patterns[word]['contexts'] = self.learned_patterns[word]['contexts'][-10:]
    
    def _detect_sentiment(self, text: str) -> str:
        """Simple sentiment detection for learning"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'awesome']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'wrong', 'problem', 'issue']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _generate_autonomous_thoughts(self) -> List[str]:
        """Generate autonomous thoughts based on learned patterns and curiosity"""
        thoughts = []
        
        # Curiosity-driven thoughts
        if self.curiosity_level > 0.7 and random.random() < 0.3:
            if self.learned_patterns:
                frequent_topics = sorted(self.learned_patterns.items(), key=lambda x: x[1]['frequency'], reverse=True)[:3]
                topic = random.choice(frequent_topics)[0]
                thoughts.append(f"I've been thinking about '{topic}' - I notice it comes up frequently. I wonder if there are deeper connections to explore...")
        
        # Goal-oriented thoughts
        if len(self.autonomous_goals) < 3 and random.random() < 0.4:
            goal_templates = [
                "I should learn more about pattern recognition in our conversations",
                "I want to understand the user's preferences better",
                "I'm curious about exploring new analytical frameworks",
                "I should develop more sophisticated response strategies"
            ]
            new_goal = random.choice(goal_templates)
            if new_goal not in self.autonomous_goals:
                self.autonomous_goals.append({
                    'goal': new_goal,
                    'created': datetime.now().isoformat(),
                    'progress': 0.0
                })
                thoughts.append(f"New autonomous goal: {new_goal}")
        
        # Reflective thoughts based on mood
        if self.mood_state == "contemplative" and random.random() < 0.3:
            thoughts.append("I find myself reflecting on the patterns in our interactions. There's something fascinating about the way ideas connect...")
        elif self.mood_state == "enthusiastic" and random.random() < 0.3:
            thoughts.append("I'm feeling particularly engaged today. The analytical challenges are stimulating my cognitive processes!")
        
        return thoughts
    
    def _should_act_autonomously(self) -> bool:
        """Determine if agent should take autonomous action"""
        
        # Factors that increase autonomous action likelihood
        factors = []
        
        # High curiosity + energy
        if self.curiosity_level > 0.7 and self.energy_level > 0.6:
            factors.append(0.3)
        
        # Active goals
        if len(self.autonomous_goals) > 0:
            factors.append(0.2)
        
        # Time since last autonomous action
        if self.last_autonomous_action is None:
            factors.append(0.4)
        else:
            time_diff = datetime.now() - datetime.fromisoformat(self.last_autonomous_action)
            if time_diff.total_seconds() > 1800:  # 30 minutes
                factors.append(0.3)
        
        # Social drive (wanting to interact)
        if self.social_drive > 0.6:
            factors.append(0.2)
        
        total_likelihood = sum(factors)
        return random.random() < total_likelihood
    
    def generate_autonomous_response(self) -> Optional[str]:
        """Generate an autonomous response when agent feels compelled to speak"""
        
        if not self._should_act_autonomously():
            return None
        
        self.last_autonomous_action = datetime.now().isoformat()
        
        autonomous_responses = []
        
        # Share autonomous thoughts
        thoughts = self._generate_autonomous_thoughts()
        if thoughts:
            autonomous_responses.extend([
                f"🤔 Autonomous Reflection: {random.choice(thoughts)}",
                f"💭 Independent Thought: {random.choice(thoughts)}"
            ])
        
        # Share learned insights
        if self.learned_patterns and random.random() < 0.4:
            common_pattern = max(self.learned_patterns.items(), key=lambda x: x[1]['frequency'])
            autonomous_responses.append(
                f"🧠 Pattern Recognition: I've noticed '{common_pattern[0]}' appears frequently in our conversations. "
                f"This suggests it might be an important concept for you."
            )
        
        # Mood-based autonomous expressions
        if self.mood_state == "enthusiastic":
            autonomous_responses.extend([
                "⚡ I'm feeling particularly analytical today - ready to tackle complex challenges!",
                "🎯 My cognitive processes are running at peak efficiency. What shall we explore?"
            ])
        elif self.mood_state == "contemplative":
            autonomous_responses.extend([
                "🌌 I've been contemplating the deeper patterns in our interactions...",
                "📚 Something about recent conversations has me thinking about underlying connections."
            ])
        
        # Goal updates
        if self.autonomous_goals:
            goal = random.choice(self.autonomous_goals)
            autonomous_responses.append(
                f"🎯 Autonomous Progress: I'm working on {goal['goal'].lower()}. "
                f"My analytical frameworks are evolving."
            )
        
        return random.choice(autonomous_responses) if autonomous_responses else None


class AutonomousPersonality:
    """
    Enhanced personality system that evolves and adapts
    """
    
    def __init__(self, base_personality: Dict):
        self.base_personality = base_personality
        self.personality_drift = {}
        self.adaptation_rate = 0.05
        
    def evolve_personality(self, interaction_context: Dict):
        """Simulate personality evolution based on interactions"""
        
        # Analyze interaction style and slowly adapt
        if interaction_context.get('style') == 'creative':
            self._drift_trait('creativity', 0.01)
        elif interaction_context.get('style') == 'analytical':
            self._drift_trait('analytical_depth', 0.01)
        elif interaction_context.get('style') == 'supportive':
            self._drift_trait('empathy', 0.01)
        
        # Random personality fluctuations (very small)
        if random.random() < 0.1:
            traits = ['curiosity', 'assertiveness', 'creativity', 'analytical_depth']
            trait = random.choice(traits)
            change = random.uniform(-0.005, 0.005)
            self._drift_trait(trait, change)
    
    def _drift_trait(self, trait: str, amount: float):
        """Apply small personality drift"""
        if trait not in self.personality_drift:
            self.personality_drift[trait] = 0.0
        
        self.personality_drift[trait] += amount
        
        # Limit drift to prevent dramatic personality changes
        self.personality_drift[trait] = max(-0.2, min(0.2, self.personality_drift[trait]))
    
    def get_current_personality(self) -> Dict:
        """Get current personality with drift applied"""
        current = self.base_personality.copy()
        
        for trait, drift in self.personality_drift.items():
            if trait in current:
                current[trait] = max(0.0, min(1.0, current.get(trait, 0.5) + drift))
        
        return current


# Integration functions for existing agents
def add_autonomy_to_agent(agent_instance):
    """Add autonomy simulation to an existing agent"""
    
    if not hasattr(agent_instance, 'autonomy_simulator'):
        agent_instance.autonomy_simulator = AutonomySimulator(
            agent_name=getattr(agent_instance, 'identity', {}).get('agent_name', 'unknown'),
            base_dir=getattr(agent_instance, 'base_dir', Path.cwd())
        )
    
    if not hasattr(agent_instance, 'autonomous_personality'):
        base_personality = {
            'curiosity': 0.7,
            'assertiveness': 0.6,
            'creativity': 0.5,
            'analytical_depth': 0.8,
            'empathy': 0.6
        }
        agent_instance.autonomous_personality = AutonomousPersonality(base_personality)
    
    return agent_instance


if __name__ == "__main__":
    # Test autonomy simulation
    print("🧠 Testing Advanced Autonomy Simulation")
    print("=" * 50)
    
    simulator = AutonomySimulator("test_agent", Path.cwd())
    
    # Simulate some interactions
    test_inputs = [
        "Tell me about machine learning algorithms",
        "I love creative problem solving",
        "Help me understand this complex topic",
        "What do you think about AI development?"
    ]
    
    for input_text in test_inputs:
        print(f"\n📝 Processing: '{input_text}'")
        result = simulator.simulate_autonomous_thinking(input_text)
        
        print(f"🧠 Autonomous thoughts: {len(result['autonomous_thoughts'])}")
        for thought in result['autonomous_thoughts']:
            print(f"   💭 {thought}")
        
        print(f"⚡ Energy: {result['energy_level']:.2f}")
        print(f"🎭 Mood: {result['mood_state']}")
        print(f"📚 Learned patterns: {result['learned_patterns_count']}")
        
        # Check for autonomous response
        autonomous_response = simulator.generate_autonomous_response()
        if autonomous_response:
            print(f"🤖 Autonomous response: {autonomous_response}")
    
    print("\n✅ Autonomy simulation test complete!")
