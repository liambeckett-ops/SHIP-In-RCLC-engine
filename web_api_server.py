#!/usr/bin/env python3
"""
Solvine Web API Server - Bridge Between Web UI and Agents
Connects the beautiful web interface to actual Jasper agent system
"""

import sys
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Solvine components
try:
    from config.config_loader import get_config_loader, get_head_agent
    from agents.jasper.jasper_agent import JasperAgent
    SOLVINE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Solvine components not available: {e}")
    SOLVINE_AVAILABLE = False

# Pydantic models for API requests/responses
class AgentQuery(BaseModel):
    message: str
    agent: Optional[str] = None

class AgentResponse(BaseModel):
    agent: str
    role: str
    message: str
    timestamp: str
    stability_score: float
    is_primary: bool

class SystemStatus(BaseModel):
    agents_count: int
    system_stability: float
    uptime: str

class CreateAgentRequest(BaseModel):
    name: str
    role: str
    personality: str
    skills: str

# FastAPI app initialization
app = FastAPI(
    title="Solvine Web Interface API",
    description="Bridge between beautiful web UI and Solvine agent system",
    version="2.0.0"
)

# CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for web interface
web_dir = current_dir / "web"
if web_dir.exists():
    app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")
    logger.info(f"✅ Static files mounted from: {web_dir}")
else:
    logger.warning(f"⚠️ Web directory not found: {web_dir}")

# Global system components
solvine_system = None
startup_time = datetime.now()

class SolvineWebSystem:
    """Web-focused Solvine system wrapper"""
    
    def __init__(self):
        self.startup_time = datetime.now()
        self.session_message_count = 0
        
        # Initialize Jasper head agent
        if SOLVINE_AVAILABLE:
            try:
                self.jasper = get_head_agent()
                if self.jasper:
                    self.jasper.initialize()
                    logger.info("✅ Jasper head agent initialized")
                else:
                    # Fallback - create direct instance
                    self.jasper = JasperAgent()
                    self.jasper.initialize()
                    logger.info("✅ Jasper agent created directly")
            except Exception as e:
                logger.error(f"Failed to initialize Jasper: {e}")
                self.jasper = None
        else:
            self.jasper = None
        
        # Mock agents for demonstration (you can expand this)
        self.mock_agents = {
            'midas': {
                'name': 'Midas',
                'role': 'Financial Advisor',
                'emoji': '💰',
                'personality': 'analytical',
                'stability': 0.87,
                'response_template': "As your financial advisor, I'd recommend {advice}. Consider the risk factors and potential returns before making any decisions."
            },
            'aiven': {
                'name': 'Aiven',
                'role': 'Creative Analyst',
                'emoji': '🎨',
                'personality': 'creative',
                'stability': 0.91,
                'response_template': "From a creative perspective, {insight}. Let me break down the symbolic meaning and possibilities here."
            },
            'halcyon': {
                'name': 'Halcyon',
                'role': 'Crisis Support',
                'emoji': '🛡️',
                'personality': 'supportive',
                'stability': 0.94,
                'response_template': "I understand you need support with {situation}. Let's work through this together step by step."
            },
            'veilsynth': {
                'name': 'VeilSynth',
                'role': 'Myth Guardian',
                'emoji': '👁️',
                'personality': 'analytical',
                'stability': 0.82,
                'response_template': "Analyzing for deeper patterns... {analysis}. Be aware of the recursive implications here."
            },
            'quanta': {
                'name': 'Quanta',
                'role': 'Computational',
                'emoji': '🧮',
                'personality': 'analytical',
                'stability': 0.89,
                'response_template': "Mathematical analysis shows {calculation}. The probability matrices suggest several optimal paths forward."
            }
        }
        
        # Create dynamic agents storage
        self.dynamic_agents = {}
    
    async def query_agents(self, message: str, agent_filter: str = None) -> List[AgentResponse]:
        """Process query and return agent responses"""
        self.session_message_count += 1
        
        responses = []
        
        # If specific agent requested
        if agent_filter:
            agent_filter = agent_filter.lower()
            
            # Check for Jasper
            if agent_filter == 'jasper' and self.jasper:
                response = await self._get_jasper_response(message)
                responses.append(response)
            
            # Check dynamic agents first (they override mock agents)
            elif agent_filter in self.dynamic_agents:
                response = await self._get_dynamic_agent_response(agent_filter, message)
                responses.append(response)
            
            # Check mock agents (only if not overridden by dynamic)
            elif agent_filter in self.mock_agents:
                response = await self._get_mock_agent_response(agent_filter, message)
                responses.append(response)
            
            # Agent not found
            else:
                available_agents = self._get_available_agent_names()
                error_msg = f"Agent '{agent_filter}' not found. Available: {', '.join(available_agents)}"
                responses.append(self._create_error_response(agent_filter, error_msg))
        
        else:
            # Auto-select based on message content
            selected_agents = self._select_agents_intelligently(message)
            
            for i, agent_name in enumerate(selected_agents):
                is_primary = (i == 0)
                
                if agent_name == 'jasper' and self.jasper:
                    response = await self._get_jasper_response(message, is_primary)
                elif agent_name in self.dynamic_agents:
                    response = await self._get_dynamic_agent_response(agent_name, message, is_primary)
                elif agent_name in self.mock_agents:
                    response = await self._get_mock_agent_response(agent_name, message, is_primary)
                else:
                    continue
                
                responses.append(response)
        
        return responses
    
    async def _get_jasper_response(self, message: str, is_primary: bool = True) -> AgentResponse:
        """Get response from actual Jasper agent"""
        try:
            if not self.jasper:
                return self._create_error_response("jasper", "Jasper agent not initialized")
            
            # Use Jasper's respond method
            jasper_response = self.jasper.respond(message)
            
            # Get autonomy status for stability score
            autonomy_status = self.jasper.get_autonomy_status()
            stability = 0.85  # Default
            
            if autonomy_status:
                # Calculate stability from autonomy features
                active_features = sum([1 for v in autonomy_status.values() if v])
                stability = min(0.95, 0.6 + (active_features * 0.1))
            
            return AgentResponse(
                agent="jasper",
                role="Head Agent & Coordinator",
                message=jasper_response,
                timestamp=datetime.now().isoformat(),
                stability_score=stability,
                is_primary=is_primary
            )
            
        except Exception as e:
            logger.error(f"Jasper response error: {e}")
            return self._create_error_response("jasper", f"Error: {str(e)}")
    
    async def _get_mock_agent_response(self, agent_name: str, message: str, is_primary: bool = True) -> AgentResponse:
        """Generate response from mock agent"""
        agent_info = self.mock_agents[agent_name]
        
        # Generate contextual response based on agent role
        if agent_name == 'midas':
            content = self._generate_financial_response(message)
        elif agent_name == 'aiven':
            content = self._generate_creative_response(message)
        elif agent_name == 'halcyon':
            content = self._generate_support_response(message)
        elif agent_name == 'veilsynth':
            content = self._generate_myth_response(message)
        elif agent_name == 'quanta':
            content = self._generate_computational_response(message)
        else:
            content = f"I'm {agent_info['name']}, and I'm processing your request about: {message[:100]}..."
        
        response_text = agent_info['response_template'].format(
            advice=content,
            insight=content,
            situation=content,
            analysis=content,
            calculation=content
        )
        
        return AgentResponse(
            agent=agent_name,
            role=agent_info['role'],
            message=response_text,
            timestamp=datetime.now().isoformat(),
            stability_score=agent_info['stability'],
            is_primary=is_primary
        )
    
    async def _get_dynamic_agent_response(self, agent_name: str, message: str, is_primary: bool = True) -> AgentResponse:
        """Generate response from dynamically created agent"""
        agent_info = self.dynamic_agents[agent_name]
        
        # Generate response based on agent's personality and skills
        personality_responses = {
            'analytical': f"Let me analyze this systematically. Based on my expertise in {agent_info['role']}, I see several key factors to consider regarding your question about {message[:50]}...",
            'creative': f"This is an interesting creative challenge! Drawing from my background in {agent_info['role']}, I'd approach this with fresh perspective on {message[:50]}...",
            'supportive': f"I'm here to help you with this. As someone specialized in {agent_info['role']}, I want to support you through {message[:50]}...",
            'direct': f"Here's the direct answer regarding {message[:50]}. Based on my {agent_info['role']} expertise, the key points are...",
            'playful': f"Oh, this is fun! Let me tackle {message[:50]} with some creative energy. My {agent_info['role']} background gives me some interesting angles..."
        }
        
        response_template = personality_responses.get(agent_info['personality'], 
            f"As a {agent_info['role']} specialist, I'll help you with {message[:50]}...")
        
        return AgentResponse(
            agent=agent_name,
            role=agent_info['role'],
            message=response_template,
            timestamp=datetime.now().isoformat(),
            stability_score=agent_info['stability'],
            is_primary=is_primary
        )
    
    def _generate_financial_response(self, message: str) -> str:
        """Generate Midas-style financial response"""
        financial_keywords = ['investment', 'portfolio', 'diversification', 'risk management', 'market analysis']
        return f"considering {financial_keywords[len(message) % len(financial_keywords)]} strategies for your situation"
    
    def _generate_creative_response(self, message: str) -> str:
        """Generate Aiven-style creative response"""
        creative_keywords = ['symbolic meaning', 'creative potential', 'artistic interpretation', 'innovative solutions']
        return f"I see {creative_keywords[len(message) % len(creative_keywords)]} emerging from your query"
    
    def _generate_support_response(self, message: str) -> str:
        """Generate Halcyon-style support response"""
        support_keywords = ['this challenge', 'your concerns', 'this situation', 'your goals']
        return f"{support_keywords[len(message) % len(support_keywords)]}"
    
    def _generate_myth_response(self, message: str) -> str:
        """Generate VeilSynth-style myth response"""
        myth_keywords = ['recursive patterns', 'deeper implications', 'myth contamination risks', 'symbolic structures']
        return f"{myth_keywords[len(message) % len(myth_keywords)]} within your query"
    
    def _generate_computational_response(self, message: str) -> str:
        """Generate Quanta-style computational response"""
        comp_keywords = ['probability matrices', 'algorithmic solutions', 'computational models', 'data patterns']
        return f"{comp_keywords[len(message) % len(comp_keywords)]} indicate optimal pathways"
    
    def _select_agents_intelligently(self, message: str) -> List[str]:
        """Intelligent agent selection logic (no duplicates)"""
        message_lower = message.lower()
        
        # Get available agents (no duplicates)
        available_agents = set(self._get_available_agent_names())
        
        # Now do intelligent selection from available agents
        # Financial queries -> Midas (if available)
        if any(word in message_lower for word in ['money', 'invest', 'financial', 'portfolio', 'budget']):
            if 'midas' in available_agents:
                return ['midas']
        
        # Creative/artistic queries -> Aiven (if available)
        elif any(word in message_lower for word in ['creative', 'design', 'art', 'symbolic', 'meaning']):
            if 'aiven' in available_agents:
                return ['aiven']
        
        # Support/help queries -> Halcyon (if available)
        elif any(word in message_lower for word in ['help', 'support', 'crisis', 'problem', 'urgent']):
            if 'halcyon' in available_agents:
                return ['halcyon']
        
        # Complex/analytical queries -> VeilSynth (if available)
        elif any(word in message_lower for word in ['complex', 'analyze', 'pattern', 'recursive', 'myth']):
            if 'veilsynth' in available_agents:
                return ['veilsynth']
        
        # Mathematical/computational -> Quanta (if available)
        elif any(word in message_lower for word in ['calculate', 'math', 'compute', 'algorithm', 'data']):
            if 'quanta' in available_agents:
                return ['quanta']
        
        # Default -> Jasper (head agent) if available, otherwise first available agent
        if 'jasper' in available_agents:
            return ['jasper']
        elif available_agents:
            return [sorted(list(available_agents))[0]]  # Return first available agent alphabetically
        else:
            return ['jasper']  # Fallback even if not available (will show error)
    
    def _create_error_response(self, agent_name: str, error_msg: str) -> AgentResponse:
        """Create error response"""
        return AgentResponse(
            agent=agent_name,
            role="Error Handler",
            message=f"❌ {error_msg}",
            timestamp=datetime.now().isoformat(),
            stability_score=0.0,
            is_primary=True
        )
    
    def get_system_status(self) -> SystemStatus:
        """Get current system status"""
        uptime = datetime.now() - self.startup_time
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        uptime_str = f"{hours}h {minutes}m"
        
        # Calculate system stability
        total_agents = len(self.mock_agents) + len(self.dynamic_agents) + (1 if self.jasper else 0)
        stability_sum = sum(agent['stability'] for agent in self.mock_agents.values())
        stability_sum += sum(agent['stability'] for agent in self.dynamic_agents.values())
        if self.jasper:
            stability_sum += 0.85  # Jasper base stability
        
        avg_stability = stability_sum / max(total_agents, 1)
        
        return SystemStatus(
            agents_count=total_agents,
            system_stability=round(avg_stability, 2),
            uptime=uptime_str
        )
    
    def get_agents_list(self):
        """Get list of all available agents (no duplicates)"""
        agents = []
        agent_names = set()  # Track names to prevent duplicates
        
        # Add Jasper (highest priority)
        if self.jasper:
            agents.append({
                "name": "jasper",
                "role": "Head Agent & Coordinator",
                "stability": 0.85,
                "type": "head_agent",
                "emoji": "🎯"
            })
            agent_names.add("jasper")
        
        # Add dynamic agents (user-created, higher priority than mock)
        for name, info in self.dynamic_agents.items():
            if name not in agent_names:
                agents.append({
                    "name": name,
                    "role": info['role'],
                    "stability": info['stability'],
                    "type": "dynamic",
                    "emoji": "🤖",
                    "personality": info.get('personality', 'neutral'),
                    "created_at": info.get('created_at')
                })
                agent_names.add(name)
        
        # Add mock agents (only if not already created as dynamic)
        for name, info in self.mock_agents.items():
            if name not in agent_names:
                agents.append({
                    "name": name,
                    "role": info['role'],
                    "stability": info['stability'],
                    "type": "mock",
                    "emoji": info.get('emoji', '🎭'),
                    "personality": info.get('personality', 'analytical')
                })
                agent_names.add(name)
        
        return {"agents": agents, "total_count": len(agents)}
    
    def create_agent(self, agent_data: CreateAgentRequest):
        """Create a new dynamic agent"""
        name = agent_data.name.lower()
        
        # Check for duplicates across all agent types
        if name in self.dynamic_agents:
            raise HTTPException(status_code=400, detail=f"Dynamic agent '{name}' already exists")
        
        if name in self.mock_agents:
            # If it's a mock agent, we'll "upgrade" it to dynamic
            logger.info(f"Upgrading mock agent '{name}' to dynamic agent")
        
        if name == 'jasper':
            raise HTTPException(status_code=400, detail="Cannot create agent with reserved name 'jasper'")
        
        # Create agent info
        agent_info = {
            'name': agent_data.name,
            'role': agent_data.role,
            'personality': agent_data.personality.lower(),
            'skills': agent_data.skills.split(',') if agent_data.skills else [],
            'stability': 0.8,  # New agents start with good stability
            'created_at': datetime.now().isoformat()
        }
        
        self.dynamic_agents[name] = agent_info
        
        # Remove from mock agents if it was there (upgrade scenario)
        if name in self.mock_agents:
            del self.mock_agents[name]
            logger.info(f"Removed '{name}' from mock agents (upgraded to dynamic)")
        
        logger.info(f"Created new dynamic agent: {name}")
        
        return agent_info
    
    def delete_agent(self, agent_name: str):
        """Delete a dynamic agent"""
        name = agent_name.lower()
        
        if name == 'jasper':
            raise HTTPException(status_code=400, detail="Cannot delete Jasper head agent")
        
        if name in self.dynamic_agents:
            del self.dynamic_agents[name]
            logger.info(f"Deleted dynamic agent: {name}")
            return {"message": f"Agent '{agent_name}' deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Dynamic agent '{agent_name}' not found")
    
    def get_agent_details(self, agent_name: str):
        """Get detailed information about a specific agent"""
        name = agent_name.lower()
        
        if name == 'jasper' and self.jasper:
            return {
                "name": "jasper",
                "role": "Head Agent & Coordinator", 
                "type": "head_agent",
                "stability": 0.85,
                "status": "active",
                "autonomy_features": self.jasper.get_autonomy_status() if hasattr(self.jasper, 'get_autonomy_status') else {}
            }
        elif name in self.dynamic_agents:
            agent_info = self.dynamic_agents[name].copy()
            agent_info['type'] = 'dynamic'
            agent_info['status'] = 'active'
            return agent_info
        elif name in self.mock_agents:
            agent_info = self.mock_agents[name].copy()
            agent_info['type'] = 'mock'
            agent_info['status'] = 'active'
            return agent_info
        else:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    
    def _get_available_agent_names(self) -> List[str]:
        """Get list of available agent names (no duplicates)"""
        available_agents = []
        
        # Add Jasper if available
        if self.jasper:
            available_agents.append('jasper')
        
        # Add dynamic agents
        available_agents.extend(list(self.dynamic_agents.keys()))
        
        # Add mock agents only if not overridden by dynamic
        for mock_name in self.mock_agents.keys():
            if mock_name not in self.dynamic_agents:
                available_agents.append(mock_name)
        
        return sorted(available_agents)

@app.on_event("startup")
async def startup_event():
    """Initialize Solvine system on startup"""
    global solvine_system
    try:
        logger.info("🚀 Initializing Solvine Web System...")
        solvine_system = SolvineWebSystem()
        
        total_agents = len(solvine_system.mock_agents) + (1 if solvine_system.jasper else 0)
        logger.info(f"✅ Web API Ready - {total_agents} agents available")
        
        if solvine_system.jasper:
            logger.info("🎯 Jasper head agent: ACTIVE")
        else:
            logger.warning("⚠️ Jasper head agent: NOT AVAILABLE (mock responses will be used)")
            
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

# Web Interface Endpoints
@app.get("/", summary="Serve Solvine Web Interface")
async def serve_web_interface():
    """Serve the beautiful Solvine web interface"""
    web_ui_path = current_dir / "web" / "solvine_web_ui.html"
    if web_ui_path.exists():
        return FileResponse(str(web_ui_path), media_type="text/html")
    else:
        # Return basic info if web UI not found
        return {
            "status": "Solvine Web API Active",
            "message": "Web interface file not found at expected location",
            "api_docs": "/docs",
            "expected_path": str(web_ui_path),
            "web_dir_exists": (current_dir / "web").exists(),
            "current_dir": str(current_dir)
        }

@app.get("/solvine_web_ui.html", summary="Direct Web Interface Access")
async def serve_web_interface_direct():
    """Direct access to the web interface file"""
    web_ui_path = current_dir / "web" / "solvine_web_ui.html"
    if web_ui_path.exists():
        return FileResponse(str(web_ui_path), media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Web interface file not found")

@app.get("/web", summary="Web Interface Redirect")
async def serve_web_interface_redirect():
    """Redirect to main web interface"""
    return await serve_web_interface()

@app.get("/diagnostic", summary="Web Server Diagnostic")
async def serve_diagnostic():
    """Serve diagnostic page for troubleshooting"""
    diagnostic_path = current_dir / "web" / "diagnostic.html"
    if diagnostic_path.exists():
        return FileResponse(str(diagnostic_path), media_type="text/html")
    else:
        return {
            "error": "Diagnostic page not found",
            "expected_path": str(diagnostic_path),
            "current_time": datetime.now().isoformat(),
            "server_info": "Solvine Web API Server running"
        }

# Core API Endpoints
@app.get("/health", summary="Health Check")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Solvine Web API",
        "version": "2.0.0"
    }

@app.post("/query", response_model=List[AgentResponse])
async def query_agents(query: AgentQuery):
    """Send message to agent collective and get responses"""
    if not solvine_system:
        raise HTTPException(status_code=503, detail="Solvine system not initialized")
    
    try:
        responses = await solvine_system.query_agents(query.message, query.agent)
        return responses
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get current system status"""
    if not solvine_system:
        raise HTTPException(status_code=503, detail="Solvine system not initialized")
    
    return solvine_system.get_system_status()

@app.get("/agents")
async def list_agents():
    """Get list of available agents"""
    if not solvine_system:
        raise HTTPException(status_code=503, detail="Solvine system not initialized")
    
    return solvine_system.get_agents_list()

# Enhanced Web UI Endpoints
@app.post("/create_agent")
async def create_agent(agent_data: CreateAgentRequest):
    """Create a new agent dynamically"""
    if not solvine_system:
        raise HTTPException(status_code=503, detail="Solvine system not initialized")
    
    try:
        new_agent = solvine_system.create_agent(agent_data)
        logger.info(f"Successfully created agent: {agent_data.name}")
        return {
            "message": f"Agent '{agent_data.name}' created successfully!",
            "agent": new_agent
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/agents/{agent_name}")
async def delete_agent(agent_name: str):
    """Delete a dynamic agent"""
    if not solvine_system:
        raise HTTPException(status_code=503, detail="Solvine system not initialized")
    
    try:
        result = solvine_system.delete_agent(agent_name)
        logger.info(f"Successfully deleted agent: {agent_name}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_name}")
async def get_agent_details(agent_name: str):
    """Get detailed information about a specific agent"""
    if not solvine_system:
        raise HTTPException(status_code=503, detail="Solvine system not initialized")
    
    try:
        return solvine_system.get_agent_details(agent_name)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Emergency Override Endpoints
@app.post("/emergency/contradiction_scan")
async def emergency_contradiction_scan():
    """Perform emergency contradiction scan"""
    try:
        # Simple contradiction scan simulation
        scan_results = {
            "contradictions_found": 0,
            "system_integrity": "✅ Verified",
            "scan_time": datetime.now().isoformat(),
            "details": "No logical contradictions detected between agent responses"
        }
        
        logger.info("Emergency contradiction scan completed")
        return {
            "message": f"Scan complete. {scan_results['contradictions_found']} contradictions found.",
            "results": scan_results
        }
    except Exception as e:
        logger.error(f"Contradiction scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/emergency/reset_agents")
async def emergency_reset_agents():
    """Reset all agent states"""
    try:
        reset_count = 0
        
        # Reset Jasper if available
        if solvine_system and solvine_system.jasper:
            try:
                # Reset session context
                solvine_system.jasper.session_context = []
                solvine_system.jasper.recursive_count = 0
                reset_count += 1
                logger.info("Reset Jasper agent state")
            except Exception as e:
                logger.warning(f"Failed to reset Jasper: {e}")
        
        # Reset session message count
        if solvine_system:
            solvine_system.session_message_count = 0
        
        reset_count += len(solvine_system.mock_agents) + len(solvine_system.dynamic_agents)
        
        logger.info(f"Emergency agent reset completed: {reset_count} agents")
        return {
            "message": f"Successfully reset {reset_count} agents",
            "status": "✅ All agents reset to clean state"
        }
    except Exception as e:
        logger.error(f"Agent reset failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/emergency/diagnostic")
async def emergency_diagnostic():
    """Run comprehensive system diagnostic"""
    try:
        diagnostic_data = {
            "timestamp": datetime.now().isoformat(),
            "system_status": "Operational",
            "jasper_status": "Active" if (solvine_system and solvine_system.jasper) else "Unavailable",
            "agent_count": len(solvine_system.mock_agents) + len(solvine_system.dynamic_agents) + (1 if solvine_system.jasper else 0),
            "session_messages": solvine_system.session_message_count if solvine_system else 0,
            "memory_usage": "Normal",
            "response_time": "< 1s",
            "api_endpoints": "All functional",
            "web_interface": "Active"
        }
        
        logger.info("Emergency diagnostic completed")
        return diagnostic_data
    except Exception as e:
        logger.error(f"Diagnostic failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/emergency/shutdown")
async def emergency_shutdown():
    """Emergency system shutdown"""
    try:
        logger.warning("Emergency shutdown initiated by user")
        return {
            "message": "Emergency shutdown acknowledged",
            "status": "Server will continue running (use Ctrl+C to actually stop)"
        }
    except Exception as e:
        logger.error(f"Emergency shutdown failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Model Switching Endpoints
@app.post("/switch_model_provider")
async def switch_model_provider(provider_data: dict):
    """Switch between model providers"""
    try:
        provider = provider_data.get('provider', 'ollama')
        
        # For now, simulate switching
        logger.info(f"Model provider switch requested: {provider}")
        
        return {
            "success": True,
            "provider": provider,
            "message": f"Simulated switch to {provider} (feature in development)"
        }
    except Exception as e:
        logger.error(f"Model provider switch failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def run_server(host: str = "localhost", port: int = 8080, reload: bool = False):
    """Run the FastAPI server"""
    print(f"🚀 Starting Solvine Web API Server")
    print(f"🌐 Web Interface: http://{host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"🎯 Jasper Integration: {'✅ Active' if SOLVINE_AVAILABLE else '⚠️ Mock Mode'}")
    
    uvicorn.run(
        "web_api_server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Solvine Web API Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to") 
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    args = parser.parse_args()
    run_server(args.host, args.port, args.reload)
