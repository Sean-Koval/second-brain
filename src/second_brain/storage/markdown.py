"""Markdown file operations with frontmatter support."""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import frontmatter


class MarkdownStorage:
    """Handle markdown file operations."""

    def __init__(self, base_path: str = "data"):
        """Initialize with base data path."""
        self.base_path = Path(base_path)
        self.projects_path = self.base_path / "projects"
        self.work_logs_path = self.base_path / "work_logs"
        self.notes_path = self.base_path / "notes"
        self.transcripts_path = self.base_path / "transcripts"

        # Ensure directories exist
        self.projects_path.mkdir(parents=True, exist_ok=True)
        self.work_logs_path.mkdir(parents=True, exist_ok=True)
        self.notes_path.mkdir(parents=True, exist_ok=True)
        self.transcripts_path.mkdir(parents=True, exist_ok=True)

    def slugify(self, text: str) -> str:
        """Convert text to slug format."""
        return text.lower().replace(" ", "-").replace("_", "-")

    # Project operations
    def create_project_file(
        self,
        name: str,
        slug: str,
        description: Optional[str] = None,
        jira_project_key: Optional[str] = None,
        tags: Optional[list] = None,
    ) -> str:
        """Create a project markdown file."""
        filepath = self.projects_path / f"{slug}.md"

        metadata = {
            "name": name,
            "slug": slug,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        if description:
            metadata["description"] = description
        if jira_project_key:
            metadata["jira_project_key"] = jira_project_key
        if tags:
            metadata["tags"] = tags

        content = f"""# {name}

## Overview

{description or 'No description provided.'}

## Tasks

<!-- Tasks will be listed here -->

## Notes

<!-- Add project notes here -->
"""

        post = frontmatter.Post(content, **metadata)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return str(filepath)

    def read_project_file(self, slug: str) -> Optional[Dict[str, Any]]:
        """Read a project markdown file."""
        filepath = self.projects_path / f"{slug}.md"
        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        return {
            "metadata": post.metadata,
            "content": post.content,
            "filepath": str(filepath),
        }

    def update_project_file(self, slug: str, metadata: Dict[str, Any], content: str) -> bool:
        """Update a project markdown file."""
        filepath = self.projects_path / f"{slug}.md"
        if not filepath.exists():
            return False

        metadata["updated_at"] = datetime.utcnow().isoformat()
        post = frontmatter.Post(content, **metadata)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return True

    # Work log operations
    def create_work_log_file(self, date: datetime) -> str:
        """Create a work log markdown file for a specific date."""
        date_str = date.strftime("%Y-%m-%d")
        filepath = self.work_logs_path / f"{date_str}.md"

        metadata = {
            "date": date.isoformat(),
            "created_at": datetime.utcnow().isoformat(),
        }

        content = f"""# Work Log - {date_str}

## Summary

<!-- Daily summary -->

## Work Done

<!-- List work entries -->

## Notes

<!-- Additional notes -->
"""

        post = frontmatter.Post(content, **metadata)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return str(filepath)

    def read_work_log_file(self, date: datetime) -> Optional[Dict[str, Any]]:
        """Read a work log markdown file."""
        date_str = date.strftime("%Y-%m-%d")
        filepath = self.work_logs_path / f"{date_str}.md"

        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        return {
            "metadata": post.metadata,
            "content": post.content,
            "filepath": str(filepath),
        }

    def append_to_work_log(
        self, date: datetime, entry: str, task_ref: Optional[str] = None
    ) -> bool:
        """Append an entry to a work log file."""
        date_str = date.strftime("%Y-%m-%d")
        filepath = self.work_logs_path / f"{date_str}.md"

        # Create file if it doesn't exist
        if not filepath.exists():
            self.create_work_log_file(date)

        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Add entry to content
        timestamp = datetime.now().strftime("%H:%M")
        task_link = f" [{task_ref}]" if task_ref else ""
        new_entry = f"\n- **{timestamp}**{task_link}: {entry}"

        # Find "## Work Done" section and append
        content_lines = post.content.split("\n")
        work_done_idx = -1
        for i, line in enumerate(content_lines):
            if line.strip() == "## Work Done":
                work_done_idx = i
                break

        if work_done_idx >= 0:
            # Insert after the "## Work Done" header and any comments
            insert_idx = work_done_idx + 1
            while insert_idx < len(content_lines) and content_lines[insert_idx].strip().startswith(
                "<!--"
            ):
                insert_idx += 1
            content_lines.insert(insert_idx + 1, new_entry)
        else:
            # Append to end if section not found
            content_lines.append(new_entry)

        post.content = "\n".join(content_lines)
        post.metadata["updated_at"] = datetime.utcnow().isoformat()

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return True

    # Note operations
    def create_note_file(
        self,
        note_id: int,
        title: str,
        content: str,
        project_id: Optional[int] = None,
        task_id: Optional[int] = None,
        tags: Optional[list] = None,
    ) -> str:
        """Create a note markdown file."""
        filepath = self.notes_path / f"note-{note_id}.md"

        metadata = {
            "id": note_id,
            "title": title,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        if project_id is not None:
            metadata["project_id"] = project_id
        if task_id is not None:
            metadata["task_id"] = task_id
        if tags:
            metadata["tags"] = tags

        # Wrap content with title
        full_content = f"""# {title}

{content}
"""

        post = frontmatter.Post(full_content, **metadata)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return str(filepath)

    def read_note_file(self, note_id: int) -> Optional[Dict[str, Any]]:
        """Read a note markdown file."""
        filepath = self.notes_path / f"note-{note_id}.md"
        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        return {
            "metadata": post.metadata,
            "content": post.content,
            "filepath": str(filepath),
        }

    def update_note_file(
        self,
        note_id: int,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update a note markdown file."""
        filepath = self.notes_path / f"note-{note_id}.md"
        if not filepath.exists():
            return False

        # Read existing metadata
        with open(filepath, "r", encoding="utf-8") as f:
            existing_post = frontmatter.load(f)

        # Merge metadata
        updated_metadata = existing_post.metadata.copy()
        if metadata:
            updated_metadata.update(metadata)
        updated_metadata["title"] = title
        updated_metadata["updated_at"] = datetime.utcnow().isoformat()

        # Wrap content with title
        full_content = f"""# {title}

{content}
"""

        post = frontmatter.Post(full_content, **updated_metadata)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return True

    def append_to_note(self, note_id: int, additional_content: str) -> bool:
        """Append content to an existing note."""
        filepath = self.notes_path / f"note-{note_id}.md"
        if not filepath.exists():
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Add timestamp separator
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        separator = f"\n\n---\n\n**Added {timestamp}:**\n\n"

        post.content = post.content + separator + additional_content
        post.metadata["updated_at"] = datetime.utcnow().isoformat()

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return True

    def list_note_files(self) -> list[Dict[str, Any]]:
        """List all note markdown files."""
        notes = []
        for filepath in self.notes_path.glob("note-*.md"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)
                notes.append({
                    "metadata": post.metadata,
                    "filepath": str(filepath),
                })
            except Exception:
                # Skip files that can't be read
                continue
        return notes

    # Transcript operations
    def create_transcript_file(
        self,
        title: str,
        transcript_date: datetime,
        raw_content: str,
        transcript_type: str = "call",
        tags: Optional[list] = None,
    ) -> tuple[str, str]:
        """Create transcript files (raw and processed)."""
        # Create slug from title and date
        date_str = transcript_date.strftime("%Y-%m-%d")
        slug = self.slugify(title)
        filename_base = f"{date_str}_{slug}"

        raw_filepath = self.transcripts_path / "raw" / f"{filename_base}.txt"
        processed_filepath = self.transcripts_path / "processed" / f"{filename_base}.md"

        # Ensure subdirectories exist
        raw_filepath.parent.mkdir(parents=True, exist_ok=True)
        processed_filepath.parent.mkdir(parents=True, exist_ok=True)

        # Save raw transcript
        with open(raw_filepath, "w", encoding="utf-8") as f:
            f.write(raw_content)

        # Create processed markdown template
        metadata = {
            "title": title,
            "type": transcript_type,
            "date": transcript_date.isoformat(),
            "raw_file": str(raw_filepath),
            "created_at": datetime.utcnow().isoformat(),
        }

        if tags:
            metadata["tags"] = tags

        content = f"""# {title}

**Date:** {date_str}
**Type:** {transcript_type}

## Summary

<!-- AI-generated or manual summary -->

## Key Points

<!-- Main discussion points -->

## Action Items

<!-- Tasks and follow-ups -->

## Linked Projects

<!-- Related projects -->

## Full Transcript

See raw file: `{raw_filepath.name}`
"""

        post = frontmatter.Post(content, **metadata)
        with open(processed_filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return str(raw_filepath), str(processed_filepath)

    def read_transcript_file(self, processed_path: str) -> Optional[Dict[str, Any]]:
        """Read a processed transcript markdown file."""
        filepath = Path(processed_path)
        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Also read raw transcript if referenced
        raw_content = None
        if "raw_file" in post.metadata:
            raw_path = Path(post.metadata["raw_file"])
            if raw_path.exists():
                with open(raw_path, "r", encoding="utf-8") as rf:
                    raw_content = rf.read()

        return {
            "metadata": post.metadata,
            "content": post.content,
            "raw_content": raw_content,
            "filepath": str(filepath),
        }

    def update_transcript_file(
        self, processed_path: str, metadata: Dict[str, Any], content: str
    ) -> bool:
        """Update a processed transcript markdown file."""
        filepath = Path(processed_path)
        if not filepath.exists():
            return False

        metadata["updated_at"] = datetime.utcnow().isoformat()
        post = frontmatter.Post(content, **metadata)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return True
