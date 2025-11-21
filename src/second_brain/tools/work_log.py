"""MCP tools for work log operations."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from ..db import get_session
from ..storage import StorageIndexer
from ..utils import datetime_utils


class WorkLogEntryInput(BaseModel):
    """Input for creating a work log entry."""

    entry_text: str = Field(..., description="The work log entry text")
    task_id: Optional[int] = Field(None, description="Optional task ID to link this entry to")
    time_spent_minutes: Optional[int] = Field(
        None, description="Time spent in minutes (optional)"
    )
    date: Optional[str] = Field(
        None, description="Date for the entry (YYYY-MM-DD), defaults to today"
    )


class WorkLogQueryInput(BaseModel):
    """Input for querying work logs."""

    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")


def create_work_log_entry_tool(engine):
    """Create a work log entry tool."""

    async def create_work_log_entry(entry: WorkLogEntryInput) -> str:
        """
        Add an entry to the daily work log.

        This tool allows agents to record work activities, link them to tasks,
        and track time spent. Entries are stored in both markdown files and
        the SQLite database for easy human reading and querying.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            # Parse date or use today
            if entry.date:
                date = datetime.strptime(entry.date, "%Y-%m-%d")
            else:
                date = datetime_utils.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # Add entry
            work_log = indexer.add_work_log_entry(
                date=date,
                entry_text=entry.entry_text,
                task_id=entry.task_id,
                time_spent_minutes=entry.time_spent_minutes,
            )

            task_info = ""
            if entry.task_id:
                from ..db import Task

                task = session.get(Task, entry.task_id)
                if task:
                    task_info = f" (linked to task: {task.title})"

            time_info = ""
            if entry.time_spent_minutes:
                time_info = f" [{entry.time_spent_minutes} minutes]"

            return (
                f"Work log entry added for {date.strftime('%Y-%m-%d')}{task_info}{time_info}\n"
                f"Entry: {entry.entry_text}"
            )
        finally:
            session.close()

    return create_work_log_entry


def get_work_logs_tool(engine):
    """Get work logs for a date range tool."""

    async def get_work_logs(query: WorkLogQueryInput) -> str:
        """
        Retrieve work logs for a specific date range.

        This tool allows agents to query work logs between two dates,
        useful for generating reports, reviewing past work, or tracking progress.
        """
        session = get_session(engine)
        try:
            from ..db.operations import WorkLogOps

            start_date = datetime.strptime(query.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(query.end_date, "%Y-%m-%d")

            work_logs = WorkLogOps.list_by_date_range(session, start_date, end_date)

            if not work_logs:
                return f"No work logs found between {query.start_date} and {query.end_date}"

            result = f"Work logs from {query.start_date} to {query.end_date}:\n\n"

            for wl in work_logs:
                result += f"## {wl.date.strftime('%Y-%m-%d')}\n"
                if wl.summary:
                    result += f"Summary: {wl.summary}\n"

                if wl.entries:
                    result += "Entries:\n"
                    for entry in wl.entries:
                        time_str = entry.timestamp.strftime("%H:%M")
                        task_str = ""
                        if entry.task:
                            task_str = f" [{entry.task.title}]"
                        time_spent_str = ""
                        if entry.time_spent_minutes:
                            time_spent_str = f" ({entry.time_spent_minutes}m)"
                        result += f"  - {time_str}{task_str}{time_spent_str}: {entry.entry_text}\n"

                result += "\n"

            return result
        finally:
            session.close()

    return get_work_logs
