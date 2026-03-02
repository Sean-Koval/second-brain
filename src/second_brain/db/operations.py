"""Database operations for CRUD and queries."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session

from sqlalchemy import text
from .models import Project, Task, WorkLog, WorkLogEntry, Note, Transcript, Journal, JournalEntry


class ProjectOps:
    """Operations for Project model."""

    @staticmethod
    def create(
        session: Session,
        name: str,
        slug: str,
        markdown_path: str,
        description: Optional[str] = None,
        jira_project_key: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> Project:
        """Create a new project."""
        project = Project(
            name=name,
            slug=slug,
            description=description,
            jira_project_key=jira_project_key,
            tags=tags,
            markdown_path=markdown_path,
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

    @staticmethod
    def get_by_slug(session: Session, slug: str) -> Optional[Project]:
        """Get project by slug."""
        return session.scalar(select(Project).where(Project.slug == slug))

    @staticmethod
    def get_by_id(session: Session, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        return session.get(Project, project_id)

    @staticmethod
    def list_all(
        session: Session, status: Optional[str] = None, tags: Optional[List[str]] = None
    ) -> List[Project]:
        """List all projects, optionally filtered by status or tags."""
        query = select(Project)
        if status:
            query = query.where(Project.status == status)
        if tags:
            # Simple tag matching - checks if any tag is in the comma-separated list
            conditions = [Project.tags.like(f"%{tag}%") for tag in tags]
            query = query.where(or_(*conditions))
        return list(session.scalars(query).all())

    @staticmethod
    def update(session: Session, project: Project, **kwargs) -> Project:
        """Update project fields."""
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        project.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(project)
        return project


class TaskOps:
    """Operations for Task model."""

    @staticmethod
    def create(
        session: Session,
        title: str,
        description: Optional[str] = None,
        status: str = "todo",
        priority: Optional[str] = None,
        project_id: Optional[int] = None,
        jira_ticket_id: Optional[str] = None,
        jira_ticket_key: Optional[str] = None,
        tags: Optional[str] = None,
        issue_id: Optional[str] = None,
    ) -> Task:
        """Create a new task."""
        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            project_id=project_id,
            jira_ticket_id=jira_ticket_id,
            jira_ticket_key=jira_ticket_key,
            tags=tags,
            issue_id=issue_id,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_by_id(session: Session, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return session.get(Task, task_id)

    @staticmethod
    def get_by_jira_key(session: Session, jira_key: str) -> Optional[Task]:
        """Get task by Jira ticket key."""
        return session.scalar(select(Task).where(Task.jira_ticket_key == jira_key))

    @staticmethod
    def list_by_project(
        session: Session, project_id: int, status: Optional[str] = None
    ) -> List[Task]:
        """List tasks for a project."""
        query = select(Task).where(Task.project_id == project_id)
        if status:
            query = query.where(Task.status == status)
        return list(session.scalars(query).all())

    @staticmethod
    def list_all(
        session: Session,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Task]:
        """List all tasks with optional filters."""
        query = select(Task)
        conditions = []
        if status:
            conditions.append(Task.status == status)
        if priority:
            conditions.append(Task.priority == priority)
        if tags:
            tag_conditions = [Task.tags.like(f"%{tag}%") for tag in tags]
            conditions.append(or_(*tag_conditions))

        if conditions:
            query = query.where(and_(*conditions))
        return list(session.scalars(query).all())

    @staticmethod
    def update(session: Session, task: Task, **kwargs) -> Task:
        """Update task fields."""
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        task.updated_at = datetime.utcnow()
        if kwargs.get("status") == "done" and not task.completed_at:
            task.completed_at = datetime.utcnow()
        session.commit()
        session.refresh(task)
        return task


class WorkLogOps:
    """Operations for WorkLog model."""

    @staticmethod
    def create(session: Session, date: datetime, markdown_path: str) -> WorkLog:
        """Create a new work log."""
        work_log = WorkLog(date=date, markdown_path=markdown_path)
        session.add(work_log)
        session.commit()
        session.refresh(work_log)
        return work_log

    @staticmethod
    def get_by_date(session: Session, date: datetime) -> Optional[WorkLog]:
        """Get work log by date."""
        return session.scalar(select(WorkLog).where(WorkLog.date == date))

    @staticmethod
    def get_or_create(session: Session, date: datetime, markdown_path: str) -> WorkLog:
        """Get existing work log or create new one."""
        work_log = WorkLogOps.get_by_date(session, date)
        if not work_log:
            work_log = WorkLogOps.create(session, date, markdown_path)
        return work_log

    @staticmethod
    def add_entry(
        session: Session,
        work_log: WorkLog,
        entry_text: str,
        task_id: Optional[int] = None,
        time_spent_minutes: Optional[int] = None,
    ) -> WorkLogEntry:
        """Add an entry to a work log."""
        entry = WorkLogEntry(
            work_log_id=work_log.id,
            task_id=task_id,
            entry_text=entry_text,
            time_spent_minutes=time_spent_minutes,
        )
        session.add(entry)
        if task_id and time_spent_minutes:
            task = session.get(Task, task_id)
            if task:
                task.time_spent_minutes += time_spent_minutes
        session.commit()
        session.refresh(entry)
        return entry

    @staticmethod
    def list_by_date_range(
        session: Session, start_date: datetime, end_date: datetime
    ) -> List[WorkLog]:
        """List work logs within a date range."""
        query = select(WorkLog).where(
            and_(WorkLog.date >= start_date, WorkLog.date <= end_date)
        )
        return list(session.scalars(query).all())


class TranscriptOps:
    """Operations for Transcript model."""

    @staticmethod
    def create(
        session: Session,
        title: str,
        raw_path: str,
        transcript_date: datetime,
        transcript_type: str = "call",
        processed_path: Optional[str] = None,
        summary: Optional[str] = None,
        action_items: Optional[str] = None,
        linked_projects: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> Transcript:
        """Create a new transcript."""
        transcript = Transcript(
            title=title,
            transcript_type=transcript_type,
            raw_path=raw_path,
            processed_path=processed_path,
            summary=summary,
            action_items=action_items,
            linked_projects=linked_projects,
            tags=tags,
            transcript_date=transcript_date,
        )
        session.add(transcript)
        session.commit()
        session.refresh(transcript)
        return transcript

    @staticmethod
    def get_by_id(session: Session, transcript_id: int) -> Optional[Transcript]:
        """Get transcript by ID."""
        return session.get(Transcript, transcript_id)

    @staticmethod
    def list_all(
        session: Session,
        transcript_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Transcript]:
        """List transcripts with optional filters."""
        query = select(Transcript)
        conditions = []

        if transcript_type:
            conditions.append(Transcript.transcript_type == transcript_type)
        if tags:
            tag_conditions = [Transcript.tags.like(f"%{tag}%") for tag in tags]
            conditions.append(or_(*tag_conditions))
        if start_date:
            conditions.append(Transcript.transcript_date >= start_date)
        if end_date:
            conditions.append(Transcript.transcript_date <= end_date)

        if conditions:
            query = query.where(and_(*conditions))
        return list(session.scalars(query).all())

    @staticmethod
    def update(session: Session, transcript: Transcript, **kwargs) -> Transcript:
        """Update transcript fields."""
        for key, value in kwargs.items():
            if hasattr(transcript, key):
                setattr(transcript, key, value)
        transcript.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(transcript)
        return transcript


class NoteOps:
    """Operations for Note model."""

    @staticmethod
    def create(
        session: Session,
        title: str,
        content: str,
        markdown_path: str,
        project_id: Optional[int] = None,
        task_id: Optional[int] = None,
        tags: Optional[str] = None,
    ) -> Note:
        """Create a new note."""
        note = Note(
            title=title,
            content=content,
            markdown_path=markdown_path,
            project_id=project_id,
            task_id=task_id,
            tags=tags,
        )
        session.add(note)
        session.commit()
        session.refresh(note)
        return note

    @staticmethod
    def get_by_id(session: Session, note_id: int) -> Optional[Note]:
        """Get note by ID."""
        return session.get(Note, note_id)

    @staticmethod
    def list_all(session: Session, tags: Optional[List[str]] = None) -> List[Note]:
        """List all notes, optionally filtered by tags."""
        query = select(Note)
        if tags:
            tag_conditions = [Note.tags.like(f"%{tag}%") for tag in tags]
            query = query.where(or_(*tag_conditions))
        return list(session.scalars(query).all())

    @staticmethod
    def list_by_project(session: Session, project_id: int) -> List[Note]:
        """List notes for a specific project."""
        query = select(Note).where(Note.project_id == project_id)
        return list(session.scalars(query).all())

    @staticmethod
    def list_by_task(session: Session, task_id: int) -> List[Note]:
        """List notes for a specific task."""
        query = select(Note).where(Note.task_id == task_id)
        return list(session.scalars(query).all())

    @staticmethod
    def list_by_tags(session: Session, tags: List[str]) -> List[Note]:
        """List notes that match any of the given tags."""
        tag_conditions = [Note.tags.like(f"%{tag}%") for tag in tags]
        query = select(Note).where(or_(*tag_conditions))
        return list(session.scalars(query).all())

    @staticmethod
    def search(session: Session, query_text: str) -> List[Note]:
        """Search notes by title or content (case-insensitive)."""
        search_pattern = f"%{query_text}%"
        query = select(Note).where(
            or_(
                Note.title.like(search_pattern),
                Note.content.like(search_pattern),
            )
        )
        return list(session.scalars(query).all())

    @staticmethod
    def update(session: Session, note: Note, **kwargs) -> Note:
        """Update note fields."""
        for key, value in kwargs.items():
            if hasattr(note, key):
                setattr(note, key, value)
        note.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(note)
        return note

    @staticmethod
    def delete(session: Session, note: Note) -> None:
        """Delete a note."""
        session.delete(note)
        session.commit()


class JournalOps:
    """Operations for Journal and JournalEntry models."""

    @staticmethod
    def create(
        session: Session,
        date: datetime,
        markdown_path: str,
        title: Optional[str] = None,
        body: Optional[str] = None,
        summary: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> Journal:
        """Create a new journal for a date."""
        journal = Journal(
            date=date,
            markdown_path=markdown_path,
            title=title,
            body=body,
            summary=summary,
            tags=tags,
        )
        session.add(journal)
        session.commit()
        session.refresh(journal)
        return journal

    @staticmethod
    def get_by_date(session: Session, date: datetime) -> Optional[Journal]:
        """Get journal by date."""
        return session.scalar(select(Journal).where(Journal.date == date))

    @staticmethod
    def get_by_id(session: Session, journal_id: int) -> Optional[Journal]:
        """Get journal by ID."""
        return session.get(Journal, journal_id)

    @staticmethod
    def get_or_create(session: Session, date: datetime, markdown_path: str) -> Journal:
        """Get existing journal or create new one."""
        journal = JournalOps.get_by_date(session, date)
        if not journal:
            journal = JournalOps.create(session, date, markdown_path)
        return journal

    @staticmethod
    def update(session: Session, journal: Journal, **kwargs) -> Journal:
        """Update journal fields."""
        for key, value in kwargs.items():
            if hasattr(journal, key):
                setattr(journal, key, value)
        journal.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(journal)
        return journal

    @staticmethod
    def add_entry(
        session: Session,
        journal: Journal,
        entry_text: str,
        tags: Optional[str] = None,
        project_id: Optional[int] = None,
        task_id: Optional[int] = None,
        timestamp: Optional[datetime] = None,
    ) -> JournalEntry:
        """Add an entry to a journal."""
        entry = JournalEntry(
            journal_id=journal.id,
            entry_text=entry_text,
            tags=tags,
            project_id=project_id,
            task_id=task_id,
            timestamp=timestamp or datetime.utcnow(),
        )
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry

    @staticmethod
    def get_entry_by_id(session: Session, entry_id: int) -> Optional[JournalEntry]:
        """Get a journal entry by ID."""
        return session.get(JournalEntry, entry_id)

    @staticmethod
    def update_entry(session: Session, entry: JournalEntry, **kwargs) -> JournalEntry:
        """Update a journal entry."""
        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        session.commit()
        session.refresh(entry)
        return entry

    @staticmethod
    def delete_entry(session: Session, entry: JournalEntry) -> None:
        """Delete a journal entry."""
        session.delete(entry)
        session.commit()

    @staticmethod
    def list_by_date_range(
        session: Session, start_date: datetime, end_date: datetime
    ) -> List[Journal]:
        """List journals within a date range."""
        query = select(Journal).where(
            and_(Journal.date >= start_date, Journal.date <= end_date)
        ).order_by(Journal.date.desc())
        return list(session.scalars(query).all())

    @staticmethod
    def list_by_tags(session: Session, tags: List[str]) -> List[Journal]:
        """List journals matching any of the given tags."""
        tag_conditions = [Journal.tags.like(f"%{tag}%") for tag in tags]
        query = select(Journal).where(or_(*tag_conditions)).order_by(Journal.date.desc())
        return list(session.scalars(query).all())

    @staticmethod
    def list_recent(session: Session, limit: int = 7) -> List[Journal]:
        """List most recent journals."""
        query = select(Journal).order_by(Journal.date.desc()).limit(limit)
        return list(session.scalars(query).all())


class FTSOps:
    """Operations for FTS5 full-text search."""

    @staticmethod
    def insert(session: Session, content_type: str, content_id: int, content: str, tags: str = "") -> None:
        """Insert a row into the FTS5 index."""
        session.execute(
            text("INSERT INTO content_fts (content_type, content_id, content, tags) VALUES (:ct, :ci, :c, :t)"),
            {"ct": content_type, "ci": str(content_id), "c": content, "t": tags},
        )
        session.commit()

    @staticmethod
    def update(session: Session, content_type: str, content_id: int, content: str, tags: str = "") -> None:
        """Update a row in the FTS5 index (delete + re-insert)."""
        FTSOps.delete(session, content_type, content_id)
        FTSOps.insert(session, content_type, content_id, content, tags)

    @staticmethod
    def delete(session: Session, content_type: str, content_id: int) -> None:
        """Delete a row from the FTS5 index."""
        session.execute(
            text("DELETE FROM content_fts WHERE content_type = :ct AND content_id = :ci"),
            {"ct": content_type, "ci": str(content_id)},
        )
        session.commit()

    @staticmethod
    def search(session: Session, query: str, content_type: Optional[str] = None) -> List[dict]:
        """Search the FTS5 index. Returns list of dicts with content_type, content_id, snippet, tags."""
        if content_type:
            result = session.execute(
                text(
                    "SELECT content_type, content_id, snippet(content_fts, 2, '<b>', '</b>', '...', 64) as snippet, tags "
                    "FROM content_fts WHERE content_fts MATCH :q AND content_type = :ct ORDER BY rank"
                ),
                {"q": query, "ct": content_type},
            )
        else:
            result = session.execute(
                text(
                    "SELECT content_type, content_id, snippet(content_fts, 2, '<b>', '</b>', '...', 64) as snippet, tags "
                    "FROM content_fts WHERE content_fts MATCH :q ORDER BY rank"
                ),
                {"q": query},
            )
        return [
            {"content_type": row[0], "content_id": int(row[1]), "snippet": row[2], "tags": row[3]}
            for row in result
        ]

    @staticmethod
    def backfill_notes(session: Session) -> int:
        """Backfill all notes into FTS5 index. Returns count."""
        notes = session.scalars(select(Note)).all()
        count = 0
        for note in notes:
            FTSOps.delete(session, "note", note.id)
            FTSOps.insert(session, "note", note.id, f"{note.title} {note.content}", note.tags or "")
            count += 1
        return count

    @staticmethod
    def backfill_work_log_entries(session: Session) -> int:
        """Backfill all work log entries into FTS5 index. Returns count."""
        entries = session.scalars(select(WorkLogEntry)).all()
        count = 0
        for entry in entries:
            FTSOps.delete(session, "work_log_entry", entry.id)
            FTSOps.insert(session, "work_log_entry", entry.id, entry.entry_text, "")
            count += 1
        return count

    @staticmethod
    def backfill_journal_entries(session: Session) -> int:
        """Backfill all journal entries into FTS5 index. Returns count."""
        entries = session.scalars(select(JournalEntry)).all()
        count = 0
        for entry in entries:
            FTSOps.delete(session, "journal_entry", entry.id)
            FTSOps.insert(session, "journal_entry", entry.id, entry.entry_text, entry.tags or "")
            count += 1
        return count
