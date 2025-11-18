"""MCP tools for note operations."""

from typing import Optional, List
from pydantic import BaseModel, Field

from ..db import get_session
from ..db.operations import NoteOps, ProjectOps, TaskOps
from ..storage import StorageIndexer


class NoteCreateInput(BaseModel):
    """Input for creating a note."""

    title: str = Field(..., description="Note title")
    content: str = Field("", description="Note content (markdown)")
    project_slug: Optional[str] = Field(None, description="Project slug to attach to")
    task_id: Optional[int] = Field(None, description="Task ID to attach to")
    tags: Optional[List[str]] = Field(None, description="List of tags")


class NoteAppendInput(BaseModel):
    """Input for appending to a note."""

    note_id: int = Field(..., description="Note ID")
    content: str = Field(..., description="Content to append (markdown)")


class NoteUpdateInput(BaseModel):
    """Input for updating a note."""

    note_id: int = Field(..., description="Note ID to update")
    title: Optional[str] = Field(None, description="New title")
    content: Optional[str] = Field(None, description="New content (markdown)")
    tags: Optional[List[str]] = Field(None, description="New tags")


class NoteQueryInput(BaseModel):
    """Input for querying notes."""

    project_slug: Optional[str] = Field(None, description="Filter by project slug")
    task_id: Optional[int] = Field(None, description="Filter by task ID")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")


class NoteSearchInput(BaseModel):
    """Input for searching notes."""

    query: str = Field(..., description="Search query (searches title and content)")


def create_note_tool(engine):
    """Create a new note tool."""

    async def create_note(note: NoteCreateInput) -> str:
        """
        Create a new note with markdown file and database entry.

        Notes can be standalone or attached to projects/tasks. They support
        rich markdown content and are fully searchable.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            # Resolve project if provided
            project_id = None
            project_name = None
            if note.project_slug:
                project = ProjectOps.get_by_slug(session, note.project_slug)
                if not project:
                    return f"Error: Project '{note.project_slug}' not found"
                project_id = project.id
                project_name = project.name

            # Validate task if provided
            if note.task_id:
                task = TaskOps.get_by_id(session, note.task_id)
                if not task:
                    return f"Error: Task #{note.task_id} not found"

            new_note = indexer.create_note(
                title=note.title,
                content=note.content,
                project_id=project_id,
                task_id=note.task_id,
                tags=note.tags,
            )

            result = (
                f"Note created successfully!\n"
                f"ID: {new_note.id}\n"
                f"Title: {new_note.title}\n"
                f"Markdown file: {new_note.markdown_path}\n"
            )

            if project_name:
                result += f"Project: {project_name}\n"
            if note.task_id:
                result += f"Task: #{note.task_id}\n"
            if note.tags:
                result += f"Tags: {', '.join(note.tags)}\n"

            return result
        finally:
            session.close()

    return create_note


def append_to_note_tool(engine):
    """Append content to an existing note tool."""

    async def append_to_note(append: NoteAppendInput) -> str:
        """
        Append content to an existing note.

        The new content will be added with a timestamp separator. Useful
        for adding incremental information or updates to existing notes.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            note = indexer.append_to_note(append.note_id, append.content)

            if not note:
                return f"Error: Note #{append.note_id} not found"

            return (
                f"Content appended to note #{note.id} ({note.title})\n"
                f"Updated file: {note.markdown_path}"
            )
        finally:
            session.close()

    return append_to_note


def update_note_tool(engine):
    """Update note tool."""

    async def update_note(update: NoteUpdateInput) -> str:
        """
        Update an existing note's properties.

        You can update the title, content, and/or tags. Fields not provided
        will remain unchanged.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            note = indexer.update_note(
                note_id=update.note_id,
                title=update.title,
                content=update.content,
                tags=update.tags,
            )

            if not note:
                return f"Error: Note #{update.note_id} not found"

            return (
                f"Note #{note.id} updated successfully!\n"
                f"Title: {note.title}\n"
                f"File: {note.markdown_path}"
            )
        finally:
            session.close()

    return update_note


def get_notes_tool(engine):
    """Get notes with optional filters tool."""

    async def get_notes(query: NoteQueryInput) -> str:
        """
        Query notes with optional filters.

        Retrieve notes by project, task, or tags. Useful for finding
        all notes related to a specific context.
        """
        session = get_session(engine)
        try:
            notes = []

            if query.project_slug:
                project = ProjectOps.get_by_slug(session, query.project_slug)
                if not project:
                    return f"Error: Project '{query.project_slug}' not found"
                notes = NoteOps.list_by_project(session, project.id)
            elif query.task_id:
                notes = NoteOps.list_by_task(session, query.task_id)
            elif query.tags:
                notes = NoteOps.list_by_tags(session, query.tags)
            else:
                notes = NoteOps.list_all(session)

            if not notes:
                filters = []
                if query.project_slug:
                    filters.append(f"project={query.project_slug}")
                if query.task_id:
                    filters.append(f"task=#{query.task_id}")
                if query.tags:
                    filters.append(f"tags={','.join(query.tags)}")
                filter_str = f" with filters: {', '.join(filters)}" if filters else ""
                return f"No notes found{filter_str}"

            result = f"Found {len(notes)} note(s):\n\n"

            for n in notes:
                result += f"**{n.title}** (#{n.id})\n"
                if n.project:
                    result += f"  Project: {n.project.name}\n"
                if n.task_id:
                    result += f"  Task: #{n.task_id}\n"
                if n.tags:
                    result += f"  Tags: {n.tags}\n"

                # Show content snippet
                snippet = n.content[:150]
                if len(n.content) > 150:
                    snippet += "..."
                result += f"  Content: {snippet}\n"
                result += f"  File: {n.markdown_path}\n\n"

            return result
        finally:
            session.close()

    return get_notes


def get_note_tool(engine):
    """Get a specific note tool."""

    async def get_note(note_id: int) -> str:
        """
        Get the full content of a specific note.

        Returns all note metadata and the complete markdown content.
        """
        session = get_session(engine)
        try:
            note = NoteOps.get_by_id(session, note_id)

            if not note:
                return f"Error: Note #{note_id} not found"

            result = f"**{note.title}** (#{note.id})\n\n"

            if note.project:
                result += f"Project: {note.project.name}\n"
            if note.task_id:
                result += f"Task: #{note.task_id}\n"
            if note.tags:
                result += f"Tags: {note.tags}\n"
            result += f"Created: {note.created_at}\n"
            result += f"Updated: {note.updated_at}\n"
            result += f"File: {note.markdown_path}\n\n"
            result += "---\n\n"
            result += note.content

            return result
        finally:
            session.close()

    return get_note


def search_notes_tool(engine):
    """Search notes tool."""

    async def search_notes(search: NoteSearchInput) -> str:
        """
        Search notes by title or content.

        Full-text search across all notes. Searches both titles and
        content fields for matches.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)
            notes = indexer.search_notes(search.query)

            if not notes:
                return f"No notes found matching '{search.query}'"

            result = f"Found {len(notes)} note(s) matching '{search.query}':\n\n"

            for n in notes:
                result += f"**{n.title}** (#{n.id})\n"
                if n.project:
                    result += f"  Project: {n.project.name}\n"
                if n.task_id:
                    result += f"  Task: #{n.task_id}\n"

                # Show content snippet
                snippet = n.content[:150]
                if len(n.content) > 150:
                    snippet += "..."
                result += f"  {snippet}\n\n"

            return result
        finally:
            session.close()

    return search_notes
