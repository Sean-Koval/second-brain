# Installation Guide

Complete installation instructions for Second Brain - a global work tracking system with CLI and MCP server integration.

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Initialize Your Second Brain](#initialize-your-second-brain)
- [MCP Server Setup](#mcp-server-setup)
- [Slash Commands Setup](#slash-commands-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

**TL;DR - Get running in 3 commands:**

```bash
# 1. Install globally with uv
uv tool install git+https://github.com/seanm/second-brain.git

# 2. Initialize globally
sb init --global

# 3. Add to shell profile
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc && source ~/.bashrc
```

Done! Now use `sb` from any directory.

---

## Prerequisites

- **Python 3.10 or higher**
- **uv** (recommended) or **pip**
- **Git**

### Install uv (if you don't have it)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Check your Python version:**
```bash
python --version  # Should be 3.10 or higher
```

---

## Installation Methods

### Method 1: Global Install with uv (Recommended)

Install Second Brain globally so the `sb` command is available everywhere:

```bash
# Install directly from GitHub
uv tool install git+https://github.com/seanm/second-brain.git

# Verify installation
sb --version
second-brain-mcp --help
```

✅ **Benefits:**
- No virtual environment to activate
- `sb` command available system-wide
- Easy to update: `uv tool upgrade second-brain`
- Works from any directory

### Method 2: Install in Virtual Environment (Development)

For development or if you want isolation:

```bash
# 1. Clone the repository
git clone https://github.com/seanm/second-brain.git
cd second-brain

# 2. Create virtual environment with uv
uv venv

# 3. Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 4. Install in editable mode
uv pip install -e .

# 5. Verify
sb --version
```

### Method 3: Install with pip (Alternative)

```bash
# Clone repository
git clone https://github.com/seanm/second-brain.git
cd second-brain

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install
pip install -e .
```

---

## Initialize Your Second Brain

After installation, initialize your global Second Brain:

### Global Setup (Recommended)

```bash
# 1. Initialize globally in ~/.second-brain/
sb init --global

# 2. Add to your shell profile
# For bash:
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc

# For zsh:
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.zshrc
source ~/.zshrc

# 3. Test from any directory
cd ~
sb log add "Second Brain is set up!"
sb log show
```

### What Gets Created

```
~/.second-brain/
├── data/
│   ├── projects/         # Project markdown files
│   ├── work_logs/        # Daily work logs
│   ├── transcripts/      # Meeting transcripts
│   └── index.db          # SQLite database
├── config.json           # Configuration
├── .gitignore            # Git ignore rules
└── README.md             # Your personal docs
```

### Optional: Set Up Git Sync

Turn your Second Brain into a git repository for syncing across machines:

```bash
cd ~/.second-brain

# Initialize git
git init

# Add everything
git add .
git commit -m "Initial second brain setup"

# Create private GitHub repo
gh repo create yourusername-second-brain --private

# Push to GitHub
git remote add origin git@github.com:yourusername/yourusername-second-brain.git
git push -u origin main
```

Now you can sync your entire work history across all your machines! 🎉

---

## MCP Server Setup

Connect Second Brain to AI agents (Claude Code, Claude Desktop, Gemini CLI).

### Prerequisites for MCP Server

If you installed with `uv tool install`, you need to find the Python path:

```bash
# Find uv tool Python path
uv tool dir
# Shows: /home/user/.local/share/uv/tools

# Your Python will be at:
# ~/.local/share/uv/tools/second-brain/bin/python
```

Or if using a virtual environment:

```bash
# Activate your venv first
which python  # macOS/Linux
where python  # Windows
```

### Claude Code Setup

**Location:** `~/.config/claude-code/mcp.json` (macOS/Linux) or `%APPDATA%\claude-code\mcp.json` (Windows)

Create or edit the file:

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/home/username/.local/share/uv/tools/second-brain/bin/python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/home/username/.second-brain"
      }
    }
  }
}
```

**Replace `/home/username/` with your actual home directory!**

**On macOS:**
```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/Users/username/.local/share/uv/tools/second-brain/bin/python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/Users/username/.second-brain"
      }
    }
  }
}
```

### Claude Desktop Setup

**Location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/Users/username/.local/share/uv/tools/second-brain/bin/python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/Users/username/.second-brain"
      }
    }
  }
}
```

### Gemini CLI Setup

Add to your Gemini CLI configuration:

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/home/username/.local/share/uv/tools/second-brain/bin/python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/home/username/.second-brain"
      }
    }
  }
}
```

### Test MCP Server

Restart Claude Code/Desktop and test:

```
In Claude: "Use Second Brain to list my projects"
```

If it works, you'll see your projects!

---

## Slash Commands Setup

Slash commands let you quickly trigger Second Brain workflows in Claude Code.

### Step 1: Copy Slash Commands to Your Project

For each project where you want to use slash commands:

```bash
# Navigate to your project
cd ~/your-project

# Create commands directory
mkdir -p .claude/commands

# Copy Second Brain slash commands
cp ~/.local/share/uv/tools/second-brain/examples/commands/*.md .claude/commands/

# Or if you cloned the repo:
cp ~/second-brain/examples/commands/*.md .claude/commands/
```

### Step 2: Restart Claude Code

Close and reopen Claude Code.

### Step 3: Use Slash Commands

Type `/sb-` in Claude Code to see all available commands:

- `/sb-log` - Add work log entry
- `/sb-current-work` - Show active work
- `/sb-task-create` - Create a task
- `/sb-task-update` - Update task
- `/sb-report` - Generate work report
- `/sb-weekly-review` - Weekly review
- And more!

See [examples/README.md](examples/README.md) for full documentation.

---

## Verification

### Test CLI

```bash
# From any directory
sb --version
sb log show
sb project list
```

### Test MCP Server

```bash
# Run MCP server directly
second-brain-mcp

# Should start without errors
```

In Claude Code/Desktop:

```
User: "Use Second Brain to show my recent work logs"
```

Should return your work logs!

### Test Slash Commands

In Claude Code:

```
Type: /sb-current-work
```

Should show your active tasks and today's logs.

---

## Troubleshooting

### `sb: command not found`

**If installed with `uv tool install`:**
```bash
# Add uv bin to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**If installed in venv:**
```bash
# Activate the virtual environment
source /path/to/venv/bin/activate
```

### MCP Server Not Connecting

1. **Check Python path is correct:**
   ```bash
   # Test the command manually
   /path/to/python -m second_brain.mcp_server
   ```

2. **Check environment variable:**
   ```bash
   echo $SECOND_BRAIN_DIR
   # Should show: /home/username/.second-brain
   ```

3. **Check MCP config file exists:**
   ```bash
   ls ~/.config/claude-code/mcp.json
   cat ~/.config/claude-code/mcp.json
   ```

4. **Restart Claude Code/Desktop** after changing config

### Slash Commands Not Showing

1. **Check commands directory:**
   ```bash
   ls .claude/commands/
   # Should show sb-*.md files
   ```

2. **Restart Claude Code**

3. **Type `/` in Claude Code** - slash commands should appear in autocomplete

### Permission Denied on ~/.second-brain

```bash
# Fix permissions
chmod 755 ~/.second-brain
chmod -R 644 ~/.second-brain/data/
chmod 755 ~/.second-brain/data/
```

### Database Locked Error

```bash
# Close any open connections
pkill -f "second_brain"

# Restart MCP server
```

---

## Updating Second Brain

### If installed with uv tool:

```bash
uv tool upgrade second-brain
```

### If installed from source:

```bash
cd second-brain
git pull
uv pip install -e .
```

---

## Uninstalling

### If installed with uv tool:

```bash
uv tool uninstall second-brain
```

### If installed in venv:

```bash
pip uninstall second-brain
```

### Remove data (optional):

```bash
# Backup first!
cp -r ~/.second-brain ~/second-brain-backup

# Remove
rm -rf ~/.second-brain
```

---

## Multiple Machines Setup

### On your first machine:

```bash
# Initialize and push to GitHub
sb init --global
cd ~/.second-brain
git init
git add .
git commit -m "Initial setup"
gh repo create yourusername-second-brain --private
git remote add origin git@github.com:yourusername/yourusername-second-brain.git
git push -u origin main
```

### On your second machine:

```bash
# Install Second Brain
uv tool install git+https://github.com/seanm/second-brain.git

# Clone your data
git clone git@github.com:yourusername/yourusername-second-brain.git ~/.second-brain

# Set environment variable
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc

# Test
sb log show
```

### Daily sync workflow:

```bash
# Pull latest
cd ~/.second-brain
git pull

# Do work...
sb log add "Working on feature X"

# Push at end of day
git add .
git commit -m "Work log updates $(date +%Y-%m-%d)"
git push
```

---

## Next Steps

1. ✅ Read [Quick Start Guide](quickstart.md) for usage examples
2. ✅ See [CLI Reference](cli-reference.md) for all CLI commands
3. ✅ Check [Workflows Guide](workflows.md) for usage patterns
4. ✅ See [examples/README.md](examples/README.md) for slash commands
5. ✅ Read [Architecture Guide](architecture.md) for system design

---

**Happy tracking! 🧠**
