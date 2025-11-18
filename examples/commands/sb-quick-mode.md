# Second Brain Quick Mode Guide

All Second Brain slash commands support **two modes**:

## Mode 1: Conversational (No Arguments)

Just type the command name:
```
/sb-log
/sb-task-create
/sb-task-update
```

The agent will ask you questions to gather the information needed.

**When to use:**
- Learning the system
- Not sure what options are available
- Want the agent to guide you through the process

---

## Mode 2: Quick (With Arguments)

Type the command with all arguments:
```
/sb-log "Fixed caching bug" --task-id 42 --time 90
/sb-task-create "Implement API" --project backend --priority high
/sb-task-update 42 --status done
```

The agent will parse your arguments and execute immediately.

**When to use:**
- You know exactly what you want to do
- You have all the information ready
- You want speed over guidance

---

## Quick Mode Syntax Reference

### Work Logging

```bash
# Basic log
/sb-log "What you worked on"

# With task tracking
/sb-log "Fixed bug" --task-id 42

# With time tracking
/sb-log "Code review" --time 30

# Full logging
/sb-log "Implemented feature" --task-id 42 --time 120 --date 2025-01-15
```

**Arguments:**
- First positional argument is the log entry text (required)
- `--task-id ID` - Link to task
- `--time MINUTES` - Time spent
- `--date YYYY-MM-DD` - Date (defaults to today)

---

### Task Creation

```bash
# Simple task
/sb-task-create "Task title"

# With project
/sb-task-create "Fix bug" --project backend-api

# With priority
/sb-task-create "Urgent fix" --priority urgent

# With description
/sb-task-create "Feature" --description "Long description here"

# Full task creation
/sb-task-create "API endpoint" --project api --priority high --description "Create user profile endpoint" --tags backend,api
```

**Arguments:**
- First positional argument is task title (required)
- `--project SLUG` - Link to project
- `--priority LEVEL` - low, medium, high, urgent
- `--description TEXT` - Task description
- `--tags TAG1,TAG2` - Comma-separated tags
- `--with-issue` - Create linked Beads issue
- `--issue-id ID` - Link to existing issue

---

### Task Updates

```bash
# Change status
/sb-task-update 42 --status in_progress
/sb-task-update 42 --status done

# Add time tracking
/sb-task-update 42 --time 60

# Change priority
/sb-task-update 42 --priority urgent

# Multiple updates
/sb-task-update 42 --status done --time 120
```

**Arguments:**
- First positional argument is task ID (required)
- `--status STATUS` - todo, in_progress, done, blocked
- `--time MINUTES` - Time spent
- `--priority LEVEL` - low, medium, high, urgent

---

### Note Creation

```bash
# Simple note
/sb-note-create "Note title" --content "Note content here"

# Project note
/sb-note-create "Architecture Decision" --project backend-api --content "We decided to use Redis..."

# Task note
/sb-note-create "Implementation Notes" --task-id 42 --content "Using FastAPI..."

# Tagged note
/sb-note-create "Research Finding" --tags research,important --content "Found that..."

# Full note
/sb-note-create "Feature Design" --project api --task-id 42 --tags design,api --content "## Overview\n\nDetailed design..."
```

**Arguments:**
- First positional argument is note title (required)
- `--content TEXT` - Note content (markdown)
- `--project SLUG` - Link to project
- `--task-id ID` - Link to task
- `--tags TAG1,TAG2` - Comma-separated tags

---

### Note Management

```bash
# Append to note
/sb-note-add 123 "Additional content to append"

# Search notes
/sb-note-search "keyword to search"

# Show note
/sb-note-show 123
```

---

### Project Management

```bash
# Create project
/sb-project-create "Project Name" --description "Project description" --tags tag1,tag2

# Project status
/sb-project-status backend-api

# List projects
/sb-projects-overview
```

---

### Finding Things

```bash
# Find tasks
/sb-find-task --project backend-api
/sb-find-task --status in_progress
/sb-find-task --priority high

# Current work
/sb-current-work

# Show logs
/sb-daily-summary
```

---

## Combining Quick Mode with Context

You can combine quick mode with shell functions for even faster workflows:

```bash
# In your ~/.bashrc or ~/.zshrc
export CURRENT_TASK=42
export CURRENT_PROJECT=backend-api

# Quick aliases
alias qlog='function _qlog() { /sb-log "$1" --task-id $CURRENT_TASK --time ${2:-0}; }; _qlog'
alias qtask='function _qtask() { /sb-task-create "$1" --project $CURRENT_PROJECT; }; _qtask'
alias qnote='function _qnote() { /sb-note-create "$1" --task-id $CURRENT_TASK --content "$2"; }; _qnote'

# Usage
qlog "Fixed bug" 30        # Logs to task 42, 30 minutes
qtask "New feature"        # Creates task in backend-api
qnote "Design" "Content"   # Note for task 42
```

---

## Quick Mode Examples by Scenario

### Scenario 1: Quick Bug Fix

```bash
# Create task
/sb-task-create "Fix login timeout" --project auth --priority urgent

# Start work (assume task ID is 55)
/sb-task-update 55 --status in_progress

# Log investigation
/sb-log "Investigating login timeout issue" --task-id 55 --time 30

# Add finding note
/sb-note-create "Login Timeout Root Cause" --task-id 55 --content "Session timeout too short"

# Log fix
/sb-log "Fixed session timeout configuration" --task-id 55 --time 45

# Complete
/sb-task-update 55 --status done --time 75
```

### Scenario 2: Feature Development

```bash
# Create feature task with issue
/sb-task-create "User profile API" --project backend --priority high --with-issue

# Add design note (assume task ID 60)
/sb-note-create "Profile API Design" --task-id 60 --content "## Endpoints\n\n- GET /api/profile\n- PUT /api/profile"

# Log implementation work
/sb-log "Implemented GET /api/profile" --task-id 60 --time 90
/sb-log "Implemented PUT /api/profile" --task-id 60 --time 75

# Update status
/sb-task-update 60 --status done
```

### Scenario 3: Research Session

```bash
# Create research note
/sb-note-create "Redis Caching Research" --project backend --tags research,performance --content "## Overview\n\nEvaluating Redis for API caching"

# Log research time (to project or standalone)
/sb-log "Researched Redis caching strategies" --time 60

# Add findings
/sb-note-add NOTE_ID "## Findings\n\n- LRU eviction works well\n- 1GB memory sufficient"
```

---

## Pro Tips

### 1. Use Tab Completion (if available)

Some terminals support tab completion for slash commands.

### 2. Template Your Common Patterns

Save frequently used command patterns in a note:

```bash
# My common patterns
/sb-log "TEXT" --task-id 42 --time X
/sb-task-create "TEXT" --project backend-api --priority high
/sb-note-create "TEXT" --task-id 42 --content "## Overview\n\n"
```

### 3. Use Shell Aliases for Project Context

```bash
# Backend work
alias be-log='function f() { /sb-log "$1" --project backend-api --time ${2:-0}; }; f'
alias be-task='function f() { /sb-task-create "$1" --project backend-api; }; f'

# Frontend work
alias fe-log='function f() { /sb-log "$1" --project frontend --time ${2:-0}; }; f'
alias fe-task='function f() { /sb-task-create "$1" --project frontend; }; f'
```

### 4. Keep Task IDs Visible

```bash
# Show current tasks in prompt
/sb-current-work

# Or create a note with active task IDs
/sb-note-create "Active Work - Week 3" --tags context --content "Task 42: Caching\nTask 55: Auth bug\nTask 67: Docs"
```

### 5. Batch Operations with Quick Mode

```bash
# Morning: Create all tasks for the day
/sb-task-create "Fix typo" --project docs --priority low
/sb-task-create "Review PR #234" --project backend --priority medium
/sb-task-create "Deploy hotfix" --project ops --priority urgent

# Throughout day: Quick logging
/sb-log "Fixed typo in README" --task-id 101 --time 5
/sb-log "Reviewed PR, left comments" --task-id 102 --time 20
/sb-log "Deployed hotfix to production" --task-id 103 --time 45

# End of day: Quick status updates
/sb-task-update 101 --status done
/sb-task-update 102 --status done
/sb-task-update 103 --status done
```

---

## When to Use Each Mode

| Situation | Use Conversational | Use Quick Mode |
|-----------|-------------------|----------------|
| First time using a command | ✅ | ❌ |
| Learning available options | ✅ | ❌ |
| Complex operation | ✅ | ❌ |
| Repetitive task | ❌ | ✅ |
| Know all parameters | ❌ | ✅ |
| Fast logging during work | ❌ | ✅ |
| Batch operations | ❌ | ✅ |
| Want agent to suggest next steps | ✅ | ❌ |

---

## Common Mistakes to Avoid

❌ **Forgetting quotes around text with spaces:**
```bash
/sb-log Fixed the bug  # WRONG - will fail
/sb-log "Fixed the bug"  # CORRECT
```

❌ **Wrong flag names:**
```bash
/sb-task-create "Task" --proj backend  # WRONG
/sb-task-create "Task" --project backend  # CORRECT
```

❌ **Mixing conversational and quick mode:**
```bash
# Don't do this - either provide all args or none
/sb-task-create "Task" --project backend
[Then answering questions]
```

✅ **Either go full quick mode:**
```bash
/sb-task-create "Task" --project backend --priority high
```

✅ **Or go conversational:**
```bash
/sb-task-create
[Answer questions]
```

---

## Fallback Behavior

If quick mode parsing fails, the agent will fall back to conversational mode:

```bash
# Malformed quick mode
/sb-log something --invalid-flag

# Agent responds:
"I couldn't parse those arguments. Let me ask you some questions instead..."
```

This ensures you never get stuck!

---

## Summary

**Quick mode = Speed**
- Type command with all arguments
- Instant execution
- Perfect for repetitive tasks

**Conversational mode = Guidance**
- Type just the command name
- Agent asks questions
- Perfect for learning

**Both modes work with the same commands - choose based on your needs!**
