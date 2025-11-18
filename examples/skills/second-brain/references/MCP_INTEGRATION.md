# MCP Integration Reference

Complete reference for using Second Brain with AI agents via Model Context Protocol (MCP) server.

## Contents

- [Overview](#overview)
- [MCP Server Setup](#mcp-server-setup)
- [Available Tools](#available-tools)
- [Tool Usage Examples](#tool-usage-examples)
- [Query Patterns](#query-patterns)
- [Best Practices](#best-practices)

---

## Overview

The Second Brain MCP server enables AI agents (Claude, Gemini, etc.) to query and update your work data. It provides tools for:

- **Querying** - List tasks, projects, work logs, notes, issues
- **Creating** - Add work logs, create tasks, projects, notes, epics, issues
- **Updating** - Update task status, add dependencies, link items
- **Analyzing** - Generate reports, find ready work, search content

**Key advantage over CLI:** AI agents can query complex data patterns and analyze your work history to answer questions.

---

## MCP Server Setup

### Claude Code

**Configuration file:** `~/.config/claude-code/mcp.json`

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/home/user/.local/share/uv/tools/second-brain/bin/python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/home/user/.second-brain"
      }
    }
  }
}
```

### Claude Desktop

**Configuration file:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/home/user/.local/share/uv/tools/second-brain/bin/python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/home/user/.second-brain"
      }
    }
  }
}
```

**Verify installation:**
1. Restart Claude Code or Claude Desktop
2. Ask: "Use Second Brain to show my projects"
3. Should see MCP tool calls in the response

---

## Available Tools

### Work Log Tools

#### `list_work_logs`
```python
list_work_logs(
    days: int = 7,
    project_slug: Optional[str] = None
) -> str
```

**Purpose:** Retrieve work log entries

**Example:**
```
"Show me what I worked on last week"
# Uses: list_work_logs(days=7)

"What have I done on the backend-api project this month?"
# Uses: list_work_logs(days=30, project_slug="backend-api")
```

#### `add_work_log`
```python
add_work_log(
    text: str,
    task_id: Optional[int] = None,
    time_minutes: Optional[int] = None,
    date: Optional[str] = None
) -> str
```

**Purpose:** Create new work log entry

**Example:**
```
"Log that I implemented OAuth integration, spent 2 hours on task 42"
# Uses: add_work_log(
#   text="Implemented OAuth integration",
#   task_id=42,
#   time_minutes=120
# )
```

---

### Task Tools

#### `list_tasks`
```python
list_tasks(
    status: Optional[str] = None,
    project_slug: Optional[str] = None,
    priority: Optional[str] = None
) -> str
```

**Purpose:** Query tasks with filters

**Status values:** `todo`, `in_progress`, `done`, `blocked`

**Priority values:** `low`, `medium`, `high`, `urgent`

**Example:**
```
"What tasks am I currently working on?"
# Uses: list_tasks(status="in_progress")

"Show high priority tasks for backend-api"
# Uses: list_tasks(priority="high", project_slug="backend-api")
```

#### `create_task`
```python
create_task(
    title: str,
    project_slug: Optional[str] = None,
    description: Optional[str] = None,
    priority: str = "medium",
    tags: Optional[List[str]] = None
) -> str
```

**Purpose:** Create new task

**Example:**
```
"Create a high priority task to implement rate limiting for the API project"
# Uses: create_task(
#   title="Implement rate limiting",
#   project_slug="backend-api",
#   priority="high"
# )
```

#### `update_task`
```python
update_task(
    task_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    time_minutes: Optional[int] = None
) -> str
```

**Purpose:** Update task status, priority, or add time

**Example:**
```
"Mark task 42 as done and add 3 hours of time"
# Uses: update_task(task_id=42, status="done", time_minutes=180)
```

#### `get_task_details`
```python
get_task_details(task_id: int) -> str
```

**Purpose:** Get complete task information including notes and work logs

**Example:**
```
"Tell me everything about task 42"
# Uses: get_task_details(task_id=42)
```

---

### Project Tools

#### `list_projects`
```python
list_projects(
    status: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> str
```

**Purpose:** List all projects with optional filters

**Example:**
```
"Show me all active projects"
# Uses: list_projects(status="active")

"What projects are tagged with 'backend'?"
# Uses: list_projects(tags=["backend"])
```

#### `create_project`
```python
create_project(
    name: str,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> str
```

**Purpose:** Create new project

**Example:**
```
"Create a project called Mobile App Redesign"
# Uses: create_project(
#   name="Mobile App Redesign",
#   description="Complete UI/UX overhaul",
#   tags=["mobile", "design"]
# )
```

#### `get_project_status`
```python
get_project_status(project_slug: str) -> str
```

**Purpose:** Get detailed project status including tasks, time, recent activity

**Example:**
```
"How is the backend-api project going?"
# Uses: get_project_status(project_slug="backend-api")
```

---

### Note Tools

#### `list_notes`
```python
list_notes(
    task_id: Optional[int] = None,
    project_slug: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> str
```

**Purpose:** List notes with filters

**Example:**
```
"Show notes for task 42"
# Uses: list_notes(task_id=42)

"What notes are tagged with 'research'?"
# Uses: list_notes(tags=["research"])
```

#### `search_notes`
```python
search_notes(query: str) -> str
```

**Purpose:** Full-text search across all notes

**Example:**
```
"Search my notes for 'authentication'"
# Uses: search_notes(query="authentication")
```

#### `create_note`
```python
create_note(
    title: str,
    content: str,
    task_id: Optional[int] = None,
    project_slug: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> str
```

**Purpose:** Create new markdown note

**Example:**
```
"Create a note about our API architecture decision for the backend project"
# Uses: create_note(
#   title="API Architecture",
#   content="Using REST over GraphQL because...",
#   project_slug="backend-api",
#   tags=["architecture", "design"]
# )
```

---

### Epic & Issue Tools (Beads Integration)

#### `create_epic_with_project`
```python
create_epic_with_project(
    title: str,
    description: str = "",
    priority: int = 2,
    labels: Optional[List[str]] = None,
    jira_project_key: Optional[str] = None
) -> str
```

**Purpose:** Create epic and project together (RECOMMENDED for new initiatives)

**Example:**
```
"Create an epic and project for Payment Integration, priority 4"
# Uses: create_epic_with_project(
#   title="Payment Integration",
#   description="Integrate Stripe for payments",
#   priority=4,
#   labels=["backend", "payments"]
# )
```

#### `create_epic`
```python
create_epic(
    title: str,
    description: str = "",
    priority: int = 2,
    labels: Optional[List[str]] = None
) -> str
```

**Purpose:** Create epic only (use create_epic_with_project instead when possible)

#### `create_issue`
```python
create_issue(
    title: str,
    description: str = "",
    issue_type: str = "task",
    priority: int = 2,
    epic_id: Optional[str] = None,
    labels: Optional[List[str]] = None,
    with_task: bool = False,
    project_slug: Optional[str] = None
) -> str
```

**Purpose:** Create issue, optionally under epic and with linked task

**Example:**
```
"Create an issue for OAuth integration under epic-042, with a linked task in the auth project"
# Uses: create_issue(
#   title="OAuth integration",
#   epic_id="epic-042",
#   priority=4,
#   with_task=True,
#   project_slug="user-authentication"
# )
```

#### `list_ready_issues`
```python
list_ready_issues(
    priority: Optional[int] = None,
    limit: int = 10
) -> str
```

**Purpose:** Find issues with no blockers (ready to work on)

**Example:**
```
"What critical work is ready to start?"
# Uses: list_ready_issues(priority=4)

"Find me some work to do"
# Uses: list_ready_issues()
```

#### `get_issue_details`
```python
get_issue_details(issue_id: str) -> str
```

**Purpose:** Get complete issue information including dependencies

**Example:**
```
"Tell me about epic-042"
# Uses: get_issue_details(issue_id="epic-042")
```

---

### Report Tools

#### `generate_work_report`
```python
generate_work_report(
    days: int = 7,
    project_slug: Optional[str] = None
) -> str
```

**Purpose:** Generate comprehensive work report

**Example:**
```
"Generate a weekly report"
# Uses: generate_work_report(days=7)

"Show me a quarterly report for the backend-api project"
# Uses: generate_work_report(days=90, project_slug="backend-api")
```

---

## Tool Usage Examples

### Query Patterns

**1. "What should I work on next?"**
```python
# AI agent uses:
ready_issues = list_ready_issues(priority=4)
in_progress = list_tasks(status="in_progress")

# Then analyzes context and recommends
```

**2. "Summarize my week"**
```python
# AI agent uses:
work_logs = list_work_logs(days=7)
completed_tasks = list_tasks(status="done")
report = generate_work_report(days=7)

# Then synthesizes into summary
```

**3. "What have I been working on for the backend project?"**
```python
# AI agent uses:
project_status = get_project_status(project_slug="backend-api")
work_logs = list_work_logs(days=30, project_slug="backend-api")
tasks = list_tasks(project_slug="backend-api")

# Then creates comprehensive overview
```

**4. "Find my notes about authentication"**
```python
# AI agent uses:
notes = search_notes(query="authentication")

# Then formats results
```

---

### Create Patterns

**1. "Log today's work: implemented OAuth, 2 hours on task 42"**
```python
# AI agent uses:
add_work_log(
    text="Implemented OAuth integration",
    task_id=42,
    time_minutes=120
)
```

**2. "Start a new feature called Payment System"**
```python
# AI agent uses:
create_epic_with_project(
    title="Payment System",
    description="Integrate Stripe payments",
    priority=4,
    labels=["backend", "payments"]
)

# Then suggests next steps:
# - Create issues under epic
# - Create tasks in project
# - Add notes
```

**3. "Create a high priority task to fix the login bug"**
```python
# AI agent uses:
create_task(
    title="Fix login timeout bug",
    priority="urgent",
    description="Users getting logged out after 5 minutes"
)
```

---

## Best Practices

### When to Use MCP vs CLI

**Use MCP tools when:**
- User asks questions about their work ("What did I do?", "What's next?")
- Need to analyze patterns or trends
- Complex queries requiring multiple data sources
- Conversational interaction ("Tell me about...", "Find...")

**Use CLI when:**
- User explicitly wants to run commands
- Scripting or automation
- Lower context usage matters
- Direct, explicit operations

**Both work! Choose based on:**
- User preference
- Context efficiency
- Task complexity

---

### Query Optimization

**Good query:**
```
"Show high priority tasks for backend-api that are in progress"
# Single focused MCP call: list_tasks(status="in_progress", priority="high", project_slug="backend-api")
```

**Bad query:**
```
# AI agent calling multiple tools when one would work
list_tasks()  # Gets all tasks
# Then filters in memory instead of using parameters
```

**Tip:** Use tool parameters to filter data at the source.

---

### Work Log Quality

When creating work logs via MCP, ensure:
- Specific descriptions (what was done, not just "worked on")
- Link to tasks when relevant
- Track time for significant work (30+ min)
- Include outcomes ("Tests passing", "Deployed to staging")

**Good:**
```python
add_work_log(
    text="Implemented OAuth2 flow with JWT tokens (RS256). Added refresh token rotation. Tests passing.",
    task_id=42,
    time_minutes=180
)
```

**Bad:**
```python
add_work_log(
    text="worked on stuff",
    time_minutes=120
)
```

---

### Error Handling

If an MCP tool fails:
1. Check that `SECOND_BRAIN_DIR` is set correctly
2. Verify Second Brain is initialized: `sb --version`
3. Check that resources exist (project slugs, task IDs, etc.)
4. Review error message for specific issue

**Common errors:**
- `ProjectNotFoundError` - Check project slug spelling
- `TaskNotFoundError` - Verify task ID exists
- `BeadsNotInitializedError` - Run `bd init` in `~/.second-brain/`

---

## Complete Tool Reference

| Category | Tool | Purpose |
|----------|------|---------|
| **Work Logs** |||
|| `list_work_logs` | Query work log entries |
|| `add_work_log` | Create work log entry |
| **Tasks** |||
|| `list_tasks` | Query tasks with filters |
|| `create_task` | Create new task |
|| `update_task` | Update task status/priority |
|| `get_task_details` | Get complete task info |
| **Projects** |||
|| `list_projects` | Query projects |
|| `create_project` | Create new project |
|| `get_project_status` | Get project details |
| **Notes** |||
|| `list_notes` | Query notes |
|| `search_notes` | Full-text search |
|| `create_note` | Create markdown note |
|| `get_note_details` | Get note content |
| **Epics/Issues** |||
|| `create_epic_with_project` | Create epic + project (RECOMMENDED) |
|| `create_epic` | Create epic only |
|| `create_issue` | Create issue |
|| `list_ready_issues` | Find unblocked work |
|| `get_issue_details` | Get issue info |
|| `add_issue_dependency` | Add dependency |
|| `get_issue_stats` | Get project stats |
| **Reports** |||
|| `generate_work_report` | Generate work summary |

---

## Related Documentation

- **[CLI Reference](CLI_REFERENCE.md)** - Complete CLI command reference
- **[Workflows](WORKFLOWS.md)** - Step-by-step workflow examples
- **[Slash Commands](SLASH_COMMANDS.md)** - Claude Code slash command guide
