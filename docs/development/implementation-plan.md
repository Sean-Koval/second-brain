# Implementation Plan: Global Second Brain

Plan for implementing the global, git-integrated second brain architecture.

## Phase 1: Core Global Setup (MVP)

### 1.1 Update Default Paths

**File:** `src/second_brain/config.py` (new file)

```python
"""Configuration management for Second Brain."""

import os
from pathlib import Path

class Config:
    """Global configuration."""

    @staticmethod
    def get_second_brain_dir() -> Path:
        """Get the second brain home directory."""
        # Priority order:
        # 1. SECOND_BRAIN_DIR environment variable
        # 2. Default: ~/.second-brain/
        env_dir = os.getenv("SECOND_BRAIN_DIR")
        if env_dir:
            return Path(env_dir).expanduser()

        return Path.home() / ".second-brain"

    @staticmethod
    def get_data_dir() -> Path:
        """Get the data directory."""
        # SECOND_BRAIN_DATA_DIR can override, otherwise use {home}/data
        env_data_dir = os.getenv("SECOND_BRAIN_DATA_DIR")
        if env_data_dir:
            return Path(env_data_dir).expanduser()

        return Config.get_second_brain_dir() / "data"

    @staticmethod
    def get_config_file() -> Path:
        """Get the config file path."""
        return Config.get_second_brain_dir() / "config.json"
```

**Changes needed:**
- Update `cli.py` to use `Config.get_data_dir()`
- Update `mcp_server.py` to use `Config.get_data_dir()`
- Update all storage paths to be relative to data dir

---

### 1.2 Enhanced `sb init` Command

**File:** `src/second_brain/cli.py`

Add `--global` flag:

```python
@cli.command()
@click.option("--data-dir", default=None, help="Data directory path")
@click.option("--global", "is_global", is_flag=True,
              help="Initialize global second brain in ~/.second-brain/")
@click.option("--git", is_flag=True, help="Initialize as git repository")
def init(data_dir, is_global, git):
    """Initialize second brain workspace."""

    if is_global:
        # Create in ~/.second-brain/
        sb_dir = Path.home() / ".second-brain"
        data_path = sb_dir / "data"
    elif data_dir:
        # Custom location
        sb_dir = Path(data_dir).parent
        data_path = Path(data_dir)
    else:
        # Local (old behavior)
        sb_dir = Path.cwd()
        data_path = Path("data")

    # Create directories
    (data_path / "projects").mkdir(parents=True, exist_ok=True)
    (data_path / "work_logs").mkdir(parents=True, exist_ok=True)
    (data_path / "transcripts" / "raw").mkdir(parents=True, exist_ok=True)
    (data_path / "transcripts" / "processed").mkdir(parents=True, exist_ok=True)

    # Initialize database
    db_path = data_path / "index.db"
    init_db(str(db_path))

    # Create config file
    if is_global:
        config_file = sb_dir / "config.json"
        create_default_config(config_file)

    # Initialize git if requested
    if git:
        init_git_repo(sb_dir)

    # Print success message
    console.print(f"[green]✓[/green] Second brain initialized in {sb_dir}/")

    if is_global:
        console.print("\nAdd to your shell profile:")
        console.print(f'  export SECOND_BRAIN_DIR="{sb_dir}"')
        console.print("\nThen restart your shell or run:")
        console.print(f"  source ~/.bashrc  # or ~/.zshrc")
```

---

### 1.3 Git Integration Commands

**File:** `src/second_brain/cli.py`

Add sync command group:

```python
@cli.group()
def sync():
    """Git synchronization commands."""
    pass

@sync.command()
@click.option("--message", "-m", help="Commit message")
def push(message):
    """Commit and push changes to remote."""
    sb_dir = Config.get_second_brain_dir()

    if not (sb_dir / ".git").exists():
        console.print("[red]Error: Not a git repository[/red]")
        console.print("Run: sb init --global --git")
        return

    # Git add, commit, push
    os.chdir(sb_dir)

    # Check if there are changes
    result = subprocess.run(["git", "status", "--porcelain"],
                          capture_output=True, text=True)

    if not result.stdout.strip():
        console.print("[yellow]No changes to push[/yellow]")
        return

    # Add all changes
    subprocess.run(["git", "add", "."])

    # Commit
    if not message:
        message = f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    subprocess.run(["git", "commit", "-m", message])

    # Push
    result = subprocess.run(["git", "push"], capture_output=True, text=True)

    if result.returncode == 0:
        console.print("[green]✓[/green] Changes pushed successfully")
    else:
        console.print(f"[red]Error pushing:[/red] {result.stderr}")

@sync.command()
def pull():
    """Pull latest changes from remote."""
    sb_dir = Config.get_second_brain_dir()

    if not (sb_dir / ".git").exists():
        console.print("[red]Error: Not a git repository[/red]")
        return

    os.chdir(sb_dir)

    result = subprocess.run(["git", "pull"], capture_output=True, text=True)

    if result.returncode == 0:
        console.print("[green]✓[/green] Pulled latest changes")
        console.print(result.stdout)
    else:
        console.print(f"[red]Error pulling:[/red] {result.stderr}")

@sync.command()
def status():
    """Show git status."""
    sb_dir = Config.get_second_brain_dir()

    if not (sb_dir / ".git").exists():
        console.print("[red]Error: Not a git repository[/red]")
        return

    os.chdir(sb_dir)

    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    console.print(result.stdout)
```

---

### 1.4 Config File Management

**File:** `src/second_brain/config_manager.py` (new)

```python
"""Configuration file management."""

import json
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG = {
    "user": {
        "name": "",
        "email": ""
    },
    "sync": {
        "auto_push": False,
        "auto_pull": True,
        "remote": "origin"
    },
    "defaults": {
        "work_log_time_tracking": True,
        "auto_link_tasks": True
    },
    "paths": {
        "data_dir": "data",
        "projects_dir": "data/projects",
        "work_logs_dir": "data/work_logs",
        "transcripts_dir": "data/transcripts"
    }
}

def create_default_config(config_path: Path) -> None:
    """Create default config file."""
    with open(config_path, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)

def load_config(config_path: Path) -> Dict[str, Any]:
    """Load config file."""
    if not config_path.exists():
        return DEFAULT_CONFIG

    with open(config_path, "r") as f:
        return json.load(f)

def save_config(config_path: Path, config: Dict[str, Any]) -> None:
    """Save config file."""
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
```

---

### 1.5 Migration Helper

**File:** `src/second_brain/cli.py`

Add migrate command:

```python
@cli.command()
@click.argument("source_dir")
@click.option("--to-global", is_flag=True, help="Migrate to global second brain")
def migrate(source_dir, to_global):
    """Migrate data from local to global setup."""

    source = Path(source_dir)

    if not source.exists():
        console.print(f"[red]Error: {source} does not exist[/red]")
        return

    if to_global:
        # Initialize global if doesn't exist
        sb_dir = Path.home() / ".second-brain"
        if not sb_dir.exists():
            console.print("Initializing global second brain...")
            # Run init --global
            ctx = click.get_current_context()
            ctx.invoke(init, is_global=True, git=True)

        dest = sb_dir / "data"
    else:
        console.print("[red]Error: --to-global is required[/red]")
        return

    # Copy data
    console.print(f"Migrating data from {source} to {dest}...")

    import shutil

    # Copy projects
    if (source / "projects").exists():
        shutil.copytree(source / "projects", dest / "projects", dirs_exist_ok=True)
        console.print("  ✓ Projects migrated")

    # Copy work logs
    if (source / "work_logs").exists():
        shutil.copytree(source / "work_logs", dest / "work_logs", dirs_exist_ok=True)
        console.print("  ✓ Work logs migrated")

    # Copy transcripts
    if (source / "transcripts").exists():
        shutil.copytree(source / "transcripts", dest / "transcripts", dirs_exist_ok=True)
        console.print("  ✓ Transcripts migrated")

    # Copy database
    if (source / "index.db").exists():
        shutil.copy(source / "index.db", dest / "index.db")
        console.print("  ✓ Database migrated")

    console.print(f"\n[green]✓[/green] Migration complete!")
    console.print("\nAdd to your shell profile:")
    console.print(f'  export SECOND_BRAIN_DIR="{sb_dir}"')
```

---

## Phase 2: Enhanced Git Features

### 2.1 Setup Helper

**Command:** `sb setup github`

```python
@cli.command()
@click.argument("repo_name")
@click.option("--private/--public", default=True)
def setup_github(repo_name, private):
    """Set up GitHub remote repository."""

    sb_dir = Config.get_second_brain_dir()

    if not (sb_dir / ".git").exists():
        console.print("[red]Error: Not a git repository[/red]")
        console.print("Run: sb init --global --git")
        return

    os.chdir(sb_dir)

    # Create GitHub repo using gh CLI
    visibility = "--private" if private else "--public"

    result = subprocess.run([
        "gh", "repo", "create", repo_name, visibility
    ], capture_output=True, text=True)

    if result.returncode != 0:
        console.print(f"[red]Error:[/red] {result.stderr}")
        return

    # Add remote
    subprocess.run([
        "git", "remote", "add", "origin",
        f"git@github.com:{repo_name}.git"
    ])

    # Initial push
    subprocess.run(["git", "push", "-u", "origin", "main"])

    console.print(f"[green]✓[/green] GitHub repo created and connected!")
    console.print(f"Repository: https://github.com/{repo_name}")
```

### 2.2 Smart Sync

**Auto-commit on changes (optional):**

```python
@sync.command()
@click.option("--interval", default=300, help="Sync interval in seconds")
def auto(interval):
    """Auto-sync changes at regular intervals."""

    console.print(f"Auto-sync enabled (every {interval}s)")
    console.print("Press Ctrl+C to stop")

    import time

    try:
        while True:
            time.sleep(interval)

            # Check for changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=Config.get_second_brain_dir()
            )

            if result.stdout.strip():
                console.print(f"[{datetime.now().strftime('%H:%M:%S')}] Syncing changes...")
                # Auto commit and push
                ctx = click.get_current_context()
                ctx.invoke(push, message=f"Auto-sync: {datetime.now().isoformat()}")

    except KeyboardInterrupt:
        console.print("\n[yellow]Auto-sync stopped[/yellow]")
```

---

## Phase 3: Documentation Updates

### 3.1 Update README.md

Add global setup as primary method:

```markdown
## Installation

### Quick Start (Global Setup - Recommended)

```bash
# 1. Install
pip install second-brain

# 2. Initialize global second brain
sb init --global --git

# 3. Configure environment
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc

# 4. Set up GitHub sync (optional)
sb setup github yourusername-second-brain

# 5. Start using!
sb project create "My First Project"
```

### 3.2 Update INSTALLATION.md

Add global setup section at the top:

```markdown
## Recommended: Global Setup

Second Brain works best as a global tool...

[Detailed instructions]
```

### 3.3 Update QUICKSTART.md

Start with global setup:

```markdown
## 1. Install and Initialize (Global)

```bash
pip install second-brain
sb init --global --git
export SECOND_BRAIN_DIR="$HOME/.second-brain"
```
```

---

## Phase 4: MCP Server Updates

### 4.1 Auto-detect Global Setup

**File:** `src/second_brain/mcp_server.py`

```python
# Update to auto-use global setup
from .config import Config

# Get data directory (auto-detects global)
DATA_DIR = str(Config.get_data_dir())
DB_PATH = str(Config.get_data_dir() / "index.db")

# Ensure data directory exists
Config.get_data_dir().mkdir(parents=True, exist_ok=True)

# Initialize database
engine = init_db(DB_PATH)
```

### 4.2 MCP Config Generator

**Command:** `sb config mcp`

```python
@cli.group()
def config():
    """Configuration commands."""
    pass

@config.command()
@click.option("--output", help="Output file path")
def mcp(output):
    """Generate MCP server configuration."""

    import sys

    # Get Python path
    python_path = sys.executable

    # Get second brain dir
    sb_dir = Config.get_second_brain_dir()

    mcp_config = {
        "mcpServers": {
            "second-brain": {
                "command": python_path,
                "args": ["-m", "second_brain.mcp_server"],
                "env": {
                    "SECOND_BRAIN_DIR": str(sb_dir)
                }
            }
        }
    }

    if output:
        with open(output, "w") as f:
            json.dump(mcp_config, f, indent=2)
        console.print(f"[green]✓[/green] MCP config written to {output}")
    else:
        console.print(json.dumps(mcp_config, indent=2))
        console.print("\nAdd this to:")
        console.print("  Claude Code: ~/.config/claude-code/mcp.json")
        console.print("  Claude Desktop: ~/Library/Application Support/Claude/claude_desktop_config.json")
```

---

## Phase 5: Additional Features

### 5.1 Backup Command

```python
@cli.command()
@click.option("--output", "-o", help="Backup file path")
def backup(output):
    """Create backup of second brain."""

    import tarfile
    from datetime import datetime

    sb_dir = Config.get_second_brain_dir()

    if not output:
        output = f"second-brain-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.tar.gz"

    console.print(f"Creating backup: {output}")

    with tarfile.open(output, "w:gz") as tar:
        tar.add(sb_dir, arcname="second-brain")

    console.print(f"[green]✓[/green] Backup created: {output}")
```

### 5.2 Status Dashboard

```python
@cli.command()
def dashboard():
    """Show second brain dashboard."""

    from rich.panel import Panel
    from rich.layout import Layout

    # Get stats
    sb_dir = Config.get_second_brain_dir()
    data_dir = Config.get_data_dir()

    # Count files
    projects = len(list((data_dir / "projects").glob("*.md")))
    work_logs = len(list((data_dir / "work_logs").glob("*.md")))

    # Git status
    os.chdir(sb_dir)
    git_result = subprocess.run(["git", "status", "--porcelain"],
                                capture_output=True, text=True)
    uncommitted = len(git_result.stdout.strip().split("\n")) if git_result.stdout.strip() else 0

    # Display dashboard
    dashboard_text = f"""
    📁 Location: {sb_dir}
    📊 Projects: {projects}
    📝 Work Logs: {work_logs}
    🔄 Uncommitted changes: {uncommitted}
    """

    console.print(Panel(dashboard_text, title="Second Brain Dashboard"))
```

---

## Implementation Order

### Week 1: Core Foundation
1. ✅ Create `config.py` with global path detection
2. ✅ Update `cli.py` to use new config
3. ✅ Update `mcp_server.py` to use new config
4. ✅ Add `--global` flag to `sb init`
5. ✅ Test basic global setup

### Week 2: Git Integration
1. ✅ Add `sb sync push/pull/status` commands
2. ✅ Add git initialization to `sb init --git`
3. ✅ Add `sb setup github` command
4. ✅ Test sync workflow
5. ✅ Add migration command

### Week 3: Polish & Docs
1. ✅ Add `sb config mcp` generator
2. ✅ Add `sb dashboard` command
3. ✅ Add `sb backup` command
4. ✅ Update all documentation
5. ✅ Create migration guide
6. ✅ Test multi-machine setup

### Week 4: Testing & Refinement
1. ✅ Test global setup from scratch
2. ✅ Test migration from local
3. ✅ Test sync across machines
4. ✅ Test MCP server with global setup
5. ✅ Update examples and workflows
6. ✅ Release v0.2.0 with global support

---

## Breaking Changes

### For Existing Users

**Migration path:**
```bash
# Save old data location
OLD_DATA=./data

# Initialize global
sb init --global --git

# Migrate data
sb migrate $OLD_DATA --to-global

# Update shell profile
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc

# Verify
source ~/.bashrc
sb log show
```

### For MCP Server Users

**Update MCP config:**
```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/path/to/python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/home/user/.second-brain"
      }
    }
  }
}
```

Or use generator:
```bash
sb config mcp --output ~/.config/claude-code/mcp.json
```

---

## Success Metrics

- ✅ User can set up in < 5 minutes
- ✅ Works across multiple machines
- ✅ No manual path configuration needed
- ✅ Git sync works reliably
- ✅ MCP server works from any directory
- ✅ Migration from local is seamless
- ✅ Documentation is clear and complete

---

## Next Steps

1. Create feature branch: `git checkout -b feature/global-setup`
2. Implement Phase 1 (core global support)
3. Test thoroughly
4. Update documentation
5. Create PR for review
6. Merge and release v0.2.0
