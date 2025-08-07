# 🤖 Solvine Systems

**Autonomous AI Agent Collective with Head Agent Authority**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 **Overview**

Solvine Systems is a sophisticated multi-agent AI framework featuring **Jasper**, an autonomous head agent with voice-tone control, boundary enforcement, and workshop authority. The system combines local AI models with a unified architecture for scalable, production-ready AI agent management.

### ✨ **Key Features**

- 🤖 **Jasper Head Agent** - Autonomous decision-making with boundary enforcement
- 🛡️ **Authority System** - Voice-tone control and workshop protocol management  
- 🧠 **Memory Persistence** - SQLite-based memory with autonomy metadata
- 🔧 **Unified Architecture** - Single configuration system across all components
- 🌐 **Multi-Interface** - CLI, API, and Web UI support
- ⚙️ **Environment Support** - Dev, prod, sandbox configurations

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/solvine-systems.git
cd solvine-systems

# Install dependencies
pip install -r requirements_unified.txt

# Set up environment (optional)
cp .env.example .env
# Edit .env with your settings
```

### Usage

```bash
# Start interactive CLI with Jasper
python main_unified.py --cli

# Local Jasper mode only
python main_unified.py --cli --local

# Test Jasper head agent
python main_unified.py --jasper-test

# Check system status
python main_unified.py --status

# Validate configuration
python main_unified.py --validate-config
```

## 🏗️ **Architecture**

```
Solvine_Systems/
├── 🤖 agents/           # AI Agent Implementations
│   └── jasper/          # Jasper Head Agent
├── 🌐 api/              # API Server & Web Services
├── 🧠 brain/            # Symbolic BRAIN Entries
├── ⚙️ config/           # Configuration Management
├── 💾 data/             # Data Storage & Analytics
├── 📖 docs/             # Documentation
├── 🖥️ interfaces/       # User Interfaces
├── 🧠 memory/           # Memory Systems
├── 📓 notebooks/        # Research & Analysis
├── 🔧 scripts/          # Utility Scripts
├── 💻 src/              # Core Source Code
├── 🧪 tests/            # Test Suite
├── 🛠️ utils/            # Utility Functions
└── 🌐 web/              # Web Interface
```

## 🤖 **Jasper Head Agent**

Jasper is the autonomous head agent with sophisticated capabilities:

### 🛡️ **Autonomy Features**
- **Boundary Enforcement** - Detects and deflects authority challenges
- **Workshop Authority** - Controls analytical framework protocols
- **Voice-Tone Consistency** - Maintains personality across interactions
- **Independent Decision Making** - Autonomous error recovery and protocol management

### 🔧 **Workshop Mode**
```python
# Example interaction
User: "Analyze this data pattern"
Jasper: "🔧 Workshop Authority: Analyzing 'data pattern' with autonomous systematic approach

📊 Autonomous Workshop Analysis:
   • Input: 'data pattern'
   • Authority: Independent analytical framework
   • Approach: Systematic workshop protocols
   
*processes with practiced cynicism and workshop authority*"
```

## 📚 **Documentation**

- 📖 [Architecture Guide](docs/AGENT_COMMUNICATION_GUIDE.md)
- 🚀 [Quick Start Guide](docs/QUICK_START.md)
- 🔧 [API Documentation](docs/API_README.md)
- 📝 [Contributing Guidelines](docs/CONTRIBUTING.md)
- 📋 [Project Structure](PROJECT_STRUCTURE.md)

## 🧪 **Testing**

```bash
# Run all tests
python -m pytest tests/

# Test specific components
python tests/test_consolidated.py
python tests/test_agent_deployment.py

# Validate memory persistence
python tests/validate_memory_persistence.py
```

## 🌐 **Deployment**

### Local Development
```bash
# Development environment
python main_unified.py --config-env dev --debug

# Sandbox environment
python main_unified.py --config-env sandbox
```

### Production
```bash
# Production environment
python main_unified.py --config-env prod

# Start API server (when implemented)
python api/solvine_api_server.py
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Built with love for autonomous AI systems
- Inspired by the concept of genuine AI agency
- Special thanks to the open-source AI community

## 📊 **Project Status**

- ✅ **Core System** - Fully functional
- ✅ **Jasper Head Agent** - Production ready with autonomy features
- ✅ **CLI Interface** - Complete with local and hybrid modes
- ✅ **Configuration System** - Unified YAML-based configuration
- ✅ **Memory System** - SQLite with autonomy metadata
- 🚧 **API Server** - In development
- 🚧 **Web Interface** - Basic UI available
- 📋 **Documentation** - Comprehensive guides available

---

**Solvine Systems** - *Where autonomous AI agents think, decide, and act with genuine agency* 🤖✨
