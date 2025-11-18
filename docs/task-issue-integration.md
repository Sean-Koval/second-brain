# Task-Issue Integration

Second Brain tasks and Beads issues are designed to work together, giving you the best of both worlds: rich note-taking with dependency tracking.

## Overview

### Two Systems, One Workflow

**Second Brain** provides:
- Rich markdown notes
- Time tracking
- Project organization
- Work logs
- Fast local search

**Beads** provides:
- Dependency graphs
- Epic breakdown
- Blocker detection
- Ready work finder
- Multi-issue relationships

By linking them, you get complete visibility and control over your work.

## Mental Model

Think of it this way:

```
Epic (Beads)
  └─ Issues (Beads) ← Dependency tracking
       └─ Tasks (Second Brain) ← Notes, time, context
            └─ Notes (Second Brain) ← Documentation
            └─ Work Logs (Second Brain) ← Daily tracking
```

### Separation of Concerns

| Concern | System | Why |
|---------|--------|-----|
| "What blocks what?" | Beads | Graph-based dependency engine |
| "What's ready to work on?" | Beads | Analyzes dependency graph |
| "How long did this take?" | Second Brain | Local time tracking |
| "What were the implementation details?" | Second Brain | Rich markdown notes |
| "What did I work on today?" | Second Brain | Daily work logs |

## Linking Strategies

### Strategy 1: Issue-First

Start with dependency planning in Beads, then create linked tasks:

```bash
# 1. Create epic in Beads
sb epic create "Payment Integration"

# 2. Break down into issues with dependencies
sb issue create "Stripe API Integration" --epic EPIC_ID --with-task --project payments
sb issue create "Payment UI" --epic EPIC_ID --blocks ISSUE_1 --with-task --project payments
sb issue create "Testing" --epic EPIC_ID --blocks ISSUE_2 --with-task --project payments

# 3. Add notes to tasks as you work
sb note create "Stripe API Notes" --task-id 10 --content "..."
```

**When to use:**
- Complex features with many dependencies
- Multi-person projects
- Work that needs dependency visualization

### Strategy 2: Task-First

Start with Second Brain tasks, optionally add issues later:

```bash
# 1. Create task
sb task add "Fix login bug" --project auth

# 2. Work on it, add notes
sb note create "Login Bug Investigation" --task-id 15 --content "..."
sb log add "Fixed session timeout issue" --task-id 15 --time 30

# 3. (Optional) Create issue for dependency tracking
sb task update 15 --with-issue
# Or create issue manually and link
sb issue create "Fix login bug" --external-ref "sb-task-15"
```

**When to use:**
- Small independent tasks
- Bug fixes
- Personal work items
- Quick tasks that don't need dependency tracking

### Strategy 3: Hybrid

Mix and match based on task complexity:

```bash
# Simple task - Second Brain only
sb task add "Update README" --project docs

# Complex feature - Both systems
sb issue create "New Authentication System" \
  --with-task --project auth \
  --description "Migrate from Basic to OAuth2"
```

## CLI Workflows

### Create Issue with Linked Task

```bash
# Create issue and automatically create linked task
sb issue create "Build Analytics Dashboard" \
  --type feature \
  --priority 3 \
  --with-task \
  --project analytics

# Result:
# - Beads issue created: ISSUE_123
# - Second Brain task #45 created with issue_id=ISSUE_123
# - Task linked to 'analytics' project
```

### Create Task with Linked Issue

```bash
# Create task and automatically create linked issue
sb task add "Implement user search" \
  --project users \
  --priority high \
  --with-issue

# Result:
# - Second Brain task #46 created
# - Beads issue ISSUE_124 created with external_ref=sb-task-46
# - Task updated with issue_id=ISSUE_124
```

### Link Existing Task to Issue

```bash
# Manually link existing task to existing issue
sb task update 50 --issue-id ISSUE_125
```

### Find Tasks for an Issue

```bash
# List all tasks
sb task list | grep ISSUE_125

# Or query database directly (future enhancement)
```

## MCP Workflows

### Create Feature with Full Stack

Using MCP tools to create a complete feature:

```python
# 1. Create issue in Beads
issue = await create_issue(
    title="Payment Gateway Integration",
    description="Integrate Stripe payment processing",
    issue_type="feature",
    priority=3,
    with_task=True,
    project_slug="payments"
)

# 2. Add implementation notes
note = await create_note(
    title="Payment Gateway Architecture",
    content="""## Overview

Using Stripe SDK for payment processing.

## Components

- Payment service (backend)
- Payment form (frontend)
- Webhook handler
    """,
    task_id=issue.task_id,  # From the linked task
    tags=["architecture", "payments"]
)

# 3. Track work
await create_work_log_entry(
    entry_text="Started Stripe integration",
    task_id=issue.task_id,
    time_spent_minutes=60
)
```

### Find Ready Work with Context

```python
# 1. Find issues ready to work on
ready_issues = await get_ready_work(limit=10, priority=3)

# 2. For each issue, get linked task and notes
for issue_id in ready_issues:
    # Get issue details
    issue = await get_issue(issue_id)

    # If it has a linked task, get task details
    if issue.external_ref and issue.external_ref.startswith("sb-task-"):
        task_id = int(issue.external_ref.split("-")[2])

        # Get task notes
        notes = await get_notes(task_id=task_id)

        # Get task details
        tasks = await get_tasks(task_id=task_id)

        # Now you have complete context
```

## Decision Tree

Use this decision tree to decide what to create:

```
Need to track dependencies?
├─ Yes → Create Issue in Beads
│   └─ Need rich notes/time tracking?
│       ├─ Yes → Use --with-task flag
│       └─ No → Issue only
└─ No → Create Task in Second Brain
    └─ Might have dependencies later?
        ├─ Yes → Use --with-issue flag
        └─ No → Task only
```

## Common Patterns

### Pattern 1: Epic with Tasks

Break down an epic into tasks with notes:

```bash
# Create epic
sb epic create "Q1 Feature Release" --priority 4

# Create features as issues with tasks
sb issue create "User Profile Page" \
  --epic EPIC_ID \
  --with-task \
  --project frontend

sb issue create "Profile API" \
  --epic EPIC_ID \
  --blocks PROFILE_UI_ISSUE \
  --with-task \
  --project backend

# Add detailed notes to each task
sb note create "Profile Page Design" --task-id TASK_1
sb note create "Profile API Endpoints" --task-id TASK_2
```

### Pattern 2: Bug Fix with Investigation

```bash
# Create bug issue
sb issue create "Slow Query Performance" \
  --type bug \
  --priority 4 \
  --with-task \
  --project database

# Document investigation
sb note create "Query Performance Investigation" \
  --task-id TASK_ID \
  --content "## Observations\n\n- Query takes 5s on production\n- Table has 10M rows..."

# Track work
sb log add "Analyzed slow query" --task-id TASK_ID --time 120

# Add findings as you go
sb note add NOTE_ID "## Solution\n\nAdded index on user_id column"
```

### Pattern 3: Research Task

```bash
# Create research task (no issue needed)
sb task add "Research Vector Databases" --project infrastructure

# Capture findings
sb note create "Vector DB Options" \
  --task-id TASK_ID \
  --tags research,databases \
  --content "## Pinecone\n\nPros:...\n\n## Weaviate\n\nPros:..."

# Track time
sb log add "Researched vector databases" --task-id TASK_ID --time 180
```

### Pattern 4: Multi-Person Feature

```bash
# Create epic
sb epic create "Notifications System"

# Create issues for each person/component
# Alice's work
sb issue create "Email Notifications" \
  --epic EPIC_ID \
  --with-task --project notifications \
  --external-ref "alice"

# Bob's work
sb issue create "Push Notifications" \
  --epic EPIC_ID \
  --blocks EMAIL_ISSUE \
  --with-task --project notifications \
  --external-ref "bob"

# Each person tracks their own work in Second Brain
# Dependencies managed in Beads
```

## Best Practices

### 1. Use External Refs Consistently

When creating issues, use a consistent external_ref pattern:

```bash
# ✅ Good
sb issue create "Task" --external-ref "sb-task-42"
sb issue create "Task" --external-ref "jira-PROJ-123"

# ❌ Bad - hard to query
sb issue create "Task" --external-ref "some random string"
```

### 2. Link at Creation Time

Link systems when creating, not later:

```bash
# ✅ Good - atomic operation
sb issue create "Feature" --with-task --project myproj

# ❌ Tedious - multiple steps
sb issue create "Feature"
sb task add "Feature" --project myproj
sb task update TASK_ID --issue-id ISSUE_ID
```

### 3. One Task Per Issue

Keep the relationship 1:1:

```bash
# ✅ Good - clear mapping
Issue A → Task 1
Issue B → Task 2

# ❌ Confusing - multiple tasks
Issue A → Task 1, Task 2, Task 3
```

### 4. Notes Go on Tasks, Not Issues

Store rich documentation in Second Brain notes:

```bash
# ✅ Good
sb note create "Implementation" --task-id 42

# ❌ Bad - Beads issues have limited description field
sb issue update ISSUE_ID --description "Long documentation..."
```

### 5. Use Beads for "What" and "When", Second Brain for "How"

```bash
# Beads: What needs to be done, what blocks what
sb issue create "API Integration"
sb issue create "Frontend" --blocks API_ISSUE

# Second Brain: How to implement, how long it took
sb note create "API Integration Guide" --task-id TASK_ID
sb log add "Implemented endpoints" --task-id TASK_ID --time 120
```

## Troubleshooting

### Issue and Task Out of Sync

If an issue is closed but task is still open:

```bash
# Update task to match
sb task update TASK_ID --status done
```

### Can't Find Linked Task

If you have an issue but can't find the task:

```bash
# Search by issue ID in task description
sb task list | grep ISSUE_ID

# Or list all tasks and manually check
sb task list
```

### Want to Un-Link

If you need to separate issue and task:

```bash
# Remove issue_id from task
sb task update TASK_ID --issue-id ""

# Or update issue external_ref
sb issue update ISSUE_ID --external-ref ""
```

## Future Enhancements

Planned improvements:

1. **Bi-directional sync**: Auto-update task status when issue closes
2. **Smart queries**: `sb task list --issue-id ISSUE_ID`
3. **Link explorer**: `sb link show TASK_ID` to see full chain
4. **Bulk linking**: Link multiple tasks to issues at once
5. **Status sync**: Keep task and issue status in sync

## See Also

- [Notes Documentation](notes.md)
- [Epics and Dependencies](epics-and-dependencies.md)
- [CLI Reference](cli-reference.md)
- [MCP Server](mcp-server.md)
