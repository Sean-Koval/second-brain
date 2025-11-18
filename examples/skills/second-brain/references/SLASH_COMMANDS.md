# Slash Commands Reference

Complete reference for Second Brain slash commands in Claude Code.

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Mode vs Conversational Mode](#quick-mode-vs-conversational-mode)
- [Command Categories](#command-categories)
- [Daily Workflow Commands](#daily-workflow-commands)
- [Epic & Project Commands](#epic--project-commands)
- [Query Commands](#query-commands)
- [Basic Operations](#basic-operations)
- [Complete Command List](#complete-command-list)
- [Best Practices](#best-practices)

---

## Overview

Second Brain provides **27 slash commands** for Claude Code, enabling guided workflows for work tracking, task management, and note-taking.

**Two modes:**
1. **Quick Mode** - Provide arguments directly (fast, autonomous)
2. **Conversational Mode** - Interactive prompts (guided, beginner-friendly)

**Key advantage:** Pre-built workflows that guide you through complex operations step-by-step.

---

## Installation

```bash
# Copy all slash commands to your project
mkdir -p .claude/commands
cp ~/.local/share/uv/tools/second-brain/examples/commands/*.md .claude/commands/

# Or globally
mkdir -p ~/.claude/commands
cp ~/.local/share/uv/tools/second-brain/examples/commands/*.md ~/.claude/commands/

# Restart Claude Code
```

**Verify installation:**
Type `/sb-` and Claude should show autocomplete suggestions for all commands.

---

## Quick Mode vs Conversational Mode

### Quick Mode (with arguments)

**Fast execution for power users:**

```
/sb-log "Implemented OAuth integration" --task-id 42 --time 120

/sb-task-create "Fix login bug" --project auth --priority urgent

/sb-epic-project-create "Mobile App v2" --priority 4 --labels mobile,frontend
```

**When to use:**
- You know exactly what you want
- Daily routine operations
- Want autonomous execution

---

### Conversational Mode (no arguments)

**Guided workflow with prompts:**

```
You: /sb-log
Claude: "What did you work on?"
You: "Implemented OAuth integration"
Claude: "Should this be linked to a task?"
You: "Yes, task 42"
Claude: "How much time did you spend? (in minutes)"
You: "120 minutes"
Claude: ✓ Work log added! Linked to task #42, 120 minutes tracked.
```

**When to use:**
- Learning the system
- Complex operations with many options
- Want guidance on what to provide

---

## Command Categories

### 1. Workflow Guides
Complete guided workflows for common scenarios

| Command | Purpose |
|---------|---------|
| `/sb-daily-dev-workflow` | Complete daily development routine |
| `/sb-epic-project-create` | Create epic + project together |
| `/sb-weekly-summary` | Weekly review and planning |
| `/sb-feature-workflow` | Starting new feature end-to-end |
| `/sb-bug-workflow` | Bug investigation and fix workflow |

---

### 2. Query Commands
View and search your work data

| Command | Purpose |
|---------|---------|
| `/sb-search-all` | Global search across everything |
| `/sb-project-view` | Complete project overview |
| `/sb-task-view` | Task details with notes and logs |
| `/sb-issue-view` | Issue/epic details with dependencies |
| `/sb-current-work` | Show active work status |

---

### 3. Basic Operations
Create and update work items

| Command | Purpose |
|---------|---------|
| `/sb-log` | Add work log entry |
| `/sb-task-create` | Create new task |
| `/sb-task-update` | Update task status/priority |
| `/sb-note-create` | Create markdown note |
| `/sb-issue-ready` | Find ready work (no blockers) |

---

## Daily Workflow Commands

### Morning Routine

**`/sb-current-work`**

Shows your current work status:
- Tasks in progress
- Today's work logs
- High priority items
- Ready issues to work on

**Quick mode:**
```
/sb-current-work
```

**No conversational mode** - Displays status immediately.

**Example output:**
```
📋 Current Work Status

🚧 In Progress (3 tasks):
  #42 Implement rate limiting (backend-api) [high]
  #45 Write integration tests (backend-api) [medium]
  #48 Add payment UI (payments) [high]

📝 Today's Logs (2 entries):
  - Fixed auth bug [1.5h] #42
  - Code review PR #234 [30m]

🎯 Ready to Start (2 issues):
  - epic-042: Webhook handling [priority: 3]
  - issue-123: Database migration [priority: 4]
```

---

**`/sb-issue-ready`**

Find work ready to start (no blockers):

**Quick mode:**
```
/sb-issue-ready
/sb-issue-ready --priority 4
/sb-issue-ready --limit 5
```

**Conversational mode:**
```
You: /sb-issue-ready
Claude: "Filter by priority? (0-4, or leave blank for all)"
You: "4"
Claude: Finding critical work ready to start...

🎯 3 issues ready (priority 4):
  1. Implement Stripe webhooks (epic-042)
  2. Add payment UI components (epic-042)
  3. Migrate auth endpoints (epic-051)

💡 All dependencies satisfied!
```

---

### During Work - Logging

**`/sb-log`**

Add work log entry:

**Quick mode:**
```
/sb-log "Implemented OAuth integration" --task-id 42 --time 120

/sb-log "Code review PR #234" --time 30

/sb-log "Sprint planning meeting" --time 60
```

**Conversational mode:**
```
You: /sb-log
Claude: "What did you work on?"
You: "Fixed authentication bug in OAuth flow"
Claude: "Should this be linked to a task? (task ID or 'no')"
You: "42"
Claude: "How much time did you spend? (minutes, or 'skip')"
You: "90"
Claude: ✓ Work log added!
       - Linked to task #42
       - 90 minutes tracked
       - Logged at 2025-01-17 14:30
```

**Best practices:**
- Be specific about what you did
- Link to tasks when relevant
- Track time for work >30 minutes
- Log as you go, don't wait until end of day

---

### During Work - Task Management

**`/sb-task-create`**

Create new task:

**Quick mode:**
```
/sb-task-create "Fix login timeout bug" --project auth --priority urgent

/sb-task-create "Implement rate limiting" --project backend-api --priority high
```

**Conversational mode:**
```
You: /sb-task-create
Claude: "Task title?"
You: "Implement Redis caching layer"
Claude: "Which project? (slug or 'none')"
You: "backend-api"
Claude: "Priority? (low/medium/high/urgent, default: medium)"
You: "high"
Claude: "Description? (optional)"
You: "Add Redis for session and response caching"
Claude: ✓ Task created! #56 - Implement Redis caching layer
       Project: backend-api
       Priority: high
```

---

**`/sb-task-update`**

Update task status or priority:

**Quick mode:**
```
/sb-task-update 42 --status done --time 180

/sb-task-update 42 --status in_progress

/sb-task-update 42 --priority urgent
```

**Conversational mode:**
```
You: /sb-task-update 42
Claude: "What would you like to update?"
       [1] Status
       [2] Priority
       [3] Add time spent
       [4] Multiple
You: "1"
Claude: "New status? (todo/in_progress/done/blocked)"
You: "done"
Claude: "Add time spent? (minutes, or 'skip')"
You: "180"
Claude: ✓ Task #42 updated!
       Status: todo → done
       Time added: 3h 0m
```

---

### Starting New Features

**`/sb-epic-project-create`**

**RECOMMENDED** way to start new initiatives:

**Quick mode:**
```
/sb-epic-project-create "Mobile App Redesign" --priority 4 --labels mobile,design

/sb-epic-project-create "API v2 Migration" --priority 3 --labels backend,api
```

**Conversational mode:**
```
You: /sb-epic-project-create
Claude: "What's the name of this initiative?"
You: "Payment System Redesign"
Claude: "Brief description? (optional)"
You: "Complete overhaul of payment processing with Stripe"
Claude: "Priority? (0-4, default 2)"
You: "4"
Claude: "Any labels/tags? (comma-separated)"
You: "backend,payments,critical"
Claude: ✓ Epic + Project created!

📋 Epic: epic-042
📦 Project: payment-system-redesign

🔗 Linked together!

Next steps:
1. Create issues: /sb-issue-create --epic epic-042
2. Create tasks: /sb-task-create --project payment-system-redesign
3. Add notes: /sb-note-create --project payment-system-redesign
```

**Why use this?**
- Creates both Beads epic (for dependencies) and Second Brain project (for notes/time) together
- Links them automatically
- One command instead of multiple steps
- Ready for both task tracking and dependency management

---

**`/sb-feature-workflow`**

Complete guided workflow for starting a new feature:

**No quick mode** - Always conversational for this complex workflow.

**Walks through:**
1. Create epic + project
2. Break down into issues
3. Add dependencies
4. Create initial notes
5. Find ready work to start

**Example:**
```
You: /sb-feature-workflow
Claude: "Let's start a new feature! What are you building?"
You: "User authentication system"
Claude: "Priority? (0-4)"
You: "4"
Claude: "Any labels?"
You: "backend,auth,security"

[Creates epic + project]

Claude: "Let's break this down. What are the main components?"
You: "OAuth integration, password reset, 2FA"

[Creates issues for each]

Claude: "Any dependencies between these?"
You: "OAuth must be done before 2FA"

[Adds dependencies]

Claude: "Any design decisions to document?"
You: "Yes, using JWT with RS256"

[Creates note]

Claude: ✓ Feature setup complete!

🎯 Ready to start:
  - OAuth integration (no blockers)
  - Password reset flow (no blockers)

📝 Next: Start working and log your progress with /sb-log
```

---

### End of Day

**`/sb-daily-summary`**

Review the day:

**Quick mode:**
```
/sb-daily-summary
```

**Shows:**
- Today's work logs
- Tasks completed
- Tasks in progress
- Time spent
- Suggestions for tomorrow

**Example output:**
```
📅 Daily Summary - 2025-01-17

✅ Completed (2 tasks):
  #42 Implement rate limiting [3h]
  #45 Write integration tests [2h]

🚧 In Progress (1 task):
  #48 Add payment UI [1h so far]

📝 Work Logs (4 entries):
  - Implemented rate limiting middleware [2h]
  - Wrote integration tests for auth [2h]
  - Code review PR #234 [30m]
  - Started payment UI design [1h]

⏱️ Total Time: 5h 30m

💡 Tomorrow:
  - Continue #48 (payment UI)
  - Review ready work: /sb-issue-ready
```

---

### Weekly Review

**`/sb-weekly-summary`**

Comprehensive weekly review:

**Quick mode:**
```
/sb-weekly-summary
```

**Walks through:**
1. Generate work report (7 days)
2. Review completed tasks
3. Check in-progress items
4. Identify blockers
5. Plan next week

**Example output:**
```
📊 Weekly Summary (Jan 13-17, 2025)

📈 Accomplishments:
  ✓ 8 tasks completed
  ✓ 38h 30m worked
  ✓ 3 projects advanced

Top achievements:
  - Payment integration (Stripe API + UI) [12h]
  - Rate limiting implementation [6h]
  - Integration test coverage [4.5h]

🚧 In Progress:
  - Redis caching layer (50% complete)
  - Mobile app refactor (25% complete)

🚨 Blockers:
  None identified

📅 Next Week:
  🎯 High priority:
    - Complete Redis caching
    - Start mobile app redesign
  💡 Ready to start:
    - Database migration (epic-051)
    - Webhook handling (epic-042)

💾 Save this summary? (creates note)
```

---

## Query Commands

### Global Search

**`/sb-search-all`**

Search everything: notes, tasks, work logs, issues.

**Quick mode:**
```
/sb-search-all "authentication"

/sb-search-all "Redis caching"
```

**Example output:**
```
🔍 Search results for "authentication"

📝 Notes (2 found):
  - Auth Architecture (project: backend-api)
    "Using JWT with RS256 for authentication..."

  - API Security (project: backend-api)
    "Authentication flow: OAuth2 with PKCE..."

📋 Tasks (3 found):
  #42 Implement OAuth authentication [done]
  #55 Add 2FA authentication [in_progress]
  #67 Fix authentication timeout bug [done]

💬 Work Logs (5 found):
  - "Implemented OAuth authentication flow" [2h]
  - "Fixed authentication timeout bug" [1.5h]
  - "Added JWT authentication middleware" [2h]
  ...

🎫 Issues (1 found):
  epic-042: User Authentication System [open]
```

---

### Project View

**`/sb-project-view`**

Complete project overview:

**Quick mode:**
```
/sb-project-view backend-api

/sb-project-view mobile-app
```

**Example output:**
```
📦 Project: Backend API (backend-api)

📊 Overview:
  Status: Active
  Created: 2025-01-01
  Tags: backend, api, core

📈 Progress:
  ✓ Completed: 12 tasks (60%)
  🚧 In Progress: 3 tasks (15%)
  📋 Todo: 5 tasks (25%)

⏱️ Time Tracking:
  Total: 85h 30m
  This week: 12h 15m
  Top tasks by time:
    - Rate limiting: 6h
    - OAuth integration: 8h 30m
    - Database optimization: 10h

📝 Notes (8):
  - API Architecture
  - Authentication Strategy
  - Rate Limiting Design
  - Database Schema
  ...

🔗 Linked Issues (3):
  - epic-042: User Authentication
  - issue-123: Rate Limiting
  - issue-145: Database Migration

💡 Recent Activity (last 7 days):
  - Completed rate limiting implementation
  - Started Redis caching layer
  - Fixed 3 authentication bugs
```

---

### Task View

**`/sb-task-view`**

Everything about a task:

**Quick mode:**
```
/sb-task-view 42
```

**Example output:**
```
📋 Task #42: Implement OAuth integration

Status: ✅ Done
Priority: High
Project: backend-api (User Authentication)
Created: 2025-01-10
Completed: 2025-01-15

📝 Description:
Implement OAuth2 authentication flow with JWT tokens.
Support Google, GitHub, and email providers.

⏱️ Time Spent: 8h 30m

💬 Work Logs (4 entries):
  2025-01-15: Deployed OAuth to production [1h]
  2025-01-14: Added refresh token rotation [2h]
  2025-01-13: Implemented Google OAuth provider [3h]
  2025-01-10: Set up OAuth2 middleware [2.5h]

📝 Notes (2):
  - OAuth Architecture (note-156)
    "Using Authorization Code flow with PKCE..."

  - Provider Configuration (note-159)
    "Google: client_id from env..."

🔗 Linked Issue: epic-042 (User Authentication System)

🎯 Status Timeline:
  2025-01-10: Created (todo)
  2025-01-10: Started (in_progress)
  2025-01-15: Completed (done)
```

---

## Basic Operations

### Quick Task Operations

**Create, update, and manage tasks:**

```
# Create task
/sb-task-create "Fix bug in API" --project backend-api --priority high

# Start working on it
/sb-task-update 42 --status in_progress

# Log work
/sb-log "Fixed API bug in error handling" --task-id 42 --time 90

# Mark done
/sb-task-update 42 --status done --time 90
```

---

### Quick Note Operations

**Create and organize notes:**

```
# Project note
/sb-note-create "API Design" --project backend-api --content "REST endpoints..."

# Task note
/sb-note-create "Implementation Notes" --task-id 42 --content "Using middleware pattern..."

# Standalone note
/sb-note-create "Research: Caching Strategies" --tags research,performance
```

---

### Quick Issue Operations

**Create epics and issues:**

```
# Epic + Project together (RECOMMENDED)
/sb-epic-project-create "Mobile App v2" --priority 4

# Issue under epic
/sb-issue-create "Redesign navigation" --epic epic-042 --priority 3

# Find ready work
/sb-issue-ready --priority 4
```

---

## Complete Command List

### Workflow Guides (5 commands)

| Command | Purpose | Mode |
|---------|---------|------|
| `/sb-daily-dev-workflow` | Complete daily routine | Conversational |
| `/sb-epic-project-create` | Create epic + project | Both |
| `/sb-weekly-summary` | Weekly review | Conversational |
| `/sb-feature-workflow` | New feature end-to-end | Conversational |
| `/sb-bug-workflow` | Bug investigation workflow | Conversational |

---

### Query Commands (10 commands)

| Command | Purpose | Mode |
|---------|---------|------|
| `/sb-search-all` | Global search | Both |
| `/sb-project-view` | Project overview | Both |
| `/sb-task-view` | Task details | Both |
| `/sb-issue-view` | Issue/epic details | Both |
| `/sb-current-work` | Active work status | Quick only |
| `/sb-note-search` | Search notes | Both |
| `/sb-log-show` | View work logs | Both |
| `/sb-task-list` | List tasks | Both |
| `/sb-issue-list` | List issues | Both |
| `/sb-daily-summary` | Today's summary | Quick only |

---

### Basic Operations (12 commands)

| Command | Purpose | Mode |
|---------|---------|------|
| `/sb-log` | Add work log | Both |
| `/sb-task-create` | Create task | Both |
| `/sb-task-update` | Update task | Both |
| `/sb-note-create` | Create note | Both |
| `/sb-note-add` | Append to note | Both |
| `/sb-issue-create` | Create issue | Both |
| `/sb-issue-ready` | Find ready work | Both |
| `/sb-project-create` | Create project | Both |
| `/sb-epic-create` | Create epic | Both |
| `/sb-dependency-add` | Add dependency | Both |
| `/sb-report` | Generate report | Both |
| `/sb-stats` | Project statistics | Quick only |

**Total: 27 commands**

---

## Best Practices

### When to Use Slash Commands

**Slash commands are best for:**
- Guided workflows (daily routine, weekly review)
- Learning the system (conversational mode)
- Complex multi-step operations (feature workflow)
- Status reviews (daily summary, current work)

**Use CLI instead for:**
- Scripting or automation
- Batch operations
- When you want to see exact commands
- Lower context usage

**Use MCP instead for:**
- Questions about your work ("What did I do?")
- Analysis and trends
- Complex queries

---

### Daily Workflow Recommendations

**Morning (3 min):**
```
/sb-current-work         # See what's active
/sb-issue-ready          # Find work to start
```

**During work (ongoing):**
```
/sb-log "..." --task-id X --time Y    # Log as you go
/sb-task-update X --status ...         # Update status
```

**End of day (5 min):**
```
/sb-daily-summary        # Review the day
```

**Weekly (15 min):**
```
/sb-weekly-summary       # Comprehensive review
```

---

### Quick Mode Tips

**Use descriptive titles:**
```
Good: /sb-task-create "Implement rate limiting middleware with Redis backend"
Bad:  /sb-task-create "rate limiting"
```

**Link work to tasks:**
```
Good: /sb-log "Fixed auth bug" --task-id 42 --time 90
Bad:  /sb-log "worked on stuff"
```

**Use priorities consistently:**
```
urgent  - Production issues, critical bugs
high    - Important features, major work
medium  - Regular tasks (default)
low     - Nice-to-have, cleanup
```

---

### Conversational Mode Tips

**Be specific in responses:**
```
Claude: "Which project?"
Good: "backend-api"
Bad:  "the API one"
```

**Use shortcuts:**
```
Claude: "Description? (optional)"
You: "skip"  or  "none"  or  just press enter
```

**Correct mistakes:**
```
If you enter wrong info, just say "oops, I meant X"
Claude will update and continue
```

---

## Related Documentation

- **[CLI Reference](CLI_REFERENCE.md)** - Complete CLI command reference
- **[Workflows](WORKFLOWS.md)** - Step-by-step workflow examples
- **[MCP Integration](MCP_INTEGRATION.md)** - MCP server tools and usage
