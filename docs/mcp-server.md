# MCP Server Tools Reference

Complete reference for all MCP server tools that AI agents can use to interact with your Second Brain.

> **Works Offline**: All tools work offline except `sync_jira_issues` and `get_jira_issue`.

## Overview

The Second Brain MCP server provides 15 tools organized into 6 categories:

1. **Work Logs** - Daily work tracking
2. **Projects** - Project management
3. **Tasks** - Task tracking and updates
4. **Reports** - Analytics and summaries
5. **Jira** - Jira integration (optional)
6. **Transcripts** - Meeting/call transcript processing

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
