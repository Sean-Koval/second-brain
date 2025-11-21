"""Command-line interface for Second Brain."""

import os
import sys
from datetime import datetime
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

from .db import init_db, get_session
from .db.operations import ProjectOps, TaskOps, WorkLogOps, TranscriptOps, NoteOps
from .storage import StorageIndexer
from .config import get_config
from .utils import datetime_utils

console = Console()

# Global config instance (initialized lazily)
_config = None


def get_app_config():
    """Get application config instance."""
    global _config
    if _config is None:
        _config = get_config()
    return _config


def get_db_session():
    """Get database session."""
    config = get_app_config()
    engine = init_db(str(config.db_path))
    return get_session(engine), engine


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Second Brain - Work tracking CLI and MCP server."""
    pass


@cli.command()
@click.option("--global", "is_global", is_flag=True, help="Initialize in ~/.second-brain/ (recommended)")
@click.option("--data-dir", default=None, help="Custom data directory path (for local setup)")
@click.option("--beads", is_flag=True, help="Initialize Beads for epic/issue tracking in current directory")
@click.option("--prefix", default="SB", help="Issue prefix for Beads (default: SB)")
def init(is_global, data_dir, beads, prefix):
    """Initialize second brain.

    By default, initializes globally in ~/.second-brain/ (recommended).
    Use --beads to initialize Beads for epic/issue tracking in current directory.
    Use --data-dir for local project setup (legacy).
    """
    global _config

    # Handle Beads initialization
    if beads:
        import subprocess

        # Check if bd is available
        try:
            result = subprocess.run(["bd", "version"], capture_output=True, text=True)
            if result.returncode != 0:
                console.print("[red]Error: bd command not found. Install beads-mcp first:[/red]")
                console.print("  uv pip install beads-mcp")
                return
        except FileNotFoundError:
            console.print("[red]Error: bd command not found. Install beads-mcp first:[/red]")
            console.print("  uv pip install beads-mcp")
            return

        # Initialize bd in current directory
        console.print(f"[bold]Initializing Beads in current directory...[/bold]")
        result = subprocess.run(["bd", "init", "--prefix", prefix], capture_output=True, text=True)

        if result.returncode == 0:
            console.print(f"[green]✓[/green] Beads initialized successfully!")
            console.print(f"\nIssue prefix: {prefix}")
            console.print(f"Database: .beads/{prefix}.db")
            console.print(f"Issues will be named: {prefix}-1, {prefix}-2, ...")
            console.print("\n[bold]You can now use epic/issue commands:[/bold]")
            console.print(f"  sb epic create \"My Epic\"")
            console.print(f"  sb issue create \"My Issue\" --epic {prefix}-1")
            console.print(f"  sb issue ready")
            console.print(f"  sb issue stats")
        else:
            console.print(f"[red]Error initializing Beads:[/red]")
            console.print(result.stderr if result.stderr else result.stdout)

        return

    # Determine setup type
    if is_global:
        config = get_config(force_global=True)
        setup_location = config.second_brain_dir
        setup_type = "global"
    elif data_dir:
        # Local setup with custom path
        setup_location = Path(data_dir)
        setup_type = "local"
        config = None
    else:
        # Default to global
        config = get_config(force_global=True)
        setup_location = config.second_brain_dir
        setup_type = "global"

    # Check if already exists
    if setup_location.exists() and any(setup_location.iterdir()):
        console.print(f"[yellow]Warning: {setup_location} already exists and is not empty[/yellow]")
        if not click.confirm("Continue anyway?"):
            return

    # Initialize based on setup type
    if setup_type == "global":
        # Use config to initialize global setup
        config.initialize_global_setup()
        init_db(str(config.db_path))

        # Create .gitignore
        gitignore_path = config.second_brain_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_content = """# Temporary files
*.tmp
*.swp
*~
.*.swp

# OS files
.DS_Store
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments (if you put one here)
venv/
.venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.sublime-*

# Uncomment to exclude sensitive data from git
# config.json
# data/transcripts/raw/
"""
            gitignore_path.write_text(gitignore_content)

        # Create README.md
        readme_path = config.second_brain_dir / "README.md"
        if not readme_path.exists():
            readme_content = f"""# My Second Brain

This is my personal Second Brain - a knowledge management and work tracking system.

## Setup

This directory contains:
- `data/` - All my work logs, projects, tasks, and transcripts
- `config.json` - My Second Brain configuration
- `.gitignore` - Git ignore rules

## Usage

From any directory on this machine:

```bash
# Add work log entry
sb log add "Working on project X"

# Create a task
sb task add "Implement feature Y"

# Generate report
sb report work --days 7
```

## Syncing

This directory is a git repository. To sync to other machines:

```bash
git add .
git commit -m "Update work logs"
git push
```

## Documentation

See the [Second Brain documentation](https://github.com/yourusername/second-brain) for more information.

---

**Location:** `{config.second_brain_dir}`
**Initialized:** {datetime.now().strftime('%Y-%m-%d')}
"""
            readme_path.write_text(readme_content)

        console.print(f"[green]✓[/green] Second Brain initialized globally!")
        console.print(f"\nLocation: {config.second_brain_dir}")
        console.print("\nCreated:")
        console.print(f"  - {config.data_dir}/")
        console.print(f"  - {config.projects_dir}/")
        console.print(f"  - {config.work_logs_dir}/")
        console.print(f"  - {config.transcripts_dir}/")
        console.print(f"  - {config.db_path}")
        console.print(f"  - {config.config_file}")
        console.print(f"  - .gitignore")
        console.print(f"  - README.md")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("1. Add to your shell profile (~/.bashrc or ~/.zshrc):")
        console.print(f'   export SECOND_BRAIN_DIR="$HOME/.second-brain"')
        console.print("\n2. (Optional) Initialize as git repository:")
        console.print(f"   cd {config.second_brain_dir}")
        console.print("   git init")
        console.print("   git add .")
        console.print('   git commit -m "Initial second brain setup"')
        console.print("\n3. (Optional) Create private GitHub repo:")
        console.print("   gh repo create {yourname}-second-brain --private")
        console.print("   git remote add origin git@github.com:{yourname}/{yourname}-second-brain.git")
        console.print("   git push -u origin main")

        # Update global config
        _config = config
    else:
        # Legacy local setup
        data_path = setup_location
        (data_path / "projects").mkdir(parents=True, exist_ok=True)
        (data_path / "work_logs").mkdir(parents=True, exist_ok=True)
        (data_path / "transcripts" / "raw").mkdir(parents=True, exist_ok=True)
        (data_path / "transcripts" / "processed").mkdir(parents=True, exist_ok=True)

        db_path = data_path / "index.db"
        init_db(str(db_path))

        console.print(f"[green]✓[/green] Second brain initialized in {data_dir}/")
        console.print("\nCreated:")
        console.print(f"  - {data_dir}/projects/")
        console.print(f"  - {data_dir}/work_logs/")
        console.print(f"  - {data_dir}/transcripts/")
        console.print(f"  - {data_dir}/index.db")
        console.print("\nSet SECOND_BRAIN_DIR environment variable to use this location:")
        console.print(f"  export SECOND_BRAIN_DIR={data_path.absolute()}")


# Work log commands
@cli.group()
def log():
    """Work log commands."""
    pass


@log.command("add")
@click.argument("entry_text")
@click.option("--task-id", type=int, help="Task ID to link")
@click.option("--time", type=int, help="Time spent in minutes")
@click.option("--date", help="Date (YYYY-MM-DD), defaults to today")
def log_add(entry_text, task_id, time, date):
    """Add a work log entry."""
    config = get_app_config()
    session, engine = get_db_session()
    try:
        indexer = StorageIndexer(session, str(config.data_dir))

        # Parse date
        if date:
            log_date = datetime.strptime(date, "%Y-%m-%d")
        else:
            log_date = datetime_utils.now().replace(hour=0, minute=0, second=0, microsecond=0)

        indexer.add_work_log_entry(log_date, entry_text, task_id, time)

        console.print(f"[green]✓[/green] Work log entry added for {log_date.strftime('%Y-%m-%d')}")
    finally:
        session.close()


@log.command("show")
@click.option("--days", type=int, default=7, help="Number of days to show")
def log_show(days):
    """Show recent work logs."""
    session, engine = get_db_session()
    try:
        from datetime import timedelta

        end_date = datetime_utils.now()
        start_date = end_date - timedelta(days=days)

        work_logs = WorkLogOps.list_by_date_range(session, start_date, end_date)

        if not work_logs:
            console.print("[yellow]No work logs found[/yellow]")
            return

        for wl in reversed(work_logs):
            console.print(f"\n[bold cyan]{wl.date.strftime('%Y-%m-%d')}[/bold cyan]")
            if wl.entries:
                for entry in wl.entries:
                    time_str = entry.timestamp.strftime("%H:%M")
                    task_str = f" [{entry.task.title}]" if entry.task else ""
                    console.print(f"  {time_str}{task_str}: {entry.entry_text}")
    finally:
        session.close()


# Project commands
@cli.group()
def project():
    """Project commands."""
    pass


@project.command("create")
@click.argument("name")
@click.option("--description", "-d", help="Project description")
@click.option("--jira", help="Jira project key")
@click.option("--tags", help="Comma-separated tags")
def project_create(name, description, jira, tags):
    """Create a new project."""
    config = get_app_config()
    session, engine = get_db_session()
    try:
        indexer = StorageIndexer(session, str(config.data_dir))

        tag_list = tags.split(",") if tags else None
        project = indexer.create_project(name, description, jira, tag_list)

        console.print(f"[green]✓[/green] Project created: {project.name}")
        console.print(f"  Slug: {project.slug}")
        console.print(f"  File: {project.markdown_path}")
    finally:
        session.close()


@project.command("list")
@click.option("--status", help="Filter by status")
def project_list(status):
    """List all projects."""
    session, engine = get_db_session()
    try:
        projects = ProjectOps.list_all(session, status=status)

        if not projects:
            console.print("[yellow]No projects found[/yellow]")
            return

        table = Table(title="Projects")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="bold")
        table.add_column("Status")
        table.add_column("Tasks")
        table.add_column("Jira")

        for p in projects:
            task_count = len(p.tasks)
            active_tasks = sum(1 for t in p.tasks if t.status in ["todo", "in_progress"])

            table.add_row(
                str(p.id),
                p.name,
                p.status,
                f"{active_tasks}/{task_count}",
                p.jira_project_key or "-",
            )

        console.print(table)
    finally:
        session.close()


@project.command("status")
@click.argument("slug")
def project_status(slug):
    """Show detailed project status."""
    session, engine = get_db_session()
    try:
        project = ProjectOps.get_by_slug(session, slug)
        if not project:
            console.print(f"[red]Error: Project '{slug}' not found[/red]")
            return

        console.print(f"\n[bold]{project.name}[/bold]")
        console.print(f"Status: {project.status}")
        if project.description:
            console.print(f"Description: {project.description}")

        tasks = TaskOps.list_by_project(session, project.id)
        if tasks:
            console.print(f"\nTotal tasks: {len(tasks)}")

            # Count by status
            for status in ["todo", "in_progress", "blocked", "done"]:
                count = sum(1 for t in tasks if t.status == status)
                if count > 0:
                    console.print(f"  {status}: {count}")

            # Show active tasks
            active = [t for t in tasks if t.status in ["todo", "in_progress"]]
            if active:
                console.print("\n[bold]Active tasks:[/bold]")
                for task in active[:5]:
                    emoji = "🔄" if task.status == "in_progress" else "⬜"
                    console.print(f"  {emoji} #{task.id}: {task.title}")
    finally:
        session.close()


# Task commands
@cli.group()
def task():
    """Task commands."""
    pass


@task.command("add")
@click.argument("title")
@click.option("--project", "-p", help="Project slug")
@click.option("--description", "-d", help="Task description")
@click.option("--priority", type=click.Choice(["low", "medium", "high", "urgent"]))
@click.option("--with-issue", is_flag=True, help="Create a linked Beads issue")
@click.option("--issue-id", help="Link to existing Beads issue ID")
def task_add(title, project, description, priority, with_issue, issue_id):
    """Add a new task."""
    session, engine = get_db_session()
    try:
        project_id = None
        proj = None
        if project:
            proj = ProjectOps.get_by_slug(session, project)
            if not proj:
                console.print(f"[red]Error: Project '{project}' not found[/red]")
                return
            project_id = proj.id

        # Create the task
        task = TaskOps.create(
            session, title, description, "todo", priority, project_id, issue_id=issue_id
        )

        console.print(f"[green]✓[/green] Task created: #{task.id} {task.title}")
        if proj:
            console.print(f"  Project: {proj.name}")

        # Create linked Beads issue if requested
        if with_issue:
            from .integrations.beads_integration import get_beads_client
            import asyncio

            config = get_app_config()
            client = get_beads_client(str(config.data_dir))

            if not client:
                console.print(
                    "[yellow]Warning: Beads integration not available. Task created without issue link.[/yellow]"
                )
            else:

                async def _create_issue():
                    try:
                        # Map priority to Beads priority (0-4)
                        priority_map = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
                        beads_priority = priority_map.get(priority, 2)

                        issue = await client.create_issue(
                            title=title,
                            description=description or "",
                            issue_type="task",
                            priority=beads_priority,
                            external_ref=f"sb-task-{task.id}",
                        )

                        # Update task with issue_id
                        TaskOps.update(session, task, issue_id=issue.id)

                        console.print(f"[green]✓[/green] Linked Beads issue created: {issue.id}")
                        console.print(f"  External ref: sb-task-{task.id}")
                    except Exception as e:
                        console.print(f"[yellow]Warning: Failed to create Beads issue: {e}[/yellow]")

                asyncio.run(_create_issue())

        if issue_id:
            console.print(f"  Linked to issue: {issue_id}")
    finally:
        session.close()


@task.command("update")
@click.argument("task_id", type=int)
@click.option("--status", type=click.Choice(["todo", "in_progress", "done", "blocked"]))
@click.option("--priority", type=click.Choice(["low", "medium", "high", "urgent"]))
@click.option("--time", type=int, help="Add time spent in minutes")
def task_update(task_id, status, priority, time):
    """Update a task."""
    session, engine = get_db_session()
    try:
        task = TaskOps.get_by_id(session, task_id)
        if not task:
            console.print(f"[red]Error: Task #{task_id} not found[/red]")
            return

        updates = {}
        if status:
            updates["status"] = status
        if priority:
            updates["priority"] = priority
        if time:
            updates["time_spent_minutes"] = task.time_spent_minutes + time

        if updates:
            TaskOps.update(session, task, **updates)
            console.print(f"[green]✓[/green] Task #{task_id} updated")
        else:
            console.print("[yellow]No updates provided[/yellow]")
    finally:
        session.close()


@task.command("list")
@click.option("--project", "-p", help="Filter by project slug")
@click.option("--status", help="Filter by status")
@click.option("--priority", help="Filter by priority")
def task_list(project, status, priority):
    """List tasks."""
    session, engine = get_db_session()
    try:
        if project:
            proj = ProjectOps.get_by_slug(session, project)
            if not proj:
                console.print(f"[red]Error: Project '{project}' not found[/red]")
                return
            tasks = TaskOps.list_by_project(session, proj.id, status=status)
        else:
            tasks = TaskOps.list_all(session, status=status, priority=priority)

        if not tasks:
            console.print("[yellow]No tasks found[/yellow]")
            return

        table = Table(title="Tasks")
        table.add_column("ID", style="cyan")
        table.add_column("Status")
        table.add_column("Title", style="bold")
        table.add_column("Priority")
        table.add_column("Project")

        for t in tasks:
            status_emoji = {"todo": "⬜", "in_progress": "🔄", "done": "✅", "blocked": "🚫"}.get(
                t.status, "⬜"
            )

            table.add_row(
                str(t.id),
                f"{status_emoji} {t.status}",
                t.title[:50] + "..." if len(t.title) > 50 else t.title,
                t.priority or "-",
                t.project.name if t.project else "-",
            )

        console.print(table)
    finally:
        session.close()


# Note commands
@cli.group()
def note():
    """Note management commands."""
    pass


@note.command("create")
@click.argument("title")
@click.option("--content", "-c", default="", help="Note content (markdown)")
@click.option("--project", "-p", help="Project slug to attach to")
@click.option("--task-id", "-t", type=int, help="Task ID to attach to")
@click.option("--tags", help="Comma-separated tags")
def note_create(title, content, project, task_id, tags):
    """Create a new note."""
    config = get_app_config()
    session, engine = get_db_session()
    try:
        indexer = StorageIndexer(session, str(config.data_dir))

        project_id = None
        proj = None
        if project:
            proj = ProjectOps.get_by_slug(session, project)
            if not proj:
                console.print(f"[red]Error: Project '{project}' not found[/red]")
                return
            project_id = proj.id

        if task_id:
            task = TaskOps.get_by_id(session, task_id)
            if not task:
                console.print(f"[red]Error: Task #{task_id} not found[/red]")
                return

        tag_list = tags.split(",") if tags else None
        note = indexer.create_note(title, content, project_id, task_id, tag_list)

        console.print(f"[green]✓[/green] Note created: #{note.id} {note.title}")
        console.print(f"  File: {note.markdown_path}")
        if proj:
            console.print(f"  Project: {proj.name}")
        if task_id:
            console.print(f"  Task: #{task_id}")
    finally:
        session.close()


@note.command("add")
@click.argument("note_id", type=int)
@click.argument("content")
def note_add(note_id, content):
    """Append content to an existing note."""
    config = get_app_config()
    session, engine = get_db_session()
    try:
        indexer = StorageIndexer(session, str(config.data_dir))
        note = indexer.append_to_note(note_id, content)

        if not note:
            console.print(f"[red]Error: Note #{note_id} not found[/red]")
            return

        console.print(f"[green]✓[/green] Content added to note #{note_id}")
    finally:
        session.close()


@note.command("list")
@click.option("--project", "-p", help="Filter by project slug")
@click.option("--task-id", "-t", type=int, help="Filter by task ID")
@click.option("--tags", help="Filter by tags (comma-separated)")
def note_list(project, task_id, tags):
    """List notes."""
    session, engine = get_db_session()
    try:
        if project:
            proj = ProjectOps.get_by_slug(session, project)
            if not proj:
                console.print(f"[red]Error: Project '{project}' not found[/red]")
                return
            notes = NoteOps.list_by_project(session, proj.id)
        elif task_id:
            notes = NoteOps.list_by_task(session, task_id)
        elif tags:
            tag_list = tags.split(",")
            notes = NoteOps.list_by_tags(session, tag_list)
        else:
            notes = NoteOps.list_all(session)

        if not notes:
            console.print("[yellow]No notes found[/yellow]")
            return

        table = Table(title="Notes")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="bold")
        table.add_column("Project")
        table.add_column("Task")
        table.add_column("Tags")

        for n in notes:
            table.add_row(
                str(n.id),
                n.title[:50] + "..." if len(n.title) > 50 else n.title,
                n.project.name if n.project else "-",
                f"#{n.task_id}" if n.task_id else "-",
                n.tags or "-",
            )

        console.print(table)
    finally:
        session.close()


@note.command("search")
@click.argument("query")
def note_search(query):
    """Search notes by title or content."""
    config = get_app_config()
    session, engine = get_db_session()
    try:
        indexer = StorageIndexer(session, str(config.data_dir))
        notes = indexer.search_notes(query)

        if not notes:
            console.print(f"[yellow]No notes found matching '{query}'[/yellow]")
            return

        console.print(f"\n[bold]Found {len(notes)} note(s) matching '{query}':[/bold]\n")

        for note in notes:
            console.print(f"[cyan]#{note.id}[/cyan] [bold]{note.title}[/bold]")
            if note.project:
                console.print(f"  Project: {note.project.name}")
            if note.task_id:
                console.print(f"  Task: #{note.task_id}")

            # Show snippet
            snippet = note.content[:150]
            if len(note.content) > 150:
                snippet += "..."
            console.print(f"  {snippet}\n")
    finally:
        session.close()


@note.command("show")
@click.argument("note_id", type=int)
def note_show(note_id):
    """Show full note content."""
    session, engine = get_db_session()
    try:
        note = NoteOps.get_by_id(session, note_id)
        if not note:
            console.print(f"[red]Error: Note #{note_id} not found[/red]")
            return

        console.print(f"\n[bold cyan]Note #{note.id}[/bold cyan]")
        console.print(f"[bold]{note.title}[/bold]\n")

        if note.project:
            console.print(f"Project: {note.project.name}")
        if note.task_id:
            console.print(f"Task: #{note.task_id}")
        if note.tags:
            console.print(f"Tags: {note.tags}")

        console.print(f"\n{'-' * 60}")
        md = Markdown(note.content)
        console.print(md)
        console.print(f"{'-' * 60}\n")

        console.print(f"File: {note.markdown_path}")
    finally:
        session.close()


# Report commands
@cli.group()
def report():
    """Generate reports."""
    pass


@report.command("work")
@click.option("--days", type=int, default=7, help="Number of days to include")
@click.option("--project", "-p", help="Filter by project slug")
def report_work(days, project):
    """Generate work report."""
    session, engine = get_db_session()
    try:
        from datetime import timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Get work logs
        work_logs = WorkLogOps.list_by_date_range(session, start_date, end_date)

        # Get completed tasks
        all_tasks = TaskOps.list_all(session, status="done")
        completed_tasks = [
            t for t in all_tasks if t.completed_at and start_date <= t.completed_at <= end_date
        ]

        console.print(f"\n[bold]Work Report[/bold]")
        console.print(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n")

        console.print(f"Work days logged: {len(work_logs)}")
        console.print(f"Tasks completed: {len(completed_tasks)}\n")

        if completed_tasks:
            console.print("[bold]Completed Tasks:[/bold]")
            for task in completed_tasks:
                project_str = f" [{task.project.name}]" if task.project else ""
                console.print(f"  ✅ {task.title}{project_str}")
    finally:
        session.close()


# Jira commands
@cli.group()
def jira():
    """Jira integration commands."""
    pass


@jira.command("sync")
@click.option("--project", "-p", help="Project slug to sync")
def jira_sync(project):
    """Sync Jira issues to local tasks."""
    session, engine = get_db_session()
    try:
        from .integrations.jira_client import JiraClient

        try:
            client = JiraClient()
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            return

        if not client.test_connection():
            console.print("[red]Error: Failed to connect to Jira[/red]")
            return

        # Get projects to sync
        if project:
            proj = ProjectOps.get_by_slug(session, project)
            if not proj:
                console.print(f"[red]Error: Project '{project}' not found[/red]")
                return
            if not proj.jira_project_key:
                console.print(f"[red]Error: Project has no Jira key configured[/red]")
                return
            projects = [proj]
        else:
            all_projects = ProjectOps.list_all(session)
            projects = [p for p in all_projects if p.jira_project_key]

        if not projects:
            console.print("[yellow]No projects with Jira integration found[/yellow]")
            return

        total_synced = 0
        for proj in projects:
            console.print(f"\nSyncing {proj.name} ({proj.jira_project_key})...")
            issues = client.get_project_issues(proj.jira_project_key)

            for issue in issues:
                existing = TaskOps.get_by_jira_key(session, issue["key"])
                if existing:
                    TaskOps.update(
                        session,
                        existing,
                        title=issue["summary"],
                        description=issue["description"],
                    )
                else:
                    TaskOps.create(
                        session,
                        title=issue["summary"],
                        description=issue["description"],
                        project_id=proj.id,
                        jira_ticket_id=issue["id"],
                        jira_ticket_key=issue["key"],
                    )
                total_synced += 1

            console.print(f"  Synced {len(issues)} issues")

        console.print(f"\n[green]✓[/green] Total issues synced: {total_synced}")
    finally:
        session.close()


# Epic and Issue commands (using Beads integration)
@cli.group()
def epic():
    """Epic management commands (using Beads)."""
    pass


@epic.command("create")
@click.argument("title")
@click.option("--description", "-d", default="", help="Epic description")
@click.option("--priority", "-p", type=int, default=2, help="Priority 0-4 (0=lowest, 4=highest)")
@click.option("--labels", "-l", help="Comma-separated labels")
def epic_create(title, description, priority, labels):
    """Create a new epic."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _create():
        try:
            label_list = labels.split(",") if labels else None
            issue = await client.create_epic(
                title=title,
                description=description,
                priority=priority,
                labels=label_list,
            )

            priority_str = ["Lowest", "Low", "Medium", "High", "Highest"][priority]
            console.print(f"[green]✓[/green] Epic created!")
            console.print(f"ID: {issue.id}")
            console.print(f"Title: {issue.title}")
            console.print(f"Priority: {priority_str} ({priority})")
            if label_list:
                console.print(f"Labels: {', '.join(label_list)}")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_create())


@epic.command("list")
@click.option("--status", "-s", help="Filter by status (open, in_progress, blocked, closed)")
@click.option("--limit", "-l", type=int, default=50, help="Max number to return")
def epic_list(status, limit):
    """List all epics."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _list():
        try:
            epics = await client.list_epics(status=status, limit=limit)

            if not epics:
                filter_str = f" with status={status}" if status else ""
                console.print(f"[yellow]No epics found{filter_str}[/yellow]")
                return

            console.print(f"\n[bold]Found {len(epics)} epic(s):[/bold]\n")

            table = Table(show_header=True)
            table.add_column("ID")
            table.add_column("Title")
            table.add_column("Status")
            table.add_column("Priority")

            for epic in epics:
                priority_str = (
                    ["Lowest", "Low", "Medium", "High", "Highest"][epic.priority]
                    if epic.priority is not None
                    else "Not set"
                )

                status_emoji = {
                    "open": "📋",
                    "in_progress": "🚀",
                    "closed": "🎉",
                    "blocked": "🚫",
                }.get(epic.status, "📋")

                table.add_row(
                    epic.id,
                    epic.title,
                    f"{status_emoji} {epic.status}",
                    priority_str,
                )

            console.print(table)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_list())


@cli.group()
def issue():
    """Issue management commands (using Beads)."""
    pass


@issue.command("create")
@click.argument("title")
@click.option("--description", "-d", default="", help="Issue description")
@click.option("--type", "-t", "issue_type", default="task", help="Type: bug, feature, task, epic, chore")
@click.option("--priority", "-p", type=int, default=2, help="Priority 0-4 (0=lowest, 4=highest)")
@click.option("--epic", "-e", help="Parent epic ID")
@click.option("--blocks", "-b", help="Comma-separated issue IDs this blocks")
@click.option("--labels", "-l", help="Comma-separated labels")
@click.option("--external-ref", "-r", help="External reference (e.g., Jira ticket)")
@click.option("--with-task", is_flag=True, help="Create a linked Second Brain task")
@click.option("--project", help="Project slug for linked task (used with --with-task)")
def issue_create(title, description, issue_type, priority, epic, blocks, labels, external_ref, with_task, project):
    """Create a new issue."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _create():
        try:
            label_list = labels.split(",") if labels else None
            blocks_list = blocks.split(",") if blocks else None

            issue = await client.create_issue(
                title=title,
                description=description,
                issue_type=issue_type,
                priority=priority,
                parent_epic_id=epic,
                blocks=blocks_list,
                labels=label_list,
                external_ref=external_ref,
            )

            priority_str = ["Lowest", "Low", "Medium", "High", "Highest"][priority]
            console.print(f"[green]✓[/green] Issue created!")
            console.print(f"ID: {issue.id}")
            console.print(f"Title: {issue.title}")
            console.print(f"Type: {issue_type}")
            console.print(f"Priority: {priority_str} ({priority})")
            if epic:
                console.print(f"Parent Epic: {epic}")
            if blocks_list:
                console.print(f"Blocks: {', '.join(blocks_list)}")
            if label_list:
                console.print(f"Labels: {', '.join(label_list)}")
            if external_ref:
                console.print(f"External Ref: {external_ref}")

            # Create linked task if requested
            if with_task:
                session, engine = get_db_session()
                try:
                    project_id = None
                    proj = None
                    if project:
                        proj = ProjectOps.get_by_slug(session, project)
                        if not proj:
                            console.print(
                                f"[yellow]Warning: Project '{project}' not found. Creating task without project link.[/yellow]"
                            )
                        else:
                            project_id = proj.id

                    # Map Beads priority to task priority
                    priority_map = {0: "low", 1: "low", 2: "medium", 3: "high", 4: "urgent"}
                    task_priority = priority_map.get(priority, "medium")

                    task = TaskOps.create(
                        session,
                        title,
                        description,
                        "todo",
                        task_priority,
                        project_id,
                        issue_id=issue.id,
                    )

                    console.print(f"[green]✓[/green] Linked Second Brain task created: #{task.id}")
                    if proj:
                        console.print(f"  Project: {proj.name}")
                finally:
                    session.close()
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_create())


@issue.command("create-with-project")
@click.argument("title")
@click.option("--description", "-d", default="", help="Description for both epic and project")
@click.option("--priority", "-p", type=int, default=2, help="Epic priority 0-4 (0=lowest, 4=highest)")
@click.option("--labels", "-l", help="Comma-separated labels/tags for both")
@click.option("--jira-project", "-j", help="Jira project key for the project")
def issue_create_with_project(title, description, priority, labels, jira_project):
    """Create an epic and linked Second Brain project together.

    This is the recommended way to start a new initiative. Creates:
    - A Beads epic for dependency tracking
    - A Second Brain project for notes and time tracking
    - Links them together with the same title and tags

    Examples:
        sb issue create-with-project "New Feature X" -d "Build feature X" -p 3 -l feature,backend
        sb issue create-with-project "API Redesign" --labels api,refactor
    """
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _create():
        try:
            label_list = labels.split(",") if labels else None

            # Create epic
            epic = await client.create_epic(
                title=title,
                description=description,
                priority=priority,
                labels=label_list or [],
            )

            priority_str = ["Lowest", "Low", "Medium", "High", "Highest"][priority]

            console.print("[green]✓ Epic + Project created successfully![/green]")
            console.print()
            console.print("[bold]📋 Epic (Beads):[/bold]")
            console.print(f"  ID: {epic.id}")
            console.print(f"  Title: {epic.title}")
            console.print(f"  Priority: {priority_str} ({priority})")
            console.print(f"  Status: {epic.status}")
            if label_list:
                console.print(f"  Labels: {', '.join(label_list)}")

            # Create project
            session, engine = get_db_session()
            try:
                from .storage import StorageIndexer

                indexer = StorageIndexer(session)
                project = indexer.create_project(
                    name=title,
                    description=description,
                    jira_project_key=jira_project,
                    tags=label_list,
                )

                console.print()
                console.print("[bold]📦 Project (Second Brain):[/bold]")
                console.print(f"  ID: {project.id}")
                console.print(f"  Name: {project.name}")
                console.print(f"  Slug: {project.slug}")
                console.print(f"  Markdown: {project.markdown_path}")
                if jira_project:
                    console.print(f"  Jira: {jira_project}")
                if label_list:
                    console.print(f"  Tags: {', '.join(label_list)}")

                console.print()
                console.print("[bold]🔗 Integration:[/bold]")
                console.print(f"  Epic ID: {epic.id} ↔️ Project Slug: {project.slug}")

                console.print()
                console.print("[bold cyan]💡 Next Steps:[/bold cyan]")
                console.print(f"  1. Create issues under epic: [dim]sb issue create \"Issue Title\" --epic {epic.id}[/dim]")
                console.print(f"  2. Create tasks in project: [dim]sb task add \"Task Title\" --project {project.slug}[/dim]")
                console.print(f"  3. Link issues to tasks: [dim]sb issue create \"Issue\" --with-task --project {project.slug}[/dim]")
                console.print(f"  4. Add notes: [dim]sb note create \"Notes\" --project {project.slug}[/dim]")
                console.print(f"  5. Track work: [dim]sb log add \"Work done\" --project {project.slug}[/dim]")
            finally:
                session.close()

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_create())


@issue.command("update")
@click.argument("issue_id")
@click.option("--title", "-t", help="New title")
@click.option("--description", "-d", help="New description")
@click.option("--status", "-s", help="New status: open, in_progress, blocked, closed")
@click.option("--priority", "-p", type=int, help="New priority 0-4")
def issue_update(issue_id, title, description, status, priority):
    """Update an existing issue."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _update():
        try:
            issue = await client.update_issue(
                issue_id=issue_id,
                title=title,
                description=description,
                status=status,
                priority=priority,
            )

            console.print(f"[green]✓[/green] Issue {issue.id} updated!")
            console.print(f"Title: {issue.title}")
            console.print(f"Status: {issue.status}")
            if issue.priority is not None:
                priority_str = ["Lowest", "Low", "Medium", "High", "Highest"][issue.priority]
                console.print(f"Priority: {priority_str} ({issue.priority})")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_update())


@issue.command("close")
@click.argument("issue_id")
@click.option("--reason", "-r", default="Completed", help="Reason for closing")
def issue_close(issue_id, reason):
    """Close an issue."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _close():
        try:
            issue = await client.close_issue(issue_id=issue_id, reason=reason)
            console.print(f"[green]✓[/green] Issue {issue.id} closed!")
            console.print(f"Title: {issue.title}")
            console.print(f"Reason: {reason}")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_close())


@issue.command("show")
@click.argument("issue_id")
def issue_show(issue_id):
    """Show detailed issue information."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _show():
        try:
            issue = await client.get_issue(issue_id=issue_id)

            priority_str = (
                ["Lowest", "Low", "Medium", "High", "Highest"][issue.priority]
                if issue.priority is not None
                else "Not set"
            )

            console.print(f"\n[bold]{issue.title}[/bold] ({issue.id})\n")
            console.print(f"Type: {issue.issue_type}")
            console.print(f"Status: {issue.status}")
            console.print(f"Priority: {priority_str}")

            if issue.description:
                console.print(f"\n[bold]Description:[/bold]")
                console.print(issue.description)

            if hasattr(issue, "labels") and issue.labels:
                console.print(f"\n[bold]Labels:[/bold] {', '.join(issue.labels)}")

            if hasattr(issue, "external_ref") and issue.external_ref:
                console.print(f"[bold]External Ref:[/bold] {issue.external_ref}")

            # Dependencies
            if hasattr(issue, "dependencies") and issue.dependencies:
                console.print(f"\n[bold]Dependencies ({len(issue.dependencies)}):[/bold]")
                for dep in issue.dependencies:
                    console.print(f"  - {dep.id}: {dep.title} [{dep.dep_type}]")

            # Dependents
            if hasattr(issue, "dependents") and issue.dependents:
                console.print(f"\n[bold]Dependents ({len(issue.dependents)}):[/bold]")
                for dep in issue.dependents:
                    console.print(f"  - {dep.id}: {dep.title}")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_show())


@issue.command("list")
@click.option("--status", "-s", help="Filter by status (open, in_progress, blocked, closed)")
@click.option("--type", "-t", "issue_type", help="Filter by type (bug, feature, task, epic, chore)")
@click.option("--priority", "-p", type=int, help="Filter by priority 0-4")
@click.option("--limit", "-l", type=int, default=50, help="Max number to return")
def issue_list(status, issue_type, priority, limit):
    """List issues with optional filters."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _list():
        try:
            issues = await client.list_issues(
                status=status,
                issue_type=issue_type,
                priority=priority,
                limit=limit,
            )

            if not issues:
                console.print("[yellow]No issues found[/yellow]")
                return

            console.print(f"\n[bold]Found {len(issues)} issue(s):[/bold]\n")

            table = Table(show_header=True)
            table.add_column("ID")
            table.add_column("Title")
            table.add_column("Type")
            table.add_column("Status")
            table.add_column("Priority")

            for issue in issues:
                priority_str = (
                    ["Lowest", "Low", "Medium", "High", "Highest"][issue.priority]
                    if issue.priority is not None
                    else "Not set"
                )

                status_emoji = {
                    "open": "⬜",
                    "in_progress": "🔄",
                    "closed": "✅",
                    "blocked": "🚫",
                }.get(issue.status, "⬜")

                table.add_row(
                    issue.id,
                    issue.title[:50] + "..." if len(issue.title) > 50 else issue.title,
                    issue.issue_type,
                    f"{status_emoji} {issue.status}",
                    priority_str,
                )

            console.print(table)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_list())


@issue.command("add-dependency")
@click.argument("issue_id")
@click.argument("depends_on_id")
@click.option("--type", "-t", "dep_type", default="blocks", help="Type: blocks, related, parent-child, discovered-from")
def issue_add_dependency(issue_id, depends_on_id, dep_type):
    """Add a dependency between two issues."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _add_dep():
        try:
            await client.add_dependency(
                issue_id=issue_id,
                depends_on_id=depends_on_id,
                dep_type=dep_type,
            )

            dep_type_desc = {
                "blocks": f"{depends_on_id} blocks {issue_id}",
                "related": f"{issue_id} is related to {depends_on_id}",
                "parent-child": f"{depends_on_id} is parent of {issue_id}",
                "discovered-from": f"{issue_id} discovered while working on {depends_on_id}",
            }.get(dep_type, "Unknown relationship")

            console.print(f"[green]✓[/green] Dependency added!")
            console.print(f"Type: {dep_type}")
            console.print(f"Relationship: {dep_type_desc}")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_add_dep())


@issue.command("ready")
@click.option("--limit", "-l", type=int, default=10, help="Max number of issues to return")
@click.option("--priority", "-p", type=int, help="Filter by priority")
def issue_ready(limit, priority):
    """Find issues ready to work on (no blockers)."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _ready():
        try:
            issues = await client.get_ready_work(limit=limit, priority=priority)

            if not issues:
                console.print("[yellow]No ready work found. All work is either blocked or completed![/yellow]")
                return

            console.print(f"\n[bold]🎯 Found {len(issues)} issue(s) ready to work on:[/bold]\n")

            table = Table(show_header=True)
            table.add_column("ID")
            table.add_column("Title")
            table.add_column("Type")
            table.add_column("Priority")

            for issue in issues:
                priority_str = (
                    ["Lowest", "Low", "Medium", "High", "Highest"][issue.priority]
                    if issue.priority is not None
                    else "Not set"
                )

                table.add_row(
                    issue.id,
                    issue.title[:50] + "..." if len(issue.title) > 50 else issue.title,
                    issue.issue_type,
                    priority_str,
                )

            console.print(table)
            console.print("\n💡 These issues have no open blockers and can be started immediately!")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_ready())


@issue.command("stats")
def issue_stats():
    """Show project statistics."""
    from .integrations.beads_integration import get_beads_client
    import asyncio

    config = get_app_config()
    client = get_beads_client(str(config.data_dir))

    if not client:
        console.print("[red]Error: Beads integration not available. Install with: uv pip install beads-mcp[/red]")
        return

    async def _stats():
        try:
            stats = await client.get_stats()

            console.print("\n[bold]📊 Project Statistics[/bold]\n")
            console.print(f"Total Issues: {stats.total_issues}")
            console.print(f"Open: {stats.open_issues}")
            console.print(f"Closed: {stats.closed_issues}")
            console.print(f"Blocked: {stats.blocked_issues}")
            console.print(f"Ready to Work: {stats.ready_issues}\n")

            if stats.ready_issues > 0:
                console.print(f"[green]💡 You have {stats.ready_issues} issue(s) ready to work on![/green]")
            elif stats.blocked_issues > 0:
                console.print(f"[yellow]⚠️  {stats.blocked_issues} issue(s) are blocked. Consider addressing blockers.[/yellow]")
            elif stats.open_issues == 0:
                console.print("[green]🎉 All issues are closed! Great work![/green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_stats())


# ============================================================================
# Key Management Commands
# ============================================================================


@cli.group()
def key():
    """Manage encryption keys."""
    pass


@key.command("generate")
@click.option("--bits", type=int, default=4096, help="Key size in bits")
@click.option("--passphrase", is_flag=True, help="Protect with passphrase")
@click.option("--force", is_flag=True, help="Overwrite existing keys")
def key_generate(bits, passphrase, force):
    """Generate a new RSA key pair for encryption."""
    from .crypto import KeyManager
    from .crypto.validators import ensure_keys_in_gitignore
    import getpass

    config = get_app_config()
    keys_dir = config.second_brain_dir / "keys"
    km = KeyManager(keys_dir)

    # Check if keys already exist
    if km.keys_exist() and not force:
        console.print("[yellow]⚠️  Warning: Keys already exist![/yellow]")
        console.print(f"Location: {keys_dir}")
        console.print("\n[red]Overwriting will make all encrypted data unrecoverable![/red]")
        console.print("\nTo proceed anyway:")
        console.print("  [cyan]sb key generate --force[/cyan]")
        console.print("\nTo backup first:")
        console.print(f"  [cyan]cp {keys_dir}/private_key.pem /secure/backup/[/cyan]")
        return

    # Get passphrase if requested
    passphrase_str = None
    if passphrase:
        try:
            passphrase_str = getpass.getpass("Enter passphrase: ")
            confirm = getpass.getpass("Confirm passphrase: ")
            if passphrase_str != confirm:
                console.print("[red]✗ Error: Passphrases don't match[/red]")
                console.print("Please try again.")
                return
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Cancelled.[/yellow]")
            return

    try:
        # Generate keys
        console.print(f"[cyan]Generating {bits}-bit RSA key pair...[/cyan]")
        private_key, public_key = km.generate_key_pair(bits, passphrase_str)

        # Save keys
        km.save_keys(private_key, public_key, passphrase_str)

        # Update .gitignore
        modified = ensure_keys_in_gitignore(config.second_brain_dir)
        if modified:
            console.print("[green]✓[/green] Updated .gitignore to protect private keys")

        # Get fingerprint
        fingerprint = km.get_fingerprint(public_key)

        # Show success
        console.print("[green]✓ Keys generated successfully![/green]")
        if passphrase:
            console.print("[green]✓ Private key encrypted with passphrase[/green]")
        console.print(f"\nPrivate key: {keys_dir}/private_key.pem (permissions: 600)")
        console.print(f"Public key:  {keys_dir}/public_key.pem (permissions: 644)")
        console.print(f"Fingerprint: {fingerprint}")

        console.print("\n[yellow]⚠️  IMPORTANT: Backup your private key securely![/yellow]")
        console.print("Without it, you cannot decrypt your data.")
        console.print(f"\nLocation: {keys_dir}/private_key.pem")
        console.print("Backup to: password manager, encrypted drive, or secure cloud storage")

    except Exception as e:
        console.print(f"[red]✗ Error generating keys: {e}[/red]")
        raise


@key.command("info")
def key_info():
    """Show encryption key information."""
    from .crypto import KeyManager
    import os

    config = get_app_config()
    keys_dir = config.second_brain_dir / "keys"
    km = KeyManager(keys_dir)

    # Check if keys exist
    if not km.keys_exist():
        console.print("[yellow]No encryption keys found.[/yellow]")
        console.print("\nGenerate keys with:")
        console.print("  [cyan]sb key generate[/cyan]")
        console.print("\nThis will create a 4096-bit RSA key pair for encrypting")
        console.print("sensitive information in your Second Brain.")
        return

    try:
        # Load metadata
        metadata = km.load_metadata()

        console.print("[cyan]Encryption Keys[/cyan]\n")

        if metadata:
            console.print(f"Algorithm:   {metadata.get('algorithm', 'Unknown')}")
            console.print(f"Fingerprint: {metadata.get('public_key_fingerprint', 'Unknown')}")

            # Format created date in user's timezone
            created_at = metadata.get('created_at', 'Unknown')
            if created_at != 'Unknown':
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(created_at)
                    from .utils import datetime_utils
                    local_dt = datetime_utils.to_local(dt)
                    created_at = local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')
                except Exception:
                    # Keep original if conversion fails
                    pass

            console.print(f"Created:     {created_at}")
            console.print(f"Passphrase:  {'Yes' if metadata.get('has_passphrase') else 'No'}")
        else:
            console.print("[yellow]Metadata not found (keys exist but no .key_metadata.json)[/yellow]")

        console.print(f"Location:    {keys_dir}\n")

        # Check key files
        private_exists = km.private_key_path.exists()
        public_exists = km.public_key_path.exists()

        if private_exists:
            private_stat = os.stat(km.private_key_path)
            private_perms = oct(private_stat.st_mode)[-3:]
            console.print(f"Private key: [green]✓[/green] Found (permissions: {private_perms})")
        else:
            console.print(f"Private key: [red]✗[/red] Not found")

        if public_exists:
            public_stat = os.stat(km.public_key_path)
            public_perms = oct(public_stat.st_mode)[-3:]
            console.print(f"Public key:  [green]✓[/green] Found (permissions: {public_perms})")
        else:
            console.print(f"Public key:  [red]✗[/red] Not found")

    except Exception as e:
        console.print(f"[red]✗ Error reading key information: {e}[/red]")


@cli.command("encrypt")
@click.argument("text")
@click.option("--output", type=click.Path(), help="Save to file instead of stdout")
@click.option("--block", is_flag=True, help="Output as markdown encrypted block")
def encrypt_text(text, output, block):
    """Encrypt text."""
    from .crypto import KeyManager, Encryptor, EncryptionError
    import getpass

    config = get_app_config()
    keys_dir = config.second_brain_dir / "keys"
    km = KeyManager(keys_dir)

    # Check if keys exist
    if not km.keys_exist():
        console.print("[red]✗ Error: No encryption keys found[/red]")
        console.print("\nGenerate keys with:")
        console.print("  [cyan]sb key generate[/cyan]")
        return

    try:
        encryptor = Encryptor(km)

        # Encrypt
        if block:
            encrypted = encryptor.create_encrypted_block(text)
        else:
            encrypted = encryptor.encrypt(text)

        # Output
        if output:
            from pathlib import Path
            Path(output).write_text(encrypted)
            console.print(f"[green]✓ Encrypted successfully![/green]")
            console.print(f"\nSaved to: {output}")
        else:
            console.print("[green]✓ Encrypted successfully![/green]\n")
            console.print(encrypted)
            console.print("\n[dim]Copy this to your note or run:[/dim]")
            console.print(f'  [cyan]sb decrypt "{encrypted[:50]}..."[/cyan]')

    except EncryptionError as e:
        console.print(f"[red]✗ Encryption failed: {e}[/red]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise


@cli.command("decrypt")
@click.argument("text", required=False)
@click.option("--file", type=click.Path(exists=True), help="Read encrypted text from file")
@click.option("--passphrase", is_flag=True, help="Prompt for key passphrase")
def decrypt_text(text, file, passphrase):
    """Decrypt encrypted text."""
    from .crypto import KeyManager, Encryptor, EncryptionError
    import getpass

    config = get_app_config()
    keys_dir = config.second_brain_dir / "keys"
    km = KeyManager(keys_dir)

    # Check if keys exist
    if not km.keys_exist():
        console.print("[red]✗ Error: No encryption keys found[/red]")
        console.print("\nGenerate keys with:")
        console.print("  [cyan]sb key generate[/cyan]")
        return

    # Get encrypted data
    if file:
        from pathlib import Path
        encrypted_data = Path(file).read_text()
    elif text:
        encrypted_data = text
    else:
        console.print("[red]✗ Error: Provide TEXT or --file[/red]")
        console.print("\nUsage:")
        console.print('  [cyan]sb decrypt "v1:RSA-AES256-GCM:..."[/cyan]')
        console.print("  [cyan]sb decrypt --file secret.txt[/cyan]")
        return

    # Get passphrase if requested
    passphrase_str = None
    if passphrase:
        try:
            passphrase_str = getpass.getpass("Enter passphrase: ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Cancelled.[/yellow]")
            return

    try:
        encryptor = Encryptor(km)

        # Check if it's a markdown with encrypted blocks
        if "<!-- ENCRYPTED:" in encrypted_data:
            plaintext = encryptor.decrypt_markdown(encrypted_data, passphrase_str)
        else:
            plaintext = encryptor.decrypt(encrypted_data.strip(), passphrase_str)

        console.print("[green]✓ Decrypted successfully![/green]\n")
        console.print(plaintext)

    except EncryptionError as e:
        console.print(f"[red]✗ Decryption failed: {e}[/red]")
        if "passphrase" in str(e).lower():
            console.print("\n[yellow]Hint: Try with --passphrase flag if your key is protected[/yellow]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise


def main():
    """Main CLI entry point."""
    cli()


if __name__ == "__main__":
    main()
