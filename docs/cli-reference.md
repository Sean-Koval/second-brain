# Command Reference

Complete reference for all Second Brain CLI commands.

> **Note:** Jira integration is entirely optional. All core features work offline without any external services.

## Table of Contents

- [Global Options](#global-options)
- [Initialization](#initialization)
- [Work Log Commands](#work-log-commands)
- [Project Commands](#project-commands)
- [Task Commands](#task-commands)
- [Note Commands](#note-commands)
- [Report Commands](#report-commands)
- [Issue Commands](#issue-commands)
- [Jira Commands](#jira-commands-optional)

---

## Global Options

```bash
sb --version              # Show version
sb --help                # Show help for all commands
sb COMMAND --help        # Show help for specific command
```

### Environment Variables

```bash
# Set data directory (default: ./data)
export SECOND_BRAIN_DATA_DIR=/path/to/your/data

# Jira integration (optional - only needed if using Jira sync)
export JIRA_SERVER="https://company.atlassian.net"
export JIRA_EMAIL="you@company.com"
export JIRA_API_TOKEN="your-token"
```

---

## Initialization

### `sb init`

Initialize a new Second Brain workspace.

**Syntax:**
```bash
sb init [OPTIONS]
```

**Options:**
- `--data-dir PATH` - Directory to create (default: `data`)

**Examples:**
```bash
# Initialize in default location
sb init

# Initialize in custom location
sb init --data-dir ~/my-second-brain

# Then set it for future use
export SECOND_BRAIN_DATA_DIR=~/my-second-brain
```

**What it creates:**
```
data/
├── projects/              # Project markdown files
├── work_logs/             # Daily work logs
├── transcripts/
│   ├── raw/              # Raw transcript text files
│   └── processed/        # Processed transcript markdown
└── index.db              # SQLite database
```

---

## Work Log Commands

Work logs are daily journals of your work activities. Each day gets its own markdown file.

### `sb log add`

Add an entry to today's work log (or a specific date).

**Syntax:**
```bash
sb log add TEXT [OPTIONS]
```

**Arguments:**
- `TEXT` - The work log entry text (required)

**Options:**
- `--task-id INTEGER` - Link this entry to a task
- `--time INTEGER` - Time spent in minutes
- `--date YYYY-MM-DD` - Specific date (default: today)

**Examples:**
```bash
# Simple entry
sb log add "Fixed bug in authentication service"

# With time tracking
sb log add "Code review session" --time 45

# Link to a task and track time
sb log add "Implemented user profile API" --task-id 12 --time 120

# Add entry for a past date
sb log add "Emergency fix in production" --date 2025-01-15 --time 60
```

**Output:**
```
✓ Work log entry added for 2025-01-17
```

**File created:** `data/work_logs/2025-01-17.md`

---

### `sb log show`

Display recent work logs.

**Syntax:**
```bash
sb log show [OPTIONS]
```

**Options:**
- `--days INTEGER` - Number of days to show (default: 7)

**Examples:**
```bash
# Show last 7 days
sb log show

# Show last 30 days
sb log show --days 30

# Show just today
sb log show --days 1
```

**Output:**
```
2025-01-17
  09:30: Fixed bug in authentication service
  11:00 [Implement user profile API]: Implemented user profile API
  14:30: Code review session
```

---

## Project Commands

Projects are the top-level organizational unit. Each project gets its own markdown file.

### `sb project create`

Create a new project.

**Syntax:**
```bash
sb project create NAME [OPTIONS]
```

**Arguments:**
- `NAME` - Project name (required)

**Options:**
- `-d, --description TEXT` - Project description
- `--jira TEXT` - Jira project key (optional, for integration)
- `--tags TEXT` - Comma-separated tags

**Examples:**
```bash
# Simple project
sb project create "Mobile App Redesign"

# With description
sb project create "API v2 Migration" \
  --description "Migrate all services to new API architecture"

# With tags for organization
sb project create "Documentation Update" \
  --tags "docs,low-priority,maintenance"

# With Jira integration (optional)
sb project create "Backend Refactor" \
  --description "Refactor backend services for better performance" \
  --jira BACKEND \
  --tags "backend,refactoring"
```

**Output:**
```
✓ Project created: Mobile App Redesign
  Slug: mobile-app-redesign
  File: data/projects/mobile-app-redesign.md
```

**File created:** `data/projects/mobile-app-redesign.md`

---

### `sb project list`

List all projects.

**Syntax:**
```bash
sb project list [OPTIONS]
```

**Options:**
- `--status TEXT` - Filter by status (active, completed, archived)

**Examples:**
```bash
# List all projects
sb project list

# List only active projects
sb project list --status active

# List completed projects
sb project list --status completed
```

**Output:**
```
                Projects
┏━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━┓
┃ ID ┃ Name               ┃ Status ┃ Tasks ┃ Jira ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━┩
│ 1  │ Mobile App Redesign│ active │ 3/8   │ -    │
│ 2  │ API v2 Migration   │ active │ 5/12  │ -    │
└────┴────────────────────┴────────┴───────┴──────┘
```

---

### `sb project status`

Show detailed status for a specific project.

**Syntax:**
```bash
sb project status SLUG
```

**Arguments:**
- `SLUG` - Project slug (auto-generated from name)

**Examples:**
```bash
sb project status mobile-app-redesign
```

**Output:**
```
Mobile App Redesign
Status: active
Description: Complete redesign of mobile UI

Total tasks: 8
  todo: 3
  in_progress: 2
  done: 3

Active tasks:
  🔄 #4: Implement new navigation system
  ⬜ #5: Design user profile screen
  ⬜ #7: Update color scheme
```

**Finding slugs:**
- Slugs are auto-generated: `"My Project"` → `my-project`
- Use `sb project list` to see all project slugs

---

## Task Commands

Tasks represent individual work items. They can be standalone or linked to projects.

### `sb task add`

Create a new task.

**Syntax:**
```bash
sb task add TITLE [OPTIONS]
```

**Arguments:**
- `TITLE` - Task title (required)

**Options:**
- `-p, --project TEXT` - Project slug to link to
- `-d, --description TEXT` - Task description
- `--priority CHOICE` - Priority: low, medium, high, urgent

**Examples:**
```bash
# Simple task
sb task add "Write unit tests for auth module"

# Task with project and priority
sb task add "Implement caching layer" \
  --project api-v2-migration \
  --priority high

# Detailed task
sb task add "Fix memory leak in worker process" \
  --description "Memory usage grows unbounded in long-running workers" \
  --priority urgent \
  --project backend-refactor
```

**Output:**
```
✓ Task created: #12 Implement caching layer
  Project: API v2 Migration
  Priority: high
  Status: todo
```

---

### `sb task update`

Update an existing task.

**Syntax:**
```bash
sb task update TASK_ID [OPTIONS]
```

**Arguments:**
- `TASK_ID` - Task ID number (required)

**Options:**
- `--status CHOICE` - Status: todo, in_progress, done, blocked
- `--priority CHOICE` - Priority: low, medium, high, urgent
- `--time INTEGER` - Add time spent in minutes (cumulative)

**Examples:**
```bash
# Start working on a task
sb task update 12 --status in_progress

# Add time tracking
sb task update 12 --time 45

# Mark as done
sb task update 12 --status done

# Mark as blocked
sb task update 8 --status blocked

# Change priority
sb task update 5 --priority urgent

# Multiple updates at once
sb task update 12 --status done --time 30
```

**Output:**
```
✓ Task #12 updated successfully!
Title: Implement caching layer
Status: done
Priority: high
Total time spent: 2h 15m
```

---

### `sb task list`

List tasks with optional filters.

**Syntax:**
```bash
sb task list [OPTIONS]
```

**Options:**
- `-p, --project TEXT` - Filter by project slug
- `--status TEXT` - Filter by status
- `--priority TEXT` - Filter by priority

**Examples:**
```bash
# List all tasks
sb task list

# List tasks for a specific project
sb task list --project mobile-app-redesign

# List all in-progress tasks
sb task list --status in_progress

# List high-priority tasks
sb task list --priority high

# Combine filters
sb task list --project api-v2-migration --status todo --priority high
```

**Output:**
```
                        Tasks
┏━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ ID ┃ Status        ┃ Title                ┃ Pri    ┃ Project        ┃
┡━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ 4  │ 🔄 in_progress│ Implement caching... │ high   │ API v2 Migr... │
│ 5  │ ⬜ todo       │ Write unit tests     │ medium │ API v2 Migr... │
│ 7  │ 🚫 blocked    │ Database migration   │ urgent │ API v2 Migr... │
└────┴───────────────┴──────────────────────┴────────┴────────────────┘
```

---

## Note Commands

Notes are markdown documents that can be linked to projects or tasks for detailed documentation.

### `sb note create`

Create a new note with optional project/task linkage.

**Syntax:**
```bash
sb note create TITLE [OPTIONS]
```

**Arguments:**
- `TITLE` - Note title (required)

**Options:**
- `-c, --content TEXT` - Note content (markdown)
- `-p, --project TEXT` - Project slug to link to
- `-t, --task-id INTEGER` - Task ID to link to
- `--tags TEXT` - Comma-separated tags

**Examples:**
```bash
# Simple note
sb note create "Meeting Notes - Q1 Planning"

# Note with content
sb note create "API Design Decisions" \
  --content "## Overview\n\nWe decided to use REST..." \
  --project backend-api

# Task-specific note
sb note create "Implementation Notes" \
  --task-id 42 \
  --content "Using Redis cluster with 3 nodes" \
  --tags architecture,caching

# Research note with tags
sb note create "ML Model Comparison" \
  --tags research,ml,experiments \
  --content "## BERT vs RoBERTa\n\nResults..."
```

**Output:**
```
✓ Note created: #156 API Design Decisions
  Project: backend-api
  File: notes/20250117_api-design-decisions.md
```

---

### `sb note add`

Append content to an existing note.

**Syntax:**
```bash
sb note add NOTE_ID CONTENT
```

**Arguments:**
- `NOTE_ID` - Note ID number (required)
- `CONTENT` - Content to append (required)

**Examples:**
```bash
# Append to note
sb note add 156 "## Update\n\nAdded rate limiting endpoint"

# Add section
sb note add 201 "## New Findings\n\nModel accuracy improved by 10%"
```

---

### `sb note list`

List notes with optional filtering.

**Syntax:**
```bash
sb note list [OPTIONS]
```

**Options:**
- `-p, --project TEXT` - Filter by project slug
- `-t, --task-id INTEGER` - Filter by task ID
- `--tags TEXT` - Filter by tags (comma-separated)

**Examples:**
```bash
# List all notes
sb note list

# Project notes
sb note list --project backend-api

# Task notes
sb note list --task-id 42

# Tagged notes
sb note list --tags research,ml

# Combine filters
sb note list --project backend-api --tags architecture
```

**Output:**
```
                           Notes
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ ID  ┃ Title                   ┃ Project    ┃ Tags          ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ 156 │ API Design Decisions    │ backend... │ architecture  │
│ 201 │ ML Model Comparison     │            │ research, ml  │
│ 189 │ Redis Caching Strategy  │ backend... │ caching       │
└─────┴─────────────────────────┴────────────┴───────────────┘
```

---

### `sb note search`

Search notes by keyword in title or content.

**Syntax:**
```bash
sb note search QUERY
```

**Arguments:**
- `QUERY` - Search query (required)

**Examples:**
```bash
# Search notes
sb note search "Redis"

# Search for phrase
sb note search "caching strategy"
```

**Output:**
```
Found 3 notes matching "Redis":

#156: API Design Decisions
  Project: backend-api
  Match: "...decided to use Redis for caching..."

#189: Redis Caching Strategy
  Tags: caching, redis
  Match: "Redis cluster with 3 nodes..."

#201: Performance Benchmarks
  Task: #42
  Match: "...Redis improved response time by 90%..."
```

---

### `sb note show`

Display full content of a note.

**Syntax:**
```bash
sb note show NOTE_ID
```

**Arguments:**
- `NOTE_ID` - Note ID number (required)

**Examples:**
```bash
# Show note
sb note show 156
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Note #156: API Design Decisions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: backend-api
Created: 2025-01-17
Tags: architecture, design

## Overview

We decided to use REST API with OpenAPI specification...

[Full markdown content displayed]
```

---

## Report Commands

Generate summaries and analytics of your work.

### `sb report work`

Generate a work report for a date range.

**Syntax:**
```bash
sb report work [OPTIONS]
```

**Options:**
- `--days INTEGER` - Number of days to include (default: 7)
- `-p, --project TEXT` - Filter by project slug

**Examples:**
```bash
# Report for last 7 days
sb report work

# Report for last 30 days
sb report work --days 30

# Report for specific project
sb report work --days 14 --project mobile-app-redesign

# Full quarter report
sb report work --days 90
```

**Output:**
```
Work Report
Period: 2025-01-10 to 2025-01-17

Work days logged: 6
Tasks completed: 8

Completed Tasks:
  ✅ Implement caching layer [API v2 Migration]
  ✅ Write unit tests [API v2 Migration]
  ✅ Design user profile screen [Mobile App Redesign]

Daily Work Logs:
### 2025-01-15
- 09:30: Daily standup
- 10:00 **[Implement caching layer]** (120m): Built Redis caching layer
- 14:30 **[Write unit tests]** (45m): Added tests for auth module

### 2025-01-16
- 09:45: Code review for PR #234
- 11:00 **[Design user profile screen]** (90m): Completed UI mockups
```

**Use cases:**
- Weekly status updates
- Performance reviews
- Promotion documentation
- Time tracking audits
- Project retrospectives

---

## Issue Commands

Issue commands integrate with Beads for epic and dependency tracking. See [Task-Issue Integration](task-issue-integration.md) for detailed guide.

### `sb issue create-with-project` ⭐

**RECOMMENDED**: Create an epic and linked Second Brain project together in one command.

This is the ideal way to start a new feature or complex initiative. It creates:
- A Beads epic for dependency tracking and high-level coordination
- A Second Brain project for day-to-day notes, tasks, and time tracking
- Links them together with the same title and tags

**Syntax:**
```bash
sb issue create-with-project TITLE [OPTIONS]
```

**Arguments:**
- `TITLE` - Title for both epic and project (required)

**Options:**
- `-d, --description TEXT` - Description for both epic and project
- `-p, --priority INTEGER` - Epic priority 0-4 (0=lowest, 4=highest, default: 2)
- `-l, --labels TEXT` - Comma-separated labels/tags for both
- `-j, --jira-project TEXT` - Jira project key for the project (optional)

**Examples:**
```bash
# Simple usage
sb issue create-with-project "Mobile App Redesign"

# With full options
sb issue create-with-project "API v2 Migration" \
  --description "Migrate all endpoints to v2" \
  --priority 4 \
  --labels backend,migration,api \
  --jira-project APIV2

# Then create issues under the epic
sb issue create "Migrate auth endpoints" \
  --epic EPIC-ID \
  --with-task \
  --project api-v2-migration
```

**Output:**
```
✓ Epic + Project created successfully!

📋 Epic (Beads):
  ID: epic-042
  Title: API v2 Migration
  Priority: Highest (4)
  Status: open

📦 Project (Second Brain):
  ID: 15
  Name: API v2 Migration
  Slug: api-v2-migration
  Markdown: ~/.second-brain/data/projects/api-v2-migration.md

🔗 Integration:
  Epic ID: epic-042 ↔️ Project Slug: api-v2-migration

💡 Next Steps:
  1. Create issues under epic
  2. Create tasks in project
  3. Link issues to tasks
  4. Add notes and track work
```

---

### `sb issue create`

Create a new Beads issue with optional Second Brain task linkage.

**Syntax:**
```bash
sb issue create TITLE [OPTIONS]
```

**Arguments:**
- `TITLE` - Issue title (required)

**Options:**
- `-d, --description TEXT` - Issue description
- `--type CHOICE` - Issue type: task, bug, feature, epic
- `--priority INTEGER` - Priority (1-4, default: 2)
- `--epic ID` - Parent epic ID
- `--labels TEXT` - Comma-separated labels
- `--with-task` - Create linked Second Brain task
- `-p, --project TEXT` - Project slug for linked task (with --with-task)

**Examples:**
```bash
# Create issue
sb issue create "Implement API rate limiting"

# Create with task
sb issue create "Fix auth bug" \
  --type bug \
  --priority 4 \
  --with-task \
  --project backend-api

# Create under epic
sb issue create "Database migration" \
  --epic epic-042 \
  --type task
```

---

### `sb issue list`

List Beads issues with filtering.

**Syntax:**
```bash
sb issue list [OPTIONS]
```

**Options:**
- `--status TEXT` - Filter by status
- `--type TEXT` - Filter by type
- `--priority INTEGER` - Filter by priority
- `--limit INTEGER` - Max results (default: 50)

**Examples:**
```bash
# List all issues
sb issue list

# Open issues
sb issue list --status open

# High priority bugs
sb issue list --type bug --priority 4
```

---

### `sb issue ready`

Show issues ready to work on (no blockers).

**Syntax:**
```bash
sb issue ready [OPTIONS]
```

**Options:**
- `--limit INTEGER` - Max results (default: 10)
- `--priority INTEGER` - Filter by priority

**Examples:**
```bash
# Show ready work
sb issue ready

# High priority ready work
sb issue ready --priority 4 --limit 5
```

---

### `sb issue show`

Display detailed issue information.

**Syntax:**
```bash
sb issue show ISSUE_ID
```

**Arguments:**
- `ISSUE_ID` - Issue ID (required)

**Examples:**
```bash
# Show issue
sb issue show BACK-123
```

See [Epics & Dependencies Guide](epics-and-dependencies.md) for advanced usage.

---

## Jira Commands (Optional)

> **Note:** Jira integration is completely optional. These commands require Jira credentials to be configured.

### Prerequisites

Set up Jira credentials (one-time):

```bash
# Get API token from: Jira > Account Settings > Security > API Tokens
export JIRA_SERVER="https://your-company.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"

# Add to your shell profile for persistence
echo 'export JIRA_SERVER="https://your-company.atlassian.net"' >> ~/.bashrc
echo 'export JIRA_EMAIL="your-email@company.com"' >> ~/.bashrc
echo 'export JIRA_API_TOKEN="your-api-token"' >> ~/.bashrc
```

### `sb jira sync`

Sync Jira issues to local tasks.

**Syntax:**
```bash
sb jira sync [OPTIONS]
```

**Options:**
- `-p, --project TEXT` - Sync only this project (default: all projects with Jira keys)

**Examples:**
```bash
# Sync all projects that have Jira integration
sb jira sync

# Sync specific project only
sb jira sync --project backend-refactor
```

**How it works:**
1. Finds all projects with a `jira_project_key` configured
2. Fetches issues from Jira for those projects
3. Creates new tasks for new issues
4. Updates existing tasks if they've changed
5. Maintains the link between local tasks and Jira tickets

**Output:**
```
Syncing Backend Refactor (BACKEND)...
  Synced 15 issues

Syncing API v2 Migration (API)...
  Synced 23 issues

✓ Total issues synced: 38
```

**Adding Jira integration to a project:**

1. **During creation:**
   ```bash
   sb project create "My Project" --jira PROJ
   ```

2. **After creation (edit markdown file):**
   ```bash
   # Edit data/projects/my-project.md
   # Add to frontmatter:
   # jira_project_key: PROJ
   ```

---

## Tips & Tricks

### 1. Quick Daily Workflow

```bash
# Morning - add standup note
sb log add "Daily standup - planning today's tasks"

# Start working
sb task update 5 --status in_progress

# Throughout the day
sb log add "Fixed production bug" --task-id 5 --time 45
sb log add "Code review" --time 30

# End of day
sb task update 5 --status done
sb log show --days 1
```

### 2. Finding Task IDs

```bash
# List tasks to find IDs
sb task list --status in_progress

# Or list for specific project
sb task list --project my-project
```

### 3. Time Tracking

```bash
# Time is cumulative
sb task update 10 --time 30  # Adds 30 minutes
sb task update 10 --time 45  # Adds 45 more (total: 75m = 1h 15m)
```

### 4. Organizing with Tags

```bash
# Use tags for better organization
sb project create "Q1 Goals" --tags "planning,2025,quarterly"
sb project create "Bug Fixes" --tags "maintenance,bugs"
sb project create "Learning" --tags "professional-development,learning"
```

### 5. Searching Your Work

```bash
# Since everything is in markdown, use standard tools
grep -r "authentication" data/
grep -r "bug fix" data/work_logs/

# Find all work on a specific date
cat data/work_logs/2025-01-15.md

# Search project files
grep -r "API" data/projects/
```

### 6. Editing Directly

All data is in human-readable markdown. You can edit files directly:

```bash
# Edit a project
vim data/projects/my-project.md

# Edit a work log
vim data/work_logs/2025-01-17.md

# Changes are synced to the database automatically on next command
```

### 7. Backup Your Data

```bash
# Everything is in the data directory
tar -czf second-brain-backup-$(date +%Y%m%d).tar.gz data/

# Or use git
cd data
git init
git add .
git commit -m "Work log backup"
```

---

## Command Cheat Sheet

```bash
# Setup
sb init
sb init --data-dir ~/work-brain

# Projects
sb project create NAME [-d DESC] [--tags TAGS] [--jira KEY]
sb project list [--status STATUS]
sb project status SLUG

# Tasks
sb task add TITLE [-p PROJECT] [-d DESC] [--priority PRI]
sb task update ID [--status STATUS] [--time MIN] [--priority PRI]
sb task list [-p PROJECT] [--status STATUS] [--priority PRI]

# Work Logs
sb log add TEXT [--task-id ID] [--time MIN] [--date DATE]
sb log show [--days N]

# Reports
sb report work [--days N] [-p PROJECT]

# Jira (optional)
sb jira sync [-p PROJECT]
```

---

## File Locations

All data is stored in your data directory (default: `./data/`):

```
data/
├── projects/
│   └── my-project.md              # Project notes (markdown)
├── work_logs/
│   └── 2025-01-17.md             # Daily work log (markdown)
├── transcripts/
│   ├── raw/
│   │   └── 2025-01-17_meeting.txt     # Raw transcript
│   └── processed/
│       └── 2025-01-17_meeting.md      # Processed notes
└── index.db                       # SQLite index (binary)
```

All markdown files use frontmatter for metadata and are fully human-readable and editable.
