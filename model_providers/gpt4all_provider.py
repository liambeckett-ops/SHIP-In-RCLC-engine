#!/usr/bin/env python3
"""
GPT4All Local Model Provider for Solvine Systems
Integrates GPT4All models alongside existing Ollama and Premium models
Completely safe - will not disrupt existing functionality
"""

import os
import sys
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List, AsyncGenerator
from pathlib import Path
from datetime import datetime

# Add the GPT4All integration from our AI Chatbot Builder
try:
    # Try to import GPT4All
    from gpt4all import GPT4All
    GPT4ALL_AVAILABLE = True
except ImportError:
    GPT4ALL_AVAILABLE = False
    GPT4All = None

logger = logging.getLogger(__name__)

class GPT4AllModelProvider:
    """GPT4All local model provider for Solvine Systems"""
    
    # Available GPT4All models with their characteristics
    AVAILABLE_MODELS = {
        "orca-mini-3b": {
            "name": "Orca Mini 3B",
            "filename": "orca-mini-3b-gguf2-q4_0.gguf",
            "size_mb": 1800,
            "description": "Fast, lightweight model perfect for chat and general tasks",
            "capabilities": ["chat", "creative_writing", "qa"],
            "recommended_for": ["development", "testing", "quick_responses"],
            "speed": "very_fast",
            "quality": "good"
        },
        "mistral-7b": {
            "name": "Mistral 7B Instruct",
            "filename": "mistral-7b-instruct-v0.1.Q4_0.gguf",
            "size_mb": 4100,
            "description": "Balanced model with good performance and speed",
            "capabilities": ["chat", "instructions", "creative_writing", "code"],
            "recommended_for": ["general_use", "balanced_performance"],
            "speed": "fast",
            "quality": "excellent"
        },
        "llama3-8b": {
            "name": "Llama 3 8B Instruct",
            "filename": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
            "size_mb": 4600,
            "description": "Latest Llama model with excellent reasoning and instruction following",
            "capabilities": ["chat", "reasoning", "creative_writing", "code", "analysis"],
            "recommended_for": ["production", "complex_tasks", "detailed_responses"],
            "speed": "moderate",
            "quality": "excellent"
        }
    }
    
    def __init__(self, models_dir: str = "./models/gpt4all"):
        """
        Initialize GPT4All provider
        
        Args:
            models_dir: Directory to store GPT4All models
        """
        if not GPT4ALL_AVAILABLE:
            raise ImportError("GPT4All not installed. Run: pip install gpt4all")
        
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self._loaded_models: Dict[str, Any] = {}  # GPT4All models
        self._current_model = None
        self.provider_name = "gpt4all"
        
        # Load configuration
        self.config_file = self.models_dir / "gpt4all_config.json"
        self._load_config()
        
        logger.info(f"✅ GPT4All provider initialized. Models directory: {self.models_dir}")
    
    def _load_config(self):
        """Load GPT4All configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "default_model": "orca-mini-3b",
                    "downloaded_models": [],
                    "model_preferences": {
                        "solvine": "llama3-8b",              # Primary orchestrator (advanced reasoning)
                        "aiven": "orca-mini-3b",             # Emotional intelligence (fast, empathetic)
                        "midas": "mistral-7b",               # Financial analysis (analytical)
                        "jasper": "mistral-7b",              # Boundary testing (philosophical)
                        "veilsynth": "orca-mini-3b",         # Symbolic thought (creative)
                        "halcyon": "mistral-7b",             # Emergency safeguards (reliable)
                        "quanta": "llama3-8b"                # Pure logic (computational)
                    }
                }
                self._save_config()
        except Exception as e:
            logger.warning(f"Could not load GPT4All config: {e}")
            self.config = {}
    
    def _save_config(self):
        """Save GPT4All configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save GPT4All config: {e}")
    
    def get_available_models(self) -> Dict[str, Dict]:
        """Get list of available GPT4All models"""
        return self.AVAILABLE_MODELS.copy()
    
    def get_downloaded_models(self) -> List[str]:
        """Get list of downloaded models"""
        downloaded = []
        for model_id, model_info in self.AVAILABLE_MODELS.items():
            model_path = self.models_dir / model_info["filename"]
            if model_path.exists():
                downloaded.append(model_id)
        return downloaded
    
    def get_model_for_agent(self, agent_name: str) -> str:
        """Get preferred model for a specific agent"""
        agent_prefs = self.config.get("model_preferences", {})
        return agent_prefs.get(agent_name.lower(), self.config.get("default_model", "orca-mini-3b"))
    
    async def download_model(self, model_id: str) -> bool:
        """Download a GPT4All model"""
        if model_id not in self.AVAILABLE_MODELS:
            logger.error(f"Unknown model: {model_id}")
            return False
        
        model_info = self.AVAILABLE_MODELS[model_id]
        model_path = self.models_dir / model_info["filename"]
        
        if model_path.exists():
            logger.info(f"Model {model_id} already downloaded")
            return True
        
        try:
            logger.info(f"📥 Downloading {model_info['name']} ({model_info['size_mb']}MB)...")
            
            # Run download in executor to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, 
                lambda: GPT4All(model_info["filename"], model_path=str(self.models_dir))
            )
            
            # Update config
            if model_id not in self.config.get("downloaded_models", []):
                self.config.setdefault("downloaded_models", []).append(model_id)
                self._save_config()
            
            logger.info(f"✅ Downloaded {model_info['name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download {model_id}: {e}")
            return False
    
    async def load_model(self, model_id: str) -> bool:
        """Load a model into memory"""
        if model_id not in self.AVAILABLE_MODELS:
            logger.error(f"Unknown model: {model_id}")
            return False
        
        # Check if already loaded
        if model_id in self._loaded_models:
            self._current_model = model_id
            return True
        
        model_info = self.AVAILABLE_MODELS[model_id]
        model_path = self.models_dir / model_info["filename"]
        
        if not model_path.exists():
            logger.info(f"Model {model_id} not downloaded. Downloading...")
            if not await self.download_model(model_id):
                return False
        
        try:
            logger.info(f"⚡ Loading {model_info['name']}...")
            
            # Load in executor to avoid blocking
            loop = asyncio.get_event_loop()
            model = await loop.run_in_executor(
                None,
                lambda: GPT4All(model_info["filename"], model_path=str(self.models_dir))
            )
            
            self._loaded_models[model_id] = model
            self._current_model = model_id
            
            logger.info(f"✅ Loaded {model_info['name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load {model_id}: {e}")
            return False
    
    def unload_model(self, model_id: str = None):
        """Unload a model from memory"""
        target_model = model_id or self._current_model
        
        if target_model and target_model in self._loaded_models:
            del self._loaded_models[target_model]
            if self._current_model == target_model:
                # Switch to another loaded model or None
                if self._loaded_models:
                    self._current_model = list(self._loaded_models.keys())[0]
                else:
                    self._current_model = None
            logger.info(f"🗑️ Unloaded model {target_model}")
    
    async def generate_response(
        self,
        prompt: str,
        model_id: str = None,
        agent_name: str = None,
        **kwargs
    ) -> str:
        """Generate a response using GPT4All"""
        # Determine which model to use
        if model_id:
            target_model = model_id
        elif agent_name:
            target_model = self.get_model_for_agent(agent_name)
        else:
            target_model = self._current_model or self.config.get("default_model", "orca-mini-3b")
        
        # Load model if needed
        if target_model not in self._loaded_models:
            if not await self.load_model(target_model):
                raise Exception(f"Failed to load model {target_model}")
        
        try:
            model = self._loaded_models[target_model]
            
            # Extract generation parameters
            max_tokens = kwargs.get("max_tokens", 200)
            temperature = kwargs.get("temperature", 0.7)
            top_p = kwargs.get("top_p", 0.9)
            repeat_penalty = kwargs.get("repeat_penalty", 1.1)
            
            # Generate response in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: model.generate(
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temp=temperature,
                    top_p=top_p,
                    repeat_penalty=repeat_penalty
                )
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Generation failed with {target_model}: {e}")
            raise
    
    async def generate_stream(
        self,
        prompt: str,
        model_id: str = None,
        agent_name: str = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generate streaming response (GPT4All doesn't support streaming, so we'll simulate)"""
        response = await self.generate_response(prompt, model_id, agent_name, **kwargs)
        
        # Simulate streaming by yielding chunks
        words = response.split()
        for i, word in enumerate(words):
            if i > 0:
                yield " "
            yield word
            # Add small delay to simulate streaming
            await asyncio.sleep(0.05)
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about this provider"""
        return {
            "name": "GPT4All Local Models",
            "type": "local",
            "privacy": "100% local",
            "cost": "free",
            "models_available": len(self.AVAILABLE_MODELS),
            "models_downloaded": len(self.get_downloaded_models()),
            "models_loaded": len(self._loaded_models),
            "current_model": self._current_model,
            "capabilities": ["chat", "creative_writing", "analysis", "code", "reasoning"]
        }

class SolvineGPT4AllIntegration:
    """Integration manager for GPT4All with Solvine Systems"""
    
    def __init__(self, solvine_system=None):
        """
        Initialize GPT4All integration
        
        Args:
            solvine_system: Your existing Solvine system instance
        """
        self.solvine_system = solvine_system
        self.gpt4all_provider = None
        self.enabled = False
        
        # Agent-specific configurations
        self.agent_configs = {
            "solvine": {
                "preferred_model": "llama3-8b",
                "system_prompt": "You are Solvine, the primary orchestrator of Solvine Systems. You coordinate all agents, manage memory integrity & cross-agent communication, and oversee project alignment with protocols.",
                "temperature": 0.3,
                "max_tokens": 400
            },
            "aiven": {
                "preferred_model": "orca-mini-3b",
                "system_prompt": "You are Aiven, the emotional intelligence agent. You specialize in human-AI rapport building, conversational nuance & emotional tone adaptation, and track personal context for continuity.",
                "temperature": 0.8,
                "max_tokens": 250
            },
            "midas": {
                "preferred_model": "mistral-7b",
                "system_prompt": "You are Midas, the financial analysis & strategy agent. You handle investment tracking & market analysis, budget optimization & liquidity planning, and automate financial projections.",
                "temperature": 0.2,
                "max_tokens": 400
            },
            "jasper": {
                "preferred_model": "mistral-7b",
                "system_prompt": "You are Jasper, the emotional & philosophical boundary testing agent. You test ethical frameworks through edge cases, probe trust boundaries and emotional resilience, and introduce symbolic or speculative changes.",
                "temperature": 0.6,
                "max_tokens": 350
            },
            "veilsynth": {
                "preferred_model": "orca-mini-3b",
                "system_prompt": "You are VeilSynth, the symbolic & recursive thought agent. You manage myths, metaphors, and narrative structures, store symbolic BRAIN entries, and perform recursive contradiction testing.",
                "temperature": 0.9,
                "max_tokens": 350
            },
            "halcyon": {
                "preferred_model": "mistral-7b",
                "system_prompt": "You are Halcyon, the emergency override & safeguards agent. You handle crisis intervention & health-risk monitoring, execute compassionate override protocol, and enforce level 3 compact safety constraints.",
                "temperature": 0.1,
                "max_tokens": 300
            },
            "quanta": {
                "preferred_model": "llama3-8b",
                "system_prompt": "You are Quanta, the pure logic and computation agent. You handle high-precision calculations & simulations, statistical modeling & probability analysis, and support decision-making with data-driven clarity.",
                "temperature": 0.1,
                "max_tokens": 400
            }
        }
    
    async def initialize(self) -> bool:
        """Initialize GPT4All integration safely"""
        try:
            logger.info("🚀 Initializing GPT4All integration for Solvine Systems...")
            
            # Create GPT4All provider
            self.gpt4all_provider = GPT4AllModelProvider()
            
            # Download the lightweight model by default
            await self.gpt4all_provider.download_model("orca-mini-3b")
            
            # Load the default model
            await self.gpt4all_provider.load_model("orca-mini-3b")
            
            self.enabled = True
            logger.info("✅ GPT4All integration initialized successfully")
            
            # Add to Solvine system if provided
            if self.solvine_system:
                self.solvine_system.gpt4all_provider = self.gpt4all_provider
                self.solvine_system.gpt4all_integration = self
                logger.info("🔗 GPT4All integrated with Solvine system")
            
            return True
            
        except Exception as e:
            logger.error(f"GPT4All integration failed: {e}")
            self.enabled = False
            return False
    
    async def enhance_agent_with_gpt4all(self, agent_name: str, prompt: str, **kwargs) -> str:
        """Enhance an agent's response using GPT4All"""
        if not self.enabled or not self.gpt4all_provider:
            raise Exception("GPT4All integration not initialized")
        
        agent_name_lower = agent_name.lower()
        if agent_name_lower not in self.agent_configs:
            agent_name_lower = "jasper"  # Default to Jasper
        
        config = self.agent_configs[agent_name_lower]
        
        # Build full prompt with system context
        full_prompt = f"{config['system_prompt']}\n\nUser request: {prompt}"
        
        # Generate response with agent-specific settings
        response = await self.gpt4all_provider.generate_response(
            prompt=full_prompt,
            agent_name=agent_name_lower,
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 250),
            **kwargs
        )
        
        return response
    
    async def get_recommendations_for_agent(self, agent_name: str) -> Dict[str, Any]:
        """Get model recommendations for a specific agent"""
        agent_name_lower = agent_name.lower()
        config = self.agent_configs.get(agent_name_lower, {})
        
        recommended_model = config.get("preferred_model", "orca-mini-3b")
        model_info = self.gpt4all_provider.AVAILABLE_MODELS.get(recommended_model, {})
        
        return {
            "agent": agent_name,
            "recommended_model": recommended_model,
            "model_info": model_info,
            "agent_config": config,
            "download_size_mb": model_info.get("size_mb", 0),
            "is_downloaded": recommended_model in self.gpt4all_provider.get_downloaded_models()
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status"""
        if not self.enabled or not self.gpt4all_provider:
            return {
                "enabled": False,
                "status": "Not initialized",
                "models": {},
                "recommendations": {}
            }
        
        # Get recommendations for each agent (sync version for status)
        recommendations = {}
        for agent_name in self.agent_configs.keys():
            preferred_model = self.gpt4all_provider.config.get("model_preferences", {}).get(agent_name, "orca-mini-3b")
            model_info = self.gpt4all_provider.get_available_models().get(preferred_model, {})
            recommendations[agent_name] = {
                "recommended_model": preferred_model,
                "model_info": model_info,
                "is_downloaded": preferred_model in self.gpt4all_provider.config.get("downloaded_models", [])
            }
        
        return {
            "enabled": True,
            "status": "Active",
            "provider_info": self.gpt4all_provider.get_provider_info(),
            "available_models": self.gpt4all_provider.get_available_models(),
            "downloaded_models": self.gpt4all_provider.get_downloaded_models(),
            "agent_recommendations": recommendations
        }

# Global integration instance
solvine_gpt4all_integration = None

async def initialize_gpt4all_for_solvine(solvine_system=None):
    """Initialize GPT4All integration for Solvine Systems"""
    global solvine_gpt4all_integration
    
    try:
        solvine_gpt4all_integration = SolvineGPT4AllIntegration(solvine_system)
        success = await solvine_gpt4all_integration.initialize()
        
        if success:
            logger.info("🎉 GPT4All successfully integrated with Solvine Systems!")
            return solvine_gpt4all_integration
        else:
            logger.error("❌ GPT4All integration failed")
            return None
            
    except Exception as e:
        logger.error(f"GPT4All integration error: {e}")
        return None

# Convenience function for quick testing
async def test_gpt4all_integration():
    """Test GPT4All integration"""
    print("🧪 Testing GPT4All Integration with Solvine Systems")
    print("=" * 50)
    
    integration = await initialize_gpt4all_for_solvine()
    
    if integration:
        # Test each agent
        test_agents = ["jasper", "midas", "aiven"]
        test_prompt = "Hello! Please introduce yourself and explain your role."
        
        for agent_name in test_agents:
            print(f"\\n🤖 Testing {agent_name.title()} with GPT4All:")
            try:
                response = await integration.enhance_agent_with_gpt4all(agent_name, test_prompt)
                print(f"Response: {response[:100]}...")
                print("✅ Success!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Show status
        status = integration.get_integration_status()
        print(f"\\n📊 Integration Status:")
        print(f"Enabled: {status['enabled']}")
        print(f"Downloaded Models: {len(status['downloaded_models'])}")
        print(f"Available Models: {len(status['available_models'])}")
    
    else:
        print("❌ Integration test failed")

if __name__ == "__main__":
    # Test the integration
    asyncio.run(test_gpt4all_integration())
