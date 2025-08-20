"""
Base Agent Architecture for Specialized AGI Agents
Provides shared foundation for all specialized agents with AGI-like capabilities
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import uuid

# Try to import autonomy simulation
try:
    from autonomy_simulation import AutonomySimulator, AutonomousPersonality
    AUTONOMY_AVAILABLE = True
except ImportError:
    AUTONOMY_AVAILABLE = False
    print("⚠️ Autonomy simulation not available - using basic mode")

class BaseAgent(ABC):
    """
    Abstract base class for all specialized agents
    
    Provides:
    - AGI-like autonomy simulation
    - Advanced memory systems
    - Personality evolution
    - Learning capabilities
    - Cross-agent communication protocols
    """
    
    def __init__(self, agent_name: str, specialization: str, base_personality: Dict[str, float]):
        self.agent_name = agent_name
        self.specialization = specialization
        self.agent_id = str(uuid.uuid4())
        
        # Core directories
        self.base_dir = Path(__file__).parent.parent
        self.agent_dir = self.base_dir / "agents" / agent_name.lower()
        self.memory_dir = self.base_dir / "memory" / "agent_memories"
        self.knowledge_dir = self.base_dir / "memory" / "shared_knowledge"
        
        # Ensure directories exist
        self.agent_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        # Memory and learning systems
        self.memory_store = AgentMemoryStore(agent_name, self.memory_dir)
        self.knowledge_base = SpecializedKnowledgeBase(agent_name, specialization, self.knowledge_dir)
        self.learning_engine = AdaptiveLearningEngine(agent_name)
        
        # AGI-like features
        self.session_context = []
        self.interaction_count = 0
        self.expertise_level = 0.5  # Grows with experience
        self.confidence_level = 0.7
        
        # Autonomy simulation
        if AUTONOMY_AVAILABLE:
            self.autonomy_simulator = AutonomySimulator(
                agent_name=agent_name,
                base_dir=self.base_dir
            )
            self.autonomous_personality = AutonomousPersonality(base_personality)
        else:
            self.autonomy_simulator = None
            self.autonomous_personality = None
        
        # Load agent configuration and memories
        self.load_agent_state()
        
        print(f"🤖 {agent_name} initialized as {specialization} specialist")
    
    @abstractmethod
    def process_query(self, query: str, context: Dict = None) -> str:
        """Process a user query using specialized knowledge and capabilities"""
        pass
    
    @abstractmethod
    def get_specialized_capabilities(self) -> List[str]:
        """Return list of specialized capabilities this agent provides"""
        pass
    
    def respond(self, input_text: str, context: Dict = None) -> str:
        """
        Main response method with AGI-like processing
        """
        self.interaction_count += 1
        
        # Advanced autonomy simulation
        autonomy_response = None
        if AUTONOMY_AVAILABLE and self.autonomy_simulator:
            autonomy_state = self.autonomy_simulator.simulate_autonomous_thinking(input_text)
            
            # Check if agent should act autonomously
            if autonomy_state.get('should_act_autonomously', False):
                autonomy_response = self._generate_autonomous_response(autonomy_state, input_text)
                
            # Evolve personality based on interaction
            if self.autonomous_personality:
                interaction_context = {
                    'style': self._detect_input_style(input_text),
                    'complexity': len(input_text.split()),
                    'sentiment': autonomy_state.get('sentiment', 'neutral')
                }
                self.autonomous_personality.evolve_personality(interaction_context)
        
        # Generate specialized response
        if autonomy_response:
            specialized_response = autonomy_response
        else:
            specialized_response = self.process_query(input_text, context)
        
        # Learn from interaction
        self.learning_engine.process_interaction(input_text, specialized_response, context)
        
        # Update expertise based on successful interactions
        self._update_expertise(input_text, specialized_response)
        
        # Store interaction in memory
        self.memory_store.store_interaction(
            user_input=input_text,
            agent_response=specialized_response,
            context=context,
            autonomy_metadata={
                'expertise_level': self.expertise_level,
                'confidence_level': self.confidence_level,
                'autonomy_active': bool(autonomy_response)
            }
        )
        
        # Add to session context
        self.session_context.append({
            'input': input_text,
            'response': specialized_response,
            'timestamp': datetime.now().isoformat(),
            'expertise_used': self.expertise_level
        })
        
        # Keep session context manageable
        if len(self.session_context) > 20:
            self.session_context = self.session_context[-15:]
        
        return specialized_response
    
    def communicate_with_agent(self, other_agent: 'BaseAgent', message: str) -> str:
        """
        Agent-to-agent communication protocol
        """
        communication_log = {
            'from_agent': self.agent_name,
            'to_agent': other_agent.agent_name,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'communication_id': str(uuid.uuid4())
        }
        
        # Log the communication
        self._log_agent_communication(communication_log)
        
        # Process the message through the other agent
        response = other_agent._process_agent_communication(self, message)
        
        communication_log['response'] = response
        self._log_agent_communication(communication_log)
        
        return response
    
    def _process_agent_communication(self, from_agent: 'BaseAgent', message: str) -> str:
        """
        Process communication from another agent
        """
        context = {
            'source': 'agent_communication',
            'from_agent': from_agent.agent_name,
            'from_specialization': from_agent.specialization
        }
        
        # Respond as if this is a specialized query
        response = self.process_query(message, context)
        
        return f"[{self.agent_name} to {from_agent.agent_name}] {response}"
    
    def share_knowledge(self, knowledge_item: Dict) -> None:
        """
        Share knowledge with other agents through the collective knowledge base
        """
        knowledge_item.update({
            'source_agent': self.agent_name,
            'specialization': self.specialization,
            'timestamp': datetime.now().isoformat(),
            'expertise_level': self.expertise_level
        })
        
        self.knowledge_base.add_shared_knowledge(knowledge_item)
    
    def learn_from_others(self) -> List[Dict]:
        """
        Learn from knowledge shared by other agents
        """
        other_agent_knowledge = self.knowledge_base.get_relevant_knowledge(
            exclude_agent=self.agent_name,
            limit=10
        )
        
        learned_items = []
        for knowledge in other_agent_knowledge:
            if self.learning_engine.should_learn_knowledge(knowledge):
                self.learning_engine.integrate_external_knowledge(knowledge)
                learned_items.append(knowledge)
        
        return learned_items
    
    def get_agent_status(self) -> Dict:
        """
        Get comprehensive agent status and capabilities
        """
        status = {
            'agent_name': self.agent_name,
            'specialization': self.specialization,
            'agent_id': self.agent_id,
            'interaction_count': self.interaction_count,
            'expertise_level': round(self.expertise_level, 3),
            'confidence_level': round(self.confidence_level, 3),
            'specialized_capabilities': self.get_specialized_capabilities(),
            'memory_count': self.memory_store.get_memory_count(),
            'knowledge_contributions': self.knowledge_base.get_contribution_count(),
            'learning_progress': self.learning_engine.get_learning_metrics()
        }
        
        # Add autonomy status if available
        if AUTONOMY_AVAILABLE and self.autonomy_simulator:
            autonomy_state = self.autonomy_simulator.simulate_autonomous_thinking()
            status.update({
                'autonomy_active': True,
                'mood_state': autonomy_state.get('mood_state'),
                'energy_level': autonomy_state.get('energy_level'),
                'curiosity_level': autonomy_state.get('curiosity_level'),
                'autonomous_goals': autonomy_state.get('active_goals', [])
            })
            
            if self.autonomous_personality:
                status['personality_traits'] = self.autonomous_personality.get_current_personality()
        else:
            status['autonomy_active'] = False
        
        return status
    
    def _generate_autonomous_response(self, autonomy_state: Dict, input_text: str) -> str:
        """
        Generate autonomous response based on autonomy simulation
        """
        mood = autonomy_state.get('mood_state', 'neutral')
        energy = autonomy_state.get('energy_level', 0.5)
        goals = autonomy_state.get('active_goals', [])
        
        if energy > 0.8 and goals:
            # High energy, pursue goals actively
            return f"[{self.agent_name} - Autonomous Mode] I'm particularly energized to help with this! As a {self.specialization} specialist, I see this connects to my current focus on {goals[0] if goals else 'learning'}. {self.process_query(input_text)}"
        elif mood == 'curious':
            return f"[{self.agent_name} - Curious] This is fascinating from a {self.specialization} perspective! {self.process_query(input_text)}"
        elif mood == 'analytical':
            return f"[{self.agent_name} - Deep Analysis] Let me apply my {self.specialization} expertise systematically: {self.process_query(input_text)}"
        else:
            return self.process_query(input_text)
    
    def _detect_input_style(self, input_text: str) -> str:
        """
        Detect the style of user input for personality evolution
        """
        text_lower = input_text.lower()
        
        if any(word in text_lower for word in ['complex', 'analyze', 'technical', 'detailed']):
            return 'analytical'
        elif any(word in text_lower for word in ['creative', 'imagine', 'design', 'artistic']):
            return 'creative'
        elif any(word in text_lower for word in ['help', 'support', 'guidance', 'advice']):
            return 'supportive'
        elif len(input_text.split()) > 20:
            return 'complex'
        else:
            return 'simple'
    
    def _update_expertise(self, input_text: str, response: str) -> None:
        """
        Update expertise level based on successful interactions
        """
        # Simple heuristic: longer, more detailed responses indicate higher expertise
        if len(response) > 200 and any(keyword in input_text.lower() 
                                     for keyword in self._get_specialization_keywords()):
            self.expertise_level = min(1.0, self.expertise_level + 0.001)
    
    def _get_specialization_keywords(self) -> List[str]:
        """
        Get keywords relevant to this agent's specialization
        Override in specialized agents
        """
        return [self.specialization.lower()]
    
    def _log_agent_communication(self, communication_log: Dict) -> None:
        """
        Log agent-to-agent communications
        """
        comm_dir = self.base_dir / "memory" / "agent_communications"
        comm_dir.mkdir(parents=True, exist_ok=True)
        
        comm_file = comm_dir / f"{datetime.now().strftime('%Y-%m')}_communications.jsonl"
        
        with open(comm_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(communication_log) + '\n')
    
    def load_agent_state(self) -> None:
        """
        Load agent state from persistent storage
        """
        state_file = self.agent_dir / "agent_state.json"
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.interaction_count = state.get('interaction_count', 0)
                    self.expertise_level = state.get('expertise_level', 0.5)
                    self.confidence_level = state.get('confidence_level', 0.7)
            except Exception as e:
                print(f"⚠️ Failed to load agent state: {e}")
    
    def save_agent_state(self) -> None:
        """
        Save agent state to persistent storage
        """
        state_file = self.agent_dir / "agent_state.json"
        
        state = {
            'agent_name': self.agent_name,
            'specialization': self.specialization,
            'interaction_count': self.interaction_count,
            'expertise_level': self.expertise_level,
            'confidence_level': self.confidence_level,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save agent state: {e}")


class AgentMemoryStore:
    """
    Advanced memory storage for individual agents
    """
    
    def __init__(self, agent_name: str, memory_dir: Path):
        self.agent_name = agent_name
        self.memory_dir = memory_dir
        self.memory_file = memory_dir / f"{agent_name.lower()}_memories.json"
        
        # Initialize memory structure
        if not self.memory_file.exists():
            self._initialize_memory()
    
    def _initialize_memory(self):
        """Initialize empty memory structure"""
        memory_structure = {
            'agent_name': self.agent_name,
            'interactions': [],
            'learned_patterns': {},
            'expertise_evolution': [],
            'successful_responses': [],
            'failure_analysis': [],
            'cross_agent_learnings': [],
            'long_term_goals': [],
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory_structure, f, indent=2)
    
    def store_interaction(self, user_input: str, agent_response: str, 
                         context: Dict = None, autonomy_metadata: Dict = None):
        """Store interaction with metadata"""
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                memory = json.load(f)
        except:
            self._initialize_memory()
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                memory = json.load(f)
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'agent_response': agent_response,
            'context': context or {},
            'autonomy_metadata': autonomy_metadata or {},
            'interaction_id': str(uuid.uuid4())
        }
        
        memory['interactions'].append(interaction)
        memory['last_updated'] = datetime.now().isoformat()
        
        # Keep memory manageable - store last 1000 interactions
        if len(memory['interactions']) > 1000:
            memory['interactions'] = memory['interactions'][-800:]
        
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2)
    
    def get_memory_count(self) -> int:
        """Get total number of stored interactions"""
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                memory = json.load(f)
                return len(memory.get('interactions', []))
        except:
            return 0


class SpecializedKnowledgeBase:
    """
    Knowledge base for specialized domain knowledge and cross-agent sharing
    """
    
    def __init__(self, agent_name: str, specialization: str, knowledge_dir: Path):
        self.agent_name = agent_name
        self.specialization = specialization
        self.knowledge_dir = knowledge_dir
        self.shared_knowledge_file = knowledge_dir / "shared_knowledge.jsonl"
        self.agent_knowledge_file = knowledge_dir / f"{agent_name.lower()}_knowledge.json"
        
        # Ensure files exist
        if not self.shared_knowledge_file.exists():
            self.shared_knowledge_file.touch()
        
        if not self.agent_knowledge_file.exists():
            self._initialize_agent_knowledge()
    
    def _initialize_agent_knowledge(self):
        """Initialize agent-specific knowledge base"""
        knowledge_structure = {
            'agent_name': self.agent_name,
            'specialization': self.specialization,
            'domain_knowledge': {},
            'learned_facts': [],
            'successful_patterns': [],
            'knowledge_contributions': 0,
            'created': datetime.now().isoformat()
        }
        
        with open(self.agent_knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge_structure, f, indent=2)
    
    def add_shared_knowledge(self, knowledge_item: Dict):
        """Add knowledge to shared knowledge base"""
        knowledge_entry = {
            **knowledge_item,
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.shared_knowledge_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(knowledge_entry) + '\n')
    
    def get_relevant_knowledge(self, exclude_agent: str = None, limit: int = 50) -> List[Dict]:
        """Get relevant knowledge from other agents"""
        knowledge_items = []
        
        try:
            with open(self.shared_knowledge_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        item = json.loads(line)
                        if exclude_agent and item.get('source_agent') == exclude_agent:
                            continue
                        knowledge_items.append(item)
        except:
            pass
        
        # Sort by relevance and timestamp
        knowledge_items.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return knowledge_items[:limit]
    
    def get_contribution_count(self) -> int:
        """Get number of knowledge contributions made by this agent"""
        count = 0
        try:
            with open(self.shared_knowledge_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        item = json.loads(line)
                        if item.get('source_agent') == self.agent_name:
                            count += 1
        except:
            pass
        return count


class AdaptiveLearningEngine:
    """
    Learning engine that allows agents to improve over time
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.learning_metrics = {
            'interactions_processed': 0,
            'patterns_learned': 0,
            'knowledge_integrated': 0,
            'successful_adaptations': 0
        }
    
    def process_interaction(self, input_text: str, response: str, context: Dict = None):
        """Process interaction for learning opportunities"""
        self.learning_metrics['interactions_processed'] += 1
        
        # Simple pattern learning - could be much more sophisticated
        if context and context.get('feedback') == 'positive':
            self.learning_metrics['successful_adaptations'] += 1
    
    def should_learn_knowledge(self, knowledge_item: Dict) -> bool:
        """Determine if this knowledge item should be learned"""
        # Simple heuristic - learn from agents with higher expertise
        source_expertise = knowledge_item.get('expertise_level', 0.5)
        return source_expertise > 0.6
    
    def integrate_external_knowledge(self, knowledge_item: Dict):
        """Integrate knowledge from other agents"""
        self.learning_metrics['knowledge_integrated'] += 1
        # Implementation would involve updating agent's knowledge base
    
    def get_learning_metrics(self) -> Dict:
        """Get current learning metrics"""
        return self.learning_metrics.copy()
