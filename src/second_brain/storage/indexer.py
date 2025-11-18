"""Sync between markdown files and SQLite database."""

from datetime import datetime
from pathlib import Path
from typing import Optional, List
from sqlalchemy.orm import Session

from ..db import Project, Task, WorkLog, Note, Transcript
from ..db.operations import ProjectOps, WorkLogOps, NoteOps, TranscriptOps
from .markdown import MarkdownStorage


class StorageIndexer:
    """Synchronize markdown files with SQLite index."""

    def __init__(self, session: Session, base_path: Optional[str] = None):
        """Initialize with database session and storage path.

        Args:
            session: SQLAlchemy database session
            base_path: Base path for data storage. If None, uses global config.
        """
        self.session = session

        # Use global config if base_path not provided
        if base_path is None:
            from ..config import get_config
            config = get_config()
            base_path = str(config.data_dir)

        self.storage = MarkdownStorage(base_path)

    def sync_project_to_db(self, slug: str) -> Optional[Project]:
        """Read project markdown and sync to database."""
        project_data = self.storage.read_project_file(slug)
        if not project_data:
            return None

        metadata = project_data["metadata"]
        filepath = project_data["filepath"]

        # Check if project already exists
        project = ProjectOps.get_by_slug(self.session, slug)

        if project:
            # Update existing
            ProjectOps.update(
                self.session,
                project,
                name=metadata.get("name", project.name),
                description=metadata.get("description", project.description),
                status=metadata.get("status", project.status),
                jira_project_key=metadata.get("jira_project_key"),
                tags=",".join(metadata.get("tags", [])) if metadata.get("tags") else None,
            )
        else:
            # Create new
            project = ProjectOps.create(
                self.session,
                name=metadata["name"],
                slug=slug,
                markdown_path=filepath,
                description=metadata.get("description"),
                jira_project_key=metadata.get("jira_project_key"),
                tags=",".join(metadata.get("tags", [])) if metadata.get("tags") else None,
            )

        return project

    def sync_project_to_markdown(self, project: Project) -> bool:
        """Sync project from database to markdown file."""
        # Read existing file or create template
        project_data = self.storage.read_project_file(project.slug)

        if project_data:
            # Update metadata
            metadata = project_data["metadata"]
            metadata.update(
                {
                    "name": project.name,
                    "slug": project.slug,
                    "status": project.status,
                    "description": project.description,
                    "jira_project_key": project.jira_project_key,
                    "tags": project.tags.split(",") if project.tags else [],
                    "updated_at": datetime.utcnow().isoformat(),
                }
            )
            return self.storage.update_project_file(
                project.slug, metadata, project_data["content"]
            )
        else:
            # Create new file
            self.storage.create_project_file(
                name=project.name,
                slug=project.slug,
                description=project.description,
                jira_project_key=project.jira_project_key,
                tags=project.tags.split(",") if project.tags else None,
            )
            return True

    def sync_work_log_to_db(self, date: datetime) -> Optional[WorkLog]:
        """Read work log markdown and sync to database."""
        work_log_data = self.storage.read_work_log_file(date)
        if not work_log_data:
            return None

        filepath = work_log_data["filepath"]

        # Get or create work log
        work_log = WorkLogOps.get_or_create(self.session, date, filepath)

        # Update summary from metadata
        metadata = work_log_data["metadata"]
        if "summary" in metadata:
            work_log.summary = metadata["summary"]
            self.session.commit()

        return work_log

    def sync_work_log_to_markdown(self, work_log: WorkLog) -> bool:
        """Sync work log from database to markdown file."""
        work_log_data = self.storage.read_work_log_file(work_log.date)

        if not work_log_data:
            # Create new file
            self.storage.create_work_log_file(work_log.date)

        return True

    def sync_transcript_to_db(self, processed_path: str) -> Optional[Transcript]:
        """Read transcript markdown and sync to database."""
        transcript_data = self.storage.read_transcript_file(processed_path)
        if not transcript_data:
            return None

        metadata = transcript_data["metadata"]
        filepath = transcript_data["filepath"]

        # Parse date
        transcript_date = datetime.fromisoformat(metadata["date"])

        # Check if transcript already exists by path
        # For simplicity, we'll create new for now
        # In production, you'd want to check for duplicates

        transcript = TranscriptOps.create(
            self.session,
            title=metadata["title"],
            raw_path=metadata.get("raw_file", ""),
            processed_path=filepath,
            transcript_date=transcript_date,
            transcript_type=metadata.get("type", "call"),
            summary=metadata.get("summary"),
            tags=",".join(metadata.get("tags", [])) if metadata.get("tags") else None,
        )

        return transcript

    def sync_transcript_to_markdown(self, transcript: Transcript) -> bool:
        """Sync transcript from database to markdown file."""
        # Read existing processed file
        if transcript.processed_path:
            transcript_data = self.storage.read_transcript_file(transcript.processed_path)
            if transcript_data:
                metadata = transcript_data["metadata"]
                metadata.update(
                    {
                        "title": transcript.title,
                        "type": transcript.transcript_type,
                        "summary": transcript.summary,
                        "tags": transcript.tags.split(",") if transcript.tags else [],
                        "updated_at": datetime.utcnow().isoformat(),
                    }
                )
                return self.storage.update_transcript_file(
                    transcript.processed_path, metadata, transcript_data["content"]
                )

        return False

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        jira_project_key: Optional[str] = None,
        tags: Optional[list] = None,
    ) -> Project:
        """Create a new project with markdown file and database entry."""
        slug = self.storage.slugify(name)

        # Create markdown file
        filepath = self.storage.create_project_file(
            name=name,
            slug=slug,
            description=description,
            jira_project_key=jira_project_key,
            tags=tags,
        )

        # Create database entry
        project = ProjectOps.create(
            self.session,
            name=name,
            slug=slug,
            markdown_path=filepath,
            description=description,
            jira_project_key=jira_project_key,
            tags=",".join(tags) if tags else None,
        )

        return project

    def add_work_log_entry(
        self,
        date: datetime,
        entry_text: str,
        task_id: Optional[int] = None,
        time_spent_minutes: Optional[int] = None,
    ) -> WorkLog:
        """Add an entry to work log (markdown and database)."""
        # Get or create work log
        date_str = date.strftime("%Y-%m-%d")
        filepath = str(self.storage.work_logs_path / f"{date_str}.md")
        work_log = WorkLogOps.get_or_create(self.session, date, filepath)

        # Add to markdown
        task_ref = None
        if task_id:
            task = self.session.get(Task, task_id)
            if task:
                task_ref = f"#{task_id}"

        self.storage.append_to_work_log(date, entry_text, task_ref)

        # Add to database
        WorkLogOps.add_entry(self.session, work_log, entry_text, task_id, time_spent_minutes)

        return work_log

    def create_transcript(
        self,
        title: str,
        raw_content: str,
        transcript_date: datetime,
        transcript_type: str = "call",
        tags: Optional[list] = None,
    ) -> Transcript:
        """Create a new transcript with files and database entry."""
        # Create markdown files
        raw_path, processed_path = self.storage.create_transcript_file(
            title=title,
            transcript_date=transcript_date,
            raw_content=raw_content,
            transcript_type=transcript_type,
            tags=tags,
        )

        # Create database entry
        transcript = TranscriptOps.create(
            self.session,
            title=title,
            raw_path=raw_path,
            processed_path=processed_path,
            transcript_date=transcript_date,
            transcript_type=transcript_type,
            tags=",".join(tags) if tags else None,
        )

        return transcript

    def create_note(
        self,
        title: str,
        content: str,
        project_id: Optional[int] = None,
        task_id: Optional[int] = None,
        tags: Optional[List[str]] = None,
    ) -> Note:
        """Create a new note with markdown file and database entry."""
        # Create database entry first to get ID
        note = NoteOps.create(
            self.session,
            title=title,
            content=content,
            markdown_path="",  # Will update after creating file
            project_id=project_id,
            task_id=task_id,
            tags=",".join(tags) if tags else None,
        )

        # Create markdown file
        filepath = self.storage.create_note_file(
            note_id=note.id,
            title=title,
            content=content,
            project_id=project_id,
            task_id=task_id,
            tags=tags,
        )

        # Update database with markdown path
        note.markdown_path = filepath
        self.session.commit()
        self.session.refresh(note)

        return note

    def update_note(
        self,
        note_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[Note]:
        """Update note content (both markdown and database)."""
        note = NoteOps.get_by_id(self.session, note_id)
        if not note:
            return None

        # Use existing values if not provided
        updated_title = title if title is not None else note.title
        updated_content = content if content is not None else note.content
        updated_tags = ",".join(tags) if tags is not None else note.tags

        # Update markdown file
        self.storage.update_note_file(
            note_id=note_id,
            title=updated_title,
            content=updated_content,
            metadata={"tags": tags} if tags else None,
        )

        # Update database
        NoteOps.update(
            self.session,
            note,
            title=updated_title,
            content=updated_content,
            tags=updated_tags,
        )

        return note

    def append_to_note(self, note_id: int, additional_content: str) -> Optional[Note]:
        """Append content to an existing note."""
        note = NoteOps.get_by_id(self.session, note_id)
        if not note:
            return None

        # Append to markdown file
        self.storage.append_to_note(note_id, additional_content)

        # Update database content
        updated_content = note.content + f"\n\n{additional_content}"
        NoteOps.update(self.session, note, content=updated_content)

        return note

    def search_notes(self, query_text: str) -> List[Note]:
        """Search notes by title or content."""
        return NoteOps.search(self.session, query_text)
