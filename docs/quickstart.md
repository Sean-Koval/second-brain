# Quick Start Guide

Get up and running with Second Brain in 5 minutes.

## 1. Install Second Brain

**Recommended: Global install with uv**

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Second Brain globally
uv tool install git+https://github.com/seanm/second-brain.git

# Verify
sb --version
```

## 2. Initialize Globally

```bash
# Initialize in ~/.second-brain/
sb init --global

# Add to your shell profile
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc

# Test from any directory!
cd ~
sb log add "Second Brain initialized!"
```

## 3. Create Your First Project

```bash
sb project create "My First Project" \
  --description "Learning Second Brain" \
  --tags "tutorial,learning"

# View it
sb project list
```

Output:
```
Projects
┏━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━┓
┃ ID ┃ Name             ┃ Status ┃ Tasks ┃ Jira ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━┩
│ 1  │ My First Project │ active │ 0/0   │ -    │
└────┴──────────────────┴────────┴───────┴──────┘
```

## 4. Add Some Tasks

```bash
sb task add "Set up development environment" \
  --project my-first-project \
  --priority high

sb task add "Write first unit test" \
  --project my-first-project \
  --priority medium

sb task add "Deploy to production" \
  --project my-first-project \
  --priority low

# View all tasks
sb task list
```

Output:
```
Tasks
┏━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Status ┃ Title                            ┃ Priority ┃ Project          ┃
┡━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ 1  │ ⬜ todo │ Set up development environment   │ high     │ My First Project │
│ 2  │ ⬜ todo │ Write first unit test            │ medium   │ My First Project │
│ 3  │ ⬜ todo │ Deploy to production             │ low      │ My First Project │
└────┴────────┴──────────────────────────────────┴──────────┴──────────────────┘
```

## 5. Log Your Work

```bash
# Simple entry
sb log add "Started working on project setup"

# With task link and time tracking (30 minutes)
sb log add "Configured project dependencies" --task-id 1 --time 30

# With custom date
sb log add "Fixed bug in authentication" --date 2025-01-15

# View recent work
sb log show --days 3
```

Output:
```
2025-01-17
  09:30 [Set up development environment]: Configured project dependencies
  10:15: Started working on project setup
```

## 6. Update Task Progress

```bash
# Start working on a task
sb task update 1 --status in_progress

# Add time spent (25 minutes)
sb task update 1 --time 25

# Mark as done
sb task update 1 --status done

# View updated tasks
sb task list --status done
```

## 7. Generate a Report

```bash
# Weekly report
sb report work --days 7

# Monthly report
sb report work --days 30

# Project-specific report
sb report work --days 14 --project my-first-project
```

Output:
```
Work Report
Period: 2025-01-10 to 2025-01-17

Work days logged: 5
Tasks completed: 1

Completed Tasks:
  ✅ Set up development environment [My First Project]
```

## 8. Optional: Set Up Git Sync

Sync your Second Brain across multiple machines:

```bash
cd ~/.second-brain

# Initialize git
git init
git add .
git commit -m "Initial second brain setup"

# Create private GitHub repo
gh repo create yourusername-second-brain --private
git remote add origin git@github.com:yourusername/yourusername-second-brain.git
git push -u origin main
```

On other machines:

```bash
# Install Second Brain
uv tool install git+https://github.com/seanm/second-brain.git

# Clone your data
git clone git@github.com:yourusername/yourusername-second-brain.git ~/.second-brain

# Set environment variable
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc
```

## 9. Optional: Set Up MCP Server

Use Second Brain with Claude Code, Claude Desktop, or Gemini CLI.

### Find Your Python Path

```bash
# For uv tool install
uv tool dir
# Shows: /home/user/.local/share/uv/tools
# Python path: ~/.local/share/uv/tools/second-brain/bin/python
```

### Claude Code Configuration

Edit `~/.config/claude-code/mcp.json`:

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

### Claude Desktop Configuration

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

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

### Test MCP Server

Restart Claude Code/Desktop and ask:

```
"Use Second Brain to show my projects"
```

If configured correctly, Claude will show your projects!

## 10. Optional: Set Up Slash Commands

Copy slash commands to your project for quick workflows in Claude Code:

```bash
# Navigate to your project
cd ~/your-project

# Create commands directory
mkdir -p .claude/commands

# Copy slash commands
cp ~/.local/share/uv/tools/second-brain/examples/commands/*.md .claude/commands/

# Restart Claude Code
```

Now you can use:
- `/sb-log` - Add work log entry
- `/sb-current-work` - Show active work
- `/sb-task-create` - Create a task
- `/sb-report` - Generate work report
- And more!

See [examples/README.md](examples/README.md) for all slash commands.

---

## Daily Workflow Example

```bash
# Morning - check what's in progress
sb task list --status in_progress

# Start working
sb task update 2 --status in_progress

# Log work throughout the day
sb log add "Implemented user authentication tests" --task-id 2 --time 90
sb log add "Code review for PR #123" --time 30
sb log add "Team standup meeting" --time 15

# Update task progress
sb task update 2 --time 135  # Total time spent
sb task update 2 --status done

# End of day - review
sb log show --days 1
sb task list --status done

# Sync to GitHub (if using git)
cd ~/.second-brain
git add .
git commit -m "Work updates $(date +%Y-%m-%d)"
git push
```

---

## Next Steps

1. ✅ Read [CLI Reference](cli-reference.md) for all CLI commands
2. ✅ See [Workflows Guide](workflows.md) for common usage patterns
3. ✅ Check [MCP Server Guide](mcp-server.md) for AI agent integration
4. ✅ See [Installation Guide](installation.md) for detailed setup
5. ✅ Read [Architecture Guide](architecture.md) to understand the design

---

## Troubleshooting

### `sb: command not found`

```bash
# Add uv bin to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### MCP server not working

1. Check Python path in config
2. Verify `SECOND_BRAIN_DIR` is set correctly
3. Restart Claude Code/Desktop
4. Test manually: `/path/to/python -m second_brain.mcp_server`

### Can't find slash commands

1. Make sure files are in `.claude/commands/` directory
2. Restart Claude Code
3. Type `/sb-` to see autocomplete

---

**🎉 You're all set! Start tracking your work and let Second Brain help you stay organized!**

For more help, see the full [Documentation Index](INDEX.md).
