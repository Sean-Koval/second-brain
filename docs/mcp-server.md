# MCP Server Tools Reference

Complete reference for all MCP server tools that AI agents can use to interact with your Second Brain.

> **Works Offline**: All tools work offline except `sync_jira_issues` and `get_jira_issue`.
>
> **Prerequisite for Epic/Issue Tools**: Run `sb init --beads --prefix SB` in your project directory once before using epic/issue tools.

## Overview

The Second Brain MCP server provides 25+ tools organized into 7 categories:

1. **Work Logs** - Daily work tracking
2. **Projects** - Project management
3. **Tasks** - Task tracking and updates
4. **Epics & Issues** - Dependency tracking and epic management (requires `bd init`)
5. **Reports** - Analytics and summaries
6. **Jira** - Jira integration (optional)
7. **Transcripts** - Meeting/call transcript processing

## Work Log Tools

### `create_work_log_entry`

Add an entry to the daily work log.

**Parameters:**
- `entry_text` (string, required): The work log entry text
- `task_id` (integer, optional): Task ID to link this entry to
- `time_spent_minutes` (integer, optional): Time spent in minutes
- `date` (string, optional): Date in YYYY-MM-DD format (defaults to today)

**Returns:** Confirmation message with entry details

**Example Usage:**
```
Agent call:
{
  "entry_text": "Fixed authentication bug in production",
  "task_id": 15,
  "time_spent_minutes": 90,
  "date": "2025-01-17"
}

Response:
"Work log entry added for 2025-01-17 (linked to task: Fix auth timeout)
Entry: Fixed authentication bug in production"
```

**Use Cases:**
- Recording daily work activities
- Tracking time spent on tasks
- Documenting decisions and progress
- Creating audit trail for work done

---

### `get_work_logs`

Retrieve work logs for a specific date range.

**Parameters:**
- `start_date` (string, required): Start date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format

**Returns:** Formatted work logs with entries and time tracking

**Example Usage:**
```
Agent call:
{
  "start_date": "2025-01-10",
  "end_date": "2025-01-17"
}

Response:
"Work logs from 2025-01-10 to 2025-01-17:

## 2025-01-15
Entries:
  - 09:30: Daily standup
  - 10:00 [Fix auth timeout] (90m): Fixed authentication bug

## 2025-01-16
Entries:
  - 09:45: Code review for PR #234
  - 11:00 [UI redesign] (120m): Implemented new dashboard layout"
```

**Use Cases:**
- Reviewing past work
- Generating weekly summaries
- Preparing status updates
- Time tracking reports

---

## Project Tools

### `create_project`

Create a new project with markdown file and database entry.

**Parameters:**
- `name` (string, required): Project name
- `description` (string, optional): Project description
- `jira_project_key` (string, optional): Jira project key (e.g., "PROJ")
- `tags` (array of strings, optional): List of tags

**Returns:** Confirmation with project details and file path

**Example Usage:**
```
Agent call:
{
  "name": "Mobile App Redesign",
  "description": "Complete UI/UX overhaul with new design system",
  "tags": ["mobile", "frontend", "design"]
}

Response:
"Project created successfully!
Name: Mobile App Redesign
Slug: mobile-app-redesign
Markdown file: data/projects/mobile-app-redesign.md"
```

**Use Cases:**
- Starting new initiatives
- Organizing related work
- Tracking long-term efforts
- Managing multiple concurrent projects

---

### `get_projects`

Query projects with optional filters.

**Parameters:**
- `status` (string, optional): Filter by status (active, completed, archived)
- `tags` (array of strings, optional): Filter by tags

**Returns:** List of projects with details and task counts

**Example Usage:**
```
Agent call:
{
  "status": "active",
  "tags": ["frontend"]
}

Response:
"Found 2 project(s):

**Mobile App Redesign** (#1, slug: mobile-app-redesign)
  Status: active
  Description: Complete UI/UX overhaul
  Tags: mobile, frontend, design
  Tasks: 5 active / 12 total

**Web Dashboard** (#3, slug: web-dashboard)
  Status: active
  Tags: frontend, web
  Tasks: 2 active / 8 total"
```

**Use Cases:**
- Getting overview of active work
- Finding specific projects
- Checking project status
- Organizing work by area

---

### `get_project_status`

Get detailed status and analytics for a specific project.

**Parameters:**
- `project_slug` (string, required): Project slug

**Returns:** Comprehensive project status including tasks, time tracking, and recent activity

**Example Usage:**
```
Agent call:
{
  "project_slug": "mobile-app-redesign"
}

Response:
"# Project Status: Mobile App Redesign

**Slug:** mobile-app-redesign
**Status:** active
**Created:** 2025-01-10

---

## Tasks Overview
**Total Tasks:** 12

**By Status:**
- todo: 5
- in_progress: 2
- done: 5

**Total Time Tracked:** 24h 30m

### Active Tasks
🔄 **Implement new navigation** (#4)
  - Priority: high
⬜ **Design user profile screen** (#5)
  - Priority: medium"
```

**Use Cases:**
- Project status updates
- Planning sessions
- Stakeholder reports
- Progress tracking

---

## Task Tools

### `create_task`

Create a new task, optionally linked to a project.

**Parameters:**
- `title` (string, required): Task title
- `description` (string, optional): Task description
- `project_slug` (string, optional): Project slug to associate with
- `priority` (string, optional): Priority: low, medium, high, urgent
- `tags` (array of strings, optional): List of tags

**Returns:** Confirmation with task ID and details

**Example Usage:**
```
Agent call:
{
  "title": "Implement rate limiting for API",
  "description": "Add rate limiting to prevent abuse",
  "project_slug": "api-v2-migration",
  "priority": "high",
  "tags": ["backend", "security"]
}

Response:
"Task created successfully!
ID: 42
Title: Implement rate limiting for API
Project: API v2 Migration
Priority: high
Tags: backend, security
Status: todo"
```

**Use Cases:**
- Breaking down project work
- Tracking individual items
- Managing backlog
- Creating action items from meetings

---

### `update_task`

Update an existing task's properties.

**Parameters:**
- `task_id` (integer, required): Task ID to update
- `title` (string, optional): New title
- `description` (string, optional): New description
- `status` (string, optional): New status: todo, in_progress, done, blocked
- `priority` (string, optional): New priority: low, medium, high, urgent
- `time_spent_minutes` (integer, optional): Add time spent (cumulative)

**Returns:** Confirmation with updated task details

**Example Usage:**
```
Agent call:
{
  "task_id": 42,
  "status": "done",
  "time_spent_minutes": 180
}

Response:
"Task #42 updated successfully!
Title: Implement rate limiting for API
Status: done
Priority: high
Total time spent: 3h 0m"
```

**Use Cases:**
- Tracking progress
- Time logging
- Status updates
- Managing blockers

---

### `get_tasks`

Query tasks with optional filters.

**Parameters:**
- `project_slug` (string, optional): Filter by project slug
- `status` (string, optional): Filter by status
- `priority` (string, optional): Filter by priority
- `tags` (array of strings, optional): Filter by tags

**Returns:** List of tasks matching filters

**Example Usage:**
```
Agent call:
{
  "status": "in_progress",
  "priority": "high"
}

Response:
"Found 3 task(s):

🔄 **Implement rate limiting** (#42)
  Status: in_progress | Priority: high | Project: API v2 Migration
  Description: Add rate limiting to prevent abuse
  Time spent: 2h 30m

🔄 **Fix memory leak** (#38)
  Status: in_progress | Priority: high | Project: Backend Services
  Jira: BACKEND-234"
```

**Use Cases:**
- Getting current workload
- Finding specific tasks
- Planning daily work
- Checking priorities

---

## Report Tools

### `generate_report`

Generate a comprehensive work report for a date range.

**Parameters:**
- `start_date` (string, required): Start date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format
- `project_slug` (string, optional): Filter by project slug
- `include_time_spent` (boolean, optional): Include time tracking (default: true)

**Returns:** Formatted markdown report with work summary

**Example Usage:**
```
Agent call:
{
  "start_date": "2025-01-01",
  "end_date": "2025-01-31",
  "include_time_spent": true
}

Response:
"# Work Report

**Period:** 2025-01-01 to 2025-01-31

---

## Summary
- Work days logged: 22
- Tasks completed: 34
- Total time tracked: 142h 30m

## Tasks Completed
- **Implement rate limiting** (#42)
  - Project: API v2 Migration
  - Completed: 2025-01-15
  - Time spent: 3h 0m

[... more tasks ...]

## Daily Work Logs
### 2025-01-15
- 09:00: Daily standup
- 10:00 **[Rate limiting]** (180m): Implemented and tested

[... more logs ...]

## Project Breakdown
### API v2 Migration
- Tasks completed: 12
- Time spent: 48h 30m

[... more projects ...]"
```

**Use Cases:**
- Weekly status updates
- Performance reviews
- Promotion documentation
- Time tracking audits
- Project retrospectives

---

## Jira Tools (Optional)

> **Note**: These tools require Jira credentials. All other tools work offline.

### `sync_jira_issues`

Synchronize Jira issues to local tasks.

**Parameters:**
- `project_slug` (string, optional): Sync only this project (default: all with Jira keys)
- `status_filter` (string, optional): Filter by issue status

**Returns:** Summary of synced issues

**Example Usage:**
```
Agent call:
{
  "project_slug": "api-v2-migration",
  "status_filter": "In Progress"
}

Response:
"Syncing API v2 Migration (API)...
  Synced 15 issues

Summary:
- Total issues synced: 15
- Created: 3
- Updated: 12"
```

**Use Cases:**
- Syncing work tickets
- Keeping local tasks up to date
- Linking Jira work to Second Brain
- Team coordination

**Requirements:**
- `JIRA_SERVER` environment variable
- `JIRA_EMAIL` environment variable
- `JIRA_API_TOKEN` environment variable
- Project must have `jira_project_key` configured

---

### `get_jira_issue`

Fetch a specific Jira issue by key.

**Parameters:**
- `issue_key` (string, required): Jira issue key (e.g., "PROJ-123")

**Returns:** Detailed issue information

**Example Usage:**
```
Agent call:
{
  "issue_key": "API-234"
}

Response:
"# API-234: Implement caching layer

**Status:** In Progress
**Priority:** High
**Assignee:** John Doe
**Type:** Story
**Project:** API

## Description
Add Redis caching to reduce database load...

---
**Local Task:** #42 - Implement rate limiting
Status: in_progress"
```

**Use Cases:**
- Fetching ticket details
- Creating local tasks from Jira
- Checking ticket status
- Linking work to Jira issues

**Requirements:**
- Same as `sync_jira_issues`

---

## Epic & Issue Tools

> **Prerequisite**: Run `sb init --beads --prefix SB` once in your project directory before using these tools.

Epic and issue tools provide dependency tracking, blocker detection, and epic management through Beads integration.

### `create_epic`

Create a new epic for organizing large initiatives.

**Parameters:**
- `title` (string, required): Epic title
- `description` (string, optional): Epic description
- `priority` (integer, optional): Priority 0-4 (0=lowest, 4=highest, default: 2)
- `labels` (array of strings, optional): Labels/tags for categorization

**Returns:** Confirmation with epic ID and details

**Example Usage:**
```
Agent call:
{
  "title": "Mobile App Redesign",
  "description": "Complete UI/UX overhaul of mobile app",
  "priority": 4,
  "labels": ["mobile", "design", "q1-2025"]
}

Response:
"Epic created!
ID: SB-1
Title: Mobile App Redesign
Priority: Highest (4)
Labels: mobile, design, q1-2025"
```

**Use Cases:**
- Organizing large multi-issue initiatives
- Planning quarterly objectives
- Tracking feature development
- Grouping related work

---

### `create_epic_with_project`

Create an epic AND a Second Brain project together (RECOMMENDED).

**Parameters:**
- `title` (string, required): Title for both epic and project
- `description` (string, optional): Description for both
- `priority` (integer, optional): Epic priority 0-4 (default: 2)
- `labels` (array of strings, optional): Labels/tags for both

**Returns:** Confirmation with epic ID, project slug, and next steps

**Example Usage:**
```
Agent call:
{
  "title": "Payment Integration",
  "description": "Add Stripe payment processing",
  "priority": 4,
  "labels": ["backend", "payments", "revenue"]
}

Response:
"Epic + Project created successfully!

Epic (Beads):
  ID: SB-5
  Title: Payment Integration
  Priority: Highest (4)
  Status: open
  Labels: backend, payments, revenue

Project (Second Brain):
  ID: 12
  Name: Payment Integration
  Slug: payment-integration
  Tags: backend, payments, revenue

Integration:
  Epic ID: SB-5 ↔️ Project Slug: payment-integration

Next Steps:
  1. Create issues: sb issue create 'Issue Title' --epic SB-5
  2. Create tasks: sb task add 'Task Title' --project payment-integration
  3. Link issues to tasks with --with-task flag
  4. Track work: sb log add 'Work done' --project payment-integration"
```

**Use Cases:**
- Starting new major features/initiatives
- Combining dependency tracking with time/note tracking
- Team collaboration on large projects
- Maintaining context across epic and daily work

---

### `create_issue`

Create a new issue (task, bug, feature, etc.).

**Parameters:**
- `title` (string, required): Issue title
- `description` (string, optional): Issue description
- `issue_type` (string, optional): Type: bug, feature, task, epic, chore (default: "task")
- `priority` (integer, optional): Priority 0-4 (default: 2)
- `parent_epic_id` (string, optional): Parent epic ID (e.g., "SB-1")
- `blocks` (array of strings, optional): Issue IDs this issue blocks
- `labels` (array of strings, optional): Labels/tags
- `external_ref` (string, optional): External reference (Jira key, GitHub issue, etc.)
- `with_task` (boolean, optional): Create linked Second Brain task (default: false)
- `project_slug` (string, optional): Project slug for linked task (required if with_task=true)

**Returns:** Confirmation with issue ID and linked task info (if created)

**Example Usage:**
```
Agent call:
{
  "title": "Implement Stripe webhook handler",
  "description": "Handle payment_intent.succeeded webhook",
  "issue_type": "task",
  "priority": 3,
  "parent_epic_id": "SB-5",
  "labels": ["backend", "webhooks"],
  "with_task": true,
  "project_slug": "payment-integration"
}

Response:
"Issue created!
ID: SB-6
Title: Implement Stripe webhook handler
Type: task
Priority: High (3)
Parent Epic: SB-5

Linked Second Brain task created: #45
  Project: Payment Integration"
```

**Use Cases:**
- Breaking down epics into actionable issues
- Tracking bugs and features
- Creating work with dependencies
- Linking issues to time/note tracking

---

### `update_issue`

Update an existing issue's properties.

**Parameters:**
- `issue_id` (string, required): Issue ID to update (e.g., "SB-6")
- `title` (string, optional): New title
- `description` (string, optional): New description
- `status` (string, optional): New status: open, in_progress, blocked, closed
- `priority` (integer, optional): New priority 0-4

**Returns:** Confirmation with updated details

**Example Usage:**
```
Agent call:
{
  "issue_id": "SB-6",
  "status": "in_progress"
}

Response:
"Issue SB-6 updated!
Title: Implement Stripe webhook handler
Status: in_progress
Priority: High (3)"
```

---

### `close_issue`

Close an issue.

**Parameters:**
- `issue_id` (string, required): Issue ID to close
- `reason` (string, optional): Reason for closing (default: "Completed")

**Returns:** Confirmation message

**Example Usage:**
```
Agent call:
{
  "issue_id": "SB-6",
  "reason": "Implemented and tested successfully"
}

Response:
"Issue SB-6 closed!
Title: Implement Stripe webhook handler
Reason: Implemented and tested successfully"
```

---

### `get_issue`

Get detailed information about a specific issue.

**Parameters:**
- `issue_id` (string, required): Issue ID (e.g., "SB-6")

**Returns:** Detailed issue information including dependencies

**Example Usage:**
```
Agent call:
{
  "issue_id": "SB-6"
}

Response:
"Implement Stripe webhook handler (SB-6)

Type: task
Status: in_progress
Priority: High

Description:
Handle payment_intent.succeeded webhook

Labels: backend, webhooks

Parent Epic: SB-5 (Payment Integration)

Dependencies (2):
  - SB-4: Set up Stripe API client [blocks]
  - SB-5: Payment Integration [parent-child]

Dependents (1):
  - SB-7: Test payment flow"
```

---

### `list_issues`

List issues with optional filtering.

**Parameters:**
- `status` (string, optional): Filter by status (open, in_progress, blocked, closed)
- `issue_type` (string, optional): Filter by type (bug, feature, task, epic, chore)
- `priority` (integer, optional): Filter by priority 0-4
- `limit` (integer, optional): Max number to return (default: 50)

**Returns:** Formatted list of matching issues

**Example Usage:**
```
Agent call:
{
  "status": "open",
  "priority": 4,
  "limit": 10
}

Response:
"Found 3 issue(s):

| ID   | Title                          | Type    | Status | Priority |
|------|--------------------------------|---------|--------|----------|
| SB-3 | Database migration             | task    | ⬜ open | Highest  |
| SB-5 | Payment Integration            | epic    | ⬜ open | Highest  |
| SB-8 | Fix memory leak in API         | bug     | ⬜ open | Highest  |"
```

---

### `list_epics`

List all epics with optional filtering.

**Parameters:**
- `status` (string, optional): Filter by status (open, in_progress, blocked, closed)
- `limit` (integer, optional): Max number to return (default: 50)

**Returns:** Formatted list of epics

**Example Usage:**
```
Agent call:
{
  "status": "open"
}

Response:
"Found 2 epic(s):

| ID   | Title               | Status | Priority |
|------|---------------------|--------|----------|
| SB-1 | Mobile App Redesign | 📋 open | Highest  |
| SB-5 | Payment Integration | 📋 open | Highest  |"
```

---

### `add_dependency`

Add a dependency relationship between two issues.

**Parameters:**
- `issue_id` (string, required): The issue that depends on another
- `depends_on_id` (string, required): The issue that is depended upon
- `dep_type` (string, optional): Dependency type: blocks, related, parent-child, discovered-from (default: "blocks")

**Returns:** Confirmation of dependency relationship

**Example Usage:**
```
Agent call:
{
  "issue_id": "SB-7",
  "depends_on_id": "SB-6",
  "dep_type": "blocks"
}

Response:
"Dependency added!
Type: blocks
Relationship: SB-6 blocks SB-7"
```

**Dependency Types:**
- **blocks**: depends_on_id must complete before issue_id can start
- **related**: Issues are related but no strict ordering
- **parent-child**: depends_on_id is parent of issue_id
- **discovered-from**: issue_id was discovered while working on depends_on_id

---

### `get_ready_work`

Find issues ready to work on (no open blockers).

**Parameters:**
- `limit` (integer, optional): Max number to return (default: 10)
- `priority` (integer, optional): Filter by specific priority

**Returns:** List of unblocked issues sorted by priority

**Example Usage:**
```
Agent call:
{
  "priority": 4,
  "limit": 5
}

Response:
"🎯 Found 2 issue(s) ready to work on:

| ID   | Title                     | Type | Priority |
|------|---------------------------|------|----------|
| SB-3 | Database migration        | task | Highest  |
| SB-8 | Fix memory leak in API    | bug  | Highest  |

💡 These issues have no open blockers and can be started immediately!"
```

**Use Cases:**
- Finding what to work on next
- Sprint planning
- Identifying unblocked work
- Prioritizing daily tasks

---

### `get_epic_stats`

Get project statistics and overview.

**Returns:** Summary of total, open, closed, blocked, and ready issues

**Example Usage:**
```
Agent call: {}

Response:
"📊 Project Statistics

Total Issues: 12
Open: 8
Closed: 4
Blocked: 2
Ready to Work: 6

💡 You have 6 issue(s) ready to work on!"
```

**Use Cases:**
- Project health overview
- Sprint planning
- Status reporting
- Identifying bottlenecks

---

## Transcript Tools

### `create_transcript`

Create a new call/meeting transcript.

**Parameters:**
- `title` (string, required): Transcript title
- `raw_content` (string, required): Raw transcript text
- `transcript_type` (string, optional): Type: call, meeting, etc. (default: "call")
- `transcript_date` (string, optional): Date in YYYY-MM-DD (default: today)
- `tags` (array of strings, optional): List of tags

**Returns:** Confirmation with file paths

**Example Usage:**
```
Agent call:
{
  "title": "Q1 Planning Meeting",
  "raw_content": "Attendees: John, Sarah, Mike\n[00:00] Discussion about roadmap...",
  "transcript_type": "meeting",
  "tags": ["planning", "q1", "roadmap"]
}

Response:
"Transcript created successfully!
ID: 5
Title: Q1 Planning Meeting
Type: meeting
Date: 2025-01-17
Tags: planning, q1, roadmap

Raw file: data/transcripts/raw/2025-01-17_q1-planning-meeting.txt
Processed file: data/transcripts/processed/2025-01-17_q1-planning-meeting.md

Use the update_transcript tool to add summary, action items, and link to projects."
```

**Use Cases:**
- Saving meeting recordings
- Storing call notes
- Archiving important conversations
- Creating searchable transcript library

---

### `update_transcript`

Update a transcript with processed information.

**Parameters:**
- `transcript_id` (integer, required): Transcript ID to update
- `summary` (string, optional): Summary of the transcript
- `action_items` (string, optional): Action items (JSON string)
- `linked_projects` (string, optional): Comma-separated project IDs
- `tags` (array of strings, optional): Updated tags

**Returns:** Confirmation with updated details

**Example Usage:**
```
Agent call:
{
  "transcript_id": 5,
  "summary": "Discussed Q1 roadmap priorities. Focus on API v2 and mobile app.",
  "action_items": "[{\"task\": \"Schedule design review\", \"owner\": \"Sarah\"}]",
  "linked_projects": "1,3"
}

Response:
"Transcript #5 updated successfully!
Title: Q1 Planning Meeting
Summary: Discussed Q1 roadmap priorities. Focus on API v2 and mobile app.
Linked projects: 1,3"
```

**Use Cases:**
- Adding AI-generated summaries
- Extracting action items
- Linking to relevant projects
- Organizing meeting notes

---

### `get_transcripts`

Query transcripts with optional filters.

**Parameters:**
- `transcript_type` (string, optional): Filter by type
- `tags` (array of strings, optional): Filter by tags
- `start_date` (string, optional): Start date in YYYY-MM-DD
- `end_date` (string, optional): End date in YYYY-MM-DD

**Returns:** List of matching transcripts

**Example Usage:**
```
Agent call:
{
  "transcript_type": "meeting",
  "tags": ["planning"],
  "start_date": "2025-01-01",
  "end_date": "2025-01-31"
}

Response:
"Found 3 transcript(s):

## Q1 Planning Meeting (#5)
**Type:** meeting
**Date:** 2025-01-17
**Tags:** planning, q1, roadmap
**Summary:** Discussed Q1 roadmap priorities...
**Raw file:** data/transcripts/raw/2025-01-17_q1-planning-meeting.txt"
```

**Use Cases:**
- Finding past meetings
- Reviewing decisions
- Searching conversations
- Building knowledge base

---

### `get_transcript_content`

Get the full content of a specific transcript.

**Parameters:**
- `transcript_id` (integer, required): Transcript ID

**Returns:** Full transcript with both raw and processed content

**Example Usage:**
```
Agent call:
{
  "transcript_id": 5
}

Response:
"# Q1 Planning Meeting

**ID:** 5
**Type:** meeting
**Date:** 2025-01-17
**Tags:** planning, q1, roadmap

---

## Processed Notes
[Markdown content from processed file...]

---

## Raw Transcript
Attendees: John, Sarah, Mike
[00:00] Discussion about roadmap...
[Full transcript content...]"
```

**Use Cases:**
- Analyzing full transcripts
- Generating summaries
- Extracting information
- Creating action items

---

## Common Agent Workflows

### Daily Standup Recording
```
1. Agent asks: "What did you work on today?"
2. User responds with summary
3. Agent uses: create_work_log_entry
4. Agent links to relevant tasks
5. Agent updates: update_task (status, time)
```

### Project Status Update
```
1. User: "Status of mobile app project?"
2. Agent uses: get_project_status
3. Agent uses: get_tasks (filter by project)
4. Agent summarizes progress and blockers
```

### Weekly Review
```
1. User: "Summarize my week"
2. Agent uses: get_work_logs (last 7 days)
3. Agent uses: get_tasks (completed this week)
4. Agent uses: generate_report
5. Agent formats summary
```

### Meeting Follow-up
```
1. User provides transcript
2. Agent uses: create_transcript
3. Agent analyzes content
4. Agent uses: update_transcript (summary, actions)
5. Agent uses: create_task (for each action item)
6. Agent links tasks to projects
```

### Planning New Initiative
```
1. User: "Start planning payment integration feature"
2. Agent uses: create_epic_with_project (creates epic + project)
3. Agent discusses breakdown with user
4. Agent uses: create_issue (multiple times for sub-tasks)
5. Agent uses: add_dependency (to set blockers)
6. Agent uses: get_ready_work (to show what can start)
```

### Finding Work to Do
```
1. User: "What should I work on next?"
2. Agent uses: get_ready_work (with priority filter)
3. Agent uses: get_issue (for each ready issue to show details)
4. Agent presents options to user
5. User chooses an issue
6. Agent uses: update_issue (status=in_progress)
7. Agent uses: create_task (with_task=true for time tracking)
```

### Epic Breakdown and Execution
```
1. User: "Break down the mobile app redesign epic"
2. Agent uses: get_issue (epic_id) to see current state
3. Agent discusses components with user
4. Agent uses: create_issue (for each component, linked to epic)
5. Agent uses: add_dependency (to set order of work)
6. Agent uses: list_issues (filter by epic) to show all items
7. Agent uses: get_epic_stats to show progress
```

### Checking Project Health
```
1. User: "How's the project looking?"
2. Agent uses: get_epic_stats (overall numbers)
3. Agent uses: list_issues (status=blocked) to see blockers
4. Agent uses: get_ready_work to see available work
5. Agent summarizes: X ready, Y blocked, Z in progress
6. Agent suggests: "Start with SB-5 (no blockers, high priority)"
```

---

## Error Handling

All tools handle errors gracefully:

- **Missing required parameters**: Returns clear error message
- **Invalid IDs**: Returns "not found" message
- **Jira credentials missing**: Returns setup instructions
- **Invalid dates**: Returns format error
- **Database errors**: Returns error details

Example error responses:
```
"Error: Project with slug 'invalid-slug' not found"
"Error: Task with ID 999 not found"
"Error: Jira credentials not configured"
"Error: Invalid date format, use YYYY-MM-DD"
```

---

## Best Practices for Agents

1. **Confirm before bulk operations**: Ask user before creating many tasks
2. **Provide context**: Show what was created/updated
3. **Use filters effectively**: Don't fetch all data when filtering is available
4. **Link related items**: Connect tasks to projects, work logs to tasks
5. **Format output**: Use markdown for better readability
6. **Handle errors**: Provide helpful messages when operations fail
7. **Suggest next steps**: Guide users on what they can do next

---

## Testing MCP Tools

You can test the MCP server directly:

```bash
# Start the server
python -m second_brain.mcp_server

# The server communicates via stdio
# Use an MCP client or Claude Desktop/Code to test
```

Or test programmatically:
```python
from second_brain.tools.work_log import WorkLogEntryInput, create_work_log_entry_tool
from second_brain.db import init_db, get_session

engine = init_db("test.db")
tool = create_work_log_entry_tool(engine)

entry = WorkLogEntryInput(
    entry_text="Test entry",
    time_spent_minutes=30
)

result = await tool(entry)
print(result)
```
