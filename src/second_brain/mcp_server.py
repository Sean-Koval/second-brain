"""MCP server for Second Brain work tracking."""

import os
from pathlib import Path
from fastmcp import FastMCP

from .db import init_db
from .config import get_config
from .tools.work_log import create_work_log_entry_tool, get_work_logs_tool
from .tools.projects import (
    create_project_tool,
    get_projects_tool,
    create_task_tool,
    update_task_tool,
    get_tasks_tool,
)
from .tools.reports import generate_report_tool, get_project_status_tool
from .tools.jira_sync import sync_jira_issues_tool, get_jira_issue_tool
from .tools.transcripts import (
    create_transcript_tool,
    update_transcript_tool,
    get_transcripts_tool,
    get_transcript_content_tool,
)
from .tools.epics import (
    create_epic_tool,
    create_issue_tool,
    update_issue_tool,
    close_issue_tool,
    get_issue_tool,
    list_issues_tool,
    list_epics_tool,
    add_dependency_tool,
    get_ready_work_tool,
    get_stats_tool,
)
from .tools.notes import (
    create_note_tool,
    append_to_note_tool,
    update_note_tool,
    get_notes_tool,
    get_note_tool,
    search_notes_tool,
)

# Initialize MCP server
mcp = FastMCP("second-brain")

# Get configuration
config = get_config()

# Ensure data directory exists
config.ensure_directories()

# Initialize database
engine = init_db(str(config.db_path))


# Register work log tools
@mcp.tool()
async def create_work_log_entry(
    entry_text: str,
    task_id: int | None = None,
    time_spent_minutes: int | None = None,
    date: str | None = None,
) -> str:
    """
    Add an entry to the daily work log.

    Args:
        entry_text: The work log entry text
        task_id: Optional task ID to link this entry to
        time_spent_minutes: Time spent in minutes (optional)
        date: Date for the entry (YYYY-MM-DD), defaults to today
    """
    from .tools.work_log import WorkLogEntryInput

    input_data = WorkLogEntryInput(
        entry_text=entry_text,
        task_id=task_id,
        time_spent_minutes=time_spent_minutes,
        date=date,
    )
    tool_func = create_work_log_entry_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_work_logs(start_date: str, end_date: str) -> str:
    """
    Retrieve work logs for a specific date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    from .tools.work_log import WorkLogQueryInput

    input_data = WorkLogQueryInput(start_date=start_date, end_date=end_date)
    tool_func = get_work_logs_tool(engine)
    return await tool_func(input_data)


# Register project and task tools
@mcp.tool()
async def create_project(
    name: str,
    description: str | None = None,
    jira_project_key: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """
    Create a new project with markdown file and database entry.

    Args:
        name: Project name
        description: Project description
        jira_project_key: Jira project key (e.g., PROJ)
        tags: List of tags
    """
    from .tools.projects import ProjectCreateInput

    input_data = ProjectCreateInput(
        name=name,
        description=description,
        jira_project_key=jira_project_key,
        tags=tags,
    )
    tool_func = create_project_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_projects(
    status: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """
    Query projects with optional filters.

    Args:
        status: Filter by status (active, completed, archived)
        tags: Filter by tags
    """
    from .tools.projects import ProjectQueryInput

    input_data = ProjectQueryInput(status=status, tags=tags)
    tool_func = get_projects_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def create_task(
    title: str,
    description: str | None = None,
    project_slug: str | None = None,
    priority: str | None = None,
    tags: list[str] | None = None,
    issue_id: str | None = None,
    with_issue: bool = False,
) -> str:
    """
    Create a new task, optionally linked to a project and/or Beads issue.

    Args:
        title: Task title
        description: Task description
        project_slug: Project slug to associate with
        priority: Priority (low, medium, high, urgent)
        tags: List of tags
        issue_id: Link to existing Beads issue ID
        with_issue: Create a linked Beads issue
    """
    from .tools.projects import TaskCreateInput

    input_data = TaskCreateInput(
        title=title,
        description=description,
        project_slug=project_slug,
        priority=priority,
        tags=tags,
        issue_id=issue_id,
        with_issue=with_issue,
    )
    tool_func = create_task_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    time_spent_minutes: int | None = None,
) -> str:
    """
    Update an existing task's properties.

    Args:
        task_id: Task ID to update
        title: New title
        description: New description
        status: New status (todo, in_progress, done, blocked)
        priority: New priority
        time_spent_minutes: Add time spent in minutes
    """
    from .tools.projects import TaskUpdateInput

    input_data = TaskUpdateInput(
        task_id=task_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        time_spent_minutes=time_spent_minutes,
    )
    tool_func = update_task_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_tasks(
    project_slug: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """
    Query tasks with optional filters.

    Args:
        project_slug: Filter by project slug
        status: Filter by status
        priority: Filter by priority
        tags: Filter by tags
    """
    from .tools.projects import TaskQueryInput

    input_data = TaskQueryInput(
        project_slug=project_slug,
        status=status,
        priority=priority,
        tags=tags,
    )
    tool_func = get_tasks_tool(engine)
    return await tool_func(input_data)


# Register report tools
@mcp.tool()
async def generate_report(
    start_date: str,
    end_date: str,
    project_slug: str | None = None,
    include_time_spent: bool = True,
) -> str:
    """
    Generate a comprehensive work report for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        project_slug: Filter by project slug (optional)
        include_time_spent: Include time tracking information
    """
    from .tools.reports import ReportInput

    input_data = ReportInput(
        start_date=start_date,
        end_date=end_date,
        project_slug=project_slug,
        include_time_spent=include_time_spent,
    )
    tool_func = generate_report_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_project_status(project_slug: str) -> str:
    """
    Get detailed status and analytics for a specific project.

    Args:
        project_slug: Project slug
    """
    tool_func = get_project_status_tool(engine)
    return await tool_func(project_slug)


# Register Jira tools
@mcp.tool()
async def sync_jira_issues(
    project_slug: str | None = None,
    status_filter: str | None = None,
) -> str:
    """
    Synchronize Jira issues to local tasks.

    Args:
        project_slug: Project slug to sync (syncs all projects if not specified)
        status_filter: Filter by issue status (optional)
    """
    from .tools.jira_sync import JiraSyncInput

    input_data = JiraSyncInput(project_slug=project_slug, status_filter=status_filter)
    tool_func = sync_jira_issues_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_jira_issue(issue_key: str) -> str:
    """
    Fetch a specific Jira issue by key.

    Args:
        issue_key: Jira issue key (e.g., PROJ-123)
    """
    from .tools.jira_sync import JiraIssueInput

    input_data = JiraIssueInput(issue_key=issue_key)
    tool_func = get_jira_issue_tool(engine)
    return await tool_func(input_data)


# Register transcript tools
@mcp.tool()
async def create_transcript(
    title: str,
    raw_content: str,
    transcript_type: str = "call",
    transcript_date: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """
    Create a new call/meeting transcript.

    Args:
        title: Transcript title
        raw_content: Raw transcript text
        transcript_type: Type of transcript (call, meeting, etc.)
        transcript_date: Date of transcript (YYYY-MM-DD), defaults to today
        tags: List of tags
    """
    from .tools.transcripts import TranscriptCreateInput

    input_data = TranscriptCreateInput(
        title=title,
        raw_content=raw_content,
        transcript_type=transcript_type,
        transcript_date=transcript_date,
        tags=tags,
    )
    tool_func = create_transcript_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def update_transcript(
    transcript_id: int,
    summary: str | None = None,
    action_items: str | None = None,
    linked_projects: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """
    Update a transcript with processed information.

    Args:
        transcript_id: Transcript ID to update
        summary: Summary of the transcript
        action_items: Action items (JSON string)
        linked_projects: Comma-separated list of project IDs to link
        tags: Updated tags
    """
    from .tools.transcripts import TranscriptUpdateInput

    input_data = TranscriptUpdateInput(
        transcript_id=transcript_id,
        summary=summary,
        action_items=action_items,
        linked_projects=linked_projects,
        tags=tags,
    )
    tool_func = update_transcript_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_transcripts(
    transcript_type: str | None = None,
    tags: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    """
    Query transcripts with optional filters.

    Args:
        transcript_type: Filter by type
        tags: Filter by tags
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    from .tools.transcripts import TranscriptQueryInput

    input_data = TranscriptQueryInput(
        transcript_type=transcript_type,
        tags=tags,
        start_date=start_date,
        end_date=end_date,
    )
    tool_func = get_transcripts_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_transcript_content(transcript_id: int) -> str:
    """
    Get the full content of a specific transcript.

    Args:
        transcript_id: Transcript ID
    """
    tool_func = get_transcript_content_tool(engine)
    return await tool_func(transcript_id)


# Register note tools
@mcp.tool()
async def create_note(
    title: str,
    content: str = "",
    project_slug: str | None = None,
    task_id: int | None = None,
    tags: list[str] | None = None,
) -> str:
    """
    Create a new note with markdown content.

    Args:
        title: Note title
        content: Note content (markdown)
        project_slug: Optional project slug to attach note to
        task_id: Optional task ID to attach note to
        tags: Optional list of tags
    """
    from .tools.notes import NoteCreateInput

    input_data = NoteCreateInput(
        title=title,
        content=content,
        project_slug=project_slug,
        task_id=task_id,
        tags=tags,
    )
    tool_func = create_note_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def append_to_note(note_id: int, content: str) -> str:
    """
    Append content to an existing note.

    Args:
        note_id: Note ID
        content: Content to append (markdown)
    """
    from .tools.notes import NoteAppendInput

    input_data = NoteAppendInput(note_id=note_id, content=content)
    tool_func = append_to_note_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def update_note(
    note_id: int,
    title: str | None = None,
    content: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """
    Update an existing note's properties.

    Args:
        note_id: Note ID to update
        title: New title
        content: New content (markdown)
        tags: New tags
    """
    from .tools.notes import NoteUpdateInput

    input_data = NoteUpdateInput(note_id=note_id, title=title, content=content, tags=tags)
    tool_func = update_note_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_notes(
    project_slug: str | None = None,
    task_id: int | None = None,
    tags: list[str] | None = None,
) -> str:
    """
    Query notes with optional filters.

    Args:
        project_slug: Filter by project slug
        task_id: Filter by task ID
        tags: Filter by tags
    """
    from .tools.notes import NoteQueryInput

    input_data = NoteQueryInput(project_slug=project_slug, task_id=task_id, tags=tags)
    tool_func = get_notes_tool(engine)
    return await tool_func(input_data)


@mcp.tool()
async def get_note(note_id: int) -> str:
    """
    Get the full content of a specific note.

    Args:
        note_id: Note ID
    """
    tool_func = get_note_tool(engine)
    return await tool_func(note_id)


@mcp.tool()
async def search_notes(query: str) -> str:
    """
    Search notes by title or content.

    Args:
        query: Search query
    """
    from .tools.notes import NoteSearchInput

    input_data = NoteSearchInput(query=query)
    tool_func = search_notes_tool(engine)
    return await tool_func(input_data)


# Register epic and issue tools
@mcp.tool()
async def create_epic(
    title: str,
    description: str = "",
    priority: int = 2,
    labels: list[str] | None = None,
) -> str:
    """
    Create a new epic for organizing large initiatives.

    Args:
        title: Epic title
        description: Epic description
        priority: Priority 0-4 (0=lowest, 4=highest)
        labels: List of labels/tags
    """
    from .tools.epics import EpicCreateInput

    input_data = EpicCreateInput(
        title=title,
        description=description,
        priority=priority,
        labels=labels,
    )
    tool_func = create_epic_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def create_issue(
    title: str,
    description: str = "",
    issue_type: str = "task",
    priority: int = 2,
    parent_epic_id: str | None = None,
    blocks: list[str] | None = None,
    labels: list[str] | None = None,
    external_ref: str | None = None,
    with_task: bool = False,
    project_slug: str | None = None,
) -> str:
    """
    Create a new issue (task, bug, feature, etc.), optionally with a linked Second Brain task.

    Args:
        title: Issue title
        description: Issue description
        issue_type: Type: bug, feature, task, epic, chore
        priority: Priority 0-4 (0=lowest, 4=highest)
        parent_epic_id: ID of parent epic (creates parent-child dependency)
        blocks: List of issue IDs this issue blocks
        labels: List of labels/tags
        external_ref: External reference (e.g., Jira ticket, GitHub issue)
        with_task: Create a linked Second Brain task
        project_slug: Project slug for linked task (used with with_task)
    """
    from .tools.epics import IssueCreateInput

    input_data = IssueCreateInput(
        title=title,
        description=description,
        issue_type=issue_type,
        priority=priority,
        parent_epic_id=parent_epic_id,
        blocks=blocks,
        labels=labels,
        external_ref=external_ref,
        with_task=with_task,
        project_slug=project_slug,
    )
    tool_func = create_issue_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def update_issue(
    issue_id: str,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,
    priority: int | None = None,
) -> str:
    """
    Update an existing issue's properties.

    Args:
        issue_id: Issue ID to update
        title: New title
        description: New description
        status: New status: open, in_progress, blocked, closed
        priority: New priority 0-4
    """
    from .tools.epics import IssueUpdateInput

    input_data = IssueUpdateInput(
        issue_id=issue_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
    )
    tool_func = update_issue_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def close_issue(issue_id: str, reason: str = "Completed") -> str:
    """
    Close an issue with a reason.

    Args:
        issue_id: Issue ID to close
        reason: Reason for closing
    """
    from .tools.epics import IssueCloseInput

    input_data = IssueCloseInput(issue_id=issue_id, reason=reason)
    tool_func = close_issue_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def get_issue(issue_id: str) -> str:
    """
    Retrieve detailed information about an issue.

    Args:
        issue_id: Issue ID
    """
    from .tools.epics import IssueQueryInput

    input_data = IssueQueryInput(issue_id=issue_id)
    tool_func = get_issue_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def list_issues(
    status: str | None = None,
    issue_type: str | None = None,
    priority: int | None = None,
    limit: int = 50,
) -> str:
    """
    Query issues with optional filters.

    Args:
        status: Filter by status: open, in_progress, blocked, closed
        issue_type: Filter by type: bug, feature, task, epic, chore
        priority: Filter by priority 0-4
        limit: Max number of issues to return
    """
    from .tools.epics import IssuesListInput

    input_data = IssuesListInput(
        status=status,
        issue_type=issue_type,
        priority=priority,
        limit=limit,
    )
    tool_func = list_issues_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def list_epics(
    status: str | None = None,
    limit: int = 50,
) -> str:
    """
    Query epics with optional filters.

    Args:
        status: Filter by status
        limit: Max number to return
    """
    from .tools.epics import EpicsListInput

    input_data = EpicsListInput(status=status, limit=limit)
    tool_func = list_epics_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def add_dependency(
    issue_id: str,
    depends_on_id: str,
    dep_type: str = "blocks",
) -> str:
    """
    Add a dependency relationship between two issues.

    Args:
        issue_id: Issue that has the dependency
        depends_on_id: Issue that is depended on
        dep_type: Type: blocks, related, parent-child, discovered-from
    """
    from .tools.epics import DependencyAddInput

    input_data = DependencyAddInput(
        issue_id=issue_id,
        depends_on_id=depends_on_id,
        dep_type=dep_type,
    )
    tool_func = add_dependency_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def get_ready_work(
    limit: int = 10,
    priority: int | None = None,
) -> str:
    """
    Find issues that are ready to work on right now.

    Args:
        limit: Max number of issues to return
        priority: Filter by priority
    """
    from .tools.epics import ReadyWorkInput

    input_data = ReadyWorkInput(limit=limit, priority=priority)
    tool_func = get_ready_work_tool(str(config.data_dir))
    return await tool_func(input_data)


@mcp.tool()
async def get_epic_stats() -> str:
    """
    Get project statistics and overview for epics/issues.
    """
    tool_func = get_stats_tool(str(config.data_dir))
    return await tool_func()


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
