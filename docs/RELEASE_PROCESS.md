# Release and Update Process

## Overview

This document explains how to release new versions of Second Brain and how users update their installations.

Second Brain is distributed in two modes:
1. **CLI Tool** - Installed locally via `uv tool`
2. **MCP Server** - Used by AI agents (Claude Code, Codex, etc.)

Both use the **same codebase** and update process.

---

## For Developers: Creating a Release

### Option 1: Development Workflow (Continuous)

**Use this for:** Active development, testing, frequent updates

```bash
# 1. Make changes
vim src/second_brain/cli.py

# 2. Test locally
uv pip install -e .
sb --version

# 3. Commit and push
git add .
git commit -m "Add new feature"
git push

# 4. Users update with:
uv tool install git+https://github.com/Sean-Koval/second-brain.git --force
```

**Pros:**
- ✅ Fast iteration
- ✅ No version management overhead
- ✅ Users always get latest code

**Cons:**
- ❌ No version tracking
- ❌ Breaking changes without warning
- ❌ Hard to rollback

**Recommended for:** Pre-1.0, active development phase

---

### Option 2: Tagged Releases (Recommended for Production)

**Use this for:** Stable releases, semantic versioning, production use

#### Step 1: Update Version Number

Edit `pyproject.toml`:

```toml
[project]
name = "second-brain"
version = "0.2.0"  # Increment this
```

#### Step 2: Update Changelog

Create/update `CHANGELOG.md`:

```markdown
# Changelog

## [0.2.0] - 2025-11-24

### Added
- Encryption system with RSA-4096 + AES-256-GCM
- Pre-commit hook validation
- Centralized data architecture

### Changed
- Default location now ~/.second-brain (was context-dependent)
- Beads database always uses ~/.second-brain/.beads/

### Breaking Changes
- Local mode now requires explicit --local flag

### Fixed
- CLI/MCP data sync issues
```

#### Step 3: Commit Version Bump

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git push
```

#### Step 4: Create Git Tag

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Release v0.2.0: Encryption & Centralized Architecture"

# Push tag to GitHub
git push origin v0.2.0
```

#### Step 5: Create GitHub Release (Optional but Recommended)

1. Go to https://github.com/Sean-Koval/second-brain/releases
2. Click "Create a new release"
3. Select tag: `v0.2.0`
4. Title: "v0.2.0 - Encryption & Centralized Architecture"
5. Description: Copy from CHANGELOG.md
6. Click "Publish release"

#### Step 6: Users Update With

```bash
# Install specific version
uv tool install git+https://github.com/Sean-Koval/second-brain.git@v0.2.0 --force

# Or latest tag
uv tool install git+https://github.com/Sean-Koval/second-brain.git --force
```

---

### Option 3: PyPI Release (Future - Most Professional)

**Use this for:** 1.0+ releases, wide distribution, maximum convenience

#### Setup (One-time)

```bash
# Install build tools
uv pip install build twine

# Create PyPI account at https://pypi.org/
# Generate API token at https://pypi.org/manage/account/token/

# Store token
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgE...  # Your token
```

#### Release Process

```bash
# 1. Update version in pyproject.toml
vim pyproject.toml  # version = "0.2.0"

# 2. Build distribution
python -m build

# 3. Upload to PyPI
twine upload dist/*

# 4. Tag release
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

#### Users Install With

```bash
# From PyPI (much simpler!)
uv tool install second-brain

# Update
uv tool install second-brain --upgrade
```

**Benefits:**
- ✅ Simple install command
- ✅ Automatic version resolution
- ✅ Standard Python packaging
- ✅ Easy to publish

**Recommended for:** v1.0.0 and beyond

---

## For Users: Updating Second Brain

### Current Installation (Git-based)

Since Second Brain isn't on PyPI yet, users install from GitHub.

#### Initial Install

```bash
# Install as CLI tool
uv tool install git+https://github.com/Sean-Koval/second-brain.git

# Verify
sb --version
```

#### Update to Latest

```bash
# Force reinstall from latest main branch
uv tool install git+https://github.com/Sean-Koval/second-brain.git --force

# Verify new version
sb --version
```

#### Update to Specific Version (if tagged)

```bash
# Install specific release
uv tool install git+https://github.com/Sean-Koval/second-brain.git@v0.2.0 --force

# Check version
sb --version
```

#### Downgrade (if needed)

```bash
# Go back to previous version
uv tool install git+https://github.com/Sean-Koval/second-brain.git@v0.1.0 --force
```

---

## For AI Agents: MCP Server Updates

MCP servers use the **same installation** as the CLI tool.

### MCP Configuration

**File:** `~/.config/claude-code/mcp.json` or `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "sb",
      "args": ["mcp"]
    }
  }
}
```

### Update Process

#### Method 1: Update CLI Tool (Recommended)

```bash
# Update the installed CLI tool
uv tool install git+https://github.com/Sean-Koval/second-brain.git --force

# Restart MCP server (restart Claude Code/Claude Desktop)
```

The MCP server uses the `sb` command from your PATH, so updating the CLI tool automatically updates the MCP server.

#### Method 2: Direct Python Path (Advanced)

If you want to use development version for MCP:

```json
{
  "mcpServers": {
    "second-brain": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/second-brain", "sb", "mcp"]
    }
  }
}
```

This runs directly from your repo (useful for development).

---

## Version Numbering (Semantic Versioning)

Format: `MAJOR.MINOR.PATCH`

- **MAJOR** (1.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.2.0): New features, backward-compatible
- **PATCH** (0.1.1): Bug fixes, backward-compatible

### Examples

- `0.1.0` → `0.1.1`: Bug fixes only
- `0.1.1` → `0.2.0`: New encryption feature (backward-compatible)
- `0.2.0` → `1.0.0`: Stable release, production-ready
- `1.0.0` → `2.0.0`: Breaking changes (e.g., database schema change)

### Pre-1.0 Note

During `0.x.y` versions:
- Breaking changes are allowed in MINOR versions
- API is not stable
- Frequent updates expected

After `1.0.0`:
- Breaking changes only in MAJOR versions
- MINOR versions are backward-compatible
- PATCH versions are bug fixes only

---

## Migration Guides

When releasing breaking changes, include migration guide:

### Example: v0.1.0 → v0.2.0 (Centralized Architecture)

**Breaking Changes:**
- Default location changed from local to global
- Local mode requires explicit `--local` flag

**Migration Steps:**

```bash
# 1. Backup existing data
cp -r ~/.second-brain ~/.second-brain.backup

# 2. Check for project-specific data
find ~/repos -name ".second-brain" -type d

# 3. Migrate if needed
# (see centralized-data-architecture.md)

# 4. Update
uv tool install git+https://github.com/Sean-Koval/second-brain.git --force

# 5. Verify
sb project list  # Should show all projects
```

---

## Testing Updates

### For Developers

```bash
# 1. Create test environment
mkdir /tmp/sb-test
cd /tmp/sb-test

# 2. Install release candidate
uv tool install git+https://github.com/Sean-Koval/second-brain.git@release-candidate --force

# 3. Test commands
sb init
sb project create "Test Project"
sb epic list
sb issue ready

# 4. Test MCP (in Claude Code)
# Restart Claude Code and test MCP tools

# 5. Clean up
uv tool uninstall second-brain
rm -rf /tmp/sb-test
```

### For Users

```bash
# Test new version before committing
# 1. Backup
cp -r ~/.second-brain ~/.second-brain.backup

# 2. Update
uv tool install git+https://github.com/Sean-Koval/second-brain.git --force

# 3. Test
sb --version
sb project list
sb epic list

# 4. If issues, rollback
uv tool install git+https://github.com/Sean-Koval/second-brain.git@v0.1.0 --force
cp -r ~/.second-brain.backup ~/.second-brain
```

---

## Recommended Workflow (Current State)

Since we're in active development (pre-1.0):

### For You (Developer)

1. **Make changes** and test locally
   ```bash
   uv pip install -e .
   sb --version
   ```

2. **Commit and push** to main
   ```bash
   git commit -m "Add feature"
   git push
   ```

3. **Tag major releases** (optional but recommended)
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

4. **Notify users** to update
   - Post in Discord/Slack
   - Update README.md with version notes
   - Create GitHub release with changelog

### For Users

**Update regularly:**
```bash
# Weekly or when notified
uv tool install git+https://github.com/Sean-Koval/second-brain.git --force
```

**For MCP:**
- Update CLI tool as above
- Restart Claude Code/Claude Desktop
- MCP server automatically uses new version

---

## Future: Automated Releases

When ready for 1.0.0, set up GitHub Actions for automated releases:

**`.github/workflows/release.yml`:**
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Build
        run: |
          pip install build
          python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: |
          pip install twine
          twine upload dist/*
```

Then releasing is just:
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
# GitHub Actions automatically builds and publishes to PyPI!
```

---

## Quick Reference

### Current Update Command (Pre-1.0)

```bash
# For users (CLI + MCP)
uv tool install git+https://github.com/Sean-Koval/second-brain.git --force

# Then restart Claude Code/Claude Desktop for MCP
```

### Future Update Command (Post-1.0)

```bash
# Once on PyPI
uv tool install second-brain --upgrade
```

### Check Current Version

```bash
sb --version
```

### Rollback to Previous Version

```bash
# If tagged
uv tool install git+https://github.com/Sean-Koval/second-brain.git@v0.1.0 --force

# If backed up
cp -r ~/.second-brain.backup ~/.second-brain
```

---

## Summary

**Current Workflow (Pre-1.0):**
1. Push to GitHub
2. Users run: `uv tool install git+https://github.com/Sean-Koval/second-brain.git --force`
3. Restart AI agents for MCP updates

**Future Workflow (1.0+):**
1. Tag release
2. GitHub Actions publishes to PyPI
3. Users run: `uv tool install second-brain --upgrade`
4. Restart AI agents for MCP updates

**Key Point:** CLI and MCP use the **same installation**, so one update command updates both!
