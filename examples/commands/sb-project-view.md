Show a comprehensive visualization of a project with all related content.

This command supports TWO MODES:

## Quick Mode (with arguments)

```
/sb-project-view backend-api
/sb-project-view mobile-app
```

## Conversational Mode (no arguments)

If no project specified, ask:
1. Which project would you like to view? (show list of active projects to choose from)

## What to Show

Gather and present a comprehensive project overview using multiple MCP tools:

### 1. Project Details
Use `get_project_status(project_slug)` to get:
- Project name, description, tags
- Status (active/completed/archived)
- Created/updated dates

### 2. Tasks Summary
Use `get_tasks(project_slug=project_slug)` to get:
- Total tasks count
- Breakdown by status (todo, in_progress, done, blocked)
- Breakdown by priority
- Active tasks with IDs

### 3. Recent Work Logs
Use `get_work_logs(start_date, end_date)` and filter by project:
- Recent work activity (last 7-14 days)
- Time spent on project
- Active contributors

### 4. Project Notes
Use `get_notes(project_slug=project_slug)` to get:
- All notes linked to this project
- Important decisions, architecture docs
- Meeting notes

### 5. Linked Issues (if any)
Use `list_issues()` and filter by external_ref containing project slug:
- Beads issues linked to project tasks
- Epic status if part of larger initiative

## Output Format

Present in a structured, visual format:

```
╔════════════════════════════════════════════════════════════╗
║ 📦 PROJECT: Backend API (backend-api)                      ║
╚════════════════════════════════════════════════════════════╝

📋 Status: Active
📅 Created: 2025-01-01
🏷️  Tags: backend, api, microservices
📝 Description: REST API service for user management and authentication

─────────────────────────────────────────────────────────────

📊 TASKS OVERVIEW

Total: 24 tasks

By Status:
  ✅ Done:         12 tasks (50%)
  🚧 In Progress:   5 tasks (21%)
  📝 Todo:          6 tasks (25%)
  🚫 Blocked:       1 task  (4%)

By Priority:
  🔴 Urgent:     2 tasks
  🟠 High:       8 tasks
  🟡 Medium:    10 tasks
  🟢 Low:        4 tasks

─────────────────────────────────────────────────────────────

🚧 ACTIVE TASKS

#42 [in_progress] Implement Redis caching (high)
    ├─ Time tracked: 4h 30m
    └─ 2 notes attached

#55 [in_progress] Fix authentication bug (urgent)
    ├─ Time tracked: 2h 15m
    ├─ Linked issue: BACK-123
    └─ 1 note attached

#67 [in_progress] API rate limiting (high)
    └─ Time tracked: 3h 00m

─────────────────────────────────────────────────────────────

⏱️  RECENT ACTIVITY (Last 7 Days)

Total time tracked: 18h 45m

2025-01-17
  • Completed Redis cluster configuration (90m) [Task #42]
  • Investigating auth timeout issue (45m) [Task #55]

2025-01-16
  • API rate limiting research (60m) [Task #67]
  • Code review for PR #234 (30m)

2025-01-15
  • Fixed auth session timeout (120m) [Task #55]
  • Redis performance testing (75m) [Task #42]

─────────────────────────────────────────────────────────────

📝 PROJECT NOTES (5 notes)

📄 "Redis Caching Strategy" (2025-01-17)
   Tags: architecture, performance, caching
   Preview: "We decided to use Redis cluster with 3 nodes for high availability..."

📄 "API Design Decisions" (2025-01-14)
   Tags: architecture, design
   Preview: "REST vs GraphQL trade-offs for our use case..."

📄 "Authentication Architecture" (2025-01-12)
   Tags: architecture, security
   Preview: "Using JWT tokens with refresh token rotation..."

📄 "Performance Benchmarks" (2025-01-16)
   Tags: performance, testing
   Preview: "Baseline: 50ms avg response time, Target: <10ms..."

📄 "Meeting Notes - Q1 Planning" (2025-01-10)
   Tags: meeting, planning
   Preview: "Discussed Q1 priorities: caching, rate limiting, auth improvements..."

─────────────────────────────────────────────────────────────

🔗 LINKED ISSUES

Issue BACK-123: "Fix OAuth login timeout"
  Status: In Progress
  Linked to: Task #55
  Dependencies: None

Issue BACK-145: "Implement rate limiting middleware"
  Status: Ready
  Linked to: Task #67
  Dependencies: None

─────────────────────────────────────────────────────────────

📈 PROJECT HEALTH

Status: 🟢 On Track

Strengths:
  • Good progress: 50% tasks completed
  • Active development: 5 tasks in progress
  • Well documented: 5 project notes

Concerns:
  • 1 blocked task - needs attention
  • 2 urgent tasks - should be prioritized

Recommendations:
  • Unblock task or reassign
  • Focus on urgent tasks #55 and #67
  • Consider closing completed tasks

─────────────────────────────────────────────────────────────
```

## Follow-up Actions

After showing the project view, offer to:
- Drill down into a specific task
- Show details of a specific note
- Create a new task for this project
- Generate a project report for sharing
- Update project status
- View linked issues in detail

## CLI Commands

If using CLI instead of MCP:

```bash
# Project status (includes tasks, time)
sb project status backend-api

# Get project tasks
sb task list --project backend-api

# Get project notes
sb note list --project backend-api

# Get work logs (manually filter by project)
sb log show --days 7
```

## Usage Examples

```
User: /sb-project-view backend-api

Agent: [Gathers all data and shows comprehensive view above]

User: "Show me more details on task #42"

Agent: [Uses /sb-task-view 42]
```

```
User: /sb-project-view

Agent: "Which project would you like to view?"
       [Shows list of active projects]

User: "backend-api"

Agent: [Shows comprehensive view]
```

## Pro Tips

- Use this command for:
  - Daily standup prep
  - Weekly project reviews
  - Onboarding new team members
  - Handoff documentation
  - Manager updates

- Combine with export:
  - Ask agent to save the view as a markdown report
  - Great for async updates
