#!/usr/bin/env python3
"""Pre-commit hook for Second Brain encryption validation.

This hook validates that sensitive data is properly encrypted before allowing commits.
Designed to run in the user's ~/.second-brain/ repository.

Exit codes:
    0 - Validation passed, allow commit
    1 - Validation failed, block commit
"""

import sys
import subprocess
from pathlib import Path
from typing import List


def get_staged_files() -> List[str]:
    """Get list of files staged for commit.

    Returns:
        List of file paths relative to repo root
    """
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f]
        return files
    except subprocess.CalledProcessError:
        # If git command fails, allow commit (fail open)
        return []


def print_header():
    """Print validation header."""
    print("\n" + "=" * 60)
    print("🔒 Second Brain - Sensitive Data Validation")
    print("=" * 60 + "\n")


def print_success():
    """Print success message."""
    print("✅ Validation passed - No sensitive data issues detected\n")


def print_bypass_hint():
    """Print hint about bypassing validation."""
    print("\n💡 To bypass this check (NOT recommended):")
    print("   git commit --no-verify\n")


def main() -> int:
    """Run pre-commit validation.

    Returns:
        0 if validation passes, 1 if validation fails
    """
    try:
        # Import Second Brain modules
        from second_brain.config import Config
        from second_brain.validation import SensitiveDataValidator

        # Print header
        print_header()

        # Get configuration
        config = Config()

        # Check if this is a Second Brain repository
        if not config.second_brain_dir.exists():
            print("⚠️  Not a Second Brain repository, skipping validation\n")
            return 0

        # Get staged files
        staged_files = get_staged_files()

        if not staged_files:
            print("ℹ️  No files staged for commit\n")
            return 0

        print(f"📋 Scanning {len(staged_files)} staged file(s)...\n")

        # Create validator
        validator = SensitiveDataValidator(config)

        # Run validation
        result = validator.validate(staged_files)

        # Check for errors
        if result.has_errors():
            print("❌ Commit blocked: Sensitive data validation failed\n")
            result.print_report()
            print_bypass_hint()
            return 1

        # Check for warnings
        if result.has_warnings():
            print("⚠️  Warnings detected:\n")
            result.print_warnings()
            print("💡 Review these warnings before committing\n")
            # Warnings don't block the commit, just inform

        # Success
        print_success()
        return 0

    except ImportError as e:
        print(f"⚠️  Could not import Second Brain modules: {e}")
        print("   Allowing commit to proceed\n")
        return 0

    except Exception as e:
        print(f"⚠️  Error during validation: {e}")
        print("   Allowing commit to proceed\n")
        # Fail open - don't block commits on unexpected errors
        return 0


if __name__ == '__main__':
    sys.exit(main())
