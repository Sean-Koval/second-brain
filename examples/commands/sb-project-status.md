Help the user get detailed status for a specific project using the Second Brain CLI.

The CLI command is:
```bash
sb project status PROJECT_SLUG
```

If the user doesn't know the project slug:
```bash
# List all projects to find the slug
sb project list

# List only active projects
sb project list --status active
```

Then construct and show them the command:

Examples:
```bash
# Get status for a specific project
sb project status mobile-app-redesign

# Get status for API project
sb project status api-v2-migration
```

The command will show:
- Project name, status, and description
- Total task count
- Task breakdown by status (todo, in_progress, blocked, done)
- List of active tasks (in-progress and high-priority todos)
- Time tracking if available

After showing the command, offer to:
- Execute it for them if they confirm
- Help them with next actions based on the status:
  - If many blocked tasks → offer to help unblock
  - If many todos → suggest prioritizing
  - If project looks complete → suggest marking as completed
- Show related commands:
  ```bash
  # View all project tasks
  sb task list --project PROJECT_SLUG

  # View only in-progress tasks
  sb task list --project PROJECT_SLUG --status in_progress

  # View project markdown file directly
  cat data/projects/PROJECT_SLUG.md
  ```

Tip: Project slugs are auto-generated from names:
- "Mobile App Redesign" → `mobile-app-redesign`
- "API v2" → `api-v2`
- Spaces become dashes, all lowercase
