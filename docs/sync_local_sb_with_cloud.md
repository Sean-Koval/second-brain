# Syncing Local Second Brain with GitHub Cloud

This guide shows you how to sync your local Second Brain installation with a private GitHub repository for backup and multi-machine access.

## Prerequisites

- Second Brain installed globally with `uv tool install`
- A GitHub account
- SSH key configured with GitHub (or use HTTPS)
- `gh` CLI tool (optional, for creating repos)

## Two Scenarios

### Scenario 1: Fresh Clone from Existing GitHub Repo (Recommended for New Machines)

Use this when you have an existing Second Brain GitHub repository and want to set it up on a new machine.

**Steps:**

1. **Install Second Brain globally:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv tool install git+https://github.com/seanm/second-brain.git
   ```

2. **Remove any existing local initialization:**
   ```bash
   rm -rf ~/.second-brain
   ```

3. **Clone your GitHub repository:**
   ```bash
   git clone git@github.com:YOUR_USERNAME/second-brain-YOUR_NAME.git ~/.second-brain
   ```

   Replace `YOUR_USERNAME/second-brain-YOUR_NAME.git` with your actual repo URL.

4. **Set environment variable:**
   ```bash
   export SECOND_BRAIN_DIR="$HOME/.second-brain"

   # Add to your shell profile for persistence
   echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.zshrc
   # OR for bash:
   # echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc

   # Apply changes
   source ~/.zshrc  # or source ~/.bashrc
   ```

5. **Verify the sync worked:**
   ```bash
   sb project list
   sb task list
   ```

**You're done!** Your local Second Brain is now synced with GitHub.

---

### Scenario 2: Sync Existing Local Data to New GitHub Repo

Use this when you have local Second Brain data and want to back it up to GitHub for the first time.

**Steps:**

1. **Navigate to your Second Brain directory:**
   ```bash
   cd ~/.second-brain
   ```

2. **Initialize git (if not already done):**
   ```bash
   git init
   ```

3. **Create a private GitHub repository:**

   **Option A: Using GitHub CLI:**
   ```bash
   gh repo create YOUR_USERNAME-second-brain --private
   ```

   **Option B: Via GitHub Web:**
   - Go to https://github.com/new
   - Name: `YOUR_USERNAME-second-brain` or `second-brain-YOUR_NAME`
   - Visibility: Private
   - Click "Create repository"

4. **Add GitHub as remote:**
   ```bash
   git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

5. **Add and commit your local data:**
   ```bash
   git add .
   git commit -m "Initial second brain setup"
   ```

6. **Push to GitHub:**
   ```bash
   git branch -M main  # Ensure you're on main branch
   git push -u origin main
   ```

**You're done!** Your Second Brain is now backed up to GitHub.

---

## Daily Sync Workflow

Once your initial setup is complete, use this workflow to keep your data synced:

### Pull Latest Changes (Start of Day)

```bash
cd ~/.second-brain
git pull
```

### Push Your Updates (End of Day)

```bash
cd ~/.second-brain
git add .
git commit -m "Work updates $(date +%Y-%m-%d)"
git push
```

### Quick Sync Alias (Optional)

Add this to your `~/.zshrc` or `~/.bashrc`:

```bash
alias sb-sync='cd ~/.second-brain && git add . && git commit -m "Work updates $(date +%Y-%m-%d)" && git push && cd -'
alias sb-pull='cd ~/.second-brain && git pull && cd -'
```

Then you can simply run:
```bash
sb-pull   # Pull latest changes
sb-sync   # Commit and push your changes
```

---

## Multi-Machine Setup

### On Your Primary Machine (Work Laptop)

Follow **Scenario 2** to create and push your initial Second Brain to GitHub.

### On Your Secondary Machine (Home Desktop)

Follow **Scenario 1** to clone your existing GitHub repo.

### Keeping Machines in Sync

**Before working (on any machine):**
```bash
sb-pull  # or: cd ~/.second-brain && git pull
```

**After working (on any machine):**
```bash
sb-sync  # or: cd ~/.second-brain && git add . && git commit -m "..." && git push
```

---

## Troubleshooting

### "fatal: not a git repository"

You haven't initialized git yet. Run:
```bash
cd ~/.second-brain
git init
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
```

### "Permission denied (publickey)"

Your SSH key isn't configured with GitHub. Either:
- Add your SSH key: https://github.com/settings/keys
- Use HTTPS instead: `https://github.com/YOUR_USERNAME/YOUR_REPO.git`

### "sb: command not found"

Second Brain isn't installed or not in PATH. Run:
```bash
uv tool install git+https://github.com/seanm/second-brain.git
```

### Environment variable not set

Run:
```bash
export SECOND_BRAIN_DIR="$HOME/.second-brain"
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.zshrc
source ~/.zshrc
```

### Merge conflicts when pulling

If you edited Second Brain on multiple machines without syncing:

```bash
cd ~/.second-brain
git pull
# Fix any conflicts in the files
git add .
git commit -m "Resolved merge conflicts"
git push
```

---

## Security Notes

1. **Always use a private repository** - Your Second Brain contains your work data
2. **Consider encrypting sensitive data** - Use Second Brain's built-in encryption features
3. **Don't commit secrets** - The `.gitignore` should already exclude sensitive files
4. **Review what's being committed** - Run `git status` before `git push`

---

## What Gets Synced

Your GitHub repo will contain:

```
~/.second-brain/
├── .git/                 # Git tracking
├── .gitignore           # Excluded files
├── config.json          # Second Brain config
├── README.md            # Repo README
├── data/
│   ├── index.db         # SQLite database
│   ├── projects/        # Project markdown files
│   ├── work_logs/       # Daily work logs
│   └── transcripts/     # Meeting transcripts
├── .beads/              # Beads epic/dependency tracking
│   ├── issues.jsonl
│   └── dependencies.jsonl
└── keys/                # Encryption keys (if using encryption)
```

Everything is synced, including the SQLite database and all markdown files!

---

## Example: Complete Setup from Scratch

Here's a complete walkthrough for setting up Second Brain with GitHub sync:

```bash
# 1. Install Second Brain
uv tool install git+https://github.com/seanm/second-brain.git

# 2. Initialize globally
sb init --global

# 3. Set environment variable
export SECOND_BRAIN_DIR="$HOME/.second-brain"
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.zshrc
source ~/.zshrc

# 4. Create some initial data
sb project create "Test Project"
sb log add "Setting up Second Brain"

# 5. Set up GitHub sync
cd ~/.second-brain
git init
git add .
git commit -m "Initial second brain setup"
gh repo create myusername-second-brain --private
git remote add origin git@github.com:myusername/myusername-second-brain.git
git push -u origin main

# 6. Create sync aliases
echo 'alias sb-sync="cd ~/.second-brain && git add . && git commit -m \"Work updates \$(date +%Y-%m-%d)\" && git push && cd -"' >> ~/.zshrc
echo 'alias sb-pull="cd ~/.second-brain && git pull && cd -"' >> ~/.zshrc
source ~/.zshrc
```

Done! Now you can use `sb-pull` and `sb-sync` to keep your Second Brain synced across machines.

---

## Related Documentation

- [Quick Start Guide](quickstart.md) - Initial Second Brain setup
- [Installation Guide](installation.md) - Detailed installation instructions
- [CLI Reference](cli-reference.md) - All Second Brain commands
- [MCP Server Setup](mcp-server.md) - Connect to AI agents
