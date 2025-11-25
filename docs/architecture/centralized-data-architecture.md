# Centralized Data Architecture

## Overview

Second Brain now uses a **fully centralized data architecture** where all data (projects, tasks, notes, epics, issues) is stored in a single location: `~/.second-brain/`

This ensures **consistent behavior** regardless of:
- Current working directory
- Whether using CLI commands or MCP server
- Which project you're working in

## Architecture

```
~/.second-brain/                    # Single source of truth
├── .beads/                         # Beads database (epics, issues, dependencies)
│   ├── beads.db                    # SQLite database
│   └── config.yaml
├── second_brain.db                 # Projects, tasks (SQLite)
├── data/
│   ├── notes/                      # All notes
│   ├── work_logs/                  # All work logs
│   ├── projects/                   # Project files
│   └── transcripts/                # Transcripts
└── keys/                           # Encryption keys
```

## How It Works

### Before (Context-Dependent)

**Problem:** Different behavior based on current directory

```bash
cd ~/projects/my-app
sb project list
# Created/used ./my-app/.second-brain/

cd ~/projects/other-app
sb project list
# Created/used ./other-app/.second-brain/

# Result: Data fragmented across multiple locations!
```

### After (Centralized)

**Solution:** Always uses `~/.second-brain/`

```bash
cd ~/projects/my-app
sb project list
# Uses ~/.second-brain/second_brain.db

cd ~/projects/other-app
sb project list
# Uses ~/.second-brain/second_brain.db

cd /tmp
sb epic list
# Uses ~/.second-brain/.beads/beads.db

# Result: Same data everywhere!
```

## Benefits

### 1. Consistency

- ✅ Same projects/tasks/epics visible from any directory
- ✅ CLI and MCP server use identical data
- ✅ No confusion about "where is my data?"

### 2. Simplicity

- ✅ One backup location (`~/.second-brain/`)
- ✅ One git repository to sync
- ✅ One place to configure

### 3. Cross-Project Visibility

- ✅ See all projects with `sb project list` from anywhere
- ✅ Track work across multiple repos/projects
- ✅ Unified time tracking and reporting

### 4. MCP Server Alignment

- ✅ MCP tools and CLI commands use same database
- ✅ No data sync issues
- ✅ Works correctly in Claude Code, Codex, etc.

## Implementation Details

### Beads Database Location

**File:** `src/second_brain/integrations/beads_integration.py`

```python
# Always use ~/.second-brain as the central beads location
self.project_dir = Path(project_dir) if project_dir else Path.home() / ".second-brain"

# Tell BdClient to use the .beads directory in our project_dir
beads_dir = str(self.project_dir / ".beads")
self.client = BdClient(beads_dir=beads_dir)
```

### Second Brain Data Directory

**File:** `src/second_brain/config.py`

```python
def _detect_global_setup(self, force_global: bool, force_local: bool) -> bool:
    """Default to global (~/.second-brain) - recommended for most users."""

    if force_global:
        return True
    if force_local:
        return False

    # Check environment variable
    if os.getenv("SECOND_BRAIN_DIR"):
        return True

    # Default to global
    return True  # Changed from: return False
```

### Environment Variable Support

You can still override the location if needed:

```bash
# Use custom location
export SECOND_BRAIN_DIR="$HOME/Dropbox/second-brain"
sb project list  # Uses ~/Dropbox/second-brain/

# Or one-time override
SECOND_BRAIN_DIR=/custom/path sb project list
```

### Force Local Mode (Advanced)

For special cases where you need project-specific data:

```bash
# Use local .second-brain/ in current directory
sb init --local
sb project list --local
```

**Note:** Local mode is NOT recommended. It breaks the unified data model.

## Migration from Old Architecture

If you have data in multiple locations from the old architecture:

### Step 1: Find All Data Locations

```bash
find ~ -name ".second-brain" -type d 2>/dev/null
```

### Step 2: Identify Primary Location

Choose which location has your most important data, or use `~/.second-brain/`.

### Step 3: Merge Data (if needed)

```bash
# Backup first!
cp -r ~/.second-brain ~/.second-brain.backup

# Merge databases (SQLite)
sqlite3 ~/.second-brain/second_brain.db "ATTACH '/path/to/other/.second-brain/second_brain.db' AS other; INSERT INTO projects SELECT * FROM other.projects; ..."

# Copy files
cp -r /path/to/other/.second-brain/data/* ~/.second-brain/data/
```

### Step 4: Remove Old Locations

```bash
# After verifying migration worked
rm -rf /path/to/old/.second-brain/
```

## MCP Server Configuration

The MCP server automatically uses the centralized location. No configuration needed!

**Before (manual config required):**
```json
{
  "mcpServers": {
    "second-brain": {
      "command": "sb",
      "args": ["mcp"],
      "env": {
        "SECOND_BRAIN_DIR": "/Users/username/.second-brain"  // Required!
      }
    }
  }
}
```

**After (works automatically):**
```json
{
  "mcpServers": {
    "second-brain": {
      "command": "sb",
      "args": ["mcp"]
      // No env needed - defaults to ~/.second-brain
    }
  }
}
```

## Troubleshooting

### Issue: CLI and MCP show different data

**Symptom:**
- `sb project list` shows project A
- MCP tools show project B

**Diagnosis:**
```bash
# Check what the CLI is using
sb project list
# Note the projects shown

# Check config
python3 -c "from second_brain.config import get_config; print(get_config().second_brain_dir)"
# Should output: /Users/username/.second-brain
```

**Solution:**
1. Ensure you're using latest version: `uv tool install second-brain --force`
2. If using environment variable, remove it: `unset SECOND_BRAIN_DIR`
3. Restart MCP server

### Issue: Data in wrong location

**Symptom:** Commands create data in `./second-brain/` instead of `~/.second-brain/`

**Solution:**
```bash
# Check if you're using old version
sb --version

# Reinstall
uv tool install second-brain --force

# Verify default location
python3 -c "from second_brain.config import get_config; print(get_config().second_brain_dir)"
```

### Issue: Want to use custom location

**Solution:**
```bash
# Set environment variable permanently
echo 'export SECOND_BRAIN_DIR="$HOME/Dropbox/second-brain"' >> ~/.bashrc
source ~/.bashrc

# Verify
echo $SECOND_BRAIN_DIR
```

## Testing Centralization

Verify everything works from any directory:

```bash
# Test from /tmp
cd /tmp
sb epic list
sb project list
sb task list

# Test from home
cd ~
sb epic list
sb project list

# Test from project directory
cd ~/projects/my-app
sb epic list
sb project list

# All should show same data!
```

## Backward Compatibility

### Breaking Changes

- **Default location changed:** No longer creates `.second-brain/` in current directory by default
- **Local mode requires flag:** Must use `--local` explicitly

### Migration Path

1. **Automatic:** If `~/.second-brain/` exists, uses it (no migration needed)
2. **Manual:** If data is in old locations, see "Migration from Old Architecture" above
3. **Fresh start:** New users get centralized setup automatically

## Best Practices

### ✅ DO

- Use default `~/.second-brain/` location
- Backup `~/.second-brain/` regularly
- Sync `~/.second-brain/` to GitHub for cross-machine access
- Use environment variable for custom locations (if needed)

### ❌ DON'T

- Use `--local` mode (unless you have specific need)
- Create multiple `.second-brain/` directories
- Manually edit database files
- Set `SECOND_BRAIN_DIR` to different locations on different machines

## Related Documentation

- [Beads Architecture](./beads-architecture.md) - Epic/issue tracking
- [Configuration Guide](../configuration.md) - Config system details
- [MCP Server](../mcp-server.md) - MCP integration
- [Sync Guide](../sync-guide.md) - Multi-machine setup

## Summary

**One location. One source of truth. Works everywhere.**

```
~/.second-brain/  ← ALL DATA HERE
```

This architecture ensures Second Brain works consistently whether you're:
- Using CLI commands
- Using MCP tools (Claude Code, Codex, etc.)
- Working in any project directory
- On any machine (with git sync)

Simple, predictable, reliable.
