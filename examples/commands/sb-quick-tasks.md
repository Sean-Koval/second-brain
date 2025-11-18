Guide the user through managing small, quick tasks efficiently.

Perfect for bugs, quick fixes, and small improvements that don't need full issue tracking!

## When to Use Quick Tasks

Use simple tasks (without issues) for:
- Bug fixes that take < 2 hours
- Documentation updates
- Small code improvements
- Quick refactors
- Configuration changes
- Urgent hotfixes

**Don't overthink it!** Not everything needs an epic and dependencies.

## Creating Quick Tasks

```bash
# Simple task - just title and project
sb task add "Update README with API examples" --project docs

# With priority
sb task add "Fix typo in error message" \
  --project backend \
  --priority low

# With description
sb task add "Add logging to auth endpoint" \
  --project backend \
  --description "Need better visibility into auth failures" \
  --priority medium

# With tags for organization
sb task add "Upgrade dependencies" \
  --project maintenance \
  --tags dependencies,security
```

## Quick Task Workflow

**Morning: Quick wins**

```bash
# List quick tasks (filter by tags, priority)
sb task list --tags quick,small
sb task list --priority low

# Pick one and start
sb task update TASK_ID --status in_progress

# Log start
sb log add "Started README updates" --task-id TASK_ID
```

**During: Fast execution**

```bash
# Work on it (no need for elaborate notes)

# Log completion
sb log add "Updated README with 3 API examples" \
  --task-id TASK_ID \
  --time 30

# Mark done
sb task update TASK_ID --status done
```

That's it! Total time: 5 minutes of admin for 30 minutes of work.

## Batch Quick Tasks

**Create multiple at once:**

```bash
# Create a batch of small tasks
sb task add "Fix button alignment" --project frontend --tags ui,quick
sb task add "Add error handling to webhook" --project backend --tags bugs,quick
sb task add "Update changelog" --project docs --tags docs,quick

# View your quick tasks
sb task list --tags quick
```

**Power through them:**

```bash
# Work through 3-4 quick tasks in one session

# Task 1
sb task update TASK1 --status in_progress
# ... work ...
sb log add "Fixed button alignment" --task-id TASK1 --time 15
sb task update TASK1 --status done

# Task 2
sb task update TASK2 --status in_progress
# ... work ...
sb log add "Added error handling" --task-id TASK2 --time 25
sb task update TASK2 --status done

# Task 3
sb task update TASK3 --status in_progress
# ... work ...
sb log add "Updated changelog" --task-id TASK3 --time 10
sb task update TASK3 --status done

# Review what you crushed
sb task list --status done | tail -3
```

## Quick Task Categories

### 1. Documentation Tasks

```bash
sb task add "Document deployment process" \
  --project docs \
  --tags documentation,runbook

sb task add "Add JSDoc comments to auth module" \
  --project backend \
  --tags documentation,code

# After completion, optionally create a note if needed
sb note create "Deployment Runbook" \
  --task-id TASK_ID \
  --content "## Steps..."
```

### 2. Dependency Updates

```bash
sb task add "Upgrade FastAPI to 0.110" \
  --project backend \
  --tags dependencies,upgrade

# When doing it
sb log add "Upgraded FastAPI, ran tests, all passing" \
  --task-id TASK_ID \
  --time 20
```

### 3. Bug Fixes (Simple Ones)

```bash
sb task add "Fix date formatting in reports" \
  --project frontend \
  --tags bug,ui \
  --priority high

# If bug is simple, just log the fix
sb log add "Fixed date formatting, used correct locale" \
  --task-id TASK_ID \
  --time 15

sb task update TASK_ID --status done
```

**Note:** For complex bugs, use the bug investigation workflow instead!

### 4. Refactoring

```bash
sb task add "Extract validation logic into util function" \
  --project backend \
  --tags refactor,code-quality

sb task add "Rename confusing variable names in payment.py" \
  --project backend \
  --tags refactor,readability
```

### 5. Configuration

```bash
sb task add "Update staging environment variables" \
  --project devops \
  --tags config,environment

sb task add "Increase rate limit for API" \
  --project backend \
  --tags config,performance
```

## When Quick Tasks Grow

**If a "quick task" gets complex:**

```bash
# Started as quick task
sb task add "Fix login redirect" --project auth

# During work, realize it's complex
# Option 1: Convert to issue with --with-issue
sb task update TASK_ID --with-issue

# Option 2: Create investigation note
sb note create "Login Redirect Investigation" \
  --task-id TASK_ID \
  --content "Turns out this is more complex than thought..."

# Option 3: Create separate issue and link
sb issue create "Fix login redirect loop" --external-ref "sb-task-TASK_ID"
```

**Red flags a task isn't quick:**
- Taking > 2 hours
- Needs multiple files changed
- Has dependencies on other work
- Affects multiple systems
- Requires testing in staging
- Needs coordination with others

When you see these, consider creating an issue!

## Organization Strategies

### Strategy 1: Tag Everything

```bash
# Use consistent tags
--tags quick          # < 30 min
--tags small          # 30-60 min
--tags medium         # 1-2 hours

--tags bug,quick
--tags docs,quick
--tags refactor,quick
```

### Strategy 2: Priority-Based

```bash
# Use priority for ordering
sb task add "..." --priority low      # Nice to have
sb task add "..." --priority medium   # Should do
sb task add "..." --priority high     # Must do
sb task add "..." --priority urgent   # ASAP
```

### Strategy 3: Time-Boxing

```bash
# Friday afternoon: Clear out quick tasks
sb task list --tags quick

# Take top 5, power through in 90 minutes
# Track time on each one
```

## Daily Quick Task Routine

**Morning (10 min):**
```bash
# Check for new urgent quick tasks
sb task list --priority urgent --status todo

# Pick 2-3 quick tasks for the day
sb task list --tags quick --priority high
```

**Lunch break (15 min):**
```bash
# Knock out a quick win
sb task list --tags quick | head -1
```

**End of day (15 min):**
```bash
# Close out any quick completions
sb task list --status in_progress | grep quick

# Create any new quick tasks found during day
sb task add "..." --tags quick
```

## Quick Task Metrics

```bash
# At end of week
sb task list --status done --tags quick

# Count completions
sb task list --status done | grep quick | wc -l

# Review time spent on quick tasks
sb report work --days 7 | grep quick
```

## Quick Task Templates

Save these as shell aliases:

```bash
# ~/.bashrc or ~/.zshrc

# Quick bug
alias qbug='function _qbug() { sb task add "$1" --project $2 --tags bug,quick --priority high; }; _qbug'

# Quick docs
alias qdoc='function _qdoc() { sb task add "$1" --project docs --tags docs,quick; }; _qdoc'

# Quick refactor
alias qref='function _qref() { sb task add "$1" --project $2 --tags refactor,quick; }; _qref'

# Usage:
# qbug "Fix null check" backend
# qdoc "Update API guide"
# qref "Rename variables" frontend
```

## Pro Tips

1. **Batch similar tasks** - Do all docs together, all configs together
2. **Time-box strictly** - If taking > planned time, stop and reassess
3. **Log immediately** - Don't wait until end of day
4. **Keep it simple** - Not every task needs notes
5. **Use quick tasks for flow** - Great for context switching
6. **Friday cleanup** - Clear out quick tasks before weekend
7. **Track time** - Even on quick tasks (adds up!)

## Anti-Patterns to Avoid

❌ Creating tasks for 5-minute changes
- Just do it and log to work log directly

❌ Over-documenting quick tasks
- Notes should be for complex things

❌ Never completing quick tasks
- Do them or delete them

❌ Letting quick tasks pile up
- Weekly cleanup needed

❌ Forgetting to track time
- Losing visibility into effort

## When NOT to Use Quick Tasks

Use full issue/epic workflow instead if:
- Work will take > 4 hours
- Multiple people involved
- Has dependencies
- Needs QA/review
- Affects critical systems
- Requires coordination
- Part of larger feature

**Remember:** Quick tasks are for speed and simplicity. If it gets complex, promote it to an issue!
