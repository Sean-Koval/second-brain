Help the user find and filter tasks using the Second Brain CLI.

The CLI command is:
```bash
sb task list [OPTIONS]
```

Options:
- `-p, --project SLUG` - Filter by project
- `--status STATUS` - Filter by status (todo, in_progress, done, blocked)
- `--priority PRIORITY` - Filter by priority (low, medium, high, urgent)

Ask the user what they're looking for:
1. Specific project? (optional)
2. Task status? (optional)
3. Priority level? (optional)

If they're not sure, show them a menu of common searches:
```bash
# All in-progress tasks
sb task list --status in_progress

# High-priority items
sb task list --priority high

# Tasks for specific project
sb task list --project mobile-app-redesign

# Blocked tasks needing attention
sb task list --status blocked

# High-priority todos (urgent work)
sb task list --priority high --status todo

# Everything
sb task list
```

Then construct and show them the appropriate command:

Examples:
```bash
# Find all in-progress work
sb task list --status in_progress

# Find high-priority tasks
sb task list --priority high

# Find tasks for a project
sb task list --project api-v2-migration

# Combine filters - high-priority in-progress items
sb task list --priority high --status in_progress

# Find blocked tasks across all projects
sb task list --status blocked

# All done tasks (recent accomplishments)
sb task list --status done

# Project-specific todos
sb task list --project mobile-app-redesign --status todo
```

The output will show:
- Task ID (important for updates!)
- Status with emoji (⬜ todo, 🔄 in_progress, ✅ done, 🚫 blocked)
- Task title
- Priority
- Associated project

**Using Task IDs:**

Once you find tasks, use the IDs with other commands:
```bash
# Start working on a task
sb task update TASK_ID --status in_progress

# Log work on a task
sb log add "Description" --task-id TASK_ID --time MINUTES

# Mark as done
sb task update TASK_ID --status done
```

**Common Workflows:**

Morning routine - find what to work on:
```bash
# Check in-progress work
sb task list --status in_progress

# Check high-priority todos
sb task list --priority high --status todo
```

Project focus:
```bash
# See all project tasks
sb task list --project PROJECT_SLUG

# Just the active ones
sb task list --project PROJECT_SLUG --status in_progress
sb task list --project PROJECT_SLUG --status todo
```

Debugging blockers:
```bash
# Find all blocked tasks
sb task list --status blocked

# Then unblock or create tasks to unblock them
```

After showing results, offer to:
- Execute the command for them
- Help with next actions based on what was found
- Refine the search with different filters
- Show how to update found tasks
