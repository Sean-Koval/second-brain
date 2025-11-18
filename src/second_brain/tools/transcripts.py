"""MCP tools for transcript processing."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from ..db import get_session
from ..db.operations import TranscriptOps
from ..storage import StorageIndexer


class TranscriptCreateInput(BaseModel):
    """Input for creating a transcript."""

    title: str = Field(..., description="Transcript title")
    raw_content: str = Field(..., description="Raw transcript text")
    transcript_type: str = Field("call", description="Type of transcript (call, meeting, etc.)")
    transcript_date: Optional[str] = Field(
        None, description="Date of transcript (YYYY-MM-DD), defaults to today"
    )
    tags: Optional[List[str]] = Field(None, description="List of tags")


class TranscriptUpdateInput(BaseModel):
    """Input for updating a transcript."""

    transcript_id: int = Field(..., description="Transcript ID to update")
    summary: Optional[str] = Field(None, description="Summary of the transcript")
    action_items: Optional[str] = Field(None, description="Action items (JSON string)")
    linked_projects: Optional[str] = Field(
        None, description="Comma-separated list of project IDs to link"
    )
    tags: Optional[List[str]] = Field(None, description="Updated tags")


class TranscriptQueryInput(BaseModel):
    """Input for querying transcripts."""

    transcript_type: Optional[str] = Field(None, description="Filter by type")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")


def create_transcript_tool(engine):
    """Create a new transcript tool."""

    async def create_transcript(transcript: TranscriptCreateInput) -> str:
        """
        Create a new call/meeting transcript.

        This tool saves both raw and processed transcript files. The raw
        transcript is stored as plain text, while a markdown template is
        created for processing notes, summaries, and action items.

        Useful for capturing and organizing meeting notes, call recordings,
        and interview transcripts.
        """
        session = get_session(engine)
        try:
            indexer = StorageIndexer(session)

            # Parse date or use today
            if transcript.transcript_date:
                trans_date = datetime.strptime(transcript.transcript_date, "%Y-%m-%d")
            else:
                trans_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # Create transcript
            new_transcript = indexer.create_transcript(
                title=transcript.title,
                raw_content=transcript.raw_content,
                transcript_date=trans_date,
                transcript_type=transcript.transcript_type,
                tags=transcript.tags,
            )

            tags_str = f"\nTags: {', '.join(transcript.tags)}" if transcript.tags else ""

            return (
                f"Transcript created successfully!\n"
                f"ID: {new_transcript.id}\n"
                f"Title: {new_transcript.title}\n"
                f"Type: {new_transcript.transcript_type}\n"
                f"Date: {trans_date.strftime('%Y-%m-%d')}{tags_str}\n\n"
                f"Raw file: {new_transcript.raw_path}\n"
                f"Processed file: {new_transcript.processed_path}\n\n"
                f"Use the update_transcript tool to add summary, action items, and link to projects."
            )
        finally:
            session.close()

    return create_transcript


def update_transcript_tool(engine):
    """Update a transcript with processed information tool."""

    async def update_transcript(update: TranscriptUpdateInput) -> str:
        """
        Update a transcript with processed information.

        Add summaries, action items, and link transcripts to relevant projects.
        This is typically done after an agent processes the raw transcript
        to extract key information.
        """
        session = get_session(engine)
        try:
            transcript = TranscriptOps.get_by_id(session, update.transcript_id)
            if not transcript:
                return f"Error: Transcript with ID {update.transcript_id} not found"

            # Prepare updates
            updates = {}
            if update.summary is not None:
                updates["summary"] = update.summary
            if update.action_items is not None:
                updates["action_items"] = update.action_items
            if update.linked_projects is not None:
                updates["linked_projects"] = update.linked_projects
            if update.tags is not None:
                updates["tags"] = ",".join(update.tags)

            if not updates:
                return "No updates provided"

            # Update database
            updated_transcript = TranscriptOps.update(session, transcript, **updates)

            # Sync to markdown
            indexer = StorageIndexer(session)
            indexer.sync_transcript_to_markdown(updated_transcript)

            result = f"Transcript #{updated_transcript.id} updated successfully!\n"
            result += f"Title: {updated_transcript.title}\n"

            if updated_transcript.summary:
                summary_preview = (
                    updated_transcript.summary[:100] + "..."
                    if len(updated_transcript.summary) > 100
                    else updated_transcript.summary
                )
                result += f"Summary: {summary_preview}\n"

            if updated_transcript.linked_projects:
                result += f"Linked projects: {updated_transcript.linked_projects}\n"

            return result
        finally:
            session.close()

    return update_transcript


def get_transcripts_tool(engine):
    """Query transcripts with filters tool."""

    async def get_transcripts(query: TranscriptQueryInput) -> str:
        """
        Query transcripts with optional filters.

        Search through call and meeting transcripts by type, tags, or date range.
        Useful for finding specific conversations, reviewing past meetings,
        or extracting information from recordings.
        """
        session = get_session(engine)
        try:
            # Parse dates
            start_date = None
            end_date = None
            if query.start_date:
                start_date = datetime.strptime(query.start_date, "%Y-%m-%d")
            if query.end_date:
                end_date = datetime.strptime(query.end_date, "%Y-%m-%d")

            transcripts = TranscriptOps.list_all(
                session,
                transcript_type=query.transcript_type,
                tags=query.tags,
                start_date=start_date,
                end_date=end_date,
            )

            if not transcripts:
                return "No transcripts found matching the criteria"

            result = f"Found {len(transcripts)} transcript(s):\n\n"

            for t in transcripts:
                result += f"## {t.title} (#{t.id})\n\n"
                result += f"**Type:** {t.transcript_type}\n"
                result += f"**Date:** {t.transcript_date.strftime('%Y-%m-%d')}\n"

                if t.tags:
                    result += f"**Tags:** {t.tags}\n"

                if t.summary:
                    summary_preview = (
                        t.summary[:150] + "..." if len(t.summary) > 150 else t.summary
                    )
                    result += f"**Summary:** {summary_preview}\n"

                if t.linked_projects:
                    result += f"**Linked Projects:** {t.linked_projects}\n"

                result += f"**Raw file:** {t.raw_path}\n"
                if t.processed_path:
                    result += f"**Processed file:** {t.processed_path}\n"

                result += "\n"

            return result
        finally:
            session.close()

    return get_transcripts


def get_transcript_content_tool(engine):
    """Get the full content of a specific transcript tool."""

    async def get_transcript_content(transcript_id: int) -> str:
        """
        Get the full content of a specific transcript.

        Retrieves both the raw transcript text and any processed notes.
        Useful when an agent needs to analyze or summarize the full transcript.
        """
        session = get_session(engine)
        try:
            transcript = TranscriptOps.get_by_id(session, transcript_id)
            if not transcript:
                return f"Error: Transcript with ID {transcript_id} not found"

            # Read the files
            indexer = StorageIndexer(session)
            storage = indexer.storage

            # Read processed file if it exists
            processed_data = None
            if transcript.processed_path:
                processed_data = storage.read_transcript_file(transcript.processed_path)

            result = f"# {transcript.title}\n\n"
            result += f"**ID:** {transcript.id}\n"
            result += f"**Type:** {transcript.transcript_type}\n"
            result += f"**Date:** {transcript.transcript_date.strftime('%Y-%m-%d')}\n"

            if transcript.tags:
                result += f"**Tags:** {transcript.tags}\n"

            result += "\n---\n\n"

            if processed_data and processed_data.get("content"):
                result += "## Processed Notes\n\n"
                result += processed_data["content"]
                result += "\n\n---\n\n"

            if processed_data and processed_data.get("raw_content"):
                result += "## Raw Transcript\n\n"
                # Truncate if too long
                raw = processed_data["raw_content"]
                if len(raw) > 5000:
                    result += f"{raw[:5000]}\n\n... [truncated, {len(raw)} characters total]"
                else:
                    result += raw
            else:
                result += "## Raw Transcript\n\n"
                result += f"Raw file path: {transcript.raw_path}\n"
                result += "(Use file reading tools to access the full raw transcript)"

            return result
        finally:
            session.close()

    return get_transcript_content
