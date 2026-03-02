"""MCP tools for journal operations."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from ..db import get_session
from ..db.operations import ProjectOps, JournalOps, FTSOps
from ..storage import StorageIndexer


class JournalEntryCreateInput(BaseModel):
    """Input for creating a journal entry."""

    entry_text: str = Field(..., description="The journal entry text")
    tags: Optional[List[str]] = Field(None, description="Tags for this entry")
    project_slug: Optional[str] = Field(None, description="Project slug to link to")
    task_id: Optional[int] = Field(None, description="Task ID to link to")
    date: Optional[str] = Field(None, description="Date override (YYYY-MM-DD), defaults to today")


class JournalUpdateInput(BaseModel):
    """Input for updating journal day-level metadata."""

    date: Optional[str] = Field(None, description="Date (YYYY-MM-DD), defaults to today")
    title: Optional[str] = Field(None, description="Daily title")
    body: Optional[str] = Field(None, description="Scratchpad body text")
    summary: Optional[str] = Field(None, description="End-of-day summary")
    tags: Optional[List[str]] = Field(None, description="Tags for the day")


class JournalQueryInput(BaseModel):
    """Input for querying a single journal."""

    date: Optional[str] = Field(None, description="Date (YYYY-MM-DD), defaults to today")


class JournalsQueryInput(BaseModel):
    """Input for querying multiple journals."""

    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    limit: int = Field(7, description="Max journals to return")


class JournalEntryUpdateInput(BaseModel):
    """Input for updating a journal entry."""

    entry_id: int = Field(..., description="Entry ID to update")
    entry_text: Optional[str] = Field(None, description="New entry text")
    tags: Optional[List[str]] = Field(None, description="New tags")


class JournalEntryDeleteInput(BaseModel):
    """Input for deleting a journal entry."""

    entry_id: int = Field(..., description="Entry ID to delete")


class ContentSearchInput(BaseModel):
    """Input for unified FTS5 search."""

    query: str = Field(..., description="Search query")
    content_type: Optional[str] = Field(
        None, description="Filter by type: journal_entry, note, work_log_entry"
    )


def _parse_date(date_str: Optional[str]) -> datetime:
    """Parse date string or return today."""
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d")
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def create_journal_entry_tool(engine):
    """Create a journal entry tool."""

    async def create_journal_entry(input: JournalEntryCreateInput) -> str:
        """
        Add a quick capture entry to the daily journal.

        This is the primary journal tool for capturing thoughts, decisions,
        ideas, and commentary throughout the day. Entries can optionally
        be tagged and linked to projects or tasks.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)
            date = _parse_date(input.date)

            project_id = None
            project_name = None
            if input.project_slug:
                project = ProjectOps.get_by_slug(session, input.project_slug)
                if not project:
                    return f"Error: Project '{input.project_slug}' not found"
                project_id = project.id
                project_name = project.name

            journal, entry = indexer.add_journal_entry(
                date=date,
                entry_text=input.entry_text,
                tags=input.tags,
                project_id=project_id,
                task_id=input.task_id,
            )

            result = (
                f"Journal entry added!\n"
                f"Entry ID: {entry.id}\n"
                f"Journal date: {date.strftime('%Y-%m-%d')}\n"
                f"Time: {entry.timestamp.strftime('%H:%M')}\n"
            )
            if project_name:
                result += f"Project: {project_name}\n"
            if input.tags:
                result += f"Tags: {', '.join(input.tags)}\n"

            return result
        finally:
            session.close()

    return create_journal_entry


def update_journal_tool(engine):
    """Update journal day-level metadata tool."""

    async def update_journal(input: JournalUpdateInput) -> str:
        """
        Update the daily journal's metadata — title, scratchpad body,
        summary, or tags. Use this to set the day's focus or write
        an end-of-day summary.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)
            date = _parse_date(input.date)

            journal = indexer.update_journal(
                date=date,
                title=input.title,
                body=input.body,
                summary=input.summary,
                tags=input.tags,
            )

            if not journal:
                return f"Error: Could not create/update journal for {date.strftime('%Y-%m-%d')}"

            result = f"Journal updated for {date.strftime('%Y-%m-%d')}\n"
            if journal.title:
                result += f"Title: {journal.title}\n"
            if journal.summary:
                result += f"Summary: {journal.summary}\n"
            if journal.tags:
                result += f"Tags: {journal.tags}\n"

            return result
        finally:
            session.close()

    return update_journal


def get_journal_tool(engine):
    """Get a single day's journal tool."""

    async def get_journal(input: JournalQueryInput) -> str:
        """
        View a single day's journal with all entries.

        Returns the journal metadata and all entries for the specified
        date (defaults to today).
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)
            date = _parse_date(input.date)

            journal = indexer.get_journal(date)
            if not journal:
                return f"No journal found for {date.strftime('%Y-%m-%d')}"

            result = f"# Journal - {date.strftime('%Y-%m-%d')}\n\n"
            if journal.title:
                result += f"**{journal.title}**\n\n"
            if journal.tags:
                result += f"Tags: {journal.tags}\n"
            if journal.body:
                result += f"\n## Scratchpad\n\n{journal.body}\n"
            if journal.summary:
                result += f"\n## Summary\n\n{journal.summary}\n"

            if journal.entries:
                result += f"\n## Entries ({len(journal.entries)})\n\n"
                for entry in sorted(journal.entries, key=lambda e: e.timestamp):
                    time_str = entry.timestamp.strftime("%H:%M")
                    tags_str = f" [{entry.tags}]" if entry.tags else ""
                    project_str = ""
                    if entry.project:
                        project_str = f" (Project: {entry.project.name})"
                    result += f"**{time_str}**{tags_str}{project_str}\n{entry.entry_text}\n\n"
            else:
                result += "\nNo entries yet.\n"

            result += f"\nFile: {journal.markdown_path}"
            return result
        finally:
            session.close()

    return get_journal


def get_journals_tool(engine):
    """Get multiple journals tool."""

    async def get_journals(input: JournalsQueryInput) -> str:
        """
        Query journals across a date range or by tags.

        Returns a summary list of journals with entry counts.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            start_date = datetime.strptime(input.start_date, "%Y-%m-%d") if input.start_date else None
            end_date = datetime.strptime(input.end_date, "%Y-%m-%d") if input.end_date else None

            journals = indexer.get_journals(
                start_date=start_date,
                end_date=end_date,
                tags=input.tags,
                limit=input.limit,
            )

            if not journals:
                return "No journals found matching the criteria."

            result = f"Found {len(journals)} journal(s):\n\n"
            for j in journals:
                date_str = j.date.strftime("%Y-%m-%d")
                title_str = f" - {j.title}" if j.title else ""
                entry_count = len(j.entries) if j.entries else 0
                tags_str = f" [{j.tags}]" if j.tags else ""
                result += f"**{date_str}**{title_str} ({entry_count} entries){tags_str}\n"
                if j.summary:
                    result += f"  Summary: {j.summary}\n"

            return result
        finally:
            session.close()

    return get_journals


def update_journal_entry_tool(engine):
    """Update a journal entry tool."""

    async def update_journal_entry(input: JournalEntryUpdateInput) -> str:
        """
        Edit a specific journal entry's text or tags.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            entry = indexer.update_journal_entry(
                entry_id=input.entry_id,
                entry_text=input.entry_text,
                tags=input.tags,
            )

            if not entry:
                return f"Error: Entry #{input.entry_id} not found"

            return f"Entry #{entry.id} updated successfully."
        finally:
            session.close()

    return update_journal_entry


def delete_journal_entry_tool(engine):
    """Delete a journal entry tool."""

    async def delete_journal_entry(input: JournalEntryDeleteInput) -> str:
        """
        Remove a journal entry.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            success = indexer.delete_journal_entry(input.entry_id)
            if not success:
                return f"Error: Entry #{input.entry_id} not found"

            return f"Entry #{input.entry_id} deleted."
        finally:
            session.close()

    return delete_journal_entry


def search_all_content_tool(engine):
    """Unified FTS5 search tool."""

    async def search_all_content(input: ContentSearchInput) -> str:
        """
        Search across all content types using full-text search.

        Searches journal entries, notes, and work log entries.
        Returns ranked results with snippets.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            results = indexer.search_all_content(input.query, input.content_type)

            if not results:
                return f"No results found for '{input.query}'"

            output = f"Found {len(results)} result(s) for '{input.query}':\n\n"
            for r in results:
                type_label = r["content_type"].replace("_", " ").title()
                output += f"**[{type_label}]** (ID: {r['content_id']})\n"
                output += f"  {r['snippet']}\n"
                if r["tags"]:
                    output += f"  Tags: {r['tags']}\n"
                output += "\n"

            return output
        finally:
            session.close()

    return search_all_content
