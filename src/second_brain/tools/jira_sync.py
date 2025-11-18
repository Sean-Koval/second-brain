"""MCP tools for Jira synchronization."""

from typing import Optional
from pydantic import BaseModel, Field

from ..db import get_session
from ..db.operations import TaskOps, ProjectOps
from ..integrations.jira_client import JiraClient


class JiraSyncInput(BaseModel):
    """Input for syncing Jira issues."""

    project_slug: Optional[str] = Field(
        None, description="Project slug to sync (syncs all projects if not specified)"
    )
    status_filter: Optional[str] = Field(None, description="Filter by issue status (optional)")


class JiraIssueInput(BaseModel):
    """Input for getting a specific Jira issue."""

    issue_key: str = Field(..., description="Jira issue key (e.g., PROJ-123)")


def sync_jira_issues_tool(engine):
    """Sync Jira issues to local tasks tool."""

    async def sync_jira_issues(sync: JiraSyncInput) -> str:
        """
        Synchronize Jira issues to local tasks.

        This tool pulls tickets from Jira and creates or updates corresponding
        tasks in the second brain. Useful for keeping track of assigned work
        and linking Jira tickets to your local workflow.
        """
        session = get_session(engine)
        try:
            # Initialize Jira client
            try:
                jira = JiraClient()
            except ValueError as e:
                return f"Error: {str(e)}\nPlease configure Jira credentials in environment variables."

            # Test connection
            if not jira.test_connection():
                return "Error: Failed to connect to Jira. Check your credentials."

            synced_count = 0
            updated_count = 0
            created_count = 0

            # Get project(s) to sync
            projects = []
            if sync.project_slug:
                project = ProjectOps.get_by_slug(session, sync.project_slug)
                if not project:
                    return f"Error: Project with slug '{sync.project_slug}' not found"
                if not project.jira_project_key:
                    return f"Error: Project '{project.name}' has no Jira project key configured"
                projects.append(project)
            else:
                # Get all projects with Jira keys
                all_projects = ProjectOps.list_all(session)
                projects = [p for p in all_projects if p.jira_project_key]

            if not projects:
                return "No projects with Jira integration found. Add a Jira project key to your projects first."

            result = f"Syncing Jira issues for {len(projects)} project(s)...\n\n"

            for project in projects:
                result += f"## {project.name} ({project.jira_project_key})\n\n"

                # Fetch issues from Jira
                issues = jira.get_project_issues(
                    project.jira_project_key, status=sync.status_filter
                )

                if not issues:
                    result += "No issues found.\n\n"
                    continue

                for issue in issues:
                    # Check if task already exists
                    existing_task = TaskOps.get_by_jira_key(session, issue["key"])

                    if existing_task:
                        # Update existing task
                        TaskOps.update(
                            session,
                            existing_task,
                            title=issue["summary"],
                            description=issue["description"],
                            status=_map_jira_status(issue["status"]),
                            priority=_map_jira_priority(issue.get("priority")),
                        )
                        updated_count += 1
                    else:
                        # Create new task
                        TaskOps.create(
                            session,
                            title=issue["summary"],
                            description=issue["description"],
                            status=_map_jira_status(issue["status"]),
                            priority=_map_jira_priority(issue.get("priority")),
                            project_id=project.id,
                            jira_ticket_id=issue["id"],
                            jira_ticket_key=issue["key"],
                            tags=",".join(issue.get("labels", [])) if issue.get("labels") else None,
                        )
                        created_count += 1

                    synced_count += 1

                result += f"Synced {len(issues)} issue(s)\n\n"

            result += "---\n\n"
            result += f"**Summary:**\n"
            result += f"- Total issues synced: {synced_count}\n"
            result += f"- Created: {created_count}\n"
            result += f"- Updated: {updated_count}\n"

            return result
        except Exception as e:
            return f"Error during sync: {str(e)}"
        finally:
            session.close()

    return sync_jira_issues


def get_jira_issue_tool(engine):
    """Get a specific Jira issue and optionally create a task tool."""

    async def get_jira_issue(issue_input: JiraIssueInput) -> str:
        """
        Fetch a specific Jira issue by key.

        Retrieves detailed information about a Jira ticket. If a task with
        this ticket doesn't exist locally, you can create one based on the
        issue details.
        """
        session = get_session(engine)
        try:
            # Initialize Jira client
            try:
                jira = JiraClient()
            except ValueError as e:
                return f"Error: {str(e)}"

            # Fetch issue
            issue = jira.get_issue(issue_input.issue_key)
            if not issue:
                return f"Error: Issue '{issue_input.issue_key}' not found in Jira"

            result = f"# {issue['key']}: {issue['summary']}\n\n"
            result += f"**Status:** {issue['status']}\n"
            if issue.get("priority"):
                result += f"**Priority:** {issue['priority']}\n"
            if issue.get("assignee"):
                result += f"**Assignee:** {issue['assignee']}\n"
            if issue.get("reporter"):
                result += f"**Reporter:** {issue['reporter']}\n"
            result += f"**Type:** {issue['issue_type']}\n"
            result += f"**Project:** {issue['project_key']}\n"
            result += f"**Created:** {issue['created']}\n"
            result += f"**Updated:** {issue['updated']}\n"

            if issue.get("labels"):
                result += f"**Labels:** {', '.join(issue['labels'])}\n"

            result += "\n## Description\n\n"
            result += issue["description"] or "No description provided."

            # Check if task exists locally
            existing_task = TaskOps.get_by_jira_key(session, issue["key"])
            if existing_task:
                result += f"\n\n---\n\n**Local Task:** #{existing_task.id} - {existing_task.title}\n"
                result += f"Status: {existing_task.status}\n"
            else:
                result += "\n\n---\n\n*No local task exists for this issue. Use create_task tool to create one.*\n"

            return result
        except Exception as e:
            return f"Error fetching issue: {str(e)}"
        finally:
            session.close()

    return get_jira_issue


def _map_jira_status(jira_status: str) -> str:
    """Map Jira status to internal status."""
    status_map = {
        "to do": "todo",
        "todo": "todo",
        "open": "todo",
        "in progress": "in_progress",
        "in review": "in_progress",
        "done": "done",
        "closed": "done",
        "resolved": "done",
        "blocked": "blocked",
        "on hold": "blocked",
    }
    return status_map.get(jira_status.lower(), "todo")


def _map_jira_priority(jira_priority: Optional[str]) -> Optional[str]:
    """Map Jira priority to internal priority."""
    if not jira_priority:
        return None

    priority_map = {
        "highest": "urgent",
        "high": "high",
        "medium": "medium",
        "low": "low",
        "lowest": "low",
    }
    return priority_map.get(jira_priority.lower(), "medium")
