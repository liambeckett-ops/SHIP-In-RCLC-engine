# 🚀 GitHub Deployment Commands

# After you've prepared your repository on GitHub, run these commands:

# 0. Configure Git (first time setup)
git config --global user.name "Liam Beckett Jorgensen"
git config --global user.email "liambeckettj@gmail.com"
git config --global core.editor "code --wait"
git config --global init.defaultBranch main

# 1. Initialize Git (if not already done)
git init

# 2. Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/liambeckett-ops/SHIP-In-RCLC-engine.git

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: Solvine Systems with Jasper head agent

- Autonomous AI agent collective with head agent authority
- Jasper head agent with boundary enforcement and workshop protocols
- Unified architecture with CLI, API, and web interfaces
- Complete memory system with autonomy metadata
- Production-ready configuration management
- Comprehensive test suite and documentation"

# 5. Push to GitHub
git push -u origin main

# Optional: Create development branch
git checkout -b develop
git push -u origin develop

# 🎯 Repository Settings Recommendations:

# 1. Enable GitHub Pages (for documentation)
# 2. Set up branch protection rules for main
# 3. Enable security alerts and dependency scanning
# 4. Add repository topics: ai, agents, autonomous, python, jasper
# 5. Create repository description:
#    "Autonomous AI Agent Collective with Jasper Head Agent - Boundary enforcement, workshop authority, and genuine AI agency"
