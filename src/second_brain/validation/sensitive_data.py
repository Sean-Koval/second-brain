"""Sensitive data validation for Second Brain.

Validates that sensitive data is properly encrypted before commits.
"""

from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
import re
import frontmatter

from .patterns import (
    HIGH_CONFIDENCE_PATTERNS,
    MEDIUM_CONFIDENCE_PATTERNS,
    should_scan_file,
    is_dangerous_file,
)


@dataclass
class ValidationIssue:
    """Represents a validation issue found during scanning.

    Attributes:
        severity: 'error' or 'warning'
        file: Path to the file with the issue
        line: Line number where issue was found (optional)
        message: Description of the issue
        remedy: Suggested remediation
        pattern: The pattern that matched (optional)
    """

    severity: str  # 'error' or 'warning'
    file: str
    message: str
    remedy: str
    line: Optional[int] = None
    pattern: Optional[str] = None


@dataclass
class ValidationResult:
    """Results of validation scan.

    Contains all errors and warnings found during validation.
    """

    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)

    def add_error(self, issue: ValidationIssue) -> None:
        """Add an error to the results."""
        self.errors.append(issue)

    def add_warning(self, issue: ValidationIssue) -> None:
        """Add a warning to the results."""
        self.warnings.append(issue)

    def has_errors(self) -> bool:
        """Check if any errors were found."""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """Check if any warnings were found."""
        return len(self.warnings) > 0

    def print_report(self) -> None:
        """Print formatted error report."""
        for error in self.errors:
            location = f"{error.file}:{error.line}" if error.line else error.file
            print(f"  ❌ {location}")
            print(f"     {error.message}")
            print(f"     💡 {error.remedy}\n")

    def print_warnings(self) -> None:
        """Print formatted warning report."""
        for warning in self.warnings:
            location = f"{warning.file}:{warning.line}" if warning.line else warning.file
            print(f"  ⚠️  {location}")
            print(f"     {warning.message}")
            if warning.remedy:
                print(f"     💡 {warning.remedy}")
            print()


class SensitiveDataValidator:
    """Validates that sensitive data is properly encrypted.

    Scans files for sensitive data patterns and ensures compliance
    with encryption requirements.
    """

    def __init__(self, config):
        """Initialize validator with configuration.

        Args:
            config: Application configuration object
        """
        self.config = config
        self.data_dir = Path(config.data_dir)
        self.second_brain_dir = Path(config.second_brain_dir)

    def validate(self, staged_files: List[str]) -> ValidationResult:
        """Run all validations on staged files.

        Args:
            staged_files: List of file paths staged for commit

        Returns:
            ValidationResult with errors and warnings
        """
        result = ValidationResult()

        # Check for dangerous files (private keys, etc.)
        self._validate_no_dangerous_files(staged_files, result)

        # Filter to only data files we should scan
        scannable_files = [f for f in staged_files if self._should_validate_file(f)]

        # Validate each file
        for file_path in scannable_files:
            self._validate_file(file_path, result)

        return result

    def _should_validate_file(self, file_path: str) -> bool:
        """Check if file should be validated.

        Args:
            file_path: Path to the file

        Returns:
            True if file should be scanned for sensitive data
        """
        # Check if it's a Second Brain data file
        is_data_file = any([
            file_path.startswith('data/notes/'),
            file_path.startswith('data/work_logs/'),
            file_path.startswith('data/projects/'),
            file_path == 'config.json',
        ])

        # Check if file type is scannable
        is_scannable = should_scan_file(file_path)

        return is_data_file and is_scannable

    def _validate_no_dangerous_files(
        self, files: List[str], result: ValidationResult
    ) -> None:
        """Ensure no dangerous files (like private keys) are staged.

        Args:
            files: List of staged files
            result: ValidationResult to add issues to
        """
        for file in files:
            if is_dangerous_file(file):
                result.add_error(
                    ValidationIssue(
                        severity='error',
                        file=file,
                        message='Private key or sensitive file should not be committed',
                        remedy='Ensure this file is in .gitignore and remove from staging',
                    )
                )

    def _validate_file(self, file_path: str, result: ValidationResult) -> None:
        """Validate a single file for sensitive data.

        Args:
            file_path: Path to the file (relative to repo root)
            result: ValidationResult to add issues to
        """
        # Construct full path
        if file_path.startswith('data/'):
            full_path = self.data_dir.parent / file_path
        else:
            full_path = self.second_brain_dir / file_path

        if not full_path.exists():
            return

        # Read file content
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            # Skip binary or unreadable files
            return

        # Parse frontmatter if markdown
        metadata = {}
        body = content

        if file_path.endswith('.md'):
            try:
                post = frontmatter.loads(content)
                metadata = post.metadata
                body = post.content
            except Exception:
                # If frontmatter parsing fails, treat as plain text
                pass

        # Validate frontmatter requirements
        self._validate_frontmatter(file_path, metadata, body, result)

        # Scan for sensitive patterns (excluding encrypted blocks)
        content_to_scan = self._remove_encrypted_blocks(body)
        self._scan_for_patterns(file_path, content_to_scan, result)

    def _validate_frontmatter(
        self, file_path: str, metadata: dict, body: str, result: ValidationResult
    ) -> None:
        """Validate that files marked as sensitive have encrypted content.

        Args:
            file_path: Path to the file
            metadata: Frontmatter metadata
            body: File body content
            result: ValidationResult to add issues to
        """
        is_sensitive = metadata.get('is_sensitive', False)
        is_encrypted = metadata.get('encrypted', False)

        if is_sensitive or is_encrypted:
            # File is marked as sensitive, must have encrypted blocks
            if '<!-- ENCRYPTED:' not in body:
                # Try to extract note ID from metadata
                note_id = metadata.get('id')
                if note_id:
                    remedy = f"Run: sb mark-sensitive --note-id {note_id}"
                else:
                    remedy = "Encrypt the sensitive content or remove the sensitive flag"

                result.add_error(
                    ValidationIssue(
                        severity='error',
                        file=file_path,
                        message='File marked as sensitive but contains no encrypted blocks',
                        remedy=remedy,
                    )
                )

    def _remove_encrypted_blocks(self, content: str) -> str:
        """Remove encrypted blocks from content before scanning.

        This ensures we don't flag encrypted data as sensitive.

        Args:
            content: File content

        Returns:
            Content with encrypted blocks removed
        """
        # Pattern to match encrypted blocks
        pattern = r'<!-- ENCRYPTED:.+? -->.*?<!-- END ENCRYPTED -->'
        return re.sub(pattern, '', content, flags=re.DOTALL)

    def _scan_for_patterns(
        self, file_path: str, content: str, result: ValidationResult
    ) -> None:
        """Scan content for sensitive data patterns.

        Args:
            file_path: Path to the file
            content: Content to scan (with encrypted blocks removed)
            result: ValidationResult to add issues to
        """
        lines = content.split('\n')

        # Scan for high-confidence patterns (errors)
        for pattern_str in HIGH_CONFIDENCE_PATTERNS:
            try:
                pattern = re.compile(pattern_str, re.IGNORECASE)
            except re.error:
                # Skip invalid patterns
                continue

            for line_num, line in enumerate(lines, 1):
                match = pattern.search(line)
                if match:
                    # Extract matched text, truncate if too long
                    matched_text = match.group()
                    if len(matched_text) > 50:
                        matched_text = matched_text[:50] + '...'

                    result.add_error(
                        ValidationIssue(
                            severity='error',
                            file=file_path,
                            line=line_num,
                            message=f'Unencrypted sensitive data detected: {matched_text}',
                            remedy='Encrypt this content or remove the sensitive data',
                            pattern=pattern_str,
                        )
                    )

        # Scan for medium-confidence patterns (warnings)
        for pattern_str in MEDIUM_CONFIDENCE_PATTERNS:
            try:
                pattern = re.compile(pattern_str, re.IGNORECASE)
            except re.error:
                continue

            for line_num, line in enumerate(lines, 1):
                match = pattern.search(line)
                if match:
                    matched_text = match.group()
                    if len(matched_text) > 50:
                        matched_text = matched_text[:50] + '...'

                    result.add_warning(
                        ValidationIssue(
                            severity='warning',
                            file=file_path,
                            line=line_num,
                            message=f'Possible sensitive content marker: {matched_text}',
                            remedy='Review and encrypt if needed',
                        )
                    )
