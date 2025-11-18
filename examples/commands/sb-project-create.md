Help the user create a new project using the Second Brain CLI.

The CLI command is:
```bash
sb project create "project name" [OPTIONS]
```

Options:
- `-d, --description TEXT` - Project description
- `--jira KEY` - Jira project key (optional, only if they use Jira)
- `--tags TEXT` - Comma-separated tags

Ask the user:
1. What is the project name? (required)
2. Brief description? (optional but recommended)
3. Any tags for organization? (optional, comma-separated)
4. Jira project key if applicable? (optional, only if they use Jira integration)

Then construct and show them the command:

Examples:
```bash
# Simple project
sb project create "Mobile App Redesign"

# With description
sb project create "API v2 Migration" \
  --description "Migrate all services to new API architecture"

# With tags for organization
sb project create "Documentation Update" \
  --tags "docs,low-priority,maintenance"

# With Jira integration
sb project create "Backend Refactor" \
  --description "Refactor backend services for better performance" \
  --jira BACKEND \
  --tags "backend,refactoring"
```

After creating a project, the user can:
- List all projects: `sb project list`
- Get project status: `sb project status PROJECT_SLUG`
- Create tasks for it: `sb task add "task" --project PROJECT_SLUG`

The project slug is auto-generated from the name:
- "Mobile App Redesign" → `mobile-app-redesign`
- "API v2 Migration" → `api-v2-migration`

After showing the command, offer to:
- Execute it for them if they confirm
- Tell them the generated slug for future reference
- Explain where the project markdown file will be saved (data/projects/SLUG.md)
- Suggest creating initial tasks with `/sb-task-create`

The project file can be edited directly in their editor for detailed notes!
