# Second Brain Architecture & Organization

## Overview

Second Brain is designed as a **global, persistent knowledge base** that follows you across all projects and machines. Think of it as your personal work database that lives in one central location.

## Design Philosophy

### Global, Not Per-Project

**Why Global?**
- Your work often spans multiple projects/repositories
- A task in one repo might relate to work in another
- Daily work logs shouldn't be scattered across projects
- One source of truth for all your professional knowledge
- Performance reviews need data from ALL projects
- Time tracking should aggregate across everything you do

**User Experience:**
```bash
# In any directory, any project:
cd ~/work/project-a
sb log add "Fixed bug in auth service"

cd ~/personal/side-project
sb log add "Implemented new feature"

cd ~/
sb report work --days 7
# ^ Shows work from ALL projects
```

---

## Directory Structure

### Recommended Setup

```
~/.second-brain/                    # Global second brain home
├── data/                           # All your data
│   ├── projects/                   # Project markdown files
│   │   ├── work-project-a.md
│   │   ├── work-project-b.md
│   │   ├── personal-blog.md
│   │   └── learning-rust.md
│   ├── work_logs/                  # Daily logs
│   │   ├── 2025-01-15.md
│   │   ├── 2025-01-16.md
│   │   └── 2025-01-17.md
│   ├── transcripts/                # Meeting transcripts
│   │   ├── raw/
│   │   └── processed/
│   └── index.db                    # SQLite database
├── config.json                     # User configuration
├── .git/                           # Git repository
├── .gitignore                      # Git ignore rules
└── README.md                       # Personal documentation

# Environment variable (set once globally)
~/.bashrc or ~/.zshrc:
export SECOND_BRAIN_DIR="$HOME/.second-brain"
```

### Why `~/.second-brain/`?

✅ **Pros:**
- Hidden by default (starts with `.`)
- Lives in home directory (persists across projects)
- Unix convention for user config/data
- Easy to find and backup
- One location for all machines

❌ **Not in project directories:**
- Don't want it scattered across repos
- Don't want to accidentally commit it to project repos
- Don't want to lose it if project is deleted

---

## Git Integration Strategy

### Setup as Git Repository

Your second brain should be a **private Git repository** for:
- Version control of your work history
- Sync across multiple machines
- Backup and disaster recovery
- Ability to share with yourself across devices

### Recommended Git Workflow

```bash
# Initialize (done once)
cd ~/.second-brain
git init
git add .
git commit -m "Initial second brain setup"

# Create private GitHub repo
gh repo create {yourname}-second-brain --private

# Push to GitHub
git remote add origin git@github.com:{yourname}/{yourname}-second-brain.git
git push -u origin main
```

### Repository Naming Convention

Recommended: `{yourname}-second-brain` (private)
- Example: `seanm-second-brain`
- Example: `johndoe-second-brain`

**Why private?**
- Contains work information (could be confidential)
- Personal task descriptions might reference company projects
- Time tracking data is sensitive
- Meeting transcripts could contain private information

### Syncing Across Machines

```bash
# Built-in sync helpers
sb sync push    # Commit and push changes
sb sync pull    # Pull latest changes
sb sync status  # Show git status

# Manual git workflow
cd ~/.second-brain
git add .
git commit -m "Work log updates"
git push

# On another machine
cd ~/.second-brain
git pull
```

### Handling Merge Conflicts

**Common scenarios:**
1. **Work logs from different machines on same day**
   - Machine A: Working from home
   - Machine B: Working from office
   - Both add entries to `2025-01-17.md`
   - Git conflict on pull

**Solution:**
- Markdown files are easy to merge manually
- Keep both entries, merge chronologically
- Or use `sb sync smart-merge` helper (to be implemented)

2. **Task updates from different locations**
   - Less common (SQLite is binary)
   - Prefer working from one machine or syncing frequently

**Best Practices:**
- Sync at start and end of day
- Use `sb sync pull` before starting work
- Use `sb sync push` before shutting down
- Let git handle markdown merges
- For database conflicts, last write wins (or manual resolution)

---

## What Gets Synced in Your Git Repo

When you turn `~/.second-brain/` into a git repository, everything is version-controlled and synced:

### Files in Your Repository

```
~/.second-brain/  (git repository root)
├── .git/                    # Git metadata
├── .gitignore               # Auto-generated ignore rules
├── README.md                # Your personal documentation
├── config.json              # Your Second Brain configuration
└── data/
    ├── index.db             # SQLite database (all tables!)
    ├── projects/            # All project markdown files
    │   ├── project-a.md
    │   ├── project-b.md
    │   └── learning-rust.md
    ├── work_logs/           # All daily work logs
    │   ├── 2025-01-15.md
    │   ├── 2025-01-16.md
    │   └── 2025-01-17.md
    └── transcripts/
        ├── raw/             # Raw meeting transcripts
        └── processed/       # Processed transcripts
```

### What's Inside

**SQLite Database (`data/index.db`):**
- All projects, tasks, work logs, transcripts
- Relationships between entities
- Time tracking data
- Full database state

**Markdown Files:**
- Human-readable versions of your data
- Project notes with frontmatter
- Daily work logs with timestamps
- Meeting transcripts with summaries

**Configuration (`config.json`):**
- User information
- Sync settings
- Jira configuration (credentials excluded via .gitignore if desired)
- Default preferences

### Real-World Example

After a week of work:

```bash
cd ~/.second-brain
git log --oneline

a1b2c3d Work updates 2025-01-17
d4e5f6g Work updates 2025-01-16
g7h8i9j Added new project: mobile-redesign
j0k1l2m Work updates 2025-01-15
```

Each commit contains:
- Updated SQLite database
- New/modified markdown files
- Any config changes

### Benefits of Git Sync

1. **Full History** - Every change is tracked
2. **Easy Recovery** - Revert mistakes with `git checkout`
3. **Multiple Machines** - Clone to any computer
4. **Offline Access** - All data local, sync when online
5. **Backup** - GitHub acts as remote backup
6. **Collaboration** - Could share with team (advanced use case)

### Viewing Your Data

Anyone with access to your repository can:

```bash
# Clone your data
git clone git@github.com:yourusername/yourusername-second-brain.git
cd yourusername-second-brain

# Browse markdown files
cat data/work_logs/2025-01-17.md
cat data/projects/mobile-redesign.md

# Query database
sqlite3 data/index.db "SELECT * FROM tasks WHERE status='in_progress';"

# View history
git log data/work_logs/
```

All your work history, tasks, projects, and notes - readable as markdown files AND queryable as a database!

---

## Multi-Machine Setup

### Initial Setup on New Machine

```bash
# On your first machine (already set up)
cd ~/.second-brain
git remote add origin git@github.com:{yourname}/{yourname}-second-brain.git
git push -u origin main

# On your second machine
git clone git@github.com:{yourname}/{yourname}-second-brain.git ~/.second-brain
cd ~/.second-brain

# Install second-brain CLI
pip install second-brain  # or from source

# Set environment variable
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc

# Verify
sb log show
sb project list
```

### Daily Workflow Across Machines

```bash
# Morning on work laptop
sb sync pull                    # Get latest from home machine
sb log add "Starting work day"

# Evening on work laptop
sb log add "Finished feature X"
sb sync push                    # Push to GitHub

# Later on home machine
sb sync pull                    # Get work laptop updates
sb log add "Evening side project work"
sb sync push
```

---

## Configuration Management

### Global Config File

`~/.second-brain/config.json`:
```json
{
  "user": {
    "name": "Sean M",
    "email": "sean@example.com"
  },
  "sync": {
    "auto_push": false,
    "auto_pull": true,
    "remote": "origin"
  },
  "jira": {
    "server": "https://company.atlassian.net",
    "email": "sean@company.com",
    "default_project": "PROJ"
  },
  "defaults": {
    "work_log_time_tracking": true,
    "auto_link_tasks": true
  },
  "paths": {
    "data_dir": "data",
    "projects_dir": "data/projects",
    "work_logs_dir": "data/work_logs",
    "transcripts_dir": "data/transcripts"
  }
}
```

### Environment Variables

```bash
# Primary variable - points to second brain home
export SECOND_BRAIN_DIR="$HOME/.second-brain"

# Optional overrides (usually not needed)
export SECOND_BRAIN_DATA_DIR="$SECOND_BRAIN_DIR/data"

# Jira credentials (optional)
export JIRA_SERVER="https://company.atlassian.net"
export JIRA_EMAIL="you@company.com"
export JIRA_API_TOKEN="your-token"
```

### MCP Server Configuration

**Claude Code** (`~/.config/claude-code/mcp.json`):
```json
{
  "mcpServers": {
    "second-brain": {
      "command": "/usr/local/bin/python3",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DIR": "/home/user/.second-brain"
      }
    }
  }
}
```

**Benefits:**
- Works from any project directory in Claude Code
- No need to reconfigure per project
- Access your entire work history from anywhere

---

## Data Organization Principles

### Project-Agnostic Storage

Projects in Second Brain ≠ Code repositories

**Examples:**

```markdown
# ~/.second-brain/data/projects/work-backend-services.md
---
name: Work - Backend Services
slug: work-backend-services
repos:
  - git@github.com:company/api-service.git
  - git@github.com:company/worker-service.git
  - git@github.com:company/auth-service.git
tags: [work, backend, microservices]
---

This project tracks work across multiple backend service repositories.
```

```markdown
# ~/.second-brain/data/projects/learning-rust.md
---
name: Learning Rust
slug: learning-rust
repos:
  - git@github.com:me/rust-exercises.git
  - git@github.com:me/rust-cli-tool.git
tags: [learning, rust, personal-development]
---

Tracking my Rust learning journey across various practice projects.
```

### Linking Work to Repositories

Work logs and tasks can reference specific repos:

```bash
# Work log entry
sb log add "Fixed bug in API service (company/api-service#123)" --time 90

# Task with repo context
sb task add "Review PR in auth-service" \
  --project work-backend-services \
  --description "PR: company/auth-service#456"
```

---

## Installation & Initialization

### Recommended Setup Process

```bash
# 1. Install second-brain
pip install second-brain

# 2. Initialize global second brain
sb init --global

# This creates:
# - ~/.second-brain/
# - ~/.second-brain/data/
# - ~/.second-brain/config.json
# - Initializes git repo

# 3. Add to shell profile
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc

# 4. Create GitHub repo and push
cd ~/.second-brain
gh repo create {yourname}-second-brain --private
git remote add origin git@github.com:{yourname}/{yourname}-second-brain.git
git push -u origin main

# 5. Configure MCP server (one-time)
sb config mcp --generate

# 6. Start using it!
sb project create "My First Project"
sb task add "Set up second brain"
sb log add "Initialized my second brain system"
```

### `sb init --global` vs `sb init`

```bash
# Global (recommended)
sb init --global
# Creates in ~/.second-brain/
# Sets up environment variable
# Works from anywhere

# Local (old way, not recommended)
sb init
# Creates in ./data/
# Only works in current project
# Need separate second brain per project (bad UX)
```

---

## Workflow Examples

### Typical Daily Workflow

```bash
# Morning - sync and check status
sb sync pull
sb current-work                 # See what's in progress

# During day - work in any project directory
cd ~/work/api-service
sb log add "Fixed timeout in auth middleware" --time 120
sb task update 15 --status in_progress

cd ~/work/frontend-app
sb log add "Updated dashboard UI" --time 90
sb task update 23 --time 90

cd ~/personal/blog
sb log add "Wrote post about Rust" --time 60

# End of day - from anywhere
sb daily-summary                # Review the day
sb sync push                    # Push to GitHub
```

### Weekly Review (from anywhere)

```bash
# Friday afternoon, in any directory
cd ~/  # or wherever

sb weekly-review                # Interactive review
sb report work --days 7 > ~/Desktop/weekly-status.md

# Sync before weekend
sb sync push
```

### Cross-Project Task Management

```bash
# Create tasks that span multiple repos
sb task add "Implement OAuth across all services" \
  --project work-backend-services \
  --priority high

# Link work from different repos
cd ~/work/api-service
sb log add "Added OAuth to API" --task-id 42 --time 180

cd ~/work/auth-service
sb log add "Implemented token refresh" --task-id 42 --time 120

cd ~/work/worker-service
sb log add "Updated auth headers" --task-id 42 --time 90

# View all work on this task
sb task show 42
# Shows work across all three repos!
```

---

## Backup & Disaster Recovery

### Backup Strategy

**Primary: Git + GitHub**
```bash
# Automatic via sync
sb sync push  # Daily at minimum
```

**Secondary: Local Backups**
```bash
# Periodic backups
cp -r ~/.second-brain ~/Dropbox/backups/second-brain-$(date +%Y%m%d)

# Or automated
crontab -e
# Add: 0 2 * * 0 tar -czf ~/Dropbox/second-brain-$(date +\%Y\%m\%d).tar.gz ~/.second-brain
```

**Tertiary: Cloud Sync**
- Keep `~/.second-brain/` in Dropbox/Google Drive/iCloud
- Automatic sync across devices
- Additional redundancy

### Recovery Scenarios

**Lost laptop:**
```bash
# On new machine
git clone git@github.com:{yourname}/{yourname}-second-brain.git ~/.second-brain
pip install second-brain
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
# All your data is back!
```

**Corrupted database:**
```bash
# Rebuild from markdown files
cd ~/.second-brain
git checkout HEAD -- data/index.db  # Revert to last commit
sb rebuild-index                     # Rebuild from markdown
```

**Accidental deletion:**
```bash
# Git history saves you
cd ~/.second-brain
git log --oneline data/work_logs/
git checkout HEAD~5 -- data/work_logs/2025-01-17.md
```

---

## Privacy & Security Considerations

### What Goes in Second Brain

**Safe to store:**
- Task titles and descriptions (use your judgment)
- Work log entries (keep general)
- Time tracking data
- Project notes
- Meeting summaries (scrubbed of sensitive info)

**Be careful with:**
- Customer names or details
- Confidential project codenames
- Financial information
- Security vulnerabilities
- API keys or credentials (NEVER!)

### Repository Privacy

**Always use private repo for:**
- Work-related tracking
- Any company project references
- Client information
- Sensitive time tracking

**Could use public repo for:**
- Personal learning projects only
- Open source contribution tracking
- Generic workflow templates

### Company Policy Compliance

**Check with your company:**
- Can you store work task descriptions in personal repos?
- Are there data retention policies?
- Can you sync work data to personal GitHub?

**Best practices:**
- Keep descriptions generic
- Don't include customer data
- Use project codes instead of names
- Review before pushing sensitive periods

---

## Migration from Local Setup

### If You Already Have Local Data

```bash
# 1. Initialize global second brain
sb init --global

# 2. Migrate existing data
cp -r ./data/* ~/.second-brain/data/

# 3. Rebuild index
cd ~/.second-brain
sb rebuild-index

# 4. Initialize git
cd ~/.second-brain
git init
git add .
git commit -m "Migrated from local setup"
git remote add origin git@github.com:{yourname}/{yourname}-second-brain.git
git push -u origin main

# 5. Update environment
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc

# 6. Remove local data
cd ~/old-project
rm -rf ./data

# 7. Test
sb log show  # Should show migrated data
```

---

## Future Enhancements

### Planned Features

1. **Better Sync**
   - `sb sync auto` - Auto-commit and push on changes
   - Smart merge conflict resolution
   - Sync status in CLI prompt

2. **Multi-User Collaboration** (Optional)
   - Share specific projects with team
   - Collaborative meeting notes
   - Shared task lists

3. **Advanced Search**
   - Full-text search across all markdown
   - Search by date ranges, tags, projects
   - Search within transcripts

4. **Analytics Dashboard**
   - Web UI to visualize work patterns
   - Time tracking charts
   - Project progress graphs
   - Generated from local data

5. **Smart Backup**
   - Encrypted backups
   - Selective sync (work vs personal)
   - Backup verification

---

## Summary

**Key Principles:**
1. ✅ Global, not per-project
2. ✅ Lives in `~/.second-brain/`
3. ✅ Git repo synced to private GitHub
4. ✅ Works from any directory
5. ✅ One source of truth
6. ✅ Easy to backup and sync
7. ✅ MCP server accessible everywhere

**User Experience:**
- Install once, use everywhere
- No configuration per project
- Natural cross-project workflows
- Safe in git with history
- Sync across all your machines
- Available to AI agents globally

This architecture makes Second Brain truly feel like **your personal work operating system**! 🧠
