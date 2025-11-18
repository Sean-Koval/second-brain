"""SQLite database models for indexing and metadata."""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Text,
    ForeignKey,
    create_engine,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Project(Base):
    """Project model for tracking work projects."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="active", nullable=False
    )  # active, completed, archived
    jira_project_key: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Comma-separated
    markdown_path: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project")
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="project")


class Task(Base):
    """Task model for tracking individual work items."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="todo", nullable=False
    )  # todo, in_progress, done, blocked
    priority: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )  # low, medium, high, urgent
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    jira_ticket_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    jira_ticket_key: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    issue_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)  # Link to Beads issue
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Comma-separated
    time_spent_minutes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="tasks")
    work_log_entries: Mapped[list["WorkLogEntry"]] = relationship(
        "WorkLogEntry", back_populates="task"
    )
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="task")


class WorkLog(Base):
    """Daily work log."""

    __tablename__ = "work_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, unique=True, nullable=False, index=True)
    markdown_path: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    entries: Mapped[list["WorkLogEntry"]] = relationship("WorkLogEntry", back_populates="work_log")


class WorkLogEntry(Base):
    """Individual entry within a work log."""

    __tablename__ = "work_log_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    work_log_id: Mapped[int] = mapped_column(ForeignKey("work_logs.id"), nullable=False)
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    entry_text: Mapped[str] = mapped_column(Text, nullable=False)
    time_spent_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    work_log: Mapped["WorkLog"] = relationship("WorkLog", back_populates="entries")
    task: Mapped[Optional["Task"]] = relationship("Task", back_populates="work_log_entries")


class Note(Base):
    """Rich markdown note attached to project or task."""

    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)  # Markdown content
    markdown_path: Mapped[str] = mapped_column(String(500), nullable=False)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Comma-separated
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="notes")
    task: Mapped[Optional["Task"]] = relationship("Task", back_populates="notes")


class Transcript(Base):
    """Call/meeting transcript."""

    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    transcript_type: Mapped[str] = mapped_column(
        String(50), default="call", nullable=False
    )  # call, meeting, etc.
    raw_path: Mapped[str] = mapped_column(String(500), nullable=False)
    processed_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_items: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    linked_projects: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # Comma-separated project IDs
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transcript_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


# Create indexes for common queries
Index("idx_project_status", Project.status)
Index("idx_task_status", Task.status)
Index("idx_task_project", Task.project_id)
Index("idx_task_issue", Task.issue_id)
Index("idx_note_project", Note.project_id)
Index("idx_note_task", Note.task_id)
Index("idx_worklog_date", WorkLog.date)
Index("idx_transcript_date", Transcript.transcript_date)


def init_db(db_path: str = "data/index.db") -> None:
    """Initialize the database with all tables."""
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine) -> Session:
    """Get a database session."""
    return Session(engine)
