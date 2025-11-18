# Epics and Dependency Management

Second Brain integrates with **Beads** to provide powerful epic/issue management and dependency tracking capabilities. This allows you to organize large initiatives, track dependencies, and automatically find work that's ready to start.

---

## Overview

The epic/issue system in Second Brain uses [Beads](https://github.com/cased/beads) under the hood - a battle-tested dependency tracking system built specifically for AI agents and complex project management.

### Key Features

- **Epic Hierarchy** - Organize work into large initiatives with parent-child relationships
- **Dependency Tracking** - Four types of dependencies: blocks, related, parent-child, discovered-from
- **Ready Work Detection** - Automatically finds issues that can be started (no blockers)
- **Issue Types** - bug, feature, task, epic, chore
- **Priority Levels** - 0-4 (Lowest to Highest)
- **Git-backed Storage** - All data stored in JSONL format for easy version control
- **External References** - Link to Jira tickets, GitHub issues, etc.

---

## Installation

Beads integration is included with Second Brain:

```bash
# Install Second Brain (includes beads-mcp)
uv tool install git+https://github.com/seanm/second-brain.git

# Initialize Beads in your project
sb init --global
```

The Beads database will be stored in `~/.second-brain/.beads/` by default.

---

## Core Concepts

### Epics

**Epics** are high-level work items that represent large initiatives or features. They can have multiple child issues and help organize complex work into manageable pieces.

Examples:
- "Mobile App Redesign"
- "API v2 Migration"
- "Performance Optimization Initiative"

### Issues

**Issues** are individual work items. They can be:
- **Tasks** - Standard work items
- **Bugs** - Defects to fix
- **Features** - New functionality
- **Chores** - Maintenance work
- **Epics** - Large initiatives (use `sb epic create` instead)

### Dependencies

Four types of relationships between issues:

1. **blocks** - One issue must be completed before another can start
   - Example: "Database schema migration" blocks "Add new API endpoints"

2. **related** - Issues are related but no strict ordering
   - Example: "Update documentation" is related to "Add feature X"

3. **parent-child** - Epic/sub-issue relationship
   - Example: "Mobile App Redesign" (parent) contains "Redesign login screen" (child)

4. **discovered-from** - Issue discovered while working on another
   - Example: "Fix memory leak" discovered from "Performance optimization"

---

## CLI Commands

### Epic Commands

#### Create Epic

```bash
sb epic create "Epic Title" \
  --description "Epic description" \
  --priority 3 \
  --labels "frontend,mobile"
```

**Options:**
- `-d, --description` - Epic description
- `-p, --priority` - Priority 0-4 (0=Lowest, 4=Highest)
- `-l, --labels` - Comma-separated labels

**Example:**
```bash
sb epic create "Mobile App Redesign" \
  --description "Complete redesign of mobile app UI/UX" \
  --priority 4 \
  --labels "mobile,design,q1-2025"
```

#### List Epics

```bash
sb epic list [--status STATUS] [--limit N]
```

**Options:**
- `-s, --status` - Filter by status (open, in_progress, blocked, closed)
- `-l, --limit` - Max number to return (default: 50)

**Example:**
```bash
sb epic list --status in_progress
```

---

### Issue Commands

#### Create Issue

```bash
sb issue create "Issue Title" \
  --type task \
  --priority 2 \
  --epic EPIC-1 \
  --description "Issue description"
```

**Options:**
- `-t, --type` - Type: bug, feature, task, epic, chore
- `-p, --priority` - Priority 0-4
- `-e, --epic` - Parent epic ID
- `-b, --blocks` - Comma-separated issue IDs this blocks
- `-l, --labels` - Comma-separated labels
- `-r, --external-ref` - External reference (Jira, GitHub, etc.)
- `-d, --description` - Issue description

**Examples:**

Create a task linked to an epic:
```bash
sb issue create "Redesign login screen" \
  --type task \
  --epic SB-1 \
  --priority 3 \
  --labels "ui,auth"
```

Create a bug that blocks another issue:
```bash
sb issue create "Fix authentication timeout" \
  --type bug \
  --priority 4 \
  --blocks SB-5 \
  --external-ref "JIRA-123"
```

#### Update Issue

```bash
sb issue update ISSUE-ID \
  --status in_progress \
  --priority 3
```

**Options:**
- `-t, --title` - New title
- `-d, --description` - New description
- `-s, --status` - New status (open, in_progress, blocked, closed)
- `-p, --priority` - New priority 0-4

**Example:**
```bash
sb issue update SB-5 --status in_progress
```

#### Close Issue

```bash
sb issue close ISSUE-ID [--reason "Reason"]
```

**Example:**
```bash
sb issue close SB-5 --reason "Fixed in PR #234"
```

#### Show Issue Details

```bash
sb issue show ISSUE-ID
```

Shows full details including dependencies and dependents.

**Example:**
```bash
sb issue show SB-5
```

Output:
```
Redesign login screen (SB-5)

Type: task
Status: in_progress
Priority: High

Description:
Update login screen with new design system

Labels: ui, auth

Dependencies (1):
  - SB-3: Update design system [blocks]

Dependents (2):
  - SB-7: Add OAuth2 support
  - SB-8: Implement password reset
```

#### List Issues

```bash
sb issue list \
  [--status STATUS] \
  [--type TYPE] \
  [--priority PRIORITY] \
  [--limit N]
```

**Options:**
- `-s, --status` - Filter by status
- `-t, --type` - Filter by type
- `-p, --priority` - Filter by priority (0-4)
- `-l, --limit` - Max number to return (default: 50)

**Examples:**

List all open high-priority bugs:
```bash
sb issue list --type bug --priority 4 --status open
```

List in-progress tasks:
```bash
sb issue list --status in_progress --type task
```

#### Add Dependency

```bash
sb issue add-dependency ISSUE-ID DEPENDS-ON-ID \
  --type blocks
```

**Dependency Types:**
- `blocks` - DEPENDS-ON-ID blocks ISSUE-ID
- `related` - Issues are related
- `parent-child` - DEPENDS-ON-ID is parent of ISSUE-ID
- `discovered-from` - ISSUE-ID discovered while working on DEPENDS-ON-ID

**Examples:**

Issue SB-3 blocks SB-5:
```bash
sb issue add-dependency SB-5 SB-3 --type blocks
```

Link related issues:
```bash
sb issue add-dependency SB-10 SB-11 --type related
```

Create parent-child relationship:
```bash
sb issue add-dependency SB-20 SB-1 --type parent-child
```

#### Find Ready Work

```bash
sb issue ready [--limit N] [--priority PRIORITY]
```

**This is the killer feature!** Automatically finds issues that:
- Are open (not closed)
- Have no open blockers
- Can be started immediately

Results are sorted by priority.

**Options:**
- `-l, --limit` - Max number to return (default: 10)
- `-p, --priority` - Filter by specific priority

**Examples:**

Find top 10 ready issues:
```bash
sb issue ready
```

Find high-priority ready work:
```bash
sb issue ready --priority 4 --limit 5
```

#### Issue Statistics

```bash
sb issue stats
```

Shows project overview:
- Total issues
- Open/closed counts
- Blocked issues
- Ready work count

**Example:**
```bash
sb issue stats
```

Output:
```
📊 Project Statistics

Total Issues: 47
Open: 23
Closed: 24
Blocked: 3
Ready to Work: 8

💡 You have 8 issue(s) ready to work on!
```

---

## MCP Tools (for AI Agents)

All CLI commands are also available as MCP tools for AI agents to use.

### Epic Tools

- **`create_epic`** - Create a new epic
- **`list_epics`** - Query epics with filters
- **`get_issue`** - Get epic details (epics are issues with type="epic")

### Issue Tools

- **`create_issue`** - Create a new issue
- **`update_issue`** - Update issue properties
- **`close_issue`** - Close an issue
- **`get_issue`** - Get detailed issue information
- **`list_issues`** - Query issues with filters
- **`add_dependency`** - Add dependency between issues
- **`get_ready_work`** - Find ready work
- **`get_epic_stats`** - Get project statistics

### MCP Tool Examples

When using with Claude Code or other AI agents:

```
User: "Create an epic for our mobile redesign project"
Agent: Uses create_epic tool

User: "What can I work on right now?"
Agent: Uses get_ready_work tool

User: "Show me all blocked issues"
Agent: Uses list_issues with status="blocked"
```

---

## Workflows

### Workflow 1: Planning a Large Initiative

```bash
# 1. Create epic
sb epic create "API v2 Migration" \
  --description "Migrate all endpoints to v2 architecture" \
  --priority 4 \
  --labels "backend,migration"

# Output: Epic created! ID: SB-1

# 2. Create sub-issues
sb issue create "Design v2 schema" \
  --epic SB-1 \
  --type task \
  --priority 4

sb issue create "Migrate auth endpoints" \
  --epic SB-1 \
  --type task \
  --priority 3

sb issue create "Migrate user endpoints" \
  --epic SB-1 \
  --type task \
  --priority 3

# 3. Add dependencies
# Auth must be done before users
sb issue add-dependency SB-3 SB-2 --type blocks

# 4. See what's ready
sb issue ready
```

### Workflow 2: Daily Work Planning

```bash
# Morning: Check ready work
sb issue ready --limit 5

# Start working on an issue
sb issue update SB-5 --status in_progress

# During work: Discover a blocker
sb issue create "Fix OAuth2 token refresh" \
  --type bug \
  --priority 4 \
  --discovered-from SB-5

# Add blocker relationship
sb issue add-dependency SB-5 SB-10 --type blocks

# Mark current issue as blocked
sb issue update SB-5 --status blocked

# Find new work
sb issue ready
```

### Workflow 3: Sprint Planning

```bash
# Check overall status
sb issue stats

# List all open issues by priority
sb issue list --status open --priority 4
sb issue list --status open --priority 3

# See what's blocked
sb issue list --status blocked

# Plan work for team
sb issue ready --limit 20
```

---

## Integration with Second Brain Tasks

Second Brain has two task systems:

### Second Brain Tasks (Original)
- Project-based task tracking
- Time tracking
- Work logs
- Reporting

### Beads Issues (New)
- Epic/issue hierarchy
- Dependency tracking
- Blocker detection
- Ready work finding

### When to Use Each

**Use Second Brain Tasks for:**
- Daily work logging
- Time tracking
- Project status reporting
- Performance reviews

**Use Beads Issues for:**
- Planning large initiatives
- Managing dependencies
- Finding what to work on next
- Complex project orchestration

**Use Both Together:**
```bash
# Create epic for project
sb epic create "Mobile Redesign"

# Create project in Second Brain
sb project create "Mobile Redesign"

# Create issue in Beads
sb issue create "Login screen" --epic SB-1

# Create task in Second Brain for same work
sb task add "Login screen redesign" --project mobile-redesign

# Log work
sb log add "Working on login screen" --time 120

# Update both systems
sb issue update SB-2 --status done
sb task update 5 --status done
```

---

## Tips and Best Practices

### Epic Organization

- Keep epics at a high level (3-10 issues per epic)
- Use descriptive titles: "Q1 Performance Initiative" not "Performance"
- Set epic priority based on business value

### Dependency Management

- Use `blocks` sparingly - only for true blocking relationships
- Use `related` liberally to document connections
- Use `parent-child` for epic breakdowns
- Use `discovered-from` to maintain work context

### Priority Levels

- **4 (Highest)** - Critical bugs, production issues
- **3 (High)** - Important features, major bugs
- **2 (Medium)** - Standard work (default)
- **1 (Low)** - Nice-to-haves
- **0 (Lowest)** - Backlog items

### Labels

Use labels for:
- Teams: "backend", "frontend", "mobile"
- Themes: "performance", "security", "ux"
- Quarters: "q1-2025", "q2-2025"
- Categories: "technical-debt", "feature-request"

### Finding Work

```bash
# Daily standup
sb issue ready --limit 5

# When blocked
sb issue ready --priority 3

# Sprint planning
sb issue ready --limit 30

# High priority only
sb issue ready --priority 4
```

---

## Advanced Features

### External References

Link to Jira, GitHub, Linear, etc:

```bash
sb issue create "Fix login bug" \
  --type bug \
  --external-ref "JIRA-123"

sb issue create "Add dark mode" \
  --type feature \
  --external-ref "https://github.com/org/repo/issues/456"
```

### Bulk Operations

Create multiple issues from a script:

```bash
#!/bin/bash
EPIC="SB-1"

cat issues.txt | while read title; do
  sb issue create "$title" --epic $EPIC --priority 2
done
```

### Dependency Visualization

Get full dependency tree:

```bash
# Show issue with all dependencies
sb issue show SB-5

# Check stats for overview
sb issue stats
```

---

## Troubleshooting

### "Beads integration not available"

**Problem:** Error when running epic/issue commands

**Solution:**
```bash
# Reinstall with beads-mcp
uv tool install git+https://github.com/seanm/second-brain.git --force

# Verify beads-mcp is installed
uv pip list | grep beads-mcp
```

### Database not found

**Problem:** `.beads` directory doesn't exist

**Solution:**
```bash
# Initialize Second Brain (creates .beads)
sb init --global
```

### Issues not showing up

**Problem:** Created issues don't appear in list

**Solution:**
```bash
# Check issue stats
sb issue stats

# List all issues (no filters)
sb issue list --limit 100

# Show specific issue
sb issue show ISSUE-ID
```

---

## Data Storage

All epic/issue data is stored in:
```
~/.second-brain/.beads/
├── issues.jsonl        # All issues (epics and issues)
├── dependencies.jsonl  # Dependency relationships
└── config.json        # Beads configuration
```

The JSONL format makes it easy to:
- Version control with git
- Search with standard tools
- Backup and restore
- Parse with scripts

---

## Next Steps

- [CLI Reference](cli-reference.md) - All Second Brain commands
- [MCP Server](mcp-server.md) - MCP tool details
- [Workflows](workflows.md) - Combined Second Brain + Beads workflows
- [Architecture](architecture.md) - How it all works together

---

**Ready to start?** Create your first epic:

```bash
sb epic create "Your First Epic" --priority 2
sb issue create "Your First Task" --epic SB-1
sb issue ready
```

🎯 **Pro tip:** Use `sb issue ready` every morning to find your top priorities!
