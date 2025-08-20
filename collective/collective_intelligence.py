"""
Collective Intelligence System
Enables knowledge sharing, agent-to-agent communication, and collaborative problem solving
"""

import json
import sqlite3
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
import uuid
import threading
import time

@dataclass
class AgentMessage:
    """Message structure for agent-to-agent communication"""
    from_agent: str
    to_agent: str
    message_type: str  # 'query', 'response', 'knowledge_share', 'collaboration_request'
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    message_id: str
    conversation_id: str

@dataclass
class KnowledgeItem:
    """Structure for shared knowledge items"""
    knowledge_id: str
    source_agent: str
    knowledge_type: str  # 'fact', 'pattern', 'strategy', 'insight'
    content: str
    confidence_level: float
    relevance_tags: List[str]
    validation_count: int
    timestamp: datetime
    expiry_date: Optional[datetime]

@dataclass
class CollaborativeTask:
    """Structure for multi-agent collaborative tasks"""
    task_id: str
    task_description: str
    requesting_agent: str
    participating_agents: List[str]
    task_status: str  # 'open', 'in_progress', 'completed', 'cancelled'
    contributions: List[Dict]
    final_result: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

class CollectiveIntelligenceHub:
    """
    Central hub for agent collective intelligence
    
    Manages:
    - Agent-to-agent communication
    - Knowledge sharing and validation
    - Collaborative problem solving
    - Cross-agent learning
    - Emergent behavior detection
    """
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.collective_dir = base_dir / "collective"
        self.collective_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize databases
        self.knowledge_db = self.collective_dir / "collective_knowledge.db"
        self.communication_db = self.collective_dir / "agent_communications.db"
        self.collaboration_db = self.collective_dir / "collaborative_tasks.db"
        
        self._initialize_databases()
        
        # Agent registry
        self.registered_agents = {}
        self.agent_capabilities = {}
        self.agent_interactions = defaultdict(int)
        
        # Active collaborations
        self.active_collaborations = {}
        self.knowledge_cache = {}
        
        # Communication channels
        self.message_queues = defaultdict(list)
        self.broadcast_channels = set()
        
        # Emergent behavior tracking
        self.behavior_patterns = defaultdict(list)
        self.interaction_networks = defaultdict(set)
        
        print("🧠 Collective Intelligence Hub initialized")
    
    def register_agent(self, agent_name: str, capabilities: List[str], agent_ref=None):
        """Register an agent with the collective"""
        self.registered_agents[agent_name] = {
            'capabilities': capabilities,
            'agent_ref': agent_ref,
            'registered_at': datetime.now(),
            'interaction_count': 0,
            'knowledge_contributions': 0,
            'collaboration_participations': 0
        }
        
        self.agent_capabilities[agent_name] = set(capabilities)
        
        print(f"🤖 Agent {agent_name} registered with {len(capabilities)} capabilities")
    
    def share_knowledge(self, source_agent: str, knowledge_type: str, 
                       content: str, confidence: float, tags: List[str] = None) -> str:
        """Share knowledge item with the collective"""
        knowledge_id = str(uuid.uuid4())
        
        knowledge_item = KnowledgeItem(
            knowledge_id=knowledge_id,
            source_agent=source_agent,
            knowledge_type=knowledge_type,
            content=content,
            confidence_level=confidence,
            relevance_tags=tags or [],
            validation_count=0,
            timestamp=datetime.now(),
            expiry_date=None
        )
        
        # Store in database
        self._store_knowledge_item(knowledge_item)
        
        # Update agent stats
        if source_agent in self.registered_agents:
            self.registered_agents[source_agent]['knowledge_contributions'] += 1
        
        # Notify relevant agents
        self._notify_relevant_agents(knowledge_item)
        
        print(f"📚 Knowledge shared by {source_agent}: {knowledge_type}")
        return knowledge_id
    
    def get_relevant_knowledge(self, requesting_agent: str, query_context: str, 
                             limit: int = 10) -> List[KnowledgeItem]:
        """Get knowledge relevant to a specific query"""
        # Simple relevance matching - could be much more sophisticated
        relevant_items = []
        
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        
        # Search by content similarity and tags
        query_words = set(query_context.lower().split())
        
        cursor.execute("""
            SELECT * FROM knowledge_items 
            WHERE source_agent != ? 
            ORDER BY confidence_level DESC, timestamp DESC
            LIMIT ?
        """, (requesting_agent, limit * 2))
        
        for row in cursor.fetchall():
            knowledge_item = self._row_to_knowledge_item(row)
            
            # Simple relevance scoring
            content_words = set(knowledge_item.content.lower().split())
            tag_words = set(' '.join(knowledge_item.relevance_tags).lower().split())
            
            relevance_score = len(query_words.intersection(content_words.union(tag_words)))
            
            if relevance_score > 0:
                relevant_items.append((knowledge_item, relevance_score))
        
        conn.close()
        
        # Sort by relevance and return top items
        relevant_items.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in relevant_items[:limit]]
    
    def send_message(self, from_agent: str, to_agent: str, message_type: str, 
                    content: str, metadata: Dict = None) -> str:
        """Send message from one agent to another"""
        message_id = str(uuid.uuid4())
        conversation_id = f"{min(from_agent, to_agent)}_{max(from_agent, to_agent)}"
        
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            metadata=metadata or {},
            timestamp=datetime.now(),
            message_id=message_id,
            conversation_id=conversation_id
        )
        
        # Store message
        self._store_message(message)
        
        # Add to recipient's queue
        self.message_queues[to_agent].append(message)
        
        # Update interaction tracking
        self.agent_interactions[f"{from_agent}->{to_agent}"] += 1
        self.interaction_networks[from_agent].add(to_agent)
        
        # Detect communication patterns
        self._analyze_communication_pattern(from_agent, to_agent, message_type)
        
        return message_id
    
    def get_messages(self, agent_name: str, since: datetime = None) -> List[AgentMessage]:
        """Get messages for an agent"""
        if agent_name not in self.message_queues:
            return []
        
        messages = self.message_queues[agent_name]
        
        if since:
            messages = [msg for msg in messages if msg.timestamp > since]
        
        return messages
    
    def start_collaboration(self, requesting_agent: str, task_description: str, 
                          required_capabilities: List[str] = None) -> str:
        """Start a collaborative task"""
        task_id = str(uuid.uuid4())
        
        # Find agents with required capabilities
        participating_agents = self._find_capable_agents(required_capabilities or [])
        
        if requesting_agent not in participating_agents:
            participating_agents.append(requesting_agent)
        
        collaboration = CollaborativeTask(
            task_id=task_id,
            task_description=task_description,
            requesting_agent=requesting_agent,
            participating_agents=participating_agents,
            task_status='open',
            contributions=[],
            final_result=None,
            created_at=datetime.now(),
            completed_at=None
        )
        
        self.active_collaborations[task_id] = collaboration
        
        # Notify participating agents
        for agent in participating_agents:
            if agent != requesting_agent:
                self.send_message(
                    from_agent="CollectiveHub",
                    to_agent=agent,
                    message_type="collaboration_request",
                    content=f"Collaboration request: {task_description}",
                    metadata={'task_id': task_id, 'required_capabilities': required_capabilities}
                )
        
        print(f"🤝 Collaboration started: {task_id} with {len(participating_agents)} agents")
        return task_id
    
    def contribute_to_collaboration(self, task_id: str, contributing_agent: str, 
                                  contribution: str, contribution_type: str = "analysis") -> bool:
        """Add contribution to collaborative task"""
        if task_id not in self.active_collaborations:
            return False
        
        collaboration = self.active_collaborations[task_id]
        
        if contributing_agent not in collaboration.participating_agents:
            return False
        
        contribution_data = {
            'agent': contributing_agent,
            'content': contribution,
            'type': contribution_type,
            'timestamp': datetime.now().isoformat(),
            'contribution_id': str(uuid.uuid4())
        }
        
        collaboration.contributions.append(contribution_data)
        
        # Update agent stats
        if contributing_agent in self.registered_agents:
            self.registered_agents[contributing_agent]['collaboration_participations'] += 1
        
        # Check if collaboration is complete
        if len(collaboration.contributions) >= len(collaboration.participating_agents):
            self._complete_collaboration(task_id)
        
        return True
    
    def get_collaboration_status(self, task_id: str) -> Optional[Dict]:
        """Get status of collaborative task"""
        if task_id not in self.active_collaborations:
            return None
        
        collaboration = self.active_collaborations[task_id]
        
        return {
            'task_id': task_id,
            'description': collaboration.task_description,
            'status': collaboration.task_status,
            'participating_agents': collaboration.participating_agents,
            'contributions_count': len(collaboration.contributions),
            'created_at': collaboration.created_at.isoformat(),
            'completed_at': collaboration.completed_at.isoformat() if collaboration.completed_at else None
        }
    
    def analyze_collective_behavior(self) -> Dict[str, Any]:
        """Analyze collective behavior patterns"""
        analysis = {
            'registered_agents': len(self.registered_agents),
            'total_knowledge_items': self._count_knowledge_items(),
            'total_communications': sum(self.agent_interactions.values()),
            'active_collaborations': len([c for c in self.active_collaborations.values() 
                                        if c.task_status in ['open', 'in_progress']]),
            'communication_patterns': dict(self.agent_interactions),
            'knowledge_distribution': self._analyze_knowledge_distribution(),
            'collaboration_success_rate': self._calculate_collaboration_success_rate(),
            'emergent_behaviors': self._detect_emergent_behaviors()
        }
        
        return analysis
    
    def cleanup_old_data(self, days_old: int = 30):
        """Clean up old communications and expired knowledge"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        # Clean old messages from queues
        for agent_name in self.message_queues:
            self.message_queues[agent_name] = [
                msg for msg in self.message_queues[agent_name] 
                if msg.timestamp > cutoff_date
            ]
        
        # Clean expired knowledge
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM knowledge_items 
            WHERE expiry_date IS NOT NULL AND expiry_date < ?
        """, (cutoff_date.isoformat(),))
        conn.commit()
        conn.close()
        
        print(f"🧹 Cleaned up data older than {days_old} days")
    
    def _initialize_databases(self):
        """Initialize SQLite databases for collective intelligence"""
        # Knowledge database
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_items (
                knowledge_id TEXT PRIMARY KEY,
                source_agent TEXT,
                knowledge_type TEXT,
                content TEXT,
                confidence_level REAL,
                relevance_tags TEXT,
                validation_count INTEGER,
                timestamp TEXT,
                expiry_date TEXT
            )
        """)
        conn.commit()
        conn.close()
        
        # Communication database
        conn = sqlite3.connect(self.communication_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id TEXT PRIMARY KEY,
                from_agent TEXT,
                to_agent TEXT,
                message_type TEXT,
                content TEXT,
                metadata TEXT,
                timestamp TEXT,
                conversation_id TEXT
            )
        """)
        conn.commit()
        conn.close()
        
        # Collaboration database
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collaborations (
                task_id TEXT PRIMARY KEY,
                task_description TEXT,
                requesting_agent TEXT,
                participating_agents TEXT,
                task_status TEXT,
                contributions TEXT,
                final_result TEXT,
                created_at TEXT,
                completed_at TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def _store_knowledge_item(self, knowledge_item: KnowledgeItem):
        """Store knowledge item in database"""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO knowledge_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            knowledge_item.knowledge_id,
            knowledge_item.source_agent,
            knowledge_item.knowledge_type,
            knowledge_item.content,
            knowledge_item.confidence_level,
            json.dumps(knowledge_item.relevance_tags),
            knowledge_item.validation_count,
            knowledge_item.timestamp.isoformat(),
            knowledge_item.expiry_date.isoformat() if knowledge_item.expiry_date else None
        ))
        conn.commit()
        conn.close()
    
    def _store_message(self, message: AgentMessage):
        """Store message in database"""
        conn = sqlite3.connect(self.communication_db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            message.message_id,
            message.from_agent,
            message.to_agent,
            message.message_type,
            message.content,
            json.dumps(message.metadata),
            message.timestamp.isoformat(),
            message.conversation_id
        ))
        conn.commit()
        conn.close()
    
    def _row_to_knowledge_item(self, row) -> KnowledgeItem:
        """Convert database row to KnowledgeItem"""
        return KnowledgeItem(
            knowledge_id=row[0],
            source_agent=row[1],
            knowledge_type=row[2],
            content=row[3],
            confidence_level=row[4],
            relevance_tags=json.loads(row[5]) if row[5] else [],
            validation_count=row[6],
            timestamp=datetime.fromisoformat(row[7]),
            expiry_date=datetime.fromisoformat(row[8]) if row[8] else None
        )
    
    def _notify_relevant_agents(self, knowledge_item: KnowledgeItem):
        """Notify agents who might be interested in this knowledge"""
        # Simple notification based on tags and capabilities
        for agent_name, capabilities in self.agent_capabilities.items():
            if agent_name == knowledge_item.source_agent:
                continue
            
            # Check if any tags match agent capabilities
            tag_match = any(tag.lower() in ' '.join(capabilities).lower() 
                          for tag in knowledge_item.relevance_tags)
            
            if tag_match:
                self.send_message(
                    from_agent="CollectiveHub",
                    to_agent=agent_name,
                    message_type="knowledge_share",
                    content=f"New {knowledge_item.knowledge_type}: {knowledge_item.content[:100]}...",
                    metadata={'knowledge_id': knowledge_item.knowledge_id}
                )
    
    def _find_capable_agents(self, required_capabilities: List[str]) -> List[str]:
        """Find agents with required capabilities"""
        capable_agents = []
        
        for agent_name, capabilities in self.agent_capabilities.items():
            capability_match = any(req_cap.lower() in ' '.join(capabilities).lower() 
                                 for req_cap in required_capabilities)
            if capability_match:
                capable_agents.append(agent_name)
        
        return capable_agents
    
    def _complete_collaboration(self, task_id: str):
        """Complete a collaborative task"""
        if task_id not in self.active_collaborations:
            return
        
        collaboration = self.active_collaborations[task_id]
        collaboration.task_status = 'completed'
        collaboration.completed_at = datetime.now()
        
        # Synthesize final result from contributions
        contributions_text = "\n\n".join([
            f"**{contrib['agent']}**: {contrib['content']}" 
            for contrib in collaboration.contributions
        ])
        
        collaboration.final_result = f"Collaborative result from {len(collaboration.participating_agents)} agents:\n\n{contributions_text}"
        
        # Notify all participants
        for agent in collaboration.participating_agents:
            self.send_message(
                from_agent="CollectiveHub",
                to_agent=agent,
                message_type="collaboration_complete",
                content=f"Collaboration completed: {collaboration.task_description}",
                metadata={'task_id': task_id, 'final_result': collaboration.final_result}
            )
        
        print(f"✅ Collaboration completed: {task_id}")
    
    def _count_knowledge_items(self) -> int:
        """Count total knowledge items"""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM knowledge_items")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def _analyze_knowledge_distribution(self) -> Dict:
        """Analyze how knowledge is distributed among agents"""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT source_agent, knowledge_type, COUNT(*) 
            FROM knowledge_items 
            GROUP BY source_agent, knowledge_type
        """)
        
        distribution = defaultdict(lambda: defaultdict(int))
        for row in cursor.fetchall():
            distribution[row[0]][row[1]] = row[2]
        
        conn.close()
        return dict(distribution)
    
    def _calculate_collaboration_success_rate(self) -> float:
        """Calculate collaboration success rate"""
        if not self.active_collaborations:
            return 0.0
        
        completed = len([c for c in self.active_collaborations.values() 
                        if c.task_status == 'completed'])
        total = len(self.active_collaborations)
        
        return completed / total
    
    def _detect_emergent_behaviors(self) -> List[str]:
        """Detect emergent behaviors in the collective"""
        behaviors = []
        
        # Detect frequent collaborators
        frequent_pairs = []
        for interaction, count in self.agent_interactions.items():
            if count > 5:  # Threshold for frequent interaction
                frequent_pairs.append(interaction)
        
        if frequent_pairs:
            behaviors.append(f"Frequent collaborations detected: {len(frequent_pairs)} agent pairs")
        
        # Detect knowledge specialization
        knowledge_dist = self._analyze_knowledge_distribution()
        specialists = []
        for agent, types in knowledge_dist.items():
            if len(types) == 1 and list(types.values())[0] > 3:
                specialists.append(agent)
        
        if specialists:
            behaviors.append(f"Knowledge specialists emerged: {', '.join(specialists)}")
        
        return behaviors
    
    def _analyze_communication_pattern(self, from_agent: str, to_agent: str, message_type: str):
        """Analyze communication patterns for emergent behavior"""
        pattern_key = f"{from_agent}-{to_agent}-{message_type}"
        self.behavior_patterns[pattern_key].append(datetime.now())
        
        # Detect rapid communication (potential emergent behavior)
        recent_messages = [
            timestamp for timestamp in self.behavior_patterns[pattern_key]
            if timestamp > datetime.now() - timedelta(minutes=10)
        ]
        
        if len(recent_messages) > 5:
            print(f"🚨 Rapid communication detected: {from_agent} -> {to_agent} ({message_type})")


# Test the collective intelligence system
if __name__ == "__main__":
    print("🧪 Testing Collective Intelligence Hub")
    print("="*50)
    
    # Initialize hub
    hub = CollectiveIntelligenceHub(Path.cwd())
    
    # Register test agents
    hub.register_agent("Jasper", ["coordination", "analysis", "workshop_management"])
    hub.register_agent("Midas", ["financial_analysis", "investment", "market_research"])
    hub.register_agent("Aiven", ["creative_analysis", "symbolic_interpretation", "art"])
    
    print(f"\n🤖 Registered {len(hub.registered_agents)} agents")
    
    # Test knowledge sharing
    print("\n📚 Testing Knowledge Sharing:")
    knowledge_id = hub.share_knowledge(
        source_agent="Midas",
        knowledge_type="investment_insight",
        content="Diversification reduces portfolio risk without proportionally reducing returns",
        confidence=0.9,
        tags=["portfolio", "risk", "diversification"]
    )
    print(f"Knowledge shared with ID: {knowledge_id}")
    
    # Test agent communication
    print("\n💬 Testing Agent Communication:")
    message_id = hub.send_message(
        from_agent="Jasper",
        to_agent="Midas",
        message_type="query",
        content="What's your assessment of current market conditions?",
        metadata={"priority": "normal"}
    )
    print(f"Message sent with ID: {message_id}")
    
    # Test collaboration
    print("\n🤝 Testing Collaboration:")
    task_id = hub.start_collaboration(
        requesting_agent="Jasper",
        task_description="Analyze the impact of AI on various industries",
        required_capabilities=["analysis", "market_research", "creative_analysis"]
    )
    print(f"Collaboration started with ID: {task_id}")
    
    # Simulate contributions
    hub.contribute_to_collaboration(
        task_id=task_id,
        contributing_agent="Midas",
        contribution="Financial sector will see major disruption in trading and analysis",
        contribution_type="analysis"
    )
    
    hub.contribute_to_collaboration(
        task_id=task_id,
        contributing_agent="Aiven",
        contribution="Creative industries face both threat and opportunity from AI tools",
        contribution_type="perspective"
    )
    
    # Analyze collective behavior
    print("\n🧠 Collective Behavior Analysis:")
    behavior_analysis = hub.analyze_collective_behavior()
    for key, value in behavior_analysis.items():
        if key not in ['communication_patterns', 'knowledge_distribution']:
            print(f"   {key}: {value}")
    
    print("\n✅ Collective Intelligence Hub test complete!")
