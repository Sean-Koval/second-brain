"""MCP tools for generating reports and summaries."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from ..db import get_session
from ..db.operations import WorkLogOps, TaskOps, ProjectOps


class ReportInput(BaseModel):
    """Input for generating a work report."""

    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    project_slug: Optional[str] = Field(None, description="Filter by project slug (optional)")
    include_time_spent: bool = Field(True, description="Include time tracking information")


def generate_report_tool(engine):
    """Generate a work summary report tool."""

    async def generate_report(report: ReportInput) -> str:
        """
        Generate a comprehensive work report for a date range.

        This tool creates a detailed summary of work done, including:
        - Work log entries
        - Tasks completed
        - Time spent tracking
        - Project-specific breakdowns

        Useful for performance reviews, promotion tracking, and audits.
        """
        session = get_session(engine)
        try:
            start_date = datetime.strptime(report.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(report.end_date, "%Y-%m-%d")

            # Get project if specified
            project = None
            if report.project_slug:
                project = ProjectOps.get_by_slug(session, report.project_slug)
                if not project:
                    return f"Error: Project with slug '{report.project_slug}' not found"

            # Get work logs
            work_logs = WorkLogOps.list_by_date_range(session, start_date, end_date)

            # Get tasks completed in this period
            all_tasks = TaskOps.list_all(session, status="done")
            completed_tasks = [
                t
                for t in all_tasks
                if t.completed_at
                and start_date <= t.completed_at <= end_date
                and (not project or t.project_id == project.id)
            ]

            # Build report
            result = "# Work Report\n\n"
            result += f"**Period:** {report.start_date} to {report.end_date}\n"
            if project:
                result += f"**Project:** {project.name}\n"
            result += "\n---\n\n"

            # Summary stats
            result += "## Summary\n\n"
            result += f"- Work days logged: {len(work_logs)}\n"
            result += f"- Tasks completed: {len(completed_tasks)}\n"

            if report.include_time_spent:
                total_time = sum(t.time_spent_minutes for t in all_tasks if t.time_spent_minutes)
                total_hours = total_time // 60
                total_minutes = total_time % 60
                result += f"- Total time tracked: {total_hours}h {total_minutes}m\n"

            result += "\n"

            # Tasks completed
            if completed_tasks:
                result += "## Tasks Completed\n\n"
                for task in completed_tasks:
                    result += f"- **{task.title}** (#{task.id})\n"
                    if task.project:
                        result += f"  - Project: {task.project.name}\n"
                    if task.description:
                        desc = (
                            task.description[:100] + "..."
                            if len(task.description) > 100
                            else task.description
                        )
                        result += f"  - Description: {desc}\n"
                    if task.completed_at:
                        result += f"  - Completed: {task.completed_at.strftime('%Y-%m-%d')}\n"
                    if report.include_time_spent and task.time_spent_minutes:
                        hours = task.time_spent_minutes // 60
                        minutes = task.time_spent_minutes % 60
                        result += f"  - Time spent: {hours}h {minutes}m\n"
                    result += "\n"

            # Daily work logs
            if work_logs:
                result += "## Daily Work Logs\n\n"
                for wl in work_logs:
                    result += f"### {wl.date.strftime('%Y-%m-%d')}\n\n"
                    if wl.summary:
                        result += f"{wl.summary}\n\n"

                    if wl.entries:
                        for entry in wl.entries:
                            # Filter by project if specified
                            if project and entry.task and entry.task.project_id != project.id:
                                continue

                            time_str = entry.timestamp.strftime("%H:%M")
                            task_str = ""
                            if entry.task:
                                task_str = f" **[{entry.task.title}]**"
                            time_spent_str = ""
                            if report.include_time_spent and entry.time_spent_minutes:
                                time_spent_str = f" ({entry.time_spent_minutes}m)"

                            result += f"- {time_str}{task_str}{time_spent_str}: {entry.entry_text}\n"

                    result += "\n"

            # Project breakdown if no specific project filter
            if not project:
                result += "## Project Breakdown\n\n"

                # Get all projects with activity in this period
                active_projects = set()
                for task in completed_tasks:
                    if task.project:
                        active_projects.add(task.project)

                for wl in work_logs:
                    for entry in wl.entries:
                        if entry.task and entry.task.project:
                            active_projects.add(entry.task.project)

                if active_projects:
                    for proj in sorted(active_projects, key=lambda p: p.name):
                        proj_tasks = [t for t in completed_tasks if t.project_id == proj.id]
                        result += f"### {proj.name}\n\n"
                        result += f"- Tasks completed: {len(proj_tasks)}\n"

                        if report.include_time_spent:
                            proj_time = sum(
                                t.time_spent_minutes for t in proj_tasks if t.time_spent_minutes
                            )
                            if proj_time > 0:
                                hours = proj_time // 60
                                minutes = proj_time % 60
                                result += f"- Time spent: {hours}h {minutes}m\n"

                        result += "\n"
                else:
                    result += "No project-specific work found in this period.\n\n"

            result += "---\n\n"
            result += f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"

            return result
        finally:
            session.close()

    return generate_report


def get_project_status_tool(engine):
    """Get detailed status of a specific project tool."""

    async def get_project_status(project_slug: str) -> str:
        """
        Get detailed status and analytics for a specific project.

        Provides a comprehensive overview including task breakdown,
        time tracking, and recent activity. Useful for project updates
        and status reports.
        """
        session = get_session(engine)
        try:
            project = ProjectOps.get_by_slug(session, project_slug)
            if not project:
                return f"Error: Project with slug '{project_slug}' not found"

            result = f"# Project Status: {project.name}\n\n"
            result += f"**Slug:** {project.slug}\n"
            result += f"**Status:** {project.status}\n"

            if project.description:
                result += f"**Description:** {project.description}\n"

            if project.jira_project_key:
                result += f"**Jira Project:** {project.jira_project_key}\n"

            if project.tags:
                result += f"**Tags:** {project.tags}\n"

            result += f"**Created:** {project.created_at.strftime('%Y-%m-%d')}\n"
            result += f"**Last Updated:** {project.updated_at.strftime('%Y-%m-%d')}\n"

            result += "\n---\n\n"

            # Task breakdown
            tasks = TaskOps.list_by_project(session, project.id)

            if tasks:
                result += "## Tasks Overview\n\n"
                result += f"**Total Tasks:** {len(tasks)}\n\n"

                # Count by status
                status_counts = {}
                for task in tasks:
                    status_counts[task.status] = status_counts.get(task.status, 0) + 1

                result += "**By Status:**\n"
                for status in ["todo", "in_progress", "blocked", "done"]:
                    count = status_counts.get(status, 0)
                    if count > 0:
                        result += f"- {status}: {count}\n"

                result += "\n"

                # Time tracking
                total_time = sum(t.time_spent_minutes for t in tasks if t.time_spent_minutes)
                if total_time > 0:
                    hours = total_time // 60
                    minutes = total_time % 60
                    result += f"**Total Time Tracked:** {hours}h {minutes}m\n\n"

                # Active tasks
                active_tasks = [t for t in tasks if t.status in ["todo", "in_progress"]]
                if active_tasks:
                    result += "### Active Tasks\n\n"
                    for task in active_tasks[:10]:  # Limit to 10
                        status_emoji = {"todo": "⬜", "in_progress": "🔄"}.get(task.status, "⬜")
                        result += f"{status_emoji} **{task.title}** (#{task.id})\n"
                        if task.priority:
                            result += f"  - Priority: {task.priority}\n"
                        if task.jira_ticket_key:
                            result += f"  - Jira: {task.jira_ticket_key}\n"
                        result += "\n"

                # Recently completed
                completed_tasks = sorted(
                    [t for t in tasks if t.status == "done" and t.completed_at],
                    key=lambda t: t.completed_at,
                    reverse=True,
                )

                if completed_tasks:
                    result += "### Recently Completed (Last 5)\n\n"
                    for task in completed_tasks[:5]:
                        result += f"✅ **{task.title}** (#{task.id})\n"
                        result += f"  - Completed: {task.completed_at.strftime('%Y-%m-%d')}\n"
                        if task.time_spent_minutes:
                            hours = task.time_spent_minutes // 60
                            minutes = task.time_spent_minutes % 60
                            result += f"  - Time spent: {hours}h {minutes}m\n"
                        result += "\n"
            else:
                result += "## Tasks\n\nNo tasks found for this project.\n\n"

            return result
        finally:
            session.close()

    return get_project_status
