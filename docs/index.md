# Second Brain Documentation

Welcome to the Second Brain documentation! This guide will help you install, configure, and use Second Brain for work tracking, task management, and AI agent integration.

---

## 🚀 Getting Started

**New to Second Brain?** Start here:

1. **[Quick Start Guide](quickstart.md)** - Get up and running in 5 minutes
2. **[Installation](installation.md)** - Detailed installation for all platforms
3. **[CLI Reference](cli-reference.md)** - Learn all the commands

---

## 📚 Core Documentation

### Essential Guides

- **[Quick Start](quickstart.md)** - 5-minute setup and first steps
- **[Installation](installation.md)** - Install globally, set up MCP server, slash commands
- **[CLI Reference](cli-reference.md)** - Complete command reference with examples
- **[Workflows](workflows.md)** - Common usage patterns and best practices

### Core Features

- **[Notes](notes.md)** - Note-taking with markdown, linked to tasks/projects
- **[Task-Issue Integration](task-issue-integration.md)** - Connect Second Brain tasks with Beads issues
- **[Epics & Dependencies](epics-and-dependencies.md)** - Track large initiatives and dependencies

### AI Agent Integration

- **[MCP Server Setup](mcp-server.md)** - Connect to Claude Code, Claude Desktop, Gemini
- **[Slash Commands](slash-commands.md)** - Quick workflows and query commands for Claude Code
- **[Examples](../examples/)** - 26+ slash command files with workflows and queries

### Advanced Topics

- **[Architecture](architecture.md)** - System design, global setup, git sync strategy
- **[Development](development/)** - Contributing and development guide

---

## 💡 Quick Links by Use Case

### "I want to..."

**...install Second Brain**
→ [Installation Guide](installation.md)

**...start using it right away**
→ [Quick Start Guide](quickstart.md)

**...use it with Claude Code/Desktop**
→ [MCP Server Setup](mcp-server.md)

**...add slash commands to my project**
→ [Slash Commands Guide](slash-commands.md)

**...see all CLI commands**
→ [CLI Reference](cli-reference.md)

**...understand daily workflows**
→ [Workflows Guide](workflows.md)

**...take notes linked to tasks/projects**
→ [Notes Guide](notes.md)

**...track large features with dependencies**
→ [Task-Issue Integration](task-issue-integration.md)

**...search and visualize my content**
→ [Slash Commands - Query Commands](slash-commands.md#query-visualization-commands)

**...sync across multiple machines**
→ [Architecture - Multi-Machine Setup](architecture.md#multi-machine-setup)

**...understand how it works**
→ [Architecture Guide](architecture.md)

---

## 📖 Documentation Structure

```
docs/
├── index.md              # This file - documentation hub
├── quickstart.md         # Get started in 5 minutes
├── installation.md       # Complete installation guide
├── cli-reference.md      # All CLI commands
├── mcp-server.md         # MCP server setup
├── slash-commands.md     # Slash commands for Claude Code
├── workflows.md          # Usage patterns
├── architecture.md       # System design
└── development/          # Development docs
    └── implementation-plan.md
```

---

## 🎯 Common Tasks

### Installation & Setup

```bash
# Install globally
uv tool install git+https://github.com/seanm/second-brain.git

# Initialize
sb init --global
export SECOND_BRAIN_DIR="$HOME/.second-brain"
```

See: [Installation Guide](installation.md)

### Daily Usage

```bash
# Add work log
sb log add "Implemented feature X" --time 90

# Create task
sb task add "Fix bug #123" --priority high

# Generate report
sb report work --days 7
```

See: [CLI Reference](cli-reference.md) • [Workflows](workflows.md)

### AI Agent Integration

```bash
# Setup MCP server
# Edit ~/.config/claude-code/mcp.json

# Copy slash commands
mkdir -p .claude/commands
cp examples/commands/*.md .claude/commands/
```

See: [MCP Server](mcp-server.md) • [Slash Commands](slash-commands.md)

### Multi-Machine Sync

```bash
# Turn into git repo
cd ~/.second-brain
git init && git add . && git commit -m "Initial"

# Push to GitHub
gh repo create yourname-second-brain --private
git push -u origin main
```

See: [Architecture - Git Sync](architecture.md#git-integration-strategy)

---

## 🔧 Reference

### CLI Commands

- **Work Logs**: `sb log add`, `sb log show`
- **Projects**: `sb project create`, `sb project list`, `sb project status`
- **Tasks**: `sb task add`, `sb task update`, `sb task list`
- **Notes**: `sb note create`, `sb note add`, `sb note list`, `sb note search`
- **Reports**: `sb report work`
- **Issues**: `sb issue create`, `sb issue list`, `sb issue ready`
- **Epic + Project**: `sb issue create-with-project` - Create both together (recommended!)
- **Jira**: `sb jira sync` *(optional)*

Full reference: [CLI Reference](cli-reference.md)

### MCP Tools

**Write Operations:**
- `create_work_log_entry` - Add daily work entries
- `create_project`, `create_task` - Create projects and tasks
- `create_note`, `append_to_note`, `update_note` - Note management
- `create_issue`, `create_epic` - Create Beads issues/epics
- `create_epic_with_project` - Create epic + project together (recommended!)
- `update_task`, `update_issue` - Update entities

**Query Operations:**
- `get_work_logs`, `get_tasks`, `get_projects` - Query entities
- `get_notes`, `get_note`, `search_notes` - Search and retrieve notes
- `list_issues`, `get_issue`, `get_ready_work` - Query issues
- `get_transcripts`, `get_transcript_content` - Transcript access
- `generate_report`, `get_project_status` - Reports and analytics

30+ total tools. Full reference: [MCP Server Guide](mcp-server.md)

### Slash Commands

**Workflow Guides (6):**
- `/sb-daily-dev-workflow` - Complete daily routine
- `/sb-ml-research-workflow`, `/sb-feature-development`, `/sb-bug-investigation`
- `/sb-weekly-summary`, `/sb-quick-tasks`

**Query & Visualization (7):**
- `/sb-search-all` - Global search across everything
- `/sb-note-search`, `/sb-project-view`, `/sb-task-view`, `/sb-issue-view`
- `/sb-explore-tags`, `/sb-transcript-view`

**Basic Operations (12):**
- `/sb-log`, `/sb-task-create`, `/sb-task-update`, `/sb-current-work`
- `/sb-project-create`, `/sb-project-status`, `/sb-daily-summary`
- And more...

**Reference:**
- `/sb-quick-mode` - Quick mode syntax guide
- `/sb-context-management` - Context management strategies

26+ total commands. Full reference: [Slash Commands Guide](slash-commands.md)

---

## 💬 Getting Help

- **Documentation**: You're reading it! 📚
- **Examples**: See [examples/](../examples/) directory
- **Issues**: [GitHub Issues](https://github.com/seanm/second-brain/issues)
- **Questions**: Open a discussion on GitHub

---

## 🗺️ Learning Path

### Beginner

1. Install with [Installation Guide](installation.md)
2. Follow [Quick Start](quickstart.md)
3. Learn basic commands: `sb log add`, `sb task add`, `sb project create`
4. Review [Common Workflows](workflows.md#daily-development-workflow)

### Intermediate

1. Set up [MCP Server](mcp-server.md) for AI agent integration
2. Add [Slash Commands](slash-commands.md) to your projects
3. Configure [Git Sync](architecture.md#git-integration-strategy)
4. Explore [All CLI Commands](cli-reference.md)

### Advanced

1. Set up multi-machine sync with git
2. Integrate with Jira for ticket management
3. Create custom workflows and reports
4. Explore [Architecture](architecture.md) for deep understanding

---

## 📋 Cheat Sheet

```bash
# Quick reference - most used commands

# Work logs
sb log add "Text" --task-id ID --time MINUTES
sb log show --days 7

# Tasks
sb task add "Title" --project SLUG --priority high
sb task update ID --status in_progress
sb task list --status in_progress

# Notes
sb note create "Title" --task-id ID --content "Content"
sb note add NOTE_ID "More content"
sb note search "keyword"
sb note list --project SLUG

# Projects
sb project create "Name" --description "Desc"
sb project status SLUG

# Issues (Beads integration)
sb issue create "Title" --with-task --project SLUG
sb issue list --status open
sb issue ready --limit 10

# Reports
sb report work --days 30

# Sync (if using git)
cd ~/.second-brain && git add . && git commit -m "Update" && git push
```

---

**Ready to get started?** → [Quick Start Guide](quickstart.md)

**Need help installing?** → [Installation Guide](installation.md)

**Want AI integration?** → [MCP Server Setup](mcp-server.md)
