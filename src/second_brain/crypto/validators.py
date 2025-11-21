"""Security validators for encryption keys.

Validates key permissions and ensures proper git configuration to prevent
accidental commits of private keys.
"""

from pathlib import Path


def ensure_keys_in_gitignore(second_brain_dir: Path) -> bool:
    """Ensure private keys are in .gitignore.

    Args:
        second_brain_dir: Second Brain root directory

    Returns:
        True if .gitignore was modified, False if entries already exist
    """
    gitignore_path = second_brain_dir / ".gitignore"

    required_entries = [
        "",  # Blank line
        "# Private encryption keys (NEVER COMMIT)",
        "keys/private_key.pem",
        "keys/*.key",
        "keys/*_private*",
        "*.pem.backup",
    ]

    # Read existing gitignore
    if gitignore_path.exists():
        content = gitignore_path.read_text()
    else:
        content = ""

    # Check if entries already exist
    if "keys/private_key.pem" in content:
        return False  # Already protected

    # Add entries
    content += "\n".join(required_entries) + "\n"
    gitignore_path.write_text(content)

    return True  # Modified
