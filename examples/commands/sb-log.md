Help the user add a work log entry using the Second Brain CLI.

This command supports TWO MODES:

## Quick Mode (with arguments)
If the user provides arguments after the command, parse them and execute immediately.

Examples:
```
/sb-log "Fixed authentication bug" --task-id 42 --time 90
/sb-log "Code review" --time 30
/sb-log "Emergency production fix" --task-id 15 --time 120 --date 2025-01-15
```

Parse the arguments and construct the CLI command directly:
```bash
sb log add "entry text" [--task-id ID] [--time MINUTES] [--date YYYY-MM-DD]
```

## Conversational Mode (no arguments)
If the user just types `/sb-log` with no arguments, ask questions:

1. What did you work on? (required)
2. Should this be linked to a task? If yes, ask for task ID (optional)
3. How much time did you spend in minutes? (optional)
4. Is this for today or a different date? (optional - defaults to today)

Then construct and show them the command:

Examples:
```bash
# Simple entry
sb log add "Fixed authentication bug in production"

# With task link and time tracking
sb log add "Implemented user profile API" --task-id 12 --time 120

# For a specific date
sb log add "Emergency production fix" --date 2025-01-15 --time 60

# All options
sb log add "Code review session" --task-id 8 --time 45 --date 2025-01-16
```

If the user wants to see recent work logs:
```bash
# Show last 7 days
sb log show

# Show last 30 days
sb log show --days 30

# Show just today
sb log show --days 1
```

After showing the command, offer to:
- Execute it for them if they confirm
- Explain what the command will do
- Show them where the log will be saved (data/work_logs/YYYY-MM-DD.md)
