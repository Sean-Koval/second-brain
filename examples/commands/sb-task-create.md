Help the user create a new task using the Second Brain CLI.

This command supports TWO MODES:

## Quick Mode (with arguments)
If the user provides arguments after the command, parse them and execute immediately.

Examples:
```
/sb-task-create "Implement rate limiting" --project backend-api --priority high
/sb-task-create "Update docs" --project docs --tags documentation,quick
/sb-task-create "Fix login bug" --description "Users can't login with OAuth" --priority urgent --with-issue
```

Parse the arguments and construct the CLI command directly:
```bash
sb task add "task title" [OPTIONS]
```

Options:
- `-p, --project SLUG` - Link to a project
- `-d, --description TEXT` - Task description
- `--priority CHOICE` - Priority: low, medium, high, urgent
- `--tags TAG1,TAG2` - Comma-separated tags
- `--with-issue` - Create linked Beads issue
- `--issue-id ID` - Link to existing Beads issue

## Conversational Mode (no arguments)
If the user just types `/sb-task-create` with no arguments, ask the user:

1. What is the task title? (required)
2. Which project should this be linked to? (provide the project slug, optional)
3. What priority level? (low, medium, high, urgent - optional)
4. Any description? (optional)
5. Should this create a linked Beads issue? (optional)

Then construct and show them the command:

Examples:
```bash
# Simple task
sb task add "Write unit tests for auth module"

# With project and priority
sb task add "Implement caching layer" --project api-v2-migration --priority high

# With all options
sb task add "Fix memory leak in worker process" \
  --project backend-refactor \
  --description "Memory usage grows unbounded in long-running workers" \
  --priority urgent
```

After creating a task, the user can:
- View all tasks: `sb task list`
- View tasks for a project: `sb task list --project PROJECT_SLUG`
- View by status: `sb task list --status in_progress`
- View by priority: `sb task list --priority high`

After showing the command, offer to:
- Execute it for them if they confirm
- Show them how to find the task ID after creation
- Suggest next steps (starting work with `/sb-task-update`)

Note: The command will output the task ID - they should save this for future reference!
