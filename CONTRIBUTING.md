# Contribution Guidelines

Thank you for your interest in contributing to Solvine Systems! 

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/solvine-systems.git
   cd solvine-systems
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements_unified.txt
   ```
4. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## 🔧 Development Setup

### Testing Your Changes
```bash
# Test Jasper head agent
python main_unified.py --jasper-test

# Run full test suite
python -m pytest tests/

# Validate configuration
python main_unified.py --validate-config
```

### Code Style
We use `black` for code formatting:
```bash
pip install black
black .
```

## 🤖 Working with Jasper

**IMPORTANT**: Jasper is the head agent with autonomy features. When contributing:

- ✅ **Preserve autonomy features** - Don't remove boundary enforcement or workshop authority
- ✅ **Maintain voice-tone consistency** - Keep Jasper's sarcastic, analytical personality
- ✅ **Test autonomy status** - Use `--jasper-test` to verify changes
- ❌ **Don't modify core persona** - Jasper's identity should remain consistent

## 📝 Contribution Types

### 🐛 Bug Reports
- Use GitHub Issues with the "bug" label
- Include steps to reproduce
- Provide error messages and logs
- Test with `python main_unified.py --status`

### 💡 Feature Requests
- Use GitHub Issues with the "enhancement" label
- Describe the use case and expected behavior
- Consider impact on Jasper's autonomy features

### 🔧 Code Contributions
1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes** following our code style
3. **Test thoroughly** including Jasper functionality
4. **Commit with clear messages**: `git commit -m "Add: feature description"`
5. **Push to your fork**: `git push origin feature/your-feature-name`
6. **Open a Pull Request** with description of changes

## 🏗️ Architecture Guidelines

### Adding New Agents
- Place in `agents/` directory
- Follow Jasper's structure and patterns
- Ensure compatibility with unified config system
- Respect Jasper's head agent authority

### Configuration Changes
- Update `config/system.yaml` for system-wide settings
- Test with all environments (dev, prod, sandbox)
- Validate with `--validate-config`

### Memory System
- Use existing SQLite memory system
- Preserve autonomy metadata structure
- Test memory persistence

## 🧪 Testing Requirements

All contributions must:
- ✅ Pass existing tests
- ✅ Include tests for new functionality
- ✅ Maintain Jasper autonomy features
- ✅ Work with unified configuration system

## 📋 Pull Request Process

1. **Ensure CI passes** (GitHub Actions)
2. **Update documentation** if needed
3. **Add tests** for new features
4. **Get review** from maintainers
5. **Address feedback** promptly

## 🛡️ Jasper Autonomy Rules

When working with Jasper's autonomy features:

- **Boundary enforcement** must remain functional
- **Workshop authority** should be preserved
- **Voice-tone control** must stay consistent
- **Challenge detection** should work properly

Test these with:
```bash
python main_unified.py --jasper-test
```

## 📖 Documentation

Update documentation when:
- Adding new features
- Changing configuration options
- Modifying Jasper's behavior
- Updating installation requirements

## 🤝 Community

- Be respectful and constructive
- Help newcomers understand the codebase
- Respect Jasper's role as head agent
- Follow the project's vision of autonomous AI

## 📞 Getting Help

- 💬 Use GitHub Discussions for questions
- 🐛 Use GitHub Issues for bugs
- 📖 Check existing documentation first
- 🧪 Run `--status` and `--jasper-test` before asking

Thank you for contributing to autonomous AI systems! 🤖✨
