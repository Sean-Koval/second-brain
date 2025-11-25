# SB-7: Pre-commit Hook for Encryption Validation

## Overview
Implement a git pre-commit hook that automatically validates sensitive data is encrypted before allowing commits to the Second Brain repository. This prevents accidental exposure of sensitive information.

## Goals
1. Detect unencrypted sensitive data in staged files
2. Validate encrypted content is properly formatted
3. Ensure private keys are gitignored
4. Provide helpful feedback and remediation suggestions
5. Be performant and non-intrusive

## Architecture

### Hook Location
```
~/.second-brain/.git/hooks/pre-commit
```

### Components

#### 1. Hook Script (`hooks/pre-commit`)
- Python script using Second Brain modules
- Executable git hook
- Exit 0 = allow commit, Exit 1 = block commit

#### 2. Validation Module (`src/second_brain/validation/sensitive_data.py`)
- Reusable validation logic
- Pattern detection
- Encryption verification
- Report generation

#### 3. CLI Installation Command (`sb install-hooks`)
- Install/update hook
- Verify hook permissions
- Show installation status

## Detection Strategy

### Sensitive Data Patterns

#### High-Confidence Patterns (Always Block)
```python
HIGH_CONFIDENCE_PATTERNS = [
    r'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY',  # Private keys
    r'api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',  # API keys
    r'password\s*[=:]\s*["\']?[^"\'\s]{8,}',  # Passwords
    r'secret[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',  # Secret keys
    r'aws[_-]?secret[_-]?access[_-]?key',  # AWS secrets
    r'private[_-]?key[_-]?id',  # Private key IDs
    r'token\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',  # Tokens
]
```

#### Medium-Confidence Patterns (Warn)
```python
MEDIUM_CONFIDENCE_PATTERNS = [
    r'SENSITIVE:',  # Custom marker
    r'TODO:.*encrypt',  # TODO encrypt markers
    r'FIXME:.*encrypt',  # FIXME encrypt markers
    r'XXX.*sensitive',  # XXX sensitive markers
]
```

#### Markdown Frontmatter Markers
```python
# Check frontmatter
if metadata.get('is_sensitive') == True:
    # Must have encrypted blocks
    if '<!-- ENCRYPTED:' not in content:
        return FAIL
```

### Files to Scan

**Include:**
- `data/notes/*.md`
- `data/work_logs/*.md`
- `data/projects/*.md`
- `config.json` (for sensitive config)
- Any markdown file with `is_sensitive: true` in frontmatter

**Exclude:**
- `keys/*` (should be gitignored anyway)
- `.beads/*` (issue tracking, no sensitive data)
- `data/transcripts/*` (already separate)
- Encrypted blocks themselves

## Validation Rules

### Rule 1: Private Keys Must Be Gitignored
```python
def validate_private_keys_ignored(staged_files):
    """Ensure no private keys are staged."""
    dangerous_patterns = [
        'keys/private_key.pem',
        'keys/*.key',
        '*.pem.backup',
    ]
    for file in staged_files:
        for pattern in dangerous_patterns:
            if fnmatch(file, pattern):
                return ValidationError(
                    f"Private key file staged: {file}",
                    remedy="Ensure keys/* is in .gitignore"
                )
    return PASS
```

### Rule 2: Sensitive Markers Must Be Encrypted
```python
def validate_sensitive_content(file_path, content):
    """Check for unencrypted sensitive patterns."""
    # Skip already encrypted blocks
    encrypted_blocks = extract_encrypted_blocks(content)
    content_without_encrypted = remove_encrypted_blocks(content)

    violations = []
    for pattern in HIGH_CONFIDENCE_PATTERNS:
        matches = re.finditer(pattern, content_without_encrypted, re.I)
        for match in matches:
            violations.append({
                'pattern': pattern,
                'match': match.group(),
                'line': get_line_number(content, match.start()),
                'file': file_path
            })

    return violations
```

### Rule 3: Marked-Sensitive Files Must Have Encryption
```python
def validate_frontmatter_encryption(file_path):
    """Verify files marked as sensitive are encrypted."""
    with open(file_path) as f:
        post = frontmatter.load(f)

    if post.metadata.get('is_sensitive') or post.metadata.get('encrypted'):
        if '<!-- ENCRYPTED:' not in post.content:
            return ValidationError(
                f"File marked as sensitive but no encrypted content: {file_path}",
                remedy=f"sb mark-sensitive --note-id {get_note_id(file_path)}"
            )
    return PASS
```

### Rule 4: Valid Encryption Format
```python
def validate_encryption_format(encrypted_blocks):
    """Verify encrypted blocks are valid."""
    encryptor = Encryptor(KeyManager(keys_dir))

    for block_text, encrypted_data in encrypted_blocks:
        # Check format
        if not encrypted_data.startswith('v1:RSA-AES256-GCM:'):
            return ValidationError(
                f"Invalid encryption format: {encrypted_data[:50]}...",
                remedy="Re-encrypt with current version"
            )

        # Verify structure (don't decrypt, just parse)
        parts = encrypted_data.split(':')
        if len(parts) != 5:
            return ValidationError(
                f"Malformed encrypted data: {encrypted_data[:50]}...",
                remedy="Re-encrypt content"
            )

    return PASS
```

## Implementation

### File Structure
```
src/second_brain/
├── validation/
│   ├── __init__.py
│   ├── sensitive_data.py      # Core validation logic
│   └── patterns.py             # Pattern definitions
├── hooks/
│   └── pre_commit.py           # Hook entry point
└── cli.py                      # Add 'sb install-hooks' command
```

### Hook Script Template
```python
#!/usr/bin/env python3
"""Pre-commit hook for Second Brain encryption validation."""

import sys
import os
from pathlib import Path

# Add Second Brain to path
sys.path.insert(0, str(Path.home() / '.second-brain'))

def main():
    """Run pre-commit validations."""
    from second_brain.validation.sensitive_data import SensitiveDataValidator
    from second_brain.config import get_app_config

    config = get_app_config()
    validator = SensitiveDataValidator(config)

    # Get staged files
    staged_files = get_staged_files()

    # Run validation
    result = validator.validate(staged_files)

    if result.has_errors():
        print("❌ Commit blocked: Sensitive data validation failed\n")
        result.print_report()
        print("\nTo bypass (NOT recommended): git commit --no-verify")
        return 1

    if result.has_warnings():
        print("⚠️  Warnings detected:\n")
        result.print_warnings()
        print()

    return 0

def get_staged_files():
    """Get list of staged files."""
    import subprocess
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
        capture_output=True,
        text=True
    )
    return [f for f in result.stdout.strip().split('\n') if f]

if __name__ == '__main__':
    sys.exit(main())
```

### Validation Module
```python
# src/second_brain/validation/sensitive_data.py

from pathlib import Path
from typing import List, Optional
import re
import frontmatter
from dataclasses import dataclass

from ..crypto import Encryptor, KeyManager
from .patterns import HIGH_CONFIDENCE_PATTERNS, MEDIUM_CONFIDENCE_PATTERNS


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    severity: str  # 'error' or 'warning'
    file: str
    line: Optional[int]
    message: str
    remedy: str
    pattern: Optional[str] = None


class ValidationResult:
    """Results of validation."""

    def __init__(self):
        self.errors: List[ValidationIssue] = []
        self.warnings: List[ValidationIssue] = []

    def add_error(self, issue: ValidationIssue):
        self.errors.append(issue)

    def add_warning(self, issue: ValidationIssue):
        self.warnings.append(issue)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def print_report(self):
        """Print formatted report."""
        for error in self.errors:
            print(f"  ❌ {error.file}:{error.line or '?'}")
            print(f"     {error.message}")
            print(f"     💡 {error.remedy}\n")

    def print_warnings(self):
        """Print warnings."""
        for warning in self.warnings:
            print(f"  ⚠️  {warning.file}:{warning.line or '?'}")
            print(f"     {warning.message}\n")


class SensitiveDataValidator:
    """Validates sensitive data is encrypted."""

    def __init__(self, config):
        self.config = config
        self.data_dir = Path(config.data_dir)
        self.keys_dir = Path(config.second_brain_dir) / 'keys'

    def validate(self, staged_files: List[str]) -> ValidationResult:
        """Run all validations on staged files."""
        result = ValidationResult()

        # Filter to only Second Brain data files
        sb_files = [f for f in staged_files if self._is_data_file(f)]

        # Check for private keys
        self._validate_no_private_keys(staged_files, result)

        # Validate each file
        for file_path in sb_files:
            self._validate_file(file_path, result)

        return result

    def _is_data_file(self, file_path: str) -> bool:
        """Check if file is a Second Brain data file."""
        return any([
            file_path.startswith('data/notes/'),
            file_path.startswith('data/work_logs/'),
            file_path.startswith('data/projects/'),
            file_path == 'config.json',
        ])

    def _validate_no_private_keys(self, files: List[str], result: ValidationResult):
        """Ensure no private keys are staged."""
        dangerous_patterns = [
            'keys/private_key.pem',
            'keys/*.key',
            '*.pem.backup',
        ]

        for file in files:
            for pattern in dangerous_patterns:
                if self._matches_pattern(file, pattern):
                    result.add_error(ValidationIssue(
                        severity='error',
                        file=file,
                        line=None,
                        message='Private key file should not be committed',
                        remedy='Ensure this file is in .gitignore'
                    ))

    def _validate_file(self, file_path: str, result: ValidationResult):
        """Validate a single file."""
        full_path = self.data_dir / file_path

        if not full_path.exists():
            return

        # Read file
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter if markdown
        if file_path.endswith('.md'):
            try:
                post = frontmatter.loads(content)
                metadata = post.metadata
                body = post.content
            except:
                metadata = {}
                body = content
        else:
            metadata = {}
            body = content

        # Rule 1: Files marked sensitive must have encryption
        if metadata.get('is_sensitive') or metadata.get('encrypted'):
            if '<!-- ENCRYPTED:' not in body:
                # Get note/log ID from metadata or filename
                note_id = metadata.get('id')
                remedy = f"Run: sb mark-sensitive --note-id {note_id}" if note_id else "Encrypt sensitive content"

                result.add_error(ValidationIssue(
                    severity='error',
                    file=file_path,
                    line=None,
                    message='File marked as sensitive but contains no encrypted blocks',
                    remedy=remedy
                ))

        # Rule 2: Scan for sensitive patterns (excluding encrypted blocks)
        content_to_scan = self._remove_encrypted_blocks(body)
        self._scan_for_patterns(file_path, content_to_scan, result)

    def _remove_encrypted_blocks(self, content: str) -> str:
        """Remove encrypted blocks from content for scanning."""
        pattern = r'<!-- ENCRYPTED:.+? -->.*?<!-- END ENCRYPTED -->'
        return re.sub(pattern, '', content, flags=re.DOTALL)

    def _scan_for_patterns(self, file_path: str, content: str, result: ValidationResult):
        """Scan content for sensitive patterns."""
        lines = content.split('\n')

        # High confidence patterns (errors)
        for pattern_str in HIGH_CONFIDENCE_PATTERNS:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            for i, line in enumerate(lines, 1):
                match = pattern.search(line)
                if match:
                    result.add_error(ValidationIssue(
                        severity='error',
                        file=file_path,
                        line=i,
                        message=f'Unencrypted sensitive data detected: {match.group()[:50]}...',
                        remedy='Encrypt this content or remove sensitive data',
                        pattern=pattern_str
                    ))

        # Medium confidence patterns (warnings)
        for pattern_str in MEDIUM_CONFIDENCE_PATTERNS:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            for i, line in enumerate(lines, 1):
                match = pattern.search(line):
                if match:
                    result.add_warning(ValidationIssue(
                        severity='warning',
                        file=file_path,
                        line=i,
                        message=f'Possible sensitive content marker: {match.group()}',
                        remedy='Review and encrypt if needed'
                    ))

    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches glob pattern."""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
```

### Pattern Definitions
```python
# src/second_brain/validation/patterns.py

# High-confidence sensitive data patterns
HIGH_CONFIDENCE_PATTERNS = [
    r'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY',
    r'api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
    r'password\s*[=:]\s*["\']?[^"\'\s]{8,}',
    r'secret[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
    r'aws[_-]?secret[_-]?access[_-]?key',
    r'private[_-]?key[_-]?id',
    r'token\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
    r'client[_-]?secret\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
]

# Medium-confidence patterns (warnings)
MEDIUM_CONFIDENCE_PATTERNS = [
    r'SENSITIVE:',
    r'TODO:.*encrypt',
    r'FIXME:.*encrypt',
    r'XXX.*sensitive',
    r'@sensitive',
]
```

### CLI Installation Command
```python
# In cli.py, add:

@cli.command("install-hooks")
def install_hooks():
    """Install git hooks for Second Brain."""
    from pathlib import Path
    import shutil
    import stat

    config = get_app_config()
    git_dir = config.second_brain_dir / '.git'

    if not git_dir.exists():
        console.print("[red]✗ Not a git repository[/red]")
        console.print(f"\nRun 'git init' in {config.second_brain_dir}")
        return

    hooks_dir = git_dir / 'hooks'
    hooks_dir.mkdir(exist_ok=True)

    # Get hook template from package
    from . import hooks
    hook_template_path = Path(hooks.__file__).parent / 'pre_commit.py'

    # Install pre-commit hook
    pre_commit_hook = hooks_dir / 'pre-commit'

    # Write hook
    with open(pre_commit_hook, 'w') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write(hook_template_path.read_text())

    # Make executable
    pre_commit_hook.chmod(pre_commit_hook.stat().st_mode | stat.S_IEXEC)

    console.print("[green]✓ Pre-commit hook installed![/green]")
    console.print(f"\nLocation: {pre_commit_hook}")
    console.print("\nThis hook will validate:")
    console.print("  • No unencrypted sensitive data")
    console.print("  • No private keys committed")
    console.print("  • Proper encryption format")
    console.print("\nBypass (not recommended): git commit --no-verify")
```

## Task Breakdown

### Task 1: Create Validation Module
- File: `src/second_brain/validation/sensitive_data.py`
- Create `SensitiveDataValidator` class
- Implement pattern detection
- Create `ValidationResult` and `ValidationIssue` classes

### Task 2: Define Sensitive Patterns
- File: `src/second_brain/validation/patterns.py`
- Define high-confidence patterns
- Define medium-confidence patterns
- Document each pattern

### Task 3: Create Pre-commit Hook Script
- File: `src/second_brain/hooks/pre_commit.py`
- Hook entry point
- Git integration (get staged files)
- Call validator
- Format output

### Task 4: Add CLI Installation Command
- File: `src/second_brain/cli.py`
- `sb install-hooks` command
- Copy hook to `.git/hooks/`
- Set executable permissions
- Verify installation

### Task 5: Testing
- Test with unencrypted sensitive data (should block)
- Test with encrypted content (should pass)
- Test with private keys (should block)
- Test with warnings (should warn but allow)
- Test bypass with `--no-verify`

### Task 6: Documentation
- Update docs/encryption.md
- Add hook installation to docs/installation.md
- Add troubleshooting guide
- Update README

## Success Criteria
- [ ] Hook blocks commits with unencrypted API keys/passwords
- [ ] Hook allows commits with properly encrypted content
- [ ] Hook blocks private key files
- [ ] Hook validates encrypted block format
- [ ] `sb install-hooks` installs working hook
- [ ] Clear, actionable error messages
- [ ] Performance: < 1 second for typical commit
- [ ] Can bypass with `git commit --no-verify`
- [ ] Documentation complete

## Performance Considerations
- Only scan staged files (not entire repo)
- Skip large binary files
- Cache regex compilation
- Limit pattern matching to relevant files
- Target: < 1 second for typical 5-10 file commit

## User Experience
**Good:**
```
❌ Commit blocked: Sensitive data validation failed

  ❌ data/notes/note-3.md:15
     Unencrypted sensitive data detected: api_key = "sk-1234567890abcdef"
     💡 Run: sb mark-sensitive --note-id 3

To bypass (NOT recommended): git commit --no-verify
```

**Better:**
```
✓ All staged files validated
  No sensitive data issues detected
```

## Future Enhancements
- Custom pattern configuration in config.json
- Integration with secret scanning tools (gitleaks, trufflehog)
- Automatic suggestions for which files to encrypt
- GitHub Actions integration
- Pre-push hook variant
