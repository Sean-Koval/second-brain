Help the user update a task's status, priority, or time tracking using the Second Brain CLI.

The CLI command is:
```bash
sb task update TASK_ID [OPTIONS]
```

Options:
- `--status CHOICE` - Status: todo, in_progress, done, blocked
- `--priority CHOICE` - Priority: low, medium, high, urgent
- `--time MINUTES` - Add time spent in minutes (cumulative)

First, if the user doesn't know the task ID, help them find it:
```bash
# List all tasks with IDs
sb task list

# List in-progress tasks
sb task list --status in_progress

# List tasks for a specific project
sb task list --project PROJECT_SLUG
```

Then ask what they want to update:
1. Which task ID?
2. Change status? (todo, in_progress, done, blocked)
3. Add time spent? (in minutes)
4. Change priority? (low, medium, high, urgent)

Show them the command:

Examples:
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

Common workflows:
```bash
# Start your work day
sb task update 15 --status in_progress

# During work, track time
sb task update 15 --time 60

# Finish the task
sb task update 15 --status done --time 30
```

After showing the command, offer to:
- Execute it for them if they confirm
- Show them the updated task details
- Suggest logging work with `/sb-log` to add notes

Note: Time tracking is cumulative - each --time adds to the total!
