Help the user see what they're currently working on using the Second Brain CLI.

This combines several commands to give a quick status check:

Commands to run:
```bash
# 1. Show in-progress tasks
sb task list --status in_progress

# 2. Show today's work log
sb log show --days 1

# 3. Show high-priority todos
sb task list --priority high --status todo
```

Execute these commands and present a summary:

**🔄 In Progress:**
[Output from first command - tasks being actively worked on]

**✏️ Today's Work Log:**
[Output from second command - what's been logged today]

**⚡ High Priority Todos:**
[Output from third command - urgent items needing attention]

Then provide suggestions based on what you see:

If NO tasks are in progress:
- Suggest: "Ready to start work! Here are your high-priority todos..."
- Offer to help them start a task: `/sb-task-update`

If MULTIPLE tasks are in progress:
- Suggest: "You have X tasks in progress. Consider focusing on one at a time."
- Offer to help move some back to 'todo' status

If NO work logged today yet:
- Remind: "Don't forget to log your work as you go with `/sb-log`"

Offer quick next actions:
```bash
# Start working on a task
sb task update TASK_ID --status in_progress

# Log current work
sb log add "What you're working on" --task-id TASK_ID --time MINUTES

# See all your tasks
sb task list
```

This is perfect for:
- Starting your work day
- Coming back from a break
- Quick status check
- Refocusing after interruptions
