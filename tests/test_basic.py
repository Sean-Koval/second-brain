"""Basic tests for second brain functionality."""

import pytest
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

from second_brain.db import init_db, get_session
from second_brain.db.operations import ProjectOps, TaskOps, WorkLogOps
from second_brain.storage import MarkdownStorage, StorageIndexer


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def db_session(temp_data_dir):
    """Create a test database session."""
    db_path = Path(temp_data_dir) / "test.db"
    engine = init_db(str(db_path))
    session = get_session(engine)
    yield session
    session.close()


@pytest.fixture
def storage(temp_data_dir):
    """Create a test markdown storage."""
    return MarkdownStorage(temp_data_dir)


@pytest.fixture
def indexer(db_session, temp_data_dir):
    """Create a test storage indexer."""
    return StorageIndexer(db_session, temp_data_dir)


class TestProjectOperations:
    """Test project CRUD operations."""

    def test_create_project(self, db_session):
        """Test creating a project."""
        project = ProjectOps.create(
            db_session,
            name="Test Project",
            slug="test-project",
            markdown_path="/tmp/test.md",
            description="A test project",
        )

        assert project.id is not None
        assert project.name == "Test Project"
        assert project.slug == "test-project"
        assert project.status == "active"

    def test_get_project_by_slug(self, db_session):
        """Test retrieving a project by slug."""
        ProjectOps.create(
            db_session,
            name="Test Project",
            slug="test-project",
            markdown_path="/tmp/test.md",
        )

        project = ProjectOps.get_by_slug(db_session, "test-project")
        assert project is not None
        assert project.name == "Test Project"

    def test_list_projects_by_status(self, db_session):
        """Test listing projects filtered by status."""
        ProjectOps.create(
            db_session, name="Active Project", slug="active", markdown_path="/tmp/active.md"
        )

        proj2 = ProjectOps.create(
            db_session, name="Done Project", slug="done", markdown_path="/tmp/done.md"
        )
        ProjectOps.update(db_session, proj2, status="completed")

        active_projects = ProjectOps.list_all(db_session, status="active")
        assert len(active_projects) == 1
        assert active_projects[0].name == "Active Project"


class TestTaskOperations:
    """Test task CRUD operations."""

    def test_create_task(self, db_session):
        """Test creating a task."""
        task = TaskOps.create(
            db_session,
            title="Test Task",
            description="A test task",
            status="todo",
            priority="high",
        )

        assert task.id is not None
        assert task.title == "Test Task"
        assert task.status == "todo"
        assert task.priority == "high"

    def test_update_task_status(self, db_session):
        """Test updating task status."""
        task = TaskOps.create(db_session, title="Test Task")
        assert task.status == "todo"
        assert task.completed_at is None

        TaskOps.update(db_session, task, status="done")
        assert task.status == "done"
        assert task.completed_at is not None

    def test_task_time_tracking(self, db_session):
        """Test time tracking on tasks."""
        task = TaskOps.create(db_session, title="Test Task")
        assert task.time_spent_minutes == 0

        TaskOps.update(db_session, task, time_spent_minutes=60)
        assert task.time_spent_minutes == 60


class TestMarkdownStorage:
    """Test markdown file operations."""

    def test_create_project_file(self, storage):
        """Test creating a project markdown file."""
        filepath = storage.create_project_file(
            name="Test Project",
            slug="test-project",
            description="A test project",
        )

        assert Path(filepath).exists()
        assert "test-project.md" in filepath

    def test_read_project_file(self, storage):
        """Test reading a project markdown file."""
        storage.create_project_file(
            name="Test Project",
            slug="test-project",
            description="A test project",
        )

        data = storage.read_project_file("test-project")
        assert data is not None
        assert data["metadata"]["name"] == "Test Project"
        assert "# Test Project" in data["content"]

    def test_create_work_log_file(self, storage):
        """Test creating a work log file."""
        date = datetime.now()
        filepath = storage.create_work_log_file(date)

        assert Path(filepath).exists()
        assert date.strftime("%Y-%m-%d") in filepath

    def test_append_to_work_log(self, storage):
        """Test appending entries to work log."""
        date = datetime.now()
        storage.create_work_log_file(date)

        result = storage.append_to_work_log(date, "Worked on testing")
        assert result is True

        data = storage.read_work_log_file(date)
        assert "Worked on testing" in data["content"]


class TestStorageIndexer:
    """Test storage synchronization."""

    def test_create_project_with_indexer(self, indexer):
        """Test creating a project with full sync."""
        project = indexer.create_project(
            name="Test Project",
            description="A test project",
            tags=["test", "demo"],
        )

        assert project.id is not None
        assert Path(project.markdown_path).exists()

    def test_add_work_log_entry(self, indexer):
        """Test adding work log entry with sync."""
        date = datetime.now()
        work_log = indexer.add_work_log_entry(date, "Completed feature X")

        assert work_log is not None
        assert len(work_log.entries) > 0
        assert work_log.entries[0].entry_text == "Completed feature X"


class TestIntegration:
    """Integration tests."""

    def test_project_with_tasks_workflow(self, indexer):
        """Test complete workflow: project -> tasks -> work log."""
        # Create project
        project = indexer.create_project("Test Project", "Integration test")

        # Create tasks
        from second_brain.db.operations import TaskOps

        task1 = TaskOps.create(
            indexer.session,
            title="Task 1",
            project_id=project.id,
            status="todo",
        )

        task2 = TaskOps.create(
            indexer.session,
            title="Task 2",
            project_id=project.id,
            status="todo",
        )

        # Update task status
        TaskOps.update(indexer.session, task1, status="in_progress")

        # Add work log
        work_log = indexer.add_work_log_entry(
            datetime.now(),
            "Worked on task 1",
            task_id=task1.id,
            time_spent_minutes=30,
        )

        # Verify
        assert len(project.tasks) == 2
        assert task1.status == "in_progress"
        assert task1.time_spent_minutes == 30
        assert len(work_log.entries) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
