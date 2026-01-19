"""Git hooks for encryption validation.

Pre-commit hook to verify no unencrypted sensitive data is being pushed.
Scans for sensitive markers and ensures encryption.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Patterns that suggest sensitive data
SENSITIVE_PATTERNS = [
    # API keys and tokens
    (r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{20,}["\']?', "API key"),
    (r'(?i)(secret|token|password|passwd|pwd)\s*[:=]\s*["\']?[^\s"\']{8,}["\']?', "Secret/Password"),
    (r'(?i)bearer\s+[a-zA-Z0-9_\-\.]+', "Bearer token"),
    
    # AWS credentials
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
    (r'(?i)aws[_-]?secret[_-]?access[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9/+=]{40}["\']?', "AWS Secret Key"),
    
    # Private keys
    (r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', "Private key"),
    (r'-----BEGIN ENCRYPTED PRIVATE KEY-----', "Encrypted private key"),
    
    # Connection strings
    (r'(?i)(mongodb|postgres|mysql|redis):\/\/[^\s]+', "Database connection string"),
    
    # Generic secrets
    (r'(?i)(client[_-]?secret|app[_-]?secret)\s*[:=]\s*["\']?[^\s"\']{10,}["\']?', "Client/App secret"),
]

# File patterns to skip
SKIP_PATTERNS = [
    r'\.git/',
    r'\.venv/',
    r'__pycache__/',
    r'node_modules/',
    r'\.pyc$',
    r'\.pyo$',
    r'\.egg-info/',
    r'\.lock$',
]


def get_staged_files() -> List[str]:
    """Get list of files staged for commit."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True
        )
        return [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    except subprocess.CalledProcessError:
        return []


def should_skip_file(filepath: str) -> bool:
    """Check if file should be skipped based on patterns."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, filepath):
            return True
    return False


def is_encrypted_content(content: str) -> bool:
    """Check if content contains encrypted markers."""
    return '<!-- ENCRYPTED:' in content or 'v1:RSA-AES256-GCM:' in content


def scan_file_for_sensitive_data(filepath: str) -> List[Tuple[int, str, str]]:
    """Scan a file for sensitive data patterns.
    
    Args:
        filepath: Path to file to scan
        
    Returns:
        List of (line_number, pattern_name, matched_text) tuples
    """
    findings = []
    
    try:
        path = Path(filepath)
        if not path.exists():
            return []
            
        # Skip binary files
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return []  # Binary file
            
        # Check if content is properly encrypted
        if is_encrypted_content(content):
            # File appears encrypted, but let's make sure nothing is exposed outside blocks
            # Split by encrypted blocks and scan non-encrypted parts
            parts = re.split(r'<!-- ENCRYPTED:.*?<!-- END ENCRYPTED -->', content, flags=re.DOTALL)
            content = '\n'.join(parts)
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            for pattern, name in SENSITIVE_PATTERNS:
                matches = re.finditer(pattern, line)
                for match in matches:
                    # Avoid false positives in comments about security
                    if 'example' in line.lower() or 'your_' in line.lower():
                        continue
                    findings.append((line_num, name, match.group()[:50] + '...'))
                    
    except Exception as e:
        print(f"Warning: Could not scan {filepath}: {e}", file=sys.stderr)
        
    return findings


def check_note_encryption_status(second_brain_dir: Path) -> List[Tuple[str, str]]:
    """Check if notes marked as sensitive are properly encrypted.
    
    Args:
        second_brain_dir: Second Brain directory
        
    Returns:
        List of (note_path, issue) tuples
    """
    issues = []
    
    # This would need database access in a full implementation
    # For the pre-commit hook, we'll scan markdown files with sensitive markers
    
    notes_dir = second_brain_dir / "data" / "notes"
    if not notes_dir.exists():
        return []
        
    for md_file in notes_dir.rglob("*.md"):
        try:
            content = md_file.read_text()
            
            # Check for sensitive marker in frontmatter
            if 'sensitive: true' in content.lower() or 'is_sensitive: true' in content.lower():
                # Ensure content is encrypted
                if not is_encrypted_content(content):
                    issues.append((str(md_file), "Marked sensitive but not encrypted"))
                    
        except Exception:
            pass
            
    return issues


def run_pre_commit_check(verbose: bool = False) -> Tuple[bool, List[str]]:
    """Run pre-commit encryption validation.
    
    Args:
        verbose: Print detailed output
        
    Returns:
        Tuple of (passed: bool, messages: List[str])
    """
    messages = []
    passed = True
    
    # Get staged files
    staged_files = get_staged_files()
    
    if verbose:
        messages.append(f"Scanning {len(staged_files)} staged files...")
    
    # Scan each file
    for filepath in staged_files:
        if should_skip_file(filepath):
            continue
            
        findings = scan_file_for_sensitive_data(filepath)
        
        if findings:
            passed = False
            messages.append(f"\n❌ Potential sensitive data in {filepath}:")
            for line_num, pattern_name, text in findings:
                messages.append(f"   Line {line_num}: {pattern_name}")
                if verbose:
                    messages.append(f"      Preview: {text}")
    
    # Check for private keys being committed
    for filepath in staged_files:
        if 'private' in filepath.lower() and filepath.endswith('.pem'):
            passed = False
            messages.append(f"\n❌ CRITICAL: Private key staged for commit: {filepath}")
            messages.append("   Remove with: git reset HEAD {filepath}")
    
    if passed:
        messages.append("✅ No sensitive data detected in staged files")
    else:
        messages.append("\n⚠️  Fix issues above or use --no-verify to bypass")
        messages.append("   To encrypt sensitive content: sb note mark-sensitive <id> --encrypt")
        
    return passed, messages


def generate_hook_script() -> str:
    """Generate the pre-commit hook script."""
    return '''#!/usr/bin/env bash
# Second Brain pre-commit hook
# Validates no unencrypted sensitive data is being committed

# Find python interpreter
PYTHON=""
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "❌ Python not found, skipping encryption check"
    exit 0
fi

# Try to run the check via sb command
if command -v sb &> /dev/null; then
    sb hook check
    exit $?
fi

# Fallback: Run directly via Python module
$PYTHON -c "
from second_brain.crypto.hooks import run_pre_commit_check
import sys

passed, messages = run_pre_commit_check(verbose=True)
for msg in messages:
    print(msg)
sys.exit(0 if passed else 1)
" 2>/dev/null

# If module not available, just pass
if [ $? -eq 0 ] || [ $? -eq 1 ]; then
    exit $?
else
    echo "⚠️  Second Brain not available, skipping encryption check"
    exit 0
fi
'''


def install_hook(repo_path: Optional[Path] = None, force: bool = False) -> Tuple[bool, str]:
    """Install the pre-commit hook to a git repository.
    
    Args:
        repo_path: Path to git repository (defaults to cwd)
        force: Overwrite existing hook
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if repo_path is None:
        repo_path = Path.cwd()
    
    hooks_dir = repo_path / ".git" / "hooks"
    
    if not hooks_dir.exists():
        return False, f"Not a git repository: {repo_path}"
    
    hook_path = hooks_dir / "pre-commit"
    
    if hook_path.exists() and not force:
        return False, f"Pre-commit hook already exists. Use --force to overwrite."
    
    # Write hook script
    hook_script = generate_hook_script()
    hook_path.write_text(hook_script)
    
    # Make executable
    hook_path.chmod(0o755)
    
    return True, f"✅ Pre-commit hook installed at {hook_path}"


def uninstall_hook(repo_path: Optional[Path] = None) -> Tuple[bool, str]:
    """Uninstall the pre-commit hook.
    
    Args:
        repo_path: Path to git repository (defaults to cwd)
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if repo_path is None:
        repo_path = Path.cwd()
    
    hook_path = repo_path / ".git" / "hooks" / "pre-commit"
    
    if not hook_path.exists():
        return False, "No pre-commit hook installed"
    
    # Check if it's our hook
    content = hook_path.read_text()
    if "Second Brain" not in content:
        return False, "Pre-commit hook exists but is not from Second Brain"
    
    hook_path.unlink()
    return True, "✅ Pre-commit hook removed"
