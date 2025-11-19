<div align="center">

# 🧠 Second Brain

**Your Personal Work Operating System**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*Track your work. Sync across machines. Integrate with AI agents.*

[Quick Start](#-quick-start) • [Installation](docs/installation.md) • [Documentation](docs/) • [Examples](examples/)

</div>

---

## ✨ What is Second Brain?

Second Brain is a **global, persistent knowledge base** that tracks your daily work, projects, and tasks. It's designed for developers who want to:

- 📝 **Track daily work** with automatic timestamping
- 🎯 **Manage tasks** across multiple projects
- 🚀 **Organize epics & dependencies** with Beads-powered issue tracking
- 📊 **Generate reports** for performance reviews and promotion tracking
- 🤖 **Work with AI agents** via MCP server (Claude Code, Claude Desktop, Gemini)
- 🔄 **Sync across machines** with private GitHub repository
- 💻 **Access from anywhere** - global installation works from any directory

**Works 100% offline** - All core features work without internet. Jira integration is completely optional.

---

## 🚀 Quick Start

**3 commands to get started:**

```bash
# 1. Install globally with uv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install git+https://github.com/seanm/second-brain.git

# 2. Initialize globally
sb init --global

# 3. Set environment variable
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc && source ~/.bashrc
```

**That's it!** Now use `sb` from any directory:

```bash
sb log add "Started working on authentication feature"
sb task add "Implement OAuth" --priority high
sb epic create "Mobile App Redesign" --priority 4
sb issue ready  # Find work with no blockers
```

👉 **See [Quick Start Guide](docs/quickstart.md) for detailed walkthrough**

---

## 🎯 Use Cases

<table>
<tr>
<td width="50%">

### 💼 Daily Work Tracking

```bash
sb log add "Fixed auth bug" --time 90
sb issue ready  # Find unblocked work
sb task update 5 --status done
sb log show --days 7
```

Track everything you do with timestamps and time tracking.

</td>
<td width="50%">

### 📊 Performance Reviews

```bash
sb report work --days 90 > Q1-review.md
```

Generate comprehensive reports with completed tasks, time spent, and project breakdown.

</td>
</tr>
<tr>
<td width="50%">

### 🚀 Epic & Dependency Management

```bash
# One-time setup per project
sb init --beads --prefix SB

# Create epic + project together (recommended)
sb issue create-with-project "API Migration" \
  --labels backend,migration

# Or separate steps
sb epic create "Mobile App"
sb issue create "Migrate auth" --epic SB-1
sb issue add-dependency SB-3 SB-2 --type blocks
sb issue ready  # Auto-find ready work
sb issue stats  # Project overview
```

**New!** Create epic + project in one command for seamless integration between dependency tracking (Beads) and notes/time tracking (Second Brain).

</td>
<td width="50%">

### 🤖 Ready Work Detection

```bash
sb issue ready              # All unblocked work
sb issue ready --priority 4 # Critical only
sb issue list --status blocked  # See what's blocked
```

Automatically finds issues with no blockers - perfect for "what should I work on next?"

</td>
</tr>
<tr>
<td width="50%">

### 🤖 AI Agent Integration

```
"Use Second Brain to show my current tasks"
"Generate a weekly work report"
"Add today's work to my log"
```

Works with Claude Code, Claude Desktop, Gemini CLI via MCP server.

</td>
<td width="50%">

### 🔄 Multi-Machine Sync

```bash
cd ~/.second-brain
git push  # Sync from work laptop

# On home machine
git pull  # Get latest work
```

Your entire work history synced via private GitHub repo.

</td>
</tr>
</table>

---

## 📦 Installation

### Recommended: Global Install

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Second Brain globally
uv tool install git+https://github.com/seanm/second-brain.git

# Initialize
sb init --global
export SECOND_BRAIN_DIR="$HOME/.second-brain"
```

### Alternative: From Source

```bash
git clone https://github.com/seanm/second-brain.git
cd second-brain
uv venv && source .venv/bin/activate
uv pip install -e .
```

📖 **Full installation guide:** [docs/installation.md](docs/installation.md)

---

## 🔧 Features

### Core Capabilities

- ✅ **Work Log Tracking** - Daily work entries with automatic timestamps
- ✅ **Project Management** - Organize work with markdown-based notes
- ✅ **Task Tracking** - Create, update, track tasks with status & priority
- ✅ **Epic & Issue Management** - Large initiative tracking with dependency graphs (powered by Beads)
- 🎯 **Ready Work Detection** - Automatically find unblocked issues to work on
- 🔗 **Dependency Tracking** - 4 types: blocks, related, parent-child, discovered-from
- ✅ **Time Tracking** - Track time spent on tasks and projects
- ✅ **Reports & Analytics** - Generate work summaries for reviews
- ✅ **Transcript Processing** - Store and process meeting transcripts
- ✅ **Jira Integration** *(optional)* - Sync tickets from Jira

### Storage

**Hybrid approach** - Best of both worlds:

```
~/.second-brain/
├── data/
│   ├── index.db          # SQLite - fast queries
│   ├── projects/         # Markdown - human readable
│   ├── work_logs/        # Markdown - daily logs
│   └── transcripts/      # Markdown - meeting notes
├── .beads/               # Beads - epic/dependency tracking
│   ├── issues.jsonl      # Issues and epics
│   └── dependencies.jsonl # Dependency relationships
├── config.json
└── .gitignore
```

- **SQLite database** for fast queries and relationships
- **Markdown files** for human readability and git-friendly diffs
- **Beads JSONL files** for dependency graphs and epic tracking
- Automatically synced - changes in one update the other

---

## 🤖 AI Agent Integration

### MCP Server

Connect Second Brain to AI agents:

**Claude Code** (`~/.config/claude-code/mcp.json`):
```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/path/to/python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/home/user/.second-brain"
      }
    }
  }
}
```

Then in Claude:
```
"Use Second Brain to show my projects"
"Add today's work to my log"
"What work is ready for me to start?"
"Create an epic for mobile redesign"
"Generate a weekly report"
```

📖 **MCP setup guide:** [docs/mcp-server.md](docs/mcp-server.md)

### Slash Commands

27 pre-built workflows for Claude Code - supports both conversational and quick modes.

#### Installation

```bash
# Copy all slash commands to your project
mkdir -p .claude/commands
cp ~/.local/share/uv/tools/second-brain/examples/commands/*.md .claude/commands/

# Restart Claude Code
```

#### Quick Mode Examples (Day-to-Day Work)

**Morning - Start Your Day:**
```
/sb-current-work
# Shows: Active tasks, today's logs, high priority items

/sb-issue-ready --priority 4
# Shows: Critical work ready to start (no blockers)
```

**During Work - Log & Create:**
```
/sb-log "Implemented OAuth integration" --task-id 42 --time 120

/sb-task-create "Fix login timeout bug" --project auth --priority high

/sb-note-create "API Architecture Decisions" --project backend --content "Using REST over GraphQL because..."
```

**Starting New Feature:**
```
/sb-epic-project-create "Mobile App v2" --priority 4 --labels mobile,frontend
# Creates both: Epic in Beads + Project in Second Brain
# Then work on it:
#   - Create issues under epic
#   - Create tasks in project
#   - Link them together
```

**Finding Information:**
```
/sb-search-all "authentication"
# Search everything: notes, tasks, work logs, issues

/sb-project-view backend-api
# Complete project overview: tasks, notes, progress, health

/sb-task-view 42
# Everything about task 42: notes, work logs, linked issue, timeline
```

**End of Day:**
```
/sb-daily-summary
# Reviews: Work logged, tasks completed, in-progress items

/sb-task-update 42 --status done --time 180
```

**Weekly Review:**
```
/sb-weekly-summary
# Comprehensive review: Accomplishments, blockers, planning

/sb-report
# Generate detailed work report for team updates
```

#### Conversational Mode Examples

Just type the command and Claude guides you:

**Example 1: Adding Work Log**
```
You: /sb-log
Claude: "What did you work on?"
You: "Fixed authentication bug in OAuth flow"
Claude: "Should this be linked to a task?"
You: "Yes, task 42"
Claude: "How much time did you spend? (in minutes)"
You: "90 minutes"
Claude: ✓ Work log added! Linked to task #42, 90 minutes tracked.
```

**Example 2: Creating Epic + Project**
```
You: /sb-epic-project-create
Claude: "What's the name of this initiative?"
You: "Payment System Redesign"
Claude: "Brief description? (optional)"
You: "Complete overhaul of payment processing with Stripe"
Claude: "Priority? (0-4, default 2)"
You: "4"
Claude: "Any labels/tags? (comma-separated)"
You: "backend,payments,high-priority"

Claude: ✓ Epic + Project created!
        Epic ID: epic-042 ↔️ Project: payment-system-redesign

        Next steps:
        1. Create issues: sb issue create "..." --epic epic-042
        2. Create tasks: sb task add "..." --project payment-system-redesign
        3. Add notes: sb note create "..." --project payment-system-redesign
```

**Example 3: Finding Ready Work**
```
You: /sb-issue-ready
Claude: Finding issues with no blockers...

        🎯 3 issues ready to work on:

        1. Implement Stripe webhooks (epic-042)
           Priority: High | Type: feature

        2. Add payment UI components (epic-042)
           Priority: High | Type: feature

        3. Write integration tests (epic-042)
           Priority: Medium | Type: task

        💡 All dependencies satisfied - start any time!
```

#### Complete Command List

| Command | Purpose | Quick Example |
|---------|---------|---------------|
| **Workflow Guides** |||
| `/sb-daily-dev-workflow` | Complete daily routine | Interactive guide |
| `/sb-epic-project-create` | Create epic + project | `/sb-epic-project-create "Feature" --priority 3` |
| `/sb-weekly-summary` | Weekly review | Generates summary |
| **Query Commands** |||
| `/sb-search-all` | Global search | `/sb-search-all "authentication"` |
| `/sb-project-view` | Project overview | `/sb-project-view backend-api` |
| `/sb-task-view` | Task details | `/sb-task-view 42` |
| `/sb-issue-view` | Issue/epic view | `/sb-issue-view epic-042` |
| **Basic Operations** |||
| `/sb-log` | Log work | `/sb-log "Fixed bug" --task-id 42 --time 90` |
| `/sb-task-create` | Create task | `/sb-task-create "Task" --project api --priority high` |
| `/sb-current-work` | Show active work | Displays status |
| `/sb-issue-ready` | Find ready work | `/sb-issue-ready --priority 4` |

📖 **Full guide:** [examples/README.md](examples/README.md) • [docs/slash-commands.md](docs/slash-commands.md)

---

## 🌍 Sync Across Machines

Turn `~/.second-brain/` into a private GitHub repository:

```bash
cd ~/.second-brain
git init
git add .
git commit -m "Initial setup"
gh repo create yourusername-second-brain --private
git remote add origin git@github.com:yourusername/yourusername-second-brain.git
git push -u origin main
```

**On other machines:**

```bash
uv tool install git+https://github.com/seanm/second-brain.git
git clone git@github.com:yourusername/yourusername-second-brain.git ~/.second-brain
export SECOND_BRAIN_DIR="$HOME/.second-brain"
```

Your entire work history - SQLite database, markdown files, all synced! 🎉

---

## 📖 Documentation

- 🚀 **[Quick Start Guide](docs/quickstart.md)** - Get started in 5 minutes
- 💿 **[Installation](docs/installation.md)** - Detailed installation for all platforms
- 💻 **[CLI Reference](docs/cli-reference.md)** - All commands and options
- 🎯 **[Epics & Dependencies](docs/epics-and-dependencies.md)** - Epic/issue management with Beads
- 🔌 **[MCP Server Setup](docs/mcp-server.md)** - Connect to AI agents
- ⚡ **[Slash Commands](examples/README.md)** - Claude Code workflows
- 🎨 **[Workflows](docs/workflows.md)** - Common usage patterns
- 🏗️ **[Architecture](docs/architecture.md)** - System design and philosophy

📚 **[Full Documentation Index](docs/)**

---

## 🎨 CLI Examples

### Daily Workflow

```bash
# Morning - check active work
sb task list --status in_progress

# Log work throughout the day
sb log add "Implemented user authentication" --task-id 5 --time 90
sb log add "Code review for PR #234" --time 30
sb log add "Team standup" --time 15

# Update task status
sb task update 5 --status done

# End of day - review and sync
sb log show --days 1
cd ~/.second-brain && git add . && git commit -m "Work updates" && git push
```

### Project Management

```bash
# Create project
sb project create "Mobile App Redesign" \
  --description "Complete UI/UX overhaul" \
  --tags "mobile,design,priority"

# Add tasks
sb task add "Design new navigation" --project mobile-app-redesign --priority high
sb task add "Implement dark mode" --project mobile-app-redesign --priority medium

# Check project status
sb project status mobile-app-redesign
```

### Epic & Issue Management

```bash
# RECOMMENDED: Create epic + project together for new initiatives
sb issue create-with-project "API v2 Migration" \
  --priority 4 \
  --labels backend,migration \
  --description "Migrate all API endpoints to v2"
# Creates both: Epic in Beads + Project in Second Brain

# Create issues under the epic
sb issue create "Migrate auth endpoints" --epic SB-1 --priority 4 --with-task --project api-v2-migration
sb issue create "Migrate user endpoints" --epic SB-1 --priority 3 --with-task --project api-v2-migration

# Add notes and track work
sb note create "Migration Strategy" --project api-v2-migration
sb log add "Started endpoint migration" --task-id 5 --time 120

# Add dependency (auth must finish before users)
sb issue add-dependency SB-3 SB-2 --type blocks

# Find work that's ready to start (no blockers)
sb issue ready

# Check overall project health
sb issue stats
```

### Reports & Analytics

```bash
# Weekly report
sb report work --days 7

# Quarterly review (for performance review)
sb report work --days 90 > Q1-accomplishments.md

# Project-specific report
sb report work --project mobile-app-redesign --days 30
```

---

## 🔌 Integrations

- ✅ **Claude Code** - Full MCP integration
- ✅ **Claude Desktop** - MCP server support
- ✅ **Gemini CLI** - MCP server support
- ✅ **Jira** - Optional ticket sync
- 🔄 **GitHub** - Git-based sync for data
- 📝 **Markdown** - Human-readable files
- 🗄️ **SQLite** - Fast queries

---

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/seanm/second-brain.git
cd second-brain

# Setup development environment
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/

# Lint
ruff check src/
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [Click](https://click.palletsprojects.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Beads](https://github.com/cased/beads) - Dependency tracking and epic management

---

## 🤝 Contributing

Contributions welcome! Please open an issue to discuss major changes.

---

<div align="center">

**Built for developers who want to track their work, organize their knowledge, and leverage AI agents for productivity.**

[Get Started](docs/quickstart.md) • [Documentation](docs/) • [Report Bug](https://github.com/seanm/second-brain/issues) • [Request Feature](https://github.com/seanm/second-brain/issues)

</div>
