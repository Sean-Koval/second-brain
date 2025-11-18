"""MCP tools for epic and issue operations using Beads integration."""

from typing import Optional, List
from pydantic import BaseModel, Field

from ..integrations.beads_integration import get_beads_client


class EpicCreateInput(BaseModel):
    """Input for creating an epic."""

    title: str = Field(..., description="Epic title")
    description: Optional[str] = Field("", description="Epic description")
    priority: int = Field(2, description="Priority 0-4 (0=lowest, 4=highest)")
    labels: Optional[List[str]] = Field(None, description="List of labels/tags")


class EpicProjectCreateInput(BaseModel):
    """Input for creating an epic and linked project together."""

    title: str = Field(..., description="Epic and project title (will be used for both)")
    description: Optional[str] = Field("", description="Description (will be used for both)")
    priority: int = Field(2, description="Epic priority 0-4 (0=lowest, 4=highest)")
    labels: Optional[List[str]] = Field(None, description="Labels/tags (will be used for both)")
    jira_project_key: Optional[str] = Field(None, description="Jira project key for the project (optional)")


class IssueCreateInput(BaseModel):
    """Input for creating an issue."""

    title: str = Field(..., description="Issue title")
    description: Optional[str] = Field("", description="Issue description")
    issue_type: str = Field("task", description="Type: bug, feature, task, epic, chore")
    priority: int = Field(2, description="Priority 0-4 (0=lowest, 4=highest)")
    parent_epic_id: Optional[str] = Field(
        None, description="ID of parent epic (creates parent-child dependency)"
    )
    blocks: Optional[List[str]] = Field(None, description="List of issue IDs this issue blocks")
    labels: Optional[List[str]] = Field(None, description="List of labels/tags")
    external_ref: Optional[str] = Field(
        None, description="External reference (e.g., Jira ticket, GitHub issue)"
    )
    with_task: bool = Field(False, description="Create a linked Second Brain task")
    project_slug: Optional[str] = Field(
        None, description="Project slug for linked task (used with with_task)"
    )


class IssueUpdateInput(BaseModel):
    """Input for updating an issue."""

    issue_id: str = Field(..., description="Issue ID to update")
    title: Optional[str] = Field(None, description="New title")
    description: Optional[str] = Field(None, description="New description")
    status: Optional[str] = Field(
        None, description="New status: open, in_progress, blocked, closed"
    )
    priority: Optional[int] = Field(None, description="New priority 0-4")


class IssueCloseInput(BaseModel):
    """Input for closing an issue."""

    issue_id: str = Field(..., description="Issue ID to close")
    reason: str = Field("Completed", description="Reason for closing")


class IssueQueryInput(BaseModel):
    """Input for querying issues."""

    issue_id: str = Field(..., description="Issue ID to retrieve")


class IssuesListInput(BaseModel):
    """Input for listing issues with filters."""

    status: Optional[str] = Field(
        None, description="Filter by status: open, in_progress, blocked, closed"
    )
    issue_type: Optional[str] = Field(
        None, description="Filter by type: bug, feature, task, epic, chore"
    )
    priority: Optional[int] = Field(None, description="Filter by priority 0-4")
    limit: int = Field(50, description="Max number of issues to return")


class EpicsListInput(BaseModel):
    """Input for listing epics with filters."""

    status: Optional[str] = Field(None, description="Filter by status")
    limit: int = Field(50, description="Max number to return")


class DependencyAddInput(BaseModel):
    """Input for adding a dependency between issues."""

    issue_id: str = Field(..., description="Issue that has the dependency")
    depends_on_id: str = Field(..., description="Issue that is depended on")
    dep_type: str = Field(
        "blocks",
        description="Type: blocks, related, parent-child, discovered-from",
    )


class ReadyWorkInput(BaseModel):
    """Input for getting ready work."""

    limit: int = Field(10, description="Max number of issues to return")
    priority: Optional[int] = Field(None, description="Filter by priority")


def create_epic_tool(project_dir: Optional[str] = None):
    """Create a new epic tool."""

    async def create_epic(epic: EpicCreateInput) -> str:
        """
        Create a new epic for organizing large initiatives.

        Epics are high-level work items that can have multiple child issues.
        They help organize complex features or initiatives into manageable pieces.
        Uses Beads dependency tracking under the hood.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            issue = await client.create_epic(
                title=epic.title,
                description=epic.description,
                priority=epic.priority,
                labels=epic.labels or [],
            )

            labels_str = f"\nLabels: {', '.join(epic.labels)}" if epic.labels else ""
            priority_str = ["Lowest", "Low", "Medium", "High", "Highest"][epic.priority]

            return (
                f"Epic created successfully!\n"
                f"ID: {issue.id}\n"
                f"Title: {issue.title}\n"
                f"Priority: {priority_str} ({epic.priority})"
                f"{labels_str}\n"
                f"Status: {issue.status}"
            )
        except Exception as e:
            return f"Error creating epic: {str(e)}"

    return create_epic


def create_issue_tool(project_dir: Optional[str] = None):
    """Create a new issue tool."""

    async def create_issue(issue_input: IssueCreateInput) -> str:
        """
        Create a new issue (task, bug, feature, etc.), optionally with a linked Second Brain task.

        Issues represent individual work items. They can be linked to parent epics,
        have dependencies on other issues, and track progress through workflows.
        Supports 4 dependency types: blocks, related, parent-child, discovered-from.
        Can also create a linked Second Brain task for rich notes and time tracking.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            issue = await client.create_issue(
                title=issue_input.title,
                description=issue_input.description,
                issue_type=issue_input.issue_type,
                priority=issue_input.priority,
                parent_epic_id=issue_input.parent_epic_id,
                blocks=issue_input.blocks,
                labels=issue_input.labels,
                external_ref=issue_input.external_ref,
            )

            priority_str = ["Lowest", "Low", "Medium", "High", "Highest"][issue_input.priority]
            result = (
                f"Issue created successfully!\n"
                f"ID: {issue.id}\n"
                f"Title: {issue.title}\n"
                f"Type: {issue_input.issue_type}\n"
                f"Priority: {priority_str} ({issue_input.priority})\n"
                f"Status: {issue.status}"
            )

            if issue_input.parent_epic_id:
                result += f"\nParent Epic: {issue_input.parent_epic_id}"

            if issue_input.blocks:
                result += f"\nBlocks: {', '.join(issue_input.blocks)}"

            if issue_input.labels:
                result += f"\nLabels: {', '.join(issue_input.labels)}"

            if issue_input.external_ref:
                result += f"\nExternal Ref: {issue_input.external_ref}"

            # Create linked Second Brain task if requested
            if issue_input.with_task:
                from ..db import init_db, get_session
                from ..db.operations import ProjectOps, TaskOps
                from ..config import get_config

                config = get_config()
                engine = init_db(str(config.db_path))
                session = get_session(engine)

                try:
                    project_id = None
                    project_name = None
                    if issue_input.project_slug:
                        project = ProjectOps.get_by_slug(session, issue_input.project_slug)
                        if not project:
                            result += f"\n\nWarning: Project '{issue_input.project_slug}' not found. Creating task without project link."
                        else:
                            project_id = project.id
                            project_name = project.name

                    # Map Beads priority to task priority
                    priority_map = {0: "low", 1: "low", 2: "medium", 3: "high", 4: "urgent"}
                    task_priority = priority_map.get(issue_input.priority, "medium")

                    task = TaskOps.create(
                        session,
                        title=issue_input.title,
                        description=issue_input.description,
                        status="todo",
                        priority=task_priority,
                        project_id=project_id,
                        issue_id=issue.id,
                    )

                    result += f"\n\nLinked Second Brain task created: #{task.id}"
                    if project_name:
                        result += f"\nProject: {project_name}"
                finally:
                    session.close()

            return result
        except Exception as e:
            return f"Error creating issue: {str(e)}"

    return create_issue


def update_issue_tool(project_dir: Optional[str] = None):
    """Update an existing issue tool."""

    async def update_issue(update: IssueUpdateInput) -> str:
        """
        Update an existing issue's properties.

        Modify issue details including title, description, status, and priority.
        Use this to track progress and manage issue lifecycle.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            issue = await client.update_issue(
                issue_id=update.issue_id,
                title=update.title,
                description=update.description,
                status=update.status,
                priority=update.priority,
            )

            result = f"Issue {issue.id} updated successfully!\n"
            result += f"Title: {issue.title}\n"
            result += f"Status: {issue.status}"

            if issue.priority is not None:
                priority_str = ["Lowest", "Low", "Medium", "High", "Highest"][issue.priority]
                result += f"\nPriority: {priority_str} ({issue.priority})"

            return result
        except Exception as e:
            return f"Error updating issue: {str(e)}"

    return update_issue


def close_issue_tool(project_dir: Optional[str] = None):
    """Close an issue tool."""

    async def close_issue(close_input: IssueCloseInput) -> str:
        """
        Close an issue with a reason.

        Mark an issue as completed or resolved. The issue remains in the system
        but is marked as closed for reporting and filtering purposes.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            issue = await client.close_issue(
                issue_id=close_input.issue_id, reason=close_input.reason
            )

            return (
                f"Issue {issue.id} closed successfully!\n"
                f"Title: {issue.title}\n"
                f"Reason: {close_input.reason}\n"
                f"Status: {issue.status}"
            )
        except Exception as e:
            return f"Error closing issue: {str(e)}"

    return close_issue


def get_issue_tool(project_dir: Optional[str] = None):
    """Get detailed issue information tool."""

    async def get_issue(query: IssueQueryInput) -> str:
        """
        Retrieve detailed information about an issue.

        Get full issue details including dependencies, blockers, and related issues.
        Shows the complete dependency graph for the issue.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            issue = await client.get_issue(issue_id=query.issue_id)

            priority_str = (
                ["Lowest", "Low", "Medium", "High", "Highest"][issue.priority]
                if issue.priority is not None
                else "Not set"
            )

            result = f"**{issue.title}** ({issue.id})\n\n"
            result += f"Type: {issue.issue_type}\n"
            result += f"Status: {issue.status}\n"
            result += f"Priority: {priority_str}\n"

            if issue.description:
                result += f"\nDescription:\n{issue.description}\n"

            if hasattr(issue, "labels") and issue.labels:
                result += f"\nLabels: {', '.join(issue.labels)}\n"

            if hasattr(issue, "external_ref") and issue.external_ref:
                result += f"External Ref: {issue.external_ref}\n"

            # Dependencies
            if hasattr(issue, "dependencies") and issue.dependencies:
                result += f"\n**Dependencies ({len(issue.dependencies)}):**\n"
                for dep in issue.dependencies:
                    result += f"  - {dep.id}: {dep.title} [{dep.dep_type}]\n"

            # Dependents (issues that depend on this one)
            if hasattr(issue, "dependents") and issue.dependents:
                result += f"\n**Dependents ({len(issue.dependents)}):**\n"
                for dep in issue.dependents:
                    result += f"  - {dep.id}: {dep.title}\n"

            return result
        except Exception as e:
            return f"Error retrieving issue: {str(e)}"

    return get_issue


def list_issues_tool(project_dir: Optional[str] = None):
    """List issues with filters tool."""

    async def list_issues(query: IssuesListInput) -> str:
        """
        Query issues with optional filters.

        Retrieve issues filtered by status, type, or priority. Useful for
        getting current workload, finding specific issues, or generating lists.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            issues = await client.list_issues(
                status=query.status,
                issue_type=query.issue_type,
                priority=query.priority,
                limit=query.limit,
            )

            if not issues:
                filters = []
                if query.status:
                    filters.append(f"status={query.status}")
                if query.issue_type:
                    filters.append(f"type={query.issue_type}")
                if query.priority is not None:
                    filters.append(f"priority={query.priority}")
                filter_str = f" with filters: {', '.join(filters)}" if filters else ""
                return f"No issues found{filter_str}"

            result = f"Found {len(issues)} issue(s):\n\n"

            for issue in issues:
                status_emoji = {
                    "open": "⬜",
                    "in_progress": "🔄",
                    "closed": "✅",
                    "blocked": "🚫",
                }.get(issue.status, "⬜")

                priority_str = (
                    ["Lowest", "Low", "Medium", "High", "Highest"][issue.priority]
                    if issue.priority is not None
                    else "Not set"
                )

                result += f"{status_emoji} **{issue.title}** ({issue.id})\n"
                result += f"  Type: {issue.issue_type} | Status: {issue.status} | Priority: {priority_str}\n"

                if hasattr(issue, "description") and issue.description:
                    desc = (
                        issue.description[:100] + "..."
                        if len(issue.description) > 100
                        else issue.description
                    )
                    result += f"  Description: {desc}\n"

                result += "\n"

            return result
        except Exception as e:
            return f"Error listing issues: {str(e)}"

    return list_issues


def list_epics_tool(project_dir: Optional[str] = None):
    """List epics with filters tool."""

    async def list_epics(query: EpicsListInput) -> str:
        """
        Query epics with optional filters.

        Retrieve all epics or filter by status. Useful for getting an overview
        of large initiatives and planning work.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            epics = await client.list_epics(status=query.status, limit=query.limit)

            if not epics:
                filter_str = f" with status={query.status}" if query.status else ""
                return f"No epics found{filter_str}"

            result = f"Found {len(epics)} epic(s):\n\n"

            for epic in epics:
                status_emoji = {
                    "open": "📋",
                    "in_progress": "🚀",
                    "closed": "🎉",
                    "blocked": "🚫",
                }.get(epic.status, "📋")

                priority_str = (
                    ["Lowest", "Low", "Medium", "High", "Highest"][epic.priority]
                    if epic.priority is not None
                    else "Not set"
                )

                result += f"{status_emoji} **{epic.title}** ({epic.id})\n"
                result += f"  Status: {epic.status} | Priority: {priority_str}\n"

                if hasattr(epic, "description") and epic.description:
                    desc = (
                        epic.description[:100] + "..."
                        if len(epic.description) > 100
                        else epic.description
                    )
                    result += f"  Description: {desc}\n"

                result += "\n"

            return result
        except Exception as e:
            return f"Error listing epics: {str(e)}"

    return list_epics


def add_dependency_tool(project_dir: Optional[str] = None):
    """Add a dependency between issues tool."""

    async def add_dependency(dep_input: DependencyAddInput) -> str:
        """
        Add a dependency relationship between two issues.

        Create dependencies to track how issues relate to each other.
        Supports 4 types:
        - blocks: One issue blocks another from starting
        - related: Issues are related but no blocking relationship
        - parent-child: Epic/sub-issue relationship
        - discovered-from: Issue discovered while working on another

        Dependencies are used to find ready work and track blockers.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            await client.add_dependency(
                issue_id=dep_input.issue_id,
                depends_on_id=dep_input.depends_on_id,
                dep_type=dep_input.dep_type,
            )

            dep_type_desc = {
                "blocks": f"{dep_input.depends_on_id} blocks {dep_input.issue_id}",
                "related": f"{dep_input.issue_id} is related to {dep_input.depends_on_id}",
                "parent-child": f"{dep_input.depends_on_id} is parent of {dep_input.issue_id}",
                "discovered-from": f"{dep_input.issue_id} discovered while working on {dep_input.depends_on_id}",
            }.get(dep_input.dep_type, "Unknown relationship")

            return (
                f"Dependency added successfully!\n"
                f"Type: {dep_input.dep_type}\n"
                f"Relationship: {dep_type_desc}"
            )
        except Exception as e:
            return f"Error adding dependency: {str(e)}"

    return add_dependency


def get_ready_work_tool(project_dir: Optional[str] = None):
    """Get ready work tool."""

    async def get_ready_work(query: ReadyWorkInput) -> str:
        """
        Find issues that are ready to work on right now.

        This is Beads' killer feature - automatically finds work that can be
        started immediately because all dependencies are satisfied and there
        are no blockers. Perfect for "what should I work on next?" questions.

        Results are sorted by priority to help you focus on the most important work.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            issues = await client.get_ready_work(limit=query.limit, priority=query.priority)

            if not issues:
                filter_str = f" with priority={query.priority}" if query.priority else ""
                return f"No ready work found{filter_str}. All work is either blocked or completed!"

            result = f"🎯 Found {len(issues)} issue(s) ready to work on:\n\n"

            for issue in issues:
                priority_str = (
                    ["Lowest", "Low", "Medium", "High", "Highest"][issue.priority]
                    if issue.priority is not None
                    else "Not set"
                )

                result += f"**{issue.title}** ({issue.id})\n"
                result += f"  Type: {issue.issue_type} | Priority: {priority_str}\n"

                if hasattr(issue, "description") and issue.description:
                    desc = (
                        issue.description[:100] + "..."
                        if len(issue.description) > 100
                        else issue.description
                    )
                    result += f"  Description: {desc}\n"

                result += "\n"

            result += "\n💡 These issues have no open blockers and can be started immediately!"

            return result
        except Exception as e:
            return f"Error getting ready work: {str(e)}"

    return get_ready_work


def get_stats_tool(project_dir: Optional[str] = None):
    """Get project statistics tool."""

    async def get_stats() -> str:
        """
        Get project statistics and overview.

        Provides a high-level view of the project including total issues,
        open/closed counts, blocked issues, and ready work. Perfect for
        status updates and understanding project health at a glance.
        """
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            stats = await client.get_stats()

            result = "📊 **Project Statistics**\n\n"
            result += f"Total Issues: {stats.total}\n"
            result += f"Open: {stats.open}\n"
            result += f"Closed: {stats.closed}\n"
            result += f"Blocked: {stats.blocked}\n"
            result += f"Ready to Work: {stats.ready}\n"

            if stats.ready > 0:
                result += f"\n💡 You have {stats.ready} issue(s) ready to work on!"
            elif stats.blocked > 0:
                result += f"\n⚠️ {stats.blocked} issue(s) are blocked. Consider addressing blockers."
            elif stats.open == 0:
                result += "\n🎉 All issues are closed! Great work!"

            return result
        except Exception as e:
            return f"Error getting stats: {str(e)}"

    return get_stats


def create_epic_with_project_tool(project_dir: Optional[str] = None):
    """Create an epic and linked project together tool."""

    async def create_epic_with_project(input_data: EpicProjectCreateInput) -> str:
        """
        Create an epic and a linked Second Brain project in one operation.

        This is the ideal workflow for starting a new initiative:
        1. Creates an epic in Beads for dependency tracking and high-level coordination
        2. Creates a Second Brain project for day-to-day notes and time tracking
        3. Links them together automatically
        4. Uses same title, description, and tags/labels for both

        Perfect for:
        - Starting new features or initiatives
        - Organizing complex work that needs both dependency tracking and detailed notes
        - Team collaboration where you need to track blockers AND capture implementation details

        After creation, you can:
        - Create issues under the epic with parent-child relationships
        - Create tasks under the project and link them to issues
        - Add notes to the project and tasks
        - Track time and work logs in Second Brain
        - Track dependencies and blockers in Beads
        """
        # Create the epic first
        client = get_beads_client(project_dir)
        if not client:
            return "Error: Beads integration not available. Install with: uv pip install beads-mcp"

        try:
            # Create epic
            epic = await client.create_epic(
                title=input_data.title,
                description=input_data.description,
                priority=input_data.priority,
                labels=input_data.labels or [],
            )

            priority_str = ["Lowest", "Low", "Medium", "High", "Highest"][input_data.priority]

            result = "✅ Epic + Project created successfully!\n\n"
            result += "📋 **Epic (Beads):**\n"
            result += f"  ID: {epic.id}\n"
            result += f"  Title: {epic.title}\n"
            result += f"  Priority: {priority_str} ({input_data.priority})\n"
            result += f"  Status: {epic.status}\n"

            if input_data.labels:
                result += f"  Labels: {', '.join(input_data.labels)}\n"

            # Create project
            from ..db import init_db, get_session
            from ..config import get_config
            from ..storage import StorageIndexer

            config = get_config()
            engine = init_db(str(config.db_path))
            session = get_session(engine)

            try:
                indexer = StorageIndexer(session)

                project = indexer.create_project(
                    name=input_data.title,
                    description=input_data.description,
                    jira_project_key=input_data.jira_project_key,
                    tags=input_data.labels,
                )

                result += f"\n📦 **Project (Second Brain):**\n"
                result += f"  ID: {project.id}\n"
                result += f"  Name: {project.name}\n"
                result += f"  Slug: {project.slug}\n"
                result += f"  Markdown: {project.markdown_path}\n"

                if input_data.jira_project_key:
                    result += f"  Jira: {input_data.jira_project_key}\n"

                if input_data.labels:
                    result += f"  Tags: {', '.join(input_data.labels)}\n"

                result += f"\n🔗 **Integration:**\n"
                result += f"Epic ID: {epic.id} ↔️ Project Slug: {project.slug}\n"
                result += f"\n💡 **Next Steps:**\n"
                result += f"1. Create issues under epic: sb issue create \"Issue Title\" --parent-epic {epic.id}\n"
                result += f"2. Create tasks in project: sb task add \"Task Title\" --project {project.slug}\n"
                result += f"3. Link issues to tasks: sb issue create \"Issue\" --with-task --project {project.slug}\n"
                result += f"4. Add notes: sb note create \"Notes\" --project {project.slug}\n"
                result += f"5. Track work: sb log add \"Work done\" --project {project.slug}\n"

                return result
            finally:
                session.close()

        except Exception as e:
            return f"Error creating epic and project: {str(e)}"

    return create_epic_with_project
