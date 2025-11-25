"""Git hooks for Second Brain.

Provides pre-commit validation and other git hook functionality.
"""

from .pre_commit import main as pre_commit_main

__all__ = ["pre_commit_main"]
