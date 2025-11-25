# Beads Architecture in Second Brain

## Design Decision: Single Central Database

Second Brain uses a **single centralized .beads/ database** located at `~/.second-brain/.beads/` for ALL issue and epic tracking.

### Rationale

**Why one central database?**

1. **Unified View**: See all work (personal projects, Second Brain development, work tasks) in one place
2. **Cross-Project Dependencies**: Link issues across different projects naturally
3. **Simplicity**: No confusion about which database you're querying
4. **Consistency**: Commands always show the same data regardless of current directory

**This mirrors how professional issue trackers work:**
- GitHub: All issues for all repos in one organization
- Jira: All issues for all projects in one workspace
- Linear: All issues across teams in one system

### Database Location

```
~/.second-brain/.beads/
├── issues.jsonl          # All epics and issues
├── dependencies.jsonl    # All dependency relationships
└── config.json          # Beads configuration
```

**Fixed location:** `~/.second-brain/.beads/` (NOT dependent on current directory)

### Organization Strategy

Use **prefixes** and **labels** to organize different contexts:

#### Issue Prefixes

```bash
# Second Brain development
SB-1, SB-2, SB-3...

# Work projects
WORK-1, WORK-2, WORK-3...

# Personal projects
PERSONAL-1, PERSONAL-2...

# Or project-specific
ALPHA-1, BETA-1, GAMMA-1...
```

#### Labels for Categorization

```bash
# Project type
--labels "second-brain,dev"
--labels "work,client-project"
--labels "personal,learning"

# Feature area
--labels "encryption,security"
--labels "ui,frontend"
--labels "backend,api"

# Status/priority
--labels "q1-2025,high-priority"
--labels "technical-debt"
```

### Example Usage

```bash
# Create epic for Second Brain development
sb epic create "Add Encryption" \
  --description "Implement RSA encryption for sensitive data" \
  --priority 4 \
  --labels "second-brain,security,encryption"
# Creates: SB-3

# Create epic for personal project
sb epic create "Learn Rust" \
  --description "Complete Rust book and build CLI tool" \
  --priority 2 \
  --labels "personal,learning,rust"
# Creates: SB-11

# List only Second Brain development work
sb issue list --labels second-brain

# List all personal projects
sb issue list --labels personal

# See everything
sb issue list
```

### Integration with Projects/Tasks

Second Brain's **Projects** and **Tasks** (SQLite database) are linked to Beads **Epics** and **Issues**:

```
~/.second-brain/
├── .beads/
│   └── issues.jsonl          # Epics and Issues (high-level planning)
│
├── second_brain.db           # Projects and Tasks (execution tracking)
│   ├── projects              # Links to epics (epic_id column)
│   └── tasks                 # Links to issues (issue_id column)
```

**Workflow:**

1. **Planning**: Create epic in Beads
   ```bash
   sb epic create "Mobile App Redesign"  # SB-15
   sb issue create "Login screen" --epic SB-15  # SB-16
   ```

2. **Execution**: Create project/tasks
   ```bash
   sb project create "Mobile Redesign" --epic SB-15
   sb task add "Redesign login" --issue SB-16
   ```

3. **Syncing**: Updates flow both ways
   - Close issue → marks linked task as done
   - Complete task → updates issue status
   - Epic progress → project progress

### Migration from Current State

**Current state:**
- Dev repo has `.beads/` at `/Users/seankoval/repos/second-brain/.beads/`
- User data has NO `.beads/` at `~/.second-brain/.beads/`

**Migration steps:**

```bash
# 1. Create .beads in user data directory
cd ~/.second-brain
bd init --prefix SB

# 2. Move existing issues from dev repo
cp /Users/seankoval/repos/second-brain/.beads/issues.jsonl ~/.second-brain/.beads/
cp /Users/seankoval/repos/second-brain/.beads/dependencies.jsonl ~/.second-brain/.beads/

# 3. Remove dev repo .beads (or gitignore it)
echo ".beads/" >> /Users/seankoval/repos/second-brain/.gitignore

# 4. Configure beads integration to always use ~/.second-brain/.beads/
# (code change needed in beads_integration.py)
```

### Code Changes Required

**File: `src/second_brain/integrations/beads_integration.py`**

```python
# Current (WRONG - uses cwd):
self.project_dir = Path(project_dir) if project_dir else Path.cwd()

# Fixed (uses fixed location):
self.project_dir = Path(project_dir) if project_dir else Path.home() / ".second-brain"
```

**File: `src/second_brain/config.py`**

```python
# Add beads directory configuration
class Config:
    def __init__(self):
        # ...
        self.beads_dir = self.data_dir / ".beads"

    def ensure_beads_initialized(self):
        """Ensure .beads directory exists and is initialized."""
        if not self.beads_dir.exists():
            self.beads_dir.mkdir(parents=True)
            # Run bd init
```

**File: `src/second_brain/cli.py` (sb init command)**

```python
@cli.command()
def init():
    """Initialize Second Brain."""
    # ... existing code ...

    # Initialize beads database
    beads_dir = data_dir / ".beads"
    if not beads_dir.exists():
        console.print("Initializing Beads issue tracker...")
        os.chdir(data_dir)
        os.system("bd init --prefix SB")
        console.print("✓ Beads initialized at ~/.second-brain/.beads/")
```

### Benefits of This Architecture

1. **No Context Switching**:
   - `sb epic list` shows the same results everywhere
   - No confusion about "which database am I looking at?"

2. **Cross-Project Linking**:
   ```bash
   # Personal learning epic can depend on Second Brain epic
   sb issue add-dependency RUST-5 SB-3 --type related
   # "Learn encryption in Rust" relates to "Add encryption to SB"
   ```

3. **Unified Ready Work**:
   ```bash
   sb issue ready
   # Shows ready work across ALL projects (work, personal, SB dev)
   # All in priority order
   ```

4. **Single Backup**:
   - One `.beads/` directory to backup
   - All in your `~/.second-brain/` git repo
   - Push to GitHub = issues backed up

### What About Team Collaboration?

**Q: If I'm working on a team project with its own .beads/, how does that work?**

**A:** You can still use project-specific .beads/ for team collaboration, but:
- Import/link team issues to your central .beads/
- Or use `--project-dir` flag to specify which .beads/ to use
- Default behavior: always use `~/.second-brain/.beads/`

```bash
# Use team project beads (explicit)
sb issue list --project-dir /work/team-project

# Use your personal beads (default)
sb issue list
```

### Alternative Considered: Multiple .beads/

**Why we rejected per-project .beads/:**

- ❌ Context-dependent behavior (confusing)
- ❌ Can't see all work in unified view
- ❌ Harder to track cross-project dependencies
- ❌ More complex mental model
- ❌ Sync problems between databases

**When to use per-project .beads/:**
- Collaborating with team (shared .beads/ in team repo)
- Strict separation needed (e.g., work vs personal for security)
- Working on large open-source projects with their own issue tracking

### Summary

**Single Source of Truth:**
```
~/.second-brain/.beads/  ← ONE DATABASE FOR ALL ISSUES
```

**Organization:**
- Use prefixes (SB-, WORK-, PERSONAL-)
- Use labels (second-brain, work, personal)
- Link to projects/tasks for execution tracking

**Benefits:**
- Simple, unified, consistent
- Mirrors industry best practices
- Easy to backup and version control
- Natural cross-project linking
