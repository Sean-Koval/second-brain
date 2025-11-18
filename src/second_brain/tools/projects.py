"""MCP tools for project and task operations."""

from typing import Optional, List
from pydantic import BaseModel, Field

from ..db import get_session
from ..db.operations import ProjectOps, TaskOps
from ..storage import StorageIndexer


class ProjectCreateInput(BaseModel):
    """Input for creating a project."""

    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    jira_project_key: Optional[str] = Field(None, description="Jira project key (e.g., PROJ)")
    tags: Optional[List[str]] = Field(None, description="List of tags")


class ProjectQueryInput(BaseModel):
    """Input for querying projects."""

    status: Optional[str] = Field(None, description="Filter by status (active, completed, archived)")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")


class TaskCreateInput(BaseModel):
    """Input for creating a task."""

    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    project_slug: Optional[str] = Field(None, description="Project slug to associate with")
    priority: Optional[str] = Field(None, description="Priority (low, medium, high, urgent)")
    tags: Optional[List[str]] = Field(None, description="List of tags")
    issue_id: Optional[str] = Field(None, description="Link to existing Beads issue ID")
    with_issue: bool = Field(False, description="Create a linked Beads issue")


class TaskUpdateInput(BaseModel):
    """Input for updating a task."""

    task_id: int = Field(..., description="Task ID to update")
    title: Optional[str] = Field(None, description="New title")
    description: Optional[str] = Field(None, description="New description")
    status: Optional[str] = Field(None, description="New status (todo, in_progress, done, blocked)")
    priority: Optional[str] = Field(None, description="New priority")
    time_spent_minutes: Optional[int] = Field(None, description="Add time spent in minutes")


class TaskQueryInput(BaseModel):
    """Input for querying tasks."""

    project_slug: Optional[str] = Field(None, description="Filter by project slug")
    status: Optional[str] = Field(None, description="Filter by status")
    priority: Optional[str] = Field(None, description="Filter by priority")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")


def create_project_tool(engine):
    """Create a new project tool."""

    async def create_project(project: ProjectCreateInput) -> str:
        """
        Create a new project with markdown file and database entry.

        Projects are the top-level organizational unit in the second brain.
        Each project gets its own markdown file for notes and a database entry
        for fast querying.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            new_project = indexer.create_project(
                name=project.name,
                description=project.description,
                jira_project_key=project.jira_project_key,
                tags=project.tags,
            )

            tags_str = f", tags: {', '.join(project.tags)}" if project.tags else ""
            jira_str = f", Jira: {project.jira_project_key}" if project.jira_project_key else ""

            return (
                f"Project created successfully!\n"
                f"Name: {new_project.name}\n"
                f"Slug: {new_project.slug}\n"
                f"Markdown file: {new_project.markdown_path}{jira_str}{tags_str}"
            )
        finally:
            session.close()

    return create_project


def get_projects_tool(engine):
    """Get projects with optional filters tool."""

    async def get_projects(query: ProjectQueryInput) -> str:
        """
        Query projects with optional filters.

        Retrieve all projects or filter by status and tags. Useful for
        getting an overview of active work or finding specific projects.
        """
        session = get_session(engine)
        try:
            projects = ProjectOps.list_all(session, status=query.status, tags=query.tags)

            if not projects:
                filters = []
                if query.status:
                    filters.append(f"status={query.status}")
                if query.tags:
                    filters.append(f"tags={','.join(query.tags)}")
                filter_str = f" with filters: {', '.join(filters)}" if filters else ""
                return f"No projects found{filter_str}"

            result = f"Found {len(projects)} project(s):\n\n"

            for p in projects:
                result += f"**{p.name}** (#{p.id}, slug: {p.slug})\n"
                result += f"  Status: {p.status}\n"
                if p.description:
                    result += f"  Description: {p.description}\n"
                if p.jira_project_key:
                    result += f"  Jira: {p.jira_project_key}\n"
                if p.tags:
                    result += f"  Tags: {p.tags}\n"

                # Count tasks
                task_count = len(p.tasks)
                if task_count > 0:
                    active_tasks = sum(1 for t in p.tasks if t.status in ["todo", "in_progress"])
                    result += f"  Tasks: {active_tasks} active / {task_count} total\n"

                result += "\n"

            return result
        finally:
            session.close()

    return get_projects


def create_task_tool(engine):
    """Create a new task tool."""

    async def create_task(task: TaskCreateInput) -> str:
        """
        Create a new task, optionally linked to a project and/or Beads issue.

        Tasks represent individual work items. They can be standalone or
        linked to a project, and can be associated with Beads issues for
        dependency tracking.
        """
        session = get_session(engine)
        try:
            # Get project if slug provided
            project_id = None
            if task.project_slug:
                project = ProjectOps.get_by_slug(session, task.project_slug)
                if project:
                    project_id = project.id
                else:
                    return f"Error: Project with slug '{task.project_slug}' not found"

            new_task = TaskOps.create(
                session,
                title=task.title,
                description=task.description,
                project_id=project_id,
                priority=task.priority,
                tags=",".join(task.tags) if task.tags else None,
                issue_id=task.issue_id,
            )

            project_str = ""
            if project_id:
                project = ProjectOps.get_by_id(session, project_id)
                project_str = f"\nProject: {project.name}"

            priority_str = f"\nPriority: {task.priority}" if task.priority else ""
            tags_str = f"\nTags: {', '.join(task.tags)}" if task.tags else ""

            result = (
                f"Task created successfully!\n"
                f"ID: {new_task.id}\n"
                f"Title: {new_task.title}{project_str}{priority_str}{tags_str}\n"
                f"Status: {new_task.status}"
            )

            # Create linked Beads issue if requested
            if task.with_issue:
                from ..integrations.beads_integration import get_beads_client

                client = get_beads_client()
                if client:
                    try:
                        # Map priority to Beads priority (0-4)
                        priority_map = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
                        beads_priority = priority_map.get(task.priority, 2)

                        issue = await client.create_issue(
                            title=task.title,
                            description=task.description or "",
                            issue_type="task",
                            priority=beads_priority,
                            external_ref=f"sb-task-{new_task.id}",
                        )

                        # Update task with issue_id
                        TaskOps.update(session, new_task, issue_id=issue.id)

                        result += f"\n\nLinked Beads issue created: {issue.id}"
                        result += f"\nExternal ref: sb-task-{new_task.id}"
                    except Exception as e:
                        result += f"\n\nWarning: Failed to create Beads issue: {e}"
                else:
                    result += "\n\nWarning: Beads integration not available"

            if task.issue_id:
                result += f"\nLinked to Beads issue: {task.issue_id}"

            return result
        finally:
            session.close()

    return create_task


def update_task_tool(engine):
    """Update an existing task tool."""

    async def update_task(update: TaskUpdateInput) -> str:
        """
        Update an existing task's properties.

        Modify task details including status, priority, and time tracking.
        Use this to track progress and manage task lifecycle.
        """
        session = get_session(engine)
        try:
            task = TaskOps.get_by_id(session, update.task_id)
            if not task:
                return f"Error: Task with ID {update.task_id} not found"

            # Prepare update dict
            updates = {}
            if update.title is not None:
                updates["title"] = update.title
            if update.description is not None:
                updates["description"] = update.description
            if update.status is not None:
                updates["status"] = update.status
            if update.priority is not None:
                updates["priority"] = update.priority
            if update.time_spent_minutes is not None:
                updates["time_spent_minutes"] = task.time_spent_minutes + update.time_spent_minutes

            if not updates:
                return "No updates provided"

            updated_task = TaskOps.update(session, task, **updates)

            result = f"Task #{updated_task.id} updated successfully!\n"
            result += f"Title: {updated_task.title}\n"
            result += f"Status: {updated_task.status}\n"
            if updated_task.priority:
                result += f"Priority: {updated_task.priority}\n"
            if updated_task.time_spent_minutes > 0:
                hours = updated_task.time_spent_minutes // 60
                minutes = updated_task.time_spent_minutes % 60
                result += f"Total time spent: {hours}h {minutes}m\n"

            return result
        finally:
            session.close()

    return update_task


def get_tasks_tool(engine):
    """Get tasks with optional filters tool."""

    async def get_tasks(query: TaskQueryInput) -> str:
        """
        Query tasks with optional filters.

        Retrieve tasks filtered by project, status, priority, or tags.
        Useful for getting current workload, finding specific tasks, or
        generating task lists.
        """
        session = get_session(engine)
        try:
            tasks = []

            if query.project_slug:
                project = ProjectOps.get_by_slug(session, query.project_slug)
                if not project:
                    return f"Error: Project with slug '{query.project_slug}' not found"
                tasks = TaskOps.list_by_project(session, project.id, status=query.status)
            else:
                tasks = TaskOps.list_all(
                    session, status=query.status, priority=query.priority, tags=query.tags
                )

            if not tasks:
                return "No tasks found matching the criteria"

            result = f"Found {len(tasks)} task(s):\n\n"

            for t in tasks:
                status_emoji = {
                    "todo": "⬜",
                    "in_progress": "🔄",
                    "done": "✅",
                    "blocked": "🚫",
                }.get(t.status, "⬜")

                result += f"{status_emoji} **{t.title}** (#{t.id})\n"
                result += f"  Status: {t.status}"

                if t.priority:
                    result += f" | Priority: {t.priority}"

                if t.project:
                    result += f" | Project: {t.project.name}"

                result += "\n"

                if t.description:
                    # Truncate long descriptions
                    desc = t.description[:100] + "..." if len(t.description) > 100 else t.description
                    result += f"  Description: {desc}\n"

                if t.jira_ticket_key:
                    result += f"  Jira: {t.jira_ticket_key}\n"

                if t.time_spent_minutes > 0:
                    hours = t.time_spent_minutes // 60
                    minutes = t.time_spent_minutes % 60
                    result += f"  Time spent: {hours}h {minutes}m\n"

                result += "\n"

            return result
        finally:
            session.close()

    return get_tasks
