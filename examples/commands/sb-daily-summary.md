Help the user create an end-of-day summary using the Second Brain CLI.

Perfect for wrapping up your work day!

Commands to run:
```bash
# 1. Show today's work log
sb log show --days 1

# 2. List all tasks
sb task list

# 3. Filter to see what was completed
# (Look for tasks with status 'done' in the output)
```

Execute these commands and create a summary:

**📅 Today's Summary** (current date)

**Work Logged:**
[Show all work log entries from today's output]
- List with timestamps
- Show linked tasks if any
- Calculate total time tracked

**Tasks Completed:**
[From task list, identify any marked as 'done' today]
- List completed tasks
- Celebrate achievements!

**In Progress:**
[From task list, show status 'in_progress']
- What's actively being worked on
- Good candidates to continue tomorrow

**Stats:**
- Work entries logged: X
- Time tracked: X hours X minutes
- Tasks completed: X

**💡 End of Day Actions:**

If they haven't marked tasks as done:
```bash
# Mark a task as complete
sb task update TASK_ID --status done

# Add final time if needed
sb task update TASK_ID --status done --time 30
```

If they want to add a final log entry:
```bash
# Add end-of-day summary
sb log add "Wrapped up work on X, ready for tomorrow's Y"
```

Encourage them with positive feedback about their progress!

Suggest for tomorrow:
- Review in-progress tasks
- Check high-priority todos: `sb task list --priority high --status todo`
- Plan the day with `/sb-current-work`

This helps maintain momentum and clear mental context for the next day!
