#!/usr/bin/env python3
"""
Advanced Memory System for Solvine Agents
Enables persistent learning and memory across sessions
"""

import json
import sqlite3
import datetime
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class MemoryEntry:
    """Represents a single memory entry for an agent"""
    agent_name: str
    timestamp: str
    content_type: str  # "conversation", "learning", "preference", "skill"
    content: str
    context: str
    importance: int  # 1-10 scale
    tags: List[str]
    embedding_hash: Optional[str] = None

class AgentMemoryManager:
    """Advanced memory system for Solvine agents with learning capabilities"""
    
    def __init__(self, memory_dir: str = "./agent_memories"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Initialize databases for different types of memory
        self.conversation_db = self.memory_dir / "conversations.db"
        self.learning_db = self.memory_dir / "learned_knowledge.db"
        self.preferences_db = self.memory_dir / "user_preferences.db"
        self.skills_db = self.memory_dir / "agent_skills.db"
        
        self._init_databases()
        
        # Agent-specific memory stores
        self.agent_memories = {
            "solvine": {"role": "orchestrator", "specializations": []},
            "aiven": {"role": "emotional_intelligence", "specializations": []},
            "midas": {"role": "financial_strategy", "specializations": []},
            "jasper": {"role": "boundary_testing", "specializations": []},
            "veilsynth": {"role": "symbolic_thought", "specializations": []},
            "halcyon": {"role": "emergency_safeguards", "specializations": []},
            "quanta": {"role": "logic_computation", "specializations": []}
        }
    
    def _init_databases(self):
        """Initialize SQLite databases for persistent memory"""
        
        # Conversations database
        with sqlite3.connect(self.conversation_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    agent_response TEXT NOT NULL,
                    context TEXT,
                    session_id TEXT,
                    importance INTEGER DEFAULT 5,
                    tags TEXT
                )
            """)
        
        # Learning database
        with sqlite3.connect(self.learning_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learned_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    fact_type TEXT NOT NULL,
                    fact_content TEXT NOT NULL,
                    source TEXT,
                    confidence REAL DEFAULT 0.5,
                    verified BOOLEAN DEFAULT FALSE,
                    tags TEXT
                )
            """)
        
        # Preferences database
        with sqlite3.connect(self.preferences_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_identifier TEXT,
                    preference_type TEXT NOT NULL,
                    preference_value TEXT NOT NULL,
                    agent_context TEXT,
                    timestamp TEXT NOT NULL,
                    strength REAL DEFAULT 0.5
                )
            """)
        
        # Skills database
        with sqlite3.connect(self.skills_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    skill_name TEXT NOT NULL,
                    skill_level REAL DEFAULT 0.0,
                    experience_points INTEGER DEFAULT 0,
                    last_used TEXT,
                    improvement_areas TEXT,
                    success_rate REAL DEFAULT 0.0
                )
            """)
    
    def store_conversation(self, agent_name: str, user_input: str, agent_response: str, 
                          context: str = "", session_id: str = "", importance: int = 5, 
                          tags: List[str] = None):
        """Store a conversation for future reference and learning"""
        timestamp = datetime.datetime.now().isoformat()
        tags_str = json.dumps(tags or [])
        
        with sqlite3.connect(self.conversation_db) as conn:
            conn.execute("""
                INSERT INTO conversations 
                (agent_name, timestamp, user_input, agent_response, context, session_id, importance, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (agent_name, timestamp, user_input, agent_response, context, session_id, importance, tags_str))
        
        # Extract learning opportunities
        self._extract_learning_from_conversation(agent_name, user_input, agent_response, context)
    
    def _extract_learning_from_conversation(self, agent_name: str, user_input: str, 
                                          agent_response: str, context: str):
        """Extract potential learning points from conversations"""
        learning_indicators = [
            "I didn't know", "That's new to me", "I learned", "Thank you for teaching me",
            "I'll remember that", "Good point", "I understand now"
        ]
        
        # Simple learning extraction (could be enhanced with NLP)
        if any(indicator in agent_response.lower() for indicator in learning_indicators):
            self.store_learned_fact(
                agent_name=agent_name,
                fact_type="user_correction",
                fact_content=user_input,
                source="conversation",
                confidence=0.8
            )
    
    def store_learned_fact(self, agent_name: str, fact_type: str, fact_content: str,
                          source: str = "", confidence: float = 0.5, tags: List[str] = None):
        """Store a new learned fact"""
        timestamp = datetime.datetime.now().isoformat()
        tags_str = json.dumps(tags or [])
        
        with sqlite3.connect(self.learning_db) as conn:
            conn.execute("""
                INSERT INTO learned_facts 
                (agent_name, timestamp, fact_type, fact_content, source, confidence, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (agent_name, timestamp, fact_type, fact_content, source, confidence, tags_str))
    
    def get_relevant_memories(self, agent_name: str, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve relevant memories for context"""
        memories = []
        
        # Get recent conversations
        with sqlite3.connect(self.conversation_db) as conn:
            cursor = conn.execute("""
                SELECT user_input, agent_response, context, timestamp, importance
                FROM conversations 
                WHERE agent_name = ? 
                ORDER BY importance DESC, timestamp DESC 
                LIMIT ?
            """, (agent_name, limit))
            
            for row in cursor.fetchall():
                memories.append({
                    "type": "conversation",
                    "user_input": row[0],
                    "agent_response": row[1],
                    "context": row[2],
                    "timestamp": row[3],
                    "importance": row[4]
                })
        
        # Get learned facts
        with sqlite3.connect(self.learning_db) as conn:
            cursor = conn.execute("""
                SELECT fact_type, fact_content, source, confidence, timestamp
                FROM learned_facts 
                WHERE agent_name = ? 
                ORDER BY confidence DESC, timestamp DESC 
                LIMIT ?
            """, (agent_name, limit // 2))
            
            for row in cursor.fetchall():
                memories.append({
                    "type": "learned_fact",
                    "fact_type": row[0],
                    "content": row[1],
                    "source": row[2],
                    "confidence": row[3],
                    "timestamp": row[4]
                })
        
        return memories
    
    def update_agent_skill(self, agent_name: str, skill_name: str, success: bool = True,
                          feedback: str = ""):
        """Update agent skill levels based on performance"""
        timestamp = datetime.datetime.now().isoformat()
        
        with sqlite3.connect(self.skills_db) as conn:
            # Check if skill exists
            cursor = conn.execute("""
                SELECT skill_level, experience_points, success_rate 
                FROM agent_skills 
                WHERE agent_name = ? AND skill_name = ?
            """, (agent_name, skill_name))
            
            row = cursor.fetchone()
            
            if row:
                # Update existing skill
                current_level, exp_points, success_rate = row
                new_exp = exp_points + (10 if success else 2)
                new_level = min(10.0, current_level + (0.1 if success else -0.05))
                
                # Update success rate (simple moving average)
                new_success_rate = (success_rate * 0.9) + (1.0 if success else 0.0) * 0.1
                
                conn.execute("""
                    UPDATE agent_skills 
                    SET skill_level = ?, experience_points = ?, last_used = ?, 
                        improvement_areas = ?, success_rate = ?
                    WHERE agent_name = ? AND skill_name = ?
                """, (new_level, new_exp, timestamp, feedback, new_success_rate, agent_name, skill_name))
            else:
                # Create new skill
                conn.execute("""
                    INSERT INTO agent_skills 
                    (agent_name, skill_name, skill_level, experience_points, last_used, 
                     improvement_areas, success_rate)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (agent_name, skill_name, 1.0 if success else 0.5, 10 if success else 2, 
                     timestamp, feedback, 1.0 if success else 0.0))
    
    def get_agent_profile(self, agent_name: str) -> Dict[str, Any]:
        """Get comprehensive profile of an agent including skills and memories"""
        profile = {
            "agent_name": agent_name,
            "role": self.agent_memories.get(agent_name, {}).get("role", "unknown"),
            "skills": [],
            "recent_conversations": 0,
            "learned_facts": 0,
            "performance_metrics": {}
        }
        
        # Get skills
        with sqlite3.connect(self.skills_db) as conn:
            cursor = conn.execute("""
                SELECT skill_name, skill_level, experience_points, success_rate
                FROM agent_skills 
                WHERE agent_name = ?
                ORDER BY skill_level DESC
            """, (agent_name,))
            
            profile["skills"] = [
                {
                    "name": row[0],
                    "level": row[1],
                    "experience": row[2],
                    "success_rate": row[3]
                } for row in cursor.fetchall()
            ]
        
        # Get conversation count
        with sqlite3.connect(self.conversation_db) as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM conversations WHERE agent_name = ?
            """, (agent_name,))
            profile["recent_conversations"] = cursor.fetchone()[0]
        
        # Get learned facts count
        with sqlite3.connect(self.learning_db) as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM learned_facts WHERE agent_name = ?
            """, (agent_name,))
            profile["learned_facts"] = cursor.fetchone()[0]
        
        return profile

# Example usage and testing
def test_memory_system():
    """Test the memory system"""
    memory = AgentMemoryManager()
    
    # Simulate some interactions
    memory.store_conversation(
        agent_name="aiven",
        user_input="I'm feeling stressed about my project deadlines",
        agent_response="I understand that project deadlines can be overwhelming. Let me help you break this down into manageable steps.",
        context="emotional_support",
        importance=8,
        tags=["stress", "deadlines", "emotional_support"]
    )
    
    memory.store_learned_fact(
        agent_name="midas",
        fact_type="user_preference",
        fact_content="User prefers conservative investment strategies",
        source="conversation_analysis",
        confidence=0.9,
        tags=["investment", "risk_tolerance"]
    )
    
    memory.update_agent_skill("aiven", "emotional_support", success=True, feedback="Successfully provided calming advice")
    
    # Get agent profile
    profile = memory.get_agent_profile("aiven")
    print("Aiven's Profile:", json.dumps(profile, indent=2))
    
    return memory

if __name__ == "__main__":
    test_memory_system()
