# 🏗️ Solvine Systems - Project Structure

## 📁 Directory Organization

```
Solvine_Systems/
├── 🤖 agents/                    # AI Agent Implementations
│   └── jasper/                   # Jasper Head Agent (Primary)
├── 🌐 api/                       # API Server & Web Services
│   └── solvine_api_server.py     # FastAPI Server
├── 🧠 brain/                     # Symbolic BRAIN Entries & Core Logic
├── ⚙️ config/                    # Configuration Management
│   ├── system.yaml               # Unified System Config
│   ├── base.yaml                 # Base Configuration
│   ├── dev.yaml                  # Development Environment
│   ├── prod.yaml                 # Production Environment
│   ├── sandbox.yaml              # Sandbox Environment
│   └── config_loader.py          # Configuration Loader
├── 💾 data/                      # Data Storage & Analytics
├── 📖 docs/                      # Documentation & Guides
├── 🖥️ interfaces/                # User Interfaces
│   └── unified_cli.py            # Unified Command Line Interface
├── 🧠 memory/                    # Memory Systems & Storage
│   ├── agent_memories/           # Agent Memory Storage
│   ├── conversations/            # Conversation Logs
│   └── memory_analytics/         # Memory Analysis Tools
├── 📓 notebooks/                 # Jupyter Notebooks & Research
├── 🔧 scripts/                   # Utility & Startup Scripts
├── 💻 src/                       # Core Source Code
├── 🧪 tests/                     # Test Suite
├── 🛠️ utils/                     # Utility Functions
└── 🌐 web/                       # Web UI & Frontend
    └── solvine_web_ui.html       # Web Interface

## 🚀 Entry Points

- **`main_unified.py`** - Primary application entry point
- **`api/solvine_api_server.py`** - Web API server
- **`scripts/start_api.ps1`** - API startup script

## 🔧 Core Components

1. **Jasper Head Agent** - Primary AI agent with autonomy features
2. **Unified Configuration** - Centralized YAML-based config system
3. **Memory System** - Persistent storage with autonomy metadata
4. **Unified CLI** - Command-line interface for all operations
5. **API Server** - Web-based API for external integrations

## 📋 Key Features

- ✅ **Head Agent Authority** - Jasper controls system voice and tone
- ✅ **Autonomy Features** - Boundary enforcement and challenge detection
- ✅ **Unified Architecture** - Single point of configuration and control
- ✅ **Memory Persistence** - SQLite-based memory with metadata
- ✅ **Multi-Interface** - CLI, API, and Web UI support

## 🎯 Quick Start

```bash
# Run main application
python main_unified.py

# Start API server
python api/solvine_api_server.py

# Or use startup script
./scripts/start_api.ps1
```

---
*Organized structure following industry standards for maintainability and scalability.*
