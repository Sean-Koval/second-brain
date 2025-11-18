# Slash Commands for Claude Code

Slash commands provide quick workflows for using Second Brain directly from Claude Code. They teach the AI agent how to construct and execute `sb` CLI commands or use MCP tools directly.

---

## What Are Slash Commands?

Slash commands are shortcuts that trigger specific workflows in Claude Code:

```
You type: /sb-log
Agent asks: "What did you work on?"
You say: "Fixed authentication bug"
Agent executes: sb log add "Fixed authentication bug"
```

The slash commands work by providing prompts to the AI agent that guide it through constructing the right CLI commands or calling MCP tools.

---

## Two Modes of Operation

All slash commands support **TWO modes**:

### Conversational Mode (default)
```
You: /sb-log
Agent: "What did you work on?"
You: "Fixed bug"
Agent: "Task ID?"
You: "42"
Agent: [executes command]
```

### Quick Mode (with arguments)
```
You: /sb-log "Fixed bug" --task-id 42 --time 90
Agent: [parses args and executes immediately]
```

See `/sb-quick-mode` for complete quick mode syntax reference.

---

## Installation

### Step 1: Copy Commands to Your Project

```bash
# Navigate to your project
cd ~/your-project

# Create commands directory
mkdir -p .claude/commands

# Copy ALL slash commands (26 total)
cp ~/.local/share/uv/tools/second-brain/examples/commands/*.md .claude/commands/

# Or if you cloned the repo:
cp ~/second-brain/examples/commands/*.md .claude/commands/
```

### Step 2: Restart Claude Code

Close and reopen Claude Code to load the commands.

### Step 3: Use Slash Commands

Type `/sb-` to see all available Second Brain commands in autocomplete.

---

## Available Commands (27 Total)

### 🌟 Workflow Guides (7 commands)

Complete end-to-end workflows for common scenarios:

#### `/sb-daily-dev-workflow` ⭐
**Complete daily development routine**

Guides you through:
- Morning: Check ready work, plan day
- During work: Log work, add notes, track time
- Evening: Update statuses, create handoff notes
- Weekly: Generate summaries

Perfect for: Regular development work

---

#### `/sb-ml-research-workflow`
**ML research and experimentation workflow**

Specialized for data scientists and ML engineers:
- Literature review patterns
- Experiment tracking with results tables
- Model comparison
- Research organization

Perfect for: Research projects, model development

---

#### `/sb-feature-development`
**Complex feature development**

Full epic → issues → tasks → notes workflow:
- Planning with epics
- Breaking down into issues
- Implementation notes
- API documentation
- Deployment checklists

Perfect for: Multi-component features, team collaboration

---

#### `/sb-bug-investigation`
**Bug investigation and postmortem**

Thorough bug tracking workflow:
- Investigation notes
- Solution planning
- Implementation tracking
- Deployment runbooks
- Postmortem creation

Perfect for: Complex bugs, production incidents

---

#### `/sb-weekly-summary`
**Weekly summary and reporting**

Comprehensive weekly review:
- Gathering metrics
- Analyzing completions
- Reviewing notes
- Planning next week

Perfect for: Friday wrap-ups, team updates

---

#### `/sb-quick-tasks`
**Small task management**

Fast execution patterns:
- Quick task creation
- Batch processing
- When to promote to issues

Perfect for: Quick wins, small fixes (< 2 hours)

---

#### `/sb-epic-project-create` ⭐
**Create epic + project together for new initiatives**

The recommended way to start complex work:
- Creates Beads epic for dependency tracking
- Creates Second Brain project for notes/time tracking
- Links them together automatically
- Same title and tags for both

Quick mode:
```
/sb-epic-project-create "New Feature" --priority 3 --labels feature,backend
```

Perfect for: Starting new features, complex initiatives requiring both coordination and detailed notes

---

### 🔍 Query & Visualization Commands (7 commands)

Find, explore, and visualize your Second Brain content:

#### `/sb-search-all`
**Global search across everything**

Search notes, tasks, work logs, transcripts, issues, projects.

Quick mode:
```
/sb-search-all "caching"
/sb-search-all "API" --type note
/sb-search-all "performance" --project backend-api
```

Perfect for: Finding information, discovering related content

---

#### `/sb-note-search`
**Search and filter notes**

Find notes by keyword, tags, project, or task.

Quick mode:
```
/sb-note-search "Redis"
/sb-note-search --tags research,important
/sb-note-search --task-id 42
```

Perfect for: Finding specific notes, filtering by context

---

#### `/sb-project-view`
**Comprehensive project visualization**

See everything related to a project: tasks, notes, work logs, progress.

Quick mode:
```
/sb-project-view backend-api
```

Shows:
- Task breakdown by status/priority
- Recent work activity
- Project notes
- Linked issues
- Project health metrics

Perfect for: Standup prep, project reviews, onboarding

---

#### `/sb-task-view`
**Complete task context**

View everything about a task: notes, work logs, linked issue, timeline.

Quick mode:
```
/sb-task-view 42
```

Shows:
- Task details and status
- All linked notes
- Work log timeline
- Linked Beads issue
- Next steps
- Completion criteria

Perfect for: Before starting work, creating handoffs

---

#### `/sb-issue-view`
**Issue/Epic visualization**

View Beads issues with Second Brain context: tasks, notes, time tracking.

Quick mode:
```
/sb-issue-view BACK-123
/sb-issue-view epic-042
```

Shows:
- Issue/epic details
- Dependencies and blockers
- Linked Second Brain tasks
- Work progress
- Child issues (for epics)

Perfect for: Sprint planning, dependency management

---

#### `/sb-explore-tags`
**Discover content by tags**

Explore all content tagged with specific tags, see tag usage statistics.

Quick mode:
```
/sb-explore-tags performance
/sb-explore-tags research,ml,experiments
/sb-explore-tags --show-all
```

Shows:
- All content with tag(s)
- Related tags
- Usage statistics
- Content breakdown

Perfect for: Finding themes, topic-based reviews

---

#### `/sb-transcript-view`
**Meeting transcript viewer**

View transcripts with action items, linked tasks, related content.

Quick mode:
```
/sb-transcript-view 45
/sb-transcript-list --tags meeting,planning
```

Shows:
- Full transcript
- Summary and action items
- Linked tasks/projects
- Action item tracking

Perfect for: Reviewing decisions, tracking actions

---

### 📝 Basic Commands (12 commands)

Core operations for daily use:

#### `/sb-log`
**Add work log entry**

Quick mode: `/sb-log "Fixed bug" --task-id 42 --time 90`

Conversational mode:
```
You: /sb-log
Agent: "What did you work on?"
You: "Fixed authentication bug"
Agent: "Any task ID? Time spent?"
You: "Task 15, 2 hours"
Agent: Executes command
```

---

#### `/sb-task-create`
**Create a new task**

Quick mode: `/sb-task-create "Implement feature" --project backend --priority high`

Conversational mode guides you through title, project, priority, description.

---

#### `/sb-task-update`
**Update task status, priority, or time**

Quick mode: `/sb-task-update 42 --status done --time 120`

Conversational mode shows tasks and asks what to update.

---

#### `/sb-find-task`
**Search tasks with filters**

Filter by project, status, or priority.

---

#### `/sb-project-create`
**Create a new project**

Guides through project creation with description, tags.

---

#### `/sb-project-status`
**Get detailed project status**

Shows task breakdown, active work, blockers.

---

#### `/sb-projects-overview`
**Overview of all projects**

Birds-eye view of all active and completed projects.

---

#### `/sb-current-work`
**Show what you're currently working on**

Runs multiple commands for quick status check:
- Active tasks
- Today's logs
- High priority todos

---

#### `/sb-daily-summary`
**End-of-day summary**

Review the day: work logged, tasks completed, in-progress items.

---

#### `/sb-weekly-review`
**Comprehensive weekly review**

Structured weekly review with accomplishments, blockers, planning.

---

#### `/sb-report`
**Generate comprehensive work report**

Create detailed report for any time period.

---

#### `/sb-context-management`
**Context management strategies**

Guide for managing context when switching between projects/tasks.

Explains:
- Explicit ID-based system
- Shell functions for context
- Quick capture patterns
- Finding your context

---

### 📚 Reference Commands (1 command)

#### `/sb-quick-mode`
**Quick mode syntax guide**

Complete reference for using quick mode with all commands.

Shows syntax for:
- Work logging: `/sb-log "text" --task-id ID --time MIN`
- Task creation: `/sb-task-create "title" --project SLUG --priority LEVEL`
- Note creation: `/sb-note-create "title" --task-id ID --content "text"`
- Searching: `/sb-search-all "query" --type note --project SLUG`

And more...

---

## Usage Patterns

### Morning Routine

```
/sb-current-work          # See what's active
/sb-task-update           # Start working on task
```

### During Work

```
# Conversational
/sb-log                   # Log work as you go

# Quick mode
/sb-log "Fixed bug" --task-id 42 --time 60
```

### End of Day

```
/sb-daily-summary         # Review the day
/sb-task-update           # Mark tasks done
```

### Weekly

```
/sb-weekly-summary        # Comprehensive review
/sb-report                # Generate report
```

### Discovery & Search

```
/sb-search-all "topic"    # Find everything
/sb-explore-tags research # Explore by tag
/sb-project-view PROJECT  # See project status
/sb-task-view TASK_ID     # See task context
```

---

## Quick Mode Examples

### Work Logging

```
# Basic log
/sb-log "Fixed authentication bug"

# With task
/sb-log "Code review" --task-id 15

# With time
/sb-log "Implemented feature" --task-id 42 --time 120

# Full logging
/sb-log "Emergency fix" --task-id 55 --time 90 --date 2025-01-15
```

### Task Management

```
# Create task
/sb-task-create "Rate limiting" --project api --priority high

# Update task
/sb-task-update 42 --status done --time 180

# Search tasks
/sb-find-task --project backend --status in_progress
```

### Searching & Visualization

```
# Global search
/sb-search-all "caching strategy"
/sb-search-all "performance" --type note
/sb-search-all "bug" --date-range last-week

# View entities
/sb-project-view backend-api
/sb-task-view 42
/sb-issue-view BACK-123

# Explore tags
/sb-explore-tags performance
/sb-explore-tags --show-all
```

---

## Customizing Commands

Commands are just markdown files! Edit them to fit your workflow:

```bash
# Edit a command
vim .claude/commands/sb-log.md

# Add custom questions
# Change the command syntax
# Modify the output format
```

### Example: Create Custom Command

```bash
cat > .claude/commands/sb-standup.md <<'EOF'
Use Second Brain to prepare for daily standup.

Show:
1. What I did yesterday (yesterday's work log)
2. What I'm doing today (in-progress tasks)
3. Any blockers (blocked tasks)

Format as a standup update.
EOF
```

---

## How They Work

Slash commands are prompts that guide the AI agent:

**The slash command file** (`sb-log.md`):
```markdown
Help the user add a work log entry using the Second Brain CLI.

This command supports TWO MODES:

## Quick Mode (with arguments)
/sb-log "text" --task-id ID --time MINUTES

## Conversational Mode (no arguments)
Ask the user:
1. What did they work on?
2. Link to a task? (optional)
3. Time spent? (optional)

Then construct and run the command.
```

**What the agent does:**
1. Reads the prompt from the .md file
2. Checks if arguments provided (quick mode) or asks questions (conversational)
3. Constructs the `sb` CLI command or calls MCP tool
4. Executes it for you
5. Shows you the result

---

## MCP vs CLI Mode

Slash commands work with **both** approaches:

### CLI Mode (via Bash)
Agent runs: `sb log add "text" --task-id 42`

### MCP Mode (direct)
Agent calls: `create_work_log_entry(entry_text="text", task_id=42)`

**Both work!** The agent chooses based on what's available.

---

## Troubleshooting

### Slash Commands Not Showing

**Check:**
1. Files are in `.claude/commands/` directory
2. Files have `.md` extension
3. You restarted Claude Code

**Test:**
```bash
ls .claude/commands/
# Should show 26 sb-*.md files
```

### Commands Not Working

**Check:**
1. Second Brain is installed: `sb --version`
2. Environment variable is set: `echo $SECOND_BRAIN_DIR`
3. You can run commands manually: `sb log show`

### Slow Performance

This is normal! The agent needs to:
1. Read the command prompt
2. Ask clarifying questions (if conversational)
3. Execute the CLI command or call MCP tool

**Speed up:**
- Use quick mode: `/sb-log "text" --task-id 42 --time 90`
- Provide all info upfront
- Use MCP server instead of CLI (faster)

---

## Command Quick Reference

| Command | Purpose | Quick Mode Example |
|---------|---------|-------------------|
| **Workflow Guides** |||
| `/sb-daily-dev-workflow` | Complete daily routine | N/A (interactive guide) |
| `/sb-ml-research-workflow` | ML research patterns | N/A (interactive guide) |
| `/sb-feature-development` | Feature development | N/A (interactive guide) |
| `/sb-bug-investigation` | Bug tracking | N/A (interactive guide) |
| `/sb-weekly-summary` | Weekly reporting | N/A (generates summary) |
| `/sb-quick-tasks` | Small task guide | N/A (interactive guide) |
| `/sb-epic-project-create` | Create epic + project | `/sb-epic-project-create "Title" --priority 3 --labels tag1,tag2` |
| **Query & Visualization** |||
| `/sb-search-all` | Global search | `/sb-search-all "keyword"` |
| `/sb-note-search` | Search notes | `/sb-note-search --tags research` |
| `/sb-project-view` | Project status | `/sb-project-view backend-api` |
| `/sb-task-view` | Task context | `/sb-task-view 42` |
| `/sb-issue-view` | Issue details | `/sb-issue-view BACK-123` |
| `/sb-explore-tags` | Tag exploration | `/sb-explore-tags performance` |
| `/sb-transcript-view` | View transcript | `/sb-transcript-view 45` |
| **Basic Operations** |||
| `/sb-log` | Log work | `/sb-log "text" --task-id 42 --time 90` |
| `/sb-task-create` | Create task | `/sb-task-create "title" --project api --priority high` |
| `/sb-task-update` | Update task | `/sb-task-update 42 --status done` |
| `/sb-find-task` | Search tasks | `/sb-find-task --status in_progress` |
| `/sb-project-create` | Create project | N/A (conversational) |
| `/sb-project-status` | Project details | `/sb-project-status backend-api` |
| `/sb-projects-overview` | All projects | N/A (shows overview) |
| `/sb-current-work` | Current status | N/A (shows status) |
| `/sb-daily-summary` | Daily wrap-up | N/A (generates summary) |
| `/sb-weekly-review` | Weekly review | N/A (generates review) |
| `/sb-report` | Generate report | N/A (conversational) |
| **Reference** |||
| `/sb-quick-mode` | Quick mode syntax | N/A (reference guide) |
| `/sb-context-management` | Context strategies | N/A (reference guide) |

---

## Next Steps

1. ✅ Copy ALL commands: `cp examples/commands/*.md .claude/commands/`
2. ✅ Restart Claude Code
3. ✅ Try conversational mode: `/sb-current-work`
4. ✅ Try quick mode: `/sb-log "Fixed bug" --task-id 42 --time 60`
5. ✅ Explore workflows: `/sb-daily-dev-workflow`
6. ✅ Customize commands to fit your workflow

**Related Documentation:**
- [Installation Guide](installation.md) - Setup instructions
- [CLI Reference](cli-reference.md) - All CLI commands
- [MCP Server](mcp-server.md) - Direct MCP integration
- [Workflows](workflows.md) - Usage patterns
- [Notes Guide](notes.md) - Note-taking features
- [Task-Issue Integration](task-issue-integration.md) - Linking tasks and issues

---

**Happy tracking! 🧠**

With 26 slash commands covering workflows, queries, and basic operations, Second Brain integrates seamlessly into your daily workflow!
