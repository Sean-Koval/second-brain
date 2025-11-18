Help the user get a birds-eye view of all their projects using the Second Brain CLI.

Commands to run:
```bash
# 1. List all active projects
sb project list --status active

# 2. For each active project (up to 5), get status
sb project status PROJECT_SLUG

# 3. List recently completed projects
sb project list --status completed
```

Execute these commands and create an overview:

**🗂️ Projects Overview**

**Active Projects (X):**

For each active project:
1. Run `sb project status PROJECT_SLUG`
2. Summarize key information:
   - **Project Name** (slug)
   - Description (brief)
   - Task breakdown: X todo, X in_progress, X done
   - Active work: List 2-3 current tasks
   - Blockers if any

Example output format:
```
📌 Mobile App Redesign (mobile-app-redesign)
   Complete UI/UX overhaul with new design system

   Tasks: 3 todo, 2 in_progress, 8 done (13 total)

   Active:
   - #15: Implement new navigation (in_progress)
   - #18: Design user profile screen (in_progress)

   Recently completed:
   - #12: Create design mockups
   - #14: Set up build pipeline
```

**Recently Completed Projects:**
[From completed projects list]
- List with completion indicators
- Brief summary of what was achieved

**📊 Overall Statistics:**

Calculate from all the data:
- Total active projects: X
- Total tasks across all projects: X
- In-progress tasks: X
- Blocked tasks: X

**💡 Recommendations:**

Analyze the data and suggest:
- Projects with many blocked tasks (need attention)
- Projects close to completion (push to finish)
- Projects with no activity (consider archiving or refocusing)
- Balance of work across projects

If too many active projects (>5):
```
⚠️ You have X active projects. Consider:
- Focusing on top priorities
- Archiving inactive projects
- Reviewing and consolidating efforts
```

**Quick Actions:**
```bash
# Deep dive into a specific project
sb project status PROJECT_SLUG

# See all tasks for a project
sb task list --project PROJECT_SLUG

# Focus on high-priority work
sb task list --priority high --status todo
```

This overview is perfect for:
- Weekly planning sessions
- Quarterly reviews
- Identifying what needs focus
- Balancing multiple initiatives
