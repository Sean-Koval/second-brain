Guide the user through managing context and quickly capturing notes across different projects, tasks, and issues.

Perfect for staying organized when working on multiple things!

## The Context Problem

When working on multiple projects/tasks, it's easy to lose track of:
- Which task am I adding notes to?
- What project is this for?
- Which issue is this linked to?

**Second Brain uses explicit IDs** - you always specify what you're working with.

## Quick Capture Patterns

### Pattern 1: Task-First (Recommended)

**Start your day by noting your active tasks:**

```bash
# See what you're working on
sb task list --status in_progress

# Example output:
# ID | Status        | Title
# 42 | in_progress  | Implement caching
# 55 | in_progress  | Fix login bug
# 67 | in_progress  | Update docs
```

**Keep these IDs handy!** Write them down or keep terminal open.

**Add notes by referencing the task ID:**

```bash
# Quick note to task 42 (caching work)
sb note create "Redis Cache Implementation" \
  --task-id 42 \
  --content "Using Redis cluster with 3 nodes..."

# Later, append to that note
sb note add NOTE_ID "## Performance: 50ms -> 5ms response time"

# Add different note to task 55 (login bug)
sb note create "Login Bug Root Cause" \
  --task-id 55 \
  --content "Issue is in session validation..."
```

**Your tasks are your context anchors!**

---

### Pattern 2: Project-Scoped Work

**When doing general project work without specific tasks:**

```bash
# List your active projects
sb project list --status active

# Example output:
# ID | Name              | Slug
# 1  | Backend API       | backend-api
# 2  | Mobile App        | mobile-app
# 3  | Documentation     | docs

# Add project-level notes (using slug)
sb note create "API Design Decisions" \
  --project backend-api \
  --content "## REST vs GraphQL..."

# Add another note to different project
sb note create "Mobile Navigation Plan" \
  --project mobile-app \
  --content "## Bottom nav with 5 tabs..."
```

**Project slugs are stable** - easier to remember than IDs!

---

### Pattern 3: Work Log First, Notes Later

**For quick capture during the day:**

```bash
# Log work immediately (quick!)
sb log add "Fixed caching race condition" --task-id 42 --time 30

# Continue working...

# At end of day, create detailed notes
sb note create "Caching Race Condition Fix" \
  --task-id 42 \
  --content "## Problem

Race condition when multiple requests hit cache simultaneously.

## Solution

Added distributed lock using Redis SETNX...

## Testing

Stress test with 100 concurrent requests - no more duplicates."
```

**Work logs are fast, notes are detailed.**

---

## Context Management Strategies

### Strategy 1: Terminal Sessions per Context

**Open multiple terminal tabs/windows:**

```bash
# Terminal 1: Backend API project
cd ~/projects/backend
export CURRENT_PROJECT="backend-api"
export CURRENT_TASK=42

# Quick aliases
alias qnote='sb note create --task-id $CURRENT_TASK'
alias qlog='sb log add --task-id $CURRENT_TASK'

# Usage:
qlog "Implemented Redis cluster setup" --time 45
qnote "Redis Setup" "Config: 3 nodes, 2 replicas"
```

```bash
# Terminal 2: Mobile app project
cd ~/projects/mobile
export CURRENT_PROJECT="mobile-app"
export CURRENT_TASK=55

alias qnote='sb note create --task-id $CURRENT_TASK'
alias qlog='sb log add --task-id $CURRENT_TASK'
```

**Each terminal has its own context!**

---

### Strategy 2: Shell Functions for Context

**Add to your ~/.bashrc or ~/.zshrc:**

```bash
# Set current working context
sb_context() {
    export SB_TASK_ID=$1
    export SB_PROJECT=$2
    echo "Context: Task #$SB_TASK_ID, Project: $SB_PROJECT"
}

# Quick note with current context
qnote() {
    if [ -z "$SB_TASK_ID" ]; then
        echo "No context set. Use: sb_context TASK_ID PROJECT_SLUG"
        return 1
    fi

    sb note create "$1" \
      --task-id $SB_TASK_ID \
      --content "$2"
}

# Quick log with current context
qlog() {
    if [ -z "$SB_TASK_ID" ]; then
        echo "No context set. Use: sb_context TASK_ID PROJECT_SLUG"
        return 1
    fi

    sb log add "$1" --task-id $SB_TASK_ID --time ${2:-0}
}

# Show current context
sb_status() {
    if [ -z "$SB_TASK_ID" ]; then
        echo "No context set"
    else
        echo "Current context:"
        echo "  Task: #$SB_TASK_ID"
        echo "  Project: $SB_PROJECT"
        sb task list | grep "^$SB_TASK_ID"
    fi
}
```

**Usage:**

```bash
# Morning: Set context
sb_context 42 backend-api

# Check context
sb_status
# Output:
# Current context:
#   Task: #42
#   Project: backend-api
#   42 | in_progress | Implement caching

# Quick operations use the context
qlog "Implemented Redis setup" 30
qnote "Redis Config" "3-node cluster with sentinels"

# Switch context
sb_context 55 mobile-app
qlog "Fixed login validation bug" 45
```

---

### Strategy 3: Note Templates

**Create note templates for common scenarios:**

```bash
# Save to ~/sb-templates/

# Template: Feature implementation
cat > ~/sb-templates/feature.md <<'EOF'
## Overview

[What is this feature]

## Implementation

- [ ] Backend changes
- [ ] Frontend changes
- [ ] Tests
- [ ] Documentation

## Testing Plan

[How to test]

## Deployment Notes

[Any special considerations]
EOF

# Use template
CONTENT=$(cat ~/sb-templates/feature.md)
sb note create "New Feature: OAuth" \
  --task-id 42 \
  --content "$CONTENT"
```

**Common templates:**
- `feature.md` - Feature implementation
- `bug.md` - Bug investigation
- `research.md` - Research findings
- `meeting.md` - Meeting notes
- `decision.md` - Technical decision

---

## Finding Your Context

### When You Forgot What You're Working On

```bash
# What am I working on right now?
sb task list --status in_progress

# What did I work on today?
sb log show --days 1

# What are my recent notes?
sb note list | head -10
```

### When You Need to Find a Specific Context

```bash
# Find task by project
sb task list --project backend-api

# Search notes
sb note search "caching"

# Find task by keyword
sb task list | grep -i "login"

# Show project with all tasks
sb project status backend-api
```

### When You Need to Link to an Issue

```bash
# Find tasks linked to issues
sb task list | grep -i "issue"

# Check if task has an issue link
sb task list --project backend-api

# Show issue details (from Beads)
sb issue show ISSUE_ID
```

---

## Quick Capture Workflows

### Workflow 1: Interrupt-Driven Work

**You're working on Task A, get interrupted for Task B:**

```bash
# You're on task 42 (caching)
# Interrupt: critical bug on task 55 (login)

# Log context switch
sb log add "Switching to critical login bug" --task-id 42

# Work on bug, log it
sb log add "Fixed session timeout bug" --task-id 55 --time 30

# Add bug fix note
sb note create "Session Timeout Fix" \
  --task-id 55 \
  --content "Changed timeout from 5min to 30min"

# Switch back
sb log add "Resuming caching work" --task-id 42
```

**Your work log shows the full timeline!**

---

### Workflow 2: Multi-Task Day

**Working on 3 different things:**

```bash
# Morning - Check your tasks
sb task list --status in_progress
# Task 42: Caching
# Task 55: Login bug
# Task 67: Documentation

# 9am - Start with caching
sb log add "Working on Redis cluster setup" --task-id 42

# 10am - Switch to bug
sb log add "Investigating login timeout" --task-id 55
sb note create "Login Debug Session" \
  --task-id 55 \
  --content "Logs show timeout after 5 min..."

# 11am - Back to caching
sb log add "Completed Redis cluster config" --task-id 42 --time 90
sb note add CACHE_NOTE_ID "## Config Complete\n\n3 nodes, 2 replicas"

# 2pm - Work on docs
sb log add "Updated API documentation" --task-id 67 --time 60

# End of day - Review
sb log show --days 1
```

**Timeline is preserved across context switches!**

---

### Workflow 3: Unplanned Notes (No Task Yet)

**You discover something important but don't have a task yet:**

```bash
# Option 1: Create standalone note with tags
sb note create "Database Performance Tip" \
  --tags performance,database,tip \
  --content "Use EXPLAIN ANALYZE to find slow queries"

# Later, create task and link the note
sb task add "Optimize slow queries" --project backend-api
# Get task ID: 99

# Update note to link to task
sb note list --tags performance
# Find the note ID: 123

# Can't directly update task_id, but you can:
# 1. Create new note linked to task
# 2. Reference old note in new note
sb note create "Query Optimization" \
  --task-id 99 \
  --content "See note #123 for the EXPLAIN ANALYZE tip.

## Queries to optimize
..."

# Option 2: Create task first, then note
sb task add "Database performance investigation" --project backend-api
sb note create "Performance Tips" \
  --task-id NEW_TASK_ID \
  --content "..."
```

---

## Visualizing Your Context

### Current Working Set

```bash
# Create a "status" command
cat > ~/.local/bin/sb-status <<'EOF'
#!/bin/bash
echo "=== 📋 Current Working Context ==="
echo ""
echo "Active Tasks:"
sb task list --status in_progress
echo ""
echo "Today's Work:"
sb log show --days 1 | head -20
echo ""
echo "Recent Notes:"
sb note list | head -5
EOF

chmod +x ~/.local/bin/sb-status

# Use it
sb-status
```

### Project-Specific Views

```bash
# Create project-specific status
cat > ~/.local/bin/sb-proj <<'EOF'
#!/bin/bash
PROJECT=$1

if [ -z "$PROJECT" ]; then
    echo "Usage: sb-proj PROJECT_SLUG"
    exit 1
fi

echo "=== Project: $PROJECT ==="
echo ""
echo "Tasks:"
sb task list --project $PROJECT
echo ""
echo "Notes:"
sb note list --project $PROJECT
echo ""
echo "Status:"
sb project status $PROJECT
EOF

chmod +x ~/.local/bin/sb-proj

# Use it
sb-proj backend-api
```

---

## Agent-Assisted Context

**When using Claude Code or other AI agents:**

### Pattern: Declare Context Upfront

```
User: "I'm working on task #42 (Redis caching) in the backend-api project"
Agent: "Got it! I'll remember this context. When you ask me to add notes,
        I'll automatically link them to task #42."

User: "Add a note about the cluster configuration"
Agent: [Creates note with --task-id 42]

User: "Now I'm switching to task #55 (login bug)"
Agent: "Switching context to task #55. I'll link notes there now."
```

### Pattern: Ask Agent to Track Context

```
User: "/sb-current-work"
Agent: [Shows all in-progress tasks]

User: "Set task 42 as my current context"
Agent: "Done! I'll use task #42 for notes and logs until you tell me otherwise."

User: "Add a note: implemented Redis cluster"
Agent: [Creates note linked to task #42]
```

---

## Pro Tips

### 1. Use Consistent Naming

**Makes searching easier:**

```bash
# Good - includes project/component name
"Backend API - Redis Caching Strategy"
"Mobile App - Navigation Design"
"Docs - API Reference Update"

# Bad - ambiguous
"Implementation"
"Notes"
"TODO"
```

### 2. Tag Everything

**Tags help filter across projects:**

```bash
sb note create "Performance Optimization" \
  --task-id 42 \
  --tags performance,redis,backend

# Later find all performance notes
sb note list --tags performance

# Find across multiple tags
sb note list --tags backend,performance
```

### 3. Keep a Context Journal

**Create a daily note with your context:**

```bash
# Each morning
sb note create "Work Context - $(date +%Y-%m-%d)" \
  --tags daily,context \
  --content "## Today's Focus

Task #42: Redis caching (backend-api)
Task #55: Login bug (auth)
Task #67: Docs update (docs)

## Primary: Task #42
## Secondary: Task #55
## If time: Task #67"

# Reference throughout the day
sb note search "Work Context" | tail -1
```

### 4. Use Work Logs for Context Switches

**Log every switch:**

```bash
sb log add "Starting work on Redis caching" --task-id 42
# ... work ...
sb log add "Switching to login bug" --task-id 55
# ... work ...
sb log add "Back to Redis caching" --task-id 42
```

**Your work log becomes a context timeline!**

---

## Common Pitfalls

❌ **Creating notes without context**
```bash
# Bad - orphaned note
sb note create "Some findings"
```

✅ **Always link to project or task**
```bash
# Good - has context
sb note create "Some findings" --task-id 42
```

---

❌ **Forgetting which task you're on**
```bash
# Bad - adding to wrong task
sb note add 123 "More findings"  # Wrong note!
```

✅ **Check context first**
```bash
# Good - verify before adding
sb note list | grep -A 2 "Redis"
sb note add CORRECT_NOTE_ID "More findings"
```

---

❌ **Using note IDs instead of task IDs for organization**
```bash
# Bad - hard to remember note IDs
sb note add 123 "update"
sb note add 456 "update"
```

✅ **Use tasks as anchors, find notes from there**
```bash
# Good - find via task
sb note list --task-id 42
sb note add FOUND_NOTE_ID "update"
```

---

## Summary

**Key Principles:**

1. **Tasks are your context** - Link notes to tasks
2. **Projects group work** - Use project slugs consistently
3. **IDs are explicit** - Always specify what you're working with
4. **Work logs track switches** - Log when you change context
5. **Tags enable cross-cutting** - Tag for themes that span projects
6. **Shell helpers manage context** - Use functions/aliases for current task

**Quick Reference:**

| Scenario | Command Pattern |
|----------|----------------|
| Add note to current task | `sb note create "..." --task-id $CURRENT` |
| Add note to project | `sb note create "..." --project my-proj` |
| Find notes for task | `sb note list --task-id 42` |
| Find notes for project | `sb note list --project backend-api` |
| Search all notes | `sb note search "keyword"` |
| See what I'm working on | `sb task list --status in_progress` |
| Track context switch | `sb log add "Switching to X" --task-id Y` |
