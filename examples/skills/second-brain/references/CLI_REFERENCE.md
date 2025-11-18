# CLI Reference

Complete command reference for Second Brain (`sb`) CLI tool.

## Contents

- [Quick Reference](#quick-reference)
- [Global Commands](#global-commands)
  - [sb init](#sb-init) - Initialize Second Brain
- [Work Log Commands](#work-log-commands)
  - [sb log add](#sb-log-add) - Log work
  - [sb log show](#sb-log-show) - View logs
- [Task Commands](#task-commands)
  - [sb task add](#sb-task-add) - Create task
  - [sb task update](#sb-task-update) - Update task
  - [sb task list](#sb-task-list) - List tasks
  - [sb task show](#sb-task-show) - Show task details
- [Note Commands](#note-commands)
  - [sb note create](#sb-note-create) - Create note
  - [sb note add](#sb-note-add) - Append to note
  - [sb note list](#sb-note-list) - List notes
  - [sb note search](#sb-note-search) - Search notes
  - [sb note show](#sb-note-show) - Show note
- [Project Commands](#project-commands)
  - [sb project create](#sb-project-create) - Create project
  - [sb project list](#sb-project-list) - List projects
  - [sb project status](#sb-project-status) - Project status
- [Issue Commands](#issue-commands) (Beads Integration)
  - [sb issue create-with-project](#sb-issue-create-with-project) - Epic + Project
  - [sb issue create](#sb-issue-create) - Create issue
  - [sb issue ready](#sb-issue-ready) - Find ready work
  - [sb issue list](#sb-issue-list) - List issues
  - [sb issue show](#sb-issue-show) - Show issue
- [Report Commands](#report-commands)
  - [sb report work](#sb-report-work) - Generate report
- [Common Workflows](#common-workflows)

## Quick Reference

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `sb log add` | Log work | `--task-id`, `--time`, `--date` |
| `sb log show` | View logs | `--days`, `--project` |
| `sb task add` | Create task | `--project`, `--priority`, `--tags` |
| `sb task update` | Update task | `--status`, `--priority`, `--time` |
| `sb task list` | List tasks | `--status`, `--project`, `--priority` |
| `sb note create` | Create note | `--task-id`, `--project`, `--content`, `--tags` |
| `sb note search` | Search notes | (text query) |
| `sb project create` | Create project | `--description`, `--tags` |
| `sb project status` | Project status | (project slug) |
| `sb issue create-with-project` | Epic + Project | `--priority`, `--labels` |
| `sb issue ready` | Ready work | `--priority`, `--limit` |
| `sb report work` | Generate report | `--days`, `--project` |

## Global Commands

### sb init

Initialize Second Brain.

```bash
sb init --global              # Initialize in ~/.second-brain/ (RECOMMENDED)
sb init                       # Initialize in ./data/
```

**When to use:**
- First-time setup
- Setting up on a new machine

---

## Work Log Commands

### sb log add

Add an entry to your daily work log.

```bash
sb log add "Work description"
sb log add "Fixed bug" --task-id 42
sb log add "Code review" --time 30
sb log add "Feature implementation" --task-id 15 --time 120
sb log add "Emergency fix" --task-id 55 --time 90 --date 2025-01-15
```

**Options:**
- `TEXT` - Work description (required)
- `--task-id ID` - Link to task ID
- `--time MINUTES` - Time spent in minutes
- `--date YYYY-MM-DD` - Date (defaults to today)

**Examples:**
```bash
# Simple log
sb log add "Implemented OAuth2 flow"

# With task link
sb log add "Fixed login timeout bug" --task-id 42

# With time tracking
sb log add "Code review for PR #123" --time 45

# Full logging
sb log add "Deployed to staging" --task-id 55 --time 90 --date 2025-01-16
```

---

### sb log show

View work log entries.

```bash
sb log show                   # Last 7 days
sb log show --days 1          # Today only
sb log show --days 30         # Last 30 days
sb log show --project backend-api
```

**Options:**
- `--days N` - Number of days to show (default: 7)
- `--project SLUG` - Filter by project slug

**Examples:**
```bash
# Today's work
sb log show --days 1

# This week
sb log show --days 7

# This month
sb log show --days 30

# Project-specific
sb log show --project backend-api --days 14
```

---

## Task Commands

### sb task add

Create a new task.

```bash
sb task add "Task title"
sb task add "Implement feature" --project backend-api
sb task add "Fix bug" --priority high
sb task add "Write tests" --project api --priority medium --tags testing,backend
```

**Options:**
- `TITLE` - Task title (required)
- `--project SLUG` - Project slug
- `--description TEXT` - Task description
- `--priority LEVEL` - Priority: low, medium, high, urgent
- `--tags TAG1,TAG2` - Comma-separated tags

**Examples:**
```bash
# Simple task
sb task add "Implement rate limiting"

# With project
sb task add "Add OAuth support" --project backend-api

# With priority
sb task add "Fix critical bug" --priority urgent

# Full task
sb task add "Implement caching" \
  --project backend-api \
  --priority high \
  --description "Add Redis caching layer" \
  --tags backend,performance
```

---

### sb task update

Update an existing task.

```bash
sb task update 42 --status in_progress
sb task update 42 --priority high
sb task update 42 --status done --time 180
```

**Options:**
- `TASK_ID` - Task ID (required)
- `--status STATUS` - New status: todo, in_progress, done, blocked
- `--priority LEVEL` - New priority: low, medium, high, urgent
- `--time MINUTES` - Add time spent (minutes)

**Examples:**
```bash
# Start working on task
sb task update 42 --status in_progress

# Mark task done
sb task update 42 --status done

# Mark done with time
sb task update 42 --status done --time 180

# Change priority
sb task update 42 --priority urgent
```

---

### sb task list

List tasks with filters.

```bash
sb task list                          # All tasks
sb task list --status in_progress     # Only in-progress
sb task list --project backend-api    # Project-specific
sb task list --priority high          # High priority
sb task list --status in_progress --project api
```

**Options:**
- `--status STATUS` - Filter by status
- `--project SLUG` - Filter by project
- `--priority LEVEL` - Filter by priority
- `--tags TAG1,TAG2` - Filter by tags

**Examples:**
```bash
# Current work
sb task list --status in_progress

# High priority work
sb task list --priority high

# Project tasks
sb task list --project backend-api

# Completed tasks
sb task list --status done
```

---

### sb task show

Show detailed task information.

```bash
sb task show 42
```

**Shows:**
- Task details (title, status, priority)
- Time tracking
- Linked notes
- Work logs
- Linked Beads issue (if any)

---

## Note Commands

### sb note create

Create a new markdown note.

```bash
sb note create "Note title" --task-id 42
sb note create "Research" --project backend-api
sb note create "Design Doc" --project api --content "## Architecture\n..."
sb note create "Meeting Notes" --tags meeting,planning
```

**Options:**
- `TITLE` - Note title (required)
- `--task-id ID` - Link to task
- `--project SLUG` - Link to project
- `--content TEXT` - Note content (markdown)
- `--tags TAG1,TAG2` - Comma-separated tags

**Examples:**
```bash
# Task note
sb note create "Implementation Notes" \
  --task-id 42 \
  --content "Using Redis cluster with 3 nodes"

# Project note
sb note create "API Design" \
  --project backend-api \
  --content "## Endpoints\n- POST /auth/login\n- POST /auth/logout"

# Research note
sb note create "Caching Research" \
  --tags research,performance \
  --content "## Redis vs Memcached\n..."
```

---

### sb note add

Append content to an existing note.

```bash
sb note add 156 "Additional content to append"
sb note add 156 "## Update\n\nNew findings..."
```

**Options:**
- `NOTE_ID` - Note ID (required)
- `CONTENT` - Content to append (required)

---

### sb note list

List notes with filters.

```bash
sb note list                      # All notes
sb note list --task-id 42         # Task notes
sb note list --project backend-api # Project notes
sb note list --tags research      # Tagged notes
```

**Options:**
- `--task-id ID` - Filter by task
- `--project SLUG` - Filter by project
- `--tags TAG1,TAG2` - Filter by tags

---

### sb note search

Search notes by keyword.

```bash
sb note search "authentication"
sb note search "Redis caching"
```

**Options:**
- `QUERY` - Search query (required)

---

### sb note show

Show full note content.

```bash
sb note show 156
```

**Shows:**
- Note title and metadata
- Full markdown content
- Linked task/project
- Tags
- Creation/modification dates

---

## Project Commands

### sb project create

Create a new project.

```bash
sb project create "Project Name"
sb project create "Backend API" --description "Core services"
sb project create "Mobile App" --tags mobile,frontend
```

**Options:**
- `NAME` - Project name (required)
- `--description TEXT` - Project description
- `--tags TAG1,TAG2` - Comma-separated tags
- `--jira-project KEY` - Jira project key (optional)

**Examples:**
```bash
# Simple project
sb project create "Backend API"

# With description
sb project create "Mobile App" \
  --description "iOS and Android applications"

# With tags
sb project create "ML Pipeline" \
  --tags ml,data,python \
  --description "Machine learning data pipeline"
```

---

### sb project list

List all projects.

```bash
sb project list                   # All projects
sb project list --status active   # Only active
sb project list --tags backend    # Tagged projects
```

**Options:**
- `--status STATUS` - Filter by status (active, completed, archived)
- `--tags TAG1,TAG2` - Filter by tags

---

### sb project status

Show detailed project status.

```bash
sb project status backend-api
sb project status mobile-app
```

**Shows:**
- Project details
- Task breakdown by status
- Time tracking
- Recent activity
- Linked issues (if any)

---

## Issue Commands (Beads Integration)

### sb issue create-with-project

**RECOMMENDED:** Create epic and project together.

```bash
sb issue create-with-project "Feature Name"
sb issue create-with-project "Mobile App" --priority 4
sb issue create-with-project "API v2" \
  --description "Migrate to v2" \
  --priority 4 \
  --labels backend,api
```

**Options:**
- `TITLE` - Title for both (required)
- `--description TEXT` - Description for both
- `--priority N` - Priority 0-4 (0=lowest, 4=highest)
- `--labels LABEL1,LABEL2` - Comma-separated labels
- `--jira-project KEY` - Jira key for project

**Creates:**
- Epic in Beads (for dependency tracking)
- Project in Second Brain (for notes/time)
- Links them together

---

### sb issue create

Create a Beads issue with optional task link.

```bash
sb issue create "Issue title"
sb issue create "Fix bug" --type bug --priority 4
sb issue create "Feature" --epic epic-042 --with-task --project api
```

**Options:**
- `TITLE` - Issue title (required)
- `--description TEXT` - Description
- `--type TYPE` - Type: bug, feature, task, epic
- `--priority N` - Priority 0-4
- `--epic ID` - Parent epic ID
- `--with-task` - Create linked SB task
- `--project SLUG` - Project for linked task

---

### sb issue ready

Find issues ready to work on (no blockers).

```bash
sb issue ready                    # All ready work
sb issue ready --priority 4       # Critical only
sb issue ready --limit 5          # Limit results
```

**Options:**
- `--priority N` - Filter by priority
- `--limit N` - Max results

---

### sb issue list

List Beads issues.

```bash
sb issue list                     # All issues
sb issue list --status open       # Open only
sb issue list --type bug          # Bugs only
sb issue list --priority 4        # Priority 4 only
```

**Options:**
- `--status STATUS` - Filter by status
- `--type TYPE` - Filter by type
- `--priority N` - Filter by priority

---

### sb issue show

Show detailed issue information.

```bash
sb issue show epic-042
sb issue show issue-123
```

**Shows:**
- Issue details
- Dependencies and blockers
- Linked SB task (if any)
- Child issues (for epics)

---

## Report Commands

### sb report work

Generate comprehensive work report.

```bash
sb report work --days 7           # Weekly
sb report work --days 30          # Monthly
sb report work --days 90          # Quarterly
sb report work --project backend-api --days 30
```

**Options:**
- `--days N` - Days to include (required)
- `--project SLUG` - Project-specific report

**Shows:**
- Total time worked
- Tasks completed
- Projects worked on
- Work logs summary
- Breakdown by project

**Use for:**
- Weekly status updates
- Performance reviews
- Team reporting
- Project retrospectives

---

## Common Workflows

### Daily Workflow

**Morning:**
```bash
sb task list --status in_progress
sb log show --days 1
```

**During work:**
```bash
sb log add "Implemented feature X" --task-id 42 --time 120
sb task update 42 --status in_progress
```

**End of day:**
```bash
sb task update 42 --status done --time 180
sb log show --days 1
```

---

### Starting New Feature

```bash
# Create epic + project
sb issue create-with-project "User Auth" --priority 4 --labels backend

# Create issues
sb issue create "OAuth integration" --epic epic-042 --with-task --project user-auth
sb issue create "Password reset" --epic epic-042 --with-task --project user-auth

# Add notes
sb note create "Auth Architecture" --project user-auth
```

---

### Weekly Review

```bash
# Generate report
sb report work --days 7

# Review completed tasks
sb task list --status done

# Check in-progress
sb task list --status in_progress

# Find ready work
sb issue ready
```

---

## Environment Variables

```bash
# Required
export SECOND_BRAIN_DIR="$HOME/.second-brain"

# Optional (Jira integration)
export JIRA_SERVER="https://company.atlassian.net"
export JIRA_EMAIL="you@company.com"
export JIRA_API_TOKEN="your-token"
```

---

## Tips

1. **Always link work logs to tasks** when possible for better time tracking
2. **Use descriptive work log entries** - future you will thank you
3. **Set priorities on tasks** to help focus on what matters
4. **Use projects to organize** related tasks
5. **Create notes for design decisions** and important context
6. **Generate reports regularly** for performance reviews
7. **Use `sb issue create-with-project`** when starting complex features
8. **Track time on everything** significant (>30 minutes)
