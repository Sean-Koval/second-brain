# `sb install-hooks` Command Specification

## Overview
The `sb install-hooks` command installs git hooks into the user's Second Brain data repository (`~/.second-brain/.git/hooks/`). This automates the setup of pre-commit validation to prevent accidental commits of unencrypted sensitive data.

## Command Syntax

```bash
sb install-hooks [OPTIONS]
```

### Options
- `--check` - Check if hooks are installed without installing
- `--force` - Reinstall hooks even if they already exist
- `--help` - Show help message

## Requirements

### Prerequisites
1. User must have initialized Second Brain: `sb init --global`
2. `~/.second-brain/` directory must exist
3. `~/.second-brain/.git/` must be a git repository
4. User must have write permissions to `.git/hooks/`

### Hook Installation Steps
1. **Verify git repository exists**
   - Check for `~/.second-brain/.git/` directory
   - If not found, provide helpful error message

2. **Create hooks directory**
   - Ensure `~/.second-brain/.git/hooks/` exists
   - Create if missing

3. **Copy hook script**
   - Read hook template from `src/second_brain/hooks/pre_commit.py`
   - Write to `~/.second-brain/.git/hooks/pre-commit`
   - Add shebang line: `#!/usr/bin/env python3`

4. **Make executable**
   - Set executable permissions (chmod +x)
   - Unix: 0o755 (rwxr-xr-x)

5. **Verify installation**
   - Check file exists
   - Check file is executable
   - Optionally test hook runs without error

## Implementation Details

### File Structure
```python
# In cli.py

@cli.command("install-hooks")
@click.option("--check", is_flag=True, help="Check hook installation status")
@click.option("--force", is_flag=True, help="Reinstall hooks even if exist")
def install_hooks(check, force):
    """Install git hooks for Second Brain validation."""
    # Implementation
```

### Hook Template Format
```python
#!/usr/bin/env python3
"""Pre-commit hook for Second Brain encryption validation."""

# Import and run the hook main function
from second_brain.hooks.pre_commit import main
import sys
sys.exit(main())
```

### Error Handling

**Case 1: Not a git repository**
```
❌ Error: ~/.second-brain is not a git repository

To initialize:
  cd ~/.second-brain
  git init
```

**Case 2: No write permissions**
```
❌ Error: Cannot write to ~/.second-brain/.git/hooks/
Permission denied

Check directory permissions
```

**Case 3: Hook already exists (without --force)**
```
✓ Pre-commit hook already installed

To reinstall: sb install-hooks --force
To check status: sb install-hooks --check
```

### Success Output

**Installation:**
```
🔧 Installing git hooks...

✓ Pre-commit hook installed successfully!

Location: ~/.second-brain/.git/hooks/pre-commit
Permissions: -rwxr-xr-x

What it validates:
  • No unencrypted API keys, passwords, or secrets
  • No private key files committed
  • Files marked as sensitive are encrypted
  • Proper encryption format

Test the hook:
  cd ~/.second-brain
  # Make some changes
  git add .
  git commit -m "test"

Bypass validation (not recommended):
  git commit --no-verify
```

**Check status:**
```
🔍 Checking hook installation status...

✓ Pre-commit hook: Installed
  Location: ~/.second-brain/.git/hooks/pre-commit
  Permissions: -rwxr-xr-x
  Last modified: 2025-11-24 03:30:00

Hook is working correctly ✓
```

## Testing Plan

### Test Cases

1. **Fresh installation (no hook exists)**
   - Run `sb install-hooks`
   - Verify hook file created
   - Verify executable permissions
   - Verify hook works

2. **Hook already exists**
   - Run `sb install-hooks` again
   - Should inform user and not overwrite
   - Verify with `--force` it reinstalls

3. **Check status**
   - Run `sb install-hooks --check`
   - Should show current status
   - Should not modify anything

4. **Not a git repo**
   - Remove `.git` directory
   - Run `sb install-hooks`
   - Should show helpful error

5. **Hook execution test**
   - After install, create file with API key
   - Try to commit
   - Should block commit

## Implementation Code

```python
import os
import stat
from pathlib import Path
import shutil

@cli.command("install-hooks")
@click.option("--check", is_flag=True, help="Check hook installation status")
@click.option("--force", is_flag=True, help="Reinstall hooks even if exist")
def install_hooks(check, force):
    """Install git hooks for Second Brain validation."""
    from datetime import datetime

    config = get_app_config()
    git_dir = config.second_brain_dir / '.git'
    hooks_dir = git_dir / 'hooks'
    pre_commit_hook = hooks_dir / 'pre-commit'

    # Check if git repository exists
    if not git_dir.exists():
        console.print("[red]✗ Error: Not a git repository[/red]")
        console.print(f"\n{config.second_brain_dir} is not a git repository")
        console.print("\nTo initialize:")
        console.print(f"  cd {config.second_brain_dir}")
        console.print("  git init")
        return

    # Check status mode
    if check:
        console.print("🔍 Checking hook installation status...\n")

        if pre_commit_hook.exists():
            stat_info = pre_commit_hook.stat()
            is_executable = bool(stat_info.st_mode & stat.S_IXUSR)

            console.print("[green]✓[/green] Pre-commit hook: Installed")
            console.print(f"  Location: {pre_commit_hook}")

            # Show permissions
            mode = oct(stat_info.st_mode)[-3:]
            console.print(f"  Permissions: {mode} {'(executable)' if is_executable else '(not executable!)'}")

            # Show last modified
            mtime = datetime.fromtimestamp(stat_info.st_mtime)
            console.print(f"  Last modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

            if not is_executable:
                console.print("\n[yellow]⚠ Warning: Hook is not executable[/yellow]")
                console.print("Run: sb install-hooks --force")
            else:
                console.print("\n[green]Hook is working correctly ✓[/green]")
        else:
            console.print("[yellow]✗[/yellow] Pre-commit hook: Not installed")
            console.print(f"  Location: {pre_commit_hook}")
            console.print("\nTo install:")
            console.print("  sb install-hooks")

        return

    # Installation mode
    console.print("🔧 Installing git hooks...\n")

    # Check if hook already exists
    if pre_commit_hook.exists() and not force:
        console.print("[yellow]✓ Pre-commit hook already installed[/yellow]\n")
        console.print(f"Location: {pre_commit_hook}")
        console.print("\nTo reinstall: [cyan]sb install-hooks --force[/cyan]")
        console.print("To check status: [cyan]sb install-hooks --check[/cyan]")
        return

    # Create hooks directory if needed
    hooks_dir.mkdir(parents=True, exist_ok=True)

    # Get hook template
    from . import hooks
    hook_module_path = Path(hooks.__file__).parent / 'pre_commit.py'

    if not hook_module_path.exists():
        console.print("[red]✗ Error: Hook template not found[/red]")
        console.print(f"Expected: {hook_module_path}")
        return

    # Read template
    hook_content = hook_module_path.read_text()

    # Write hook with shebang
    with open(pre_commit_hook, 'w') as f:
        # Ensure shebang is first line
        if not hook_content.startswith('#!/'):
            f.write('#!/usr/bin/env python3\n')
        f.write(hook_content)

    # Make executable
    pre_commit_hook.chmod(pre_commit_hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Verify
    if not pre_commit_hook.exists():
        console.print("[red]✗ Failed to install hook[/red]")
        return

    stat_info = pre_commit_hook.stat()
    mode = oct(stat_info.st_mode)[-3:]

    console.print("[green]✓ Pre-commit hook installed successfully![/green]\n")
    console.print(f"Location: {pre_commit_hook}")
    console.print(f"Permissions: -{mode}\n")

    console.print("What it validates:")
    console.print("  • No unencrypted API keys, passwords, or secrets")
    console.print("  • No private key files committed")
    console.print("  • Files marked as sensitive are encrypted")
    console.print("  • Proper encryption format\n")

    console.print("Test the hook:")
    console.print(f"  cd {config.second_brain_dir}")
    console.print("  # Make some changes")
    console.print("  git add .")
    console.print('  git commit -m "test"\n')

    console.print("Bypass validation (not recommended):")
    console.print("  git commit --no-verify")
```

## Success Criteria

- [ ] Command installs hook to correct location
- [ ] Hook file is executable
- [ ] Hook works when git commit is run
- [ ] `--check` shows accurate status
- [ ] `--force` reinstalls correctly
- [ ] Helpful error messages for edge cases
- [ ] Documentation updated
