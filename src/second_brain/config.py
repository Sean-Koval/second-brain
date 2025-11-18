"""Configuration management for Second Brain.

Handles global vs local setup, environment variables, and user configuration.
"""

import json
import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration manager for Second Brain.

    Handles detection of global vs local setup and provides paths to all
    data directories.
    """

    def __init__(self, force_global: bool = False, force_local: bool = False):
        """Initialize configuration.

        Args:
            force_global: Force use of global setup (~/.second-brain/)
            force_local: Force use of local setup (./data/)
        """
        self.is_global = self._detect_global_setup(force_global, force_local)
        self.second_brain_dir = self._get_second_brain_dir(force_global, force_local)
        self.config_file = self.second_brain_dir / "config.json"
        self.user_config = self._load_user_config()

    def _detect_global_setup(self, force_global: bool, force_local: bool) -> bool:
        """Detect if we should use global or local setup.

        Priority:
        1. force_global flag
        2. force_local flag
        3. SECOND_BRAIN_DIR environment variable
        4. Existence of ~/.second-brain/ directory
        5. Default to local (for backward compatibility)
        """
        if force_global:
            return True
        if force_local:
            return False

        # Check environment variable
        if os.getenv("SECOND_BRAIN_DIR"):
            return True

        # Check if global directory exists
        global_dir = Path.home() / ".second-brain"
        if global_dir.exists() and global_dir.is_dir():
            return True

        # Default to local for backward compatibility
        return False

    def _get_second_brain_dir(self, force_global: bool, force_local: bool) -> Path:
        """Get the Second Brain home directory.

        Returns:
            Path to the Second Brain directory
        """
        if force_global:
            return Path.home() / ".second-brain"
        if force_local:
            return Path.cwd()

        # Check environment variable first
        env_dir = os.getenv("SECOND_BRAIN_DIR")
        if env_dir:
            return Path(env_dir).expanduser().resolve()

        # Check if global directory exists
        global_dir = Path.home() / ".second-brain"
        if global_dir.exists():
            return global_dir

        # Default to current directory for backward compatibility
        return Path.cwd()

    def _load_user_config(self) -> dict:
        """Load user configuration from config.json.

        Returns:
            Dictionary with user configuration or empty dict if not found
        """
        if not self.config_file.exists():
            return {}

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_user_config(self, config: dict) -> None:
        """Save user configuration to config.json.

        Args:
            config: Configuration dictionary to save
        """
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        self.user_config = config

    @property
    def data_dir(self) -> Path:
        """Get data directory path."""
        if self.is_global:
            return self.second_brain_dir / "data"
        return self.second_brain_dir / "data"

    @property
    def projects_dir(self) -> Path:
        """Get projects directory path."""
        return self.data_dir / "projects"

    @property
    def work_logs_dir(self) -> Path:
        """Get work logs directory path."""
        return self.data_dir / "work_logs"

    @property
    def transcripts_dir(self) -> Path:
        """Get transcripts directory path."""
        return self.data_dir / "transcripts"

    @property
    def transcripts_raw_dir(self) -> Path:
        """Get raw transcripts directory path."""
        return self.transcripts_dir / "raw"

    @property
    def transcripts_processed_dir(self) -> Path:
        """Get processed transcripts directory path."""
        return self.transcripts_dir / "processed"

    @property
    def db_path(self) -> Path:
        """Get database file path."""
        return self.data_dir / "index.db"

    def ensure_directories(self) -> None:
        """Create all necessary directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.work_logs_dir.mkdir(parents=True, exist_ok=True)
        self.transcripts_raw_dir.mkdir(parents=True, exist_ok=True)
        self.transcripts_processed_dir.mkdir(parents=True, exist_ok=True)

    def get_jira_config(self) -> dict:
        """Get Jira configuration from user config or environment.

        Returns:
            Dictionary with Jira configuration
        """
        jira_config = self.user_config.get("jira", {})

        # Override with environment variables if present
        return {
            "server": os.getenv("JIRA_SERVER", jira_config.get("server")),
            "email": os.getenv("JIRA_EMAIL", jira_config.get("email")),
            "api_token": os.getenv("JIRA_API_TOKEN", jira_config.get("api_token")),
            "default_project": jira_config.get("default_project"),
        }

    def get_user_info(self) -> dict:
        """Get user information from config.

        Returns:
            Dictionary with user name and email
        """
        return self.user_config.get("user", {
            "name": os.getenv("USER", "Unknown"),
            "email": "",
        })

    def initialize_global_setup(self) -> None:
        """Initialize global Second Brain setup.

        Creates directory structure and default config.json.
        """
        # Create directories
        self.ensure_directories()

        # Create default config if it doesn't exist
        if not self.config_file.exists():
            default_config = {
                "user": {
                    "name": os.getenv("USER", "User"),
                    "email": ""
                },
                "sync": {
                    "auto_push": False,
                    "auto_pull": True,
                    "remote": "origin"
                },
                "jira": {
                    "server": "",
                    "email": "",
                    "default_project": ""
                },
                "defaults": {
                    "work_log_time_tracking": True,
                    "auto_link_tasks": True
                },
                "paths": {
                    "data_dir": "data",
                    "projects_dir": "data/projects",
                    "work_logs_dir": "data/work_logs",
                    "transcripts_dir": "data/transcripts"
                }
            }
            self.save_user_config(default_config)

    def get_setup_info(self) -> str:
        """Get human-readable setup information.

        Returns:
            String describing current setup
        """
        setup_type = "Global" if self.is_global else "Local"
        location = self.second_brain_dir
        return f"{setup_type} setup at: {location}"


def get_config(force_global: bool = False, force_local: bool = False) -> Config:
    """Get configuration instance.

    Args:
        force_global: Force use of global setup
        force_local: Force use of local setup

    Returns:
        Config instance
    """
    return Config(force_global=force_global, force_local=force_local)
