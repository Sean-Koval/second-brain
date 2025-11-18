Help the user conduct a comprehensive weekly review using the Second Brain CLI.

Perfect for Friday afternoon wrap-up and planning!

Commands to run:
```bash
# 1. Generate weekly work report
sb report work --days 7

# 2. List all active projects
sb project list --status active

# 3. Show in-progress tasks
sb task list --status in_progress

# 4. Show blocked tasks
sb task list --status blocked

# 5. Show work logs from the week
sb log show --days 7
```

Execute these commands and create a structured review:

**📊 Weekly Review** (date range)

**Summary Statistics:**
[From the report command]
- Work days logged: X
- Tasks completed: X
- Total time tracked: X hours
- Active projects: X

**✅ Accomplishments This Week:**
[From report, list completed tasks grouped by project]
- Highlight significant achievements
- Note any major milestones

**🔄 In Progress:**
[From task list with status in_progress]
- What's currently being worked on
- Estimated completion for each

**🚫 Blockers:**
[From task list with status blocked]
- List any blocked tasks
- Ask what's blocking them
- Offer to help create tasks to unblock

**📈 Project Breakdown:**
[For each active project, run:]
```bash
sb project status PROJECT_SLUG
```
Show progress and status for each

**💭 Reflection Prompts:**

Ask the user:
1. What went well this week?
2. What could be improved?
3. Any patterns in how time was spent?
4. Were there unexpected challenges?
5. What should be prioritized next week?

**📅 Planning for Next Week:**

Suggest actions:
```bash
# Create tasks for next week's goals
sb task add "Next week goal 1" --priority high

# Review high-priority todos
sb task list --priority high --status todo

# Check project statuses
sb project list --status active
```

Recommend focus areas based on:
- In-progress work to complete
- Blocked items to unblock
- High-priority todos

**📄 Save the Review:**
```bash
# Save to file for records
sb report work --days 7 > weekly-review-$(date +%Y-%m-%d).md
```

End with:
- Motivational summary of the week's progress
- Encouragement for next week
- Reminder to rest and recharge!

This structured review helps close the week cleanly and start Monday prepared!
