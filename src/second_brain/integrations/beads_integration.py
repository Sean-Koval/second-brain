"""Integration with Beads issue tracker for epic and dependency management.

This module wraps the beads-mcp client to provide Second Brain with advanced
epic/issue management and dependency tracking capabilities.
"""

import os
from typing import List, Optional
from pathlib import Path

try:
    from beads_mcp.bd_client import BdClient, BdError, BdNotFoundError
    from beads_mcp.models import (
        Issue,
        CreateIssueParams,
        UpdateIssueParams,
        CloseIssueParams,
        AddDependencyParams,
        ReadyWorkParams,
        ListIssuesParams,
        ShowIssueParams,
        Stats,
        IssueStatus,
        IssueType,
        DependencyType,
    )
    BEADS_AVAILABLE = True
except ImportError:
    BEADS_AVAILABLE = False
    # Create stub classes for type hints
    class Issue:
        pass
    class BdError(Exception):
        pass


class BeadsIntegration:
    """Wrapper around Beads CLI for epic and dependency management."""

    def __init__(self, project_dir: Optional[str] = None):
        """Initialize Beads integration.

        Args:
            project_dir: Directory where .beads database lives (auto-detected if None)
        """
        if not BEADS_AVAILABLE:
            raise ImportError(
                "beads-mcp is not installed. Install with: uv pip install beads-mcp"
            )

        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self.client = BdClient()

    async def is_available(self) -> bool:
        """Check if bd CLI is available."""
        try:
            # Try to run a simple command
            await self.client.stats()
            return True
        except (BdError, BdNotFoundError):
            return False

    async def init_project(self, prefix: Optional[str] = None) -> dict:
        """Initialize Beads in current project.

        Args:
            prefix: Optional prefix for issue IDs (e.g., "SB" -> SB-1, SB-2)

        Returns:
            Dict with database path and prefix info
        """
        from beads_mcp.models import InitParams

        params = InitParams(prefix=prefix)
        result = await self.client.init(params)
        return {
            "database": result.database,
            "prefix": result.prefix,
            "message": result.message,
        }

    # Epic Management
    async def create_epic(
        self,
        title: str,
        description: str = "",
        priority: int = 2,
        labels: Optional[List[str]] = None,
    ) -> Issue:
        """Create a new epic.

        Args:
            title: Epic title
            description: Epic description
            priority: Priority 0-4 (0=lowest, 4=highest)
            labels: List of labels/tags

        Returns:
            Created epic
        """
        params = CreateIssueParams(
            title=title,
            description=description,
            priority=priority,
            issue_type="epic",
            labels=labels or [],
        )
        return await self.client.create(params)

    async def create_issue(
        self,
        title: str,
        description: str = "",
        issue_type: str = "task",
        priority: int = 2,
        parent_epic_id: Optional[str] = None,
        blocks: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        external_ref: Optional[str] = None,
    ) -> Issue:
        """Create a new issue.

        Args:
            title: Issue title
            description: Issue description
            issue_type: Type: bug, feature, task, epic, chore
            priority: Priority 0-4 (0=lowest, 4=highest)
            parent_epic_id: ID of parent epic (creates parent-child dependency)
            blocks: List of issue IDs this issue blocks
            labels: List of labels/tags
            external_ref: External reference (e.g., Jira ticket, GitHub issue)

        Returns:
            Created issue
        """
        params = CreateIssueParams(
            title=title,
            description=description,
            issue_type=issue_type,
            priority=priority,
            labels=labels or [],
            deps=blocks or [],
            external_ref=external_ref,
        )
        issue = await self.client.create(params)

        # Add parent-child dependency if epic specified
        if parent_epic_id:
            await self.add_dependency(
                issue.id, parent_epic_id, dep_type="parent-child"
            )

        return issue

    async def update_issue(
        self,
        issue_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
    ) -> Issue:
        """Update an existing issue.

        Args:
            issue_id: Issue ID to update
            title: New title
            description: New description
            status: New status: open, in_progress, blocked, closed
            priority: New priority 0-4

        Returns:
            Updated issue
        """
        params = UpdateIssueParams(
            issue_id=issue_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
        )
        return await self.client.update(params)

    async def close_issue(self, issue_id: str, reason: str = "Completed") -> Issue:
        """Close an issue.

        Args:
            issue_id: Issue ID to close
            reason: Reason for closing

        Returns:
            Closed issue
        """
        params = CloseIssueParams(issue_id=issue_id, reason=reason)
        return await self.client.close(params)

    async def get_issue(self, issue_id: str) -> Issue:
        """Get detailed issue information.

        Args:
            issue_id: Issue ID

        Returns:
            Issue with full details including dependencies
        """
        params = ShowIssueParams(issue_id=issue_id)
        return await self.client.show(params)

    async def list_issues(
        self,
        status: Optional[str] = None,
        issue_type: Optional[str] = None,
        priority: Optional[int] = None,
        limit: int = 50,
    ) -> List[Issue]:
        """List issues with filters.

        Args:
            status: Filter by status: open, in_progress, blocked, closed
            issue_type: Filter by type: bug, feature, task, epic, chore
            priority: Filter by priority 0-4
            limit: Max number of issues to return

        Returns:
            List of issues matching filters
        """
        params = ListIssuesParams(
            status=status,
            issue_type=issue_type,
            priority=priority,
            limit=limit,
        )
        return await self.client.list_issues(params)

    async def list_epics(
        self,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[Issue]:
        """List all epics.

        Args:
            status: Filter by status
            limit: Max number to return

        Returns:
            List of epics
        """
        return await self.list_issues(
            issue_type="epic",
            status=status,
            limit=limit,
        )

    # Dependency Management
    async def add_dependency(
        self,
        issue_id: str,
        depends_on_id: str,
        dep_type: str = "blocks",
    ) -> None:
        """Add a dependency between issues.

        Args:
            issue_id: Issue that has the dependency
            depends_on_id: Issue that is depended on
            dep_type: Type of dependency:
                - "blocks": depends_on_id blocks issue_id
                - "related": Issues are related
                - "parent-child": depends_on_id is parent of issue_id
                - "discovered-from": issue_id discovered while working on depends_on_id
        """
        params = AddDependencyParams(
            issue_id=issue_id,
            depends_on_id=depends_on_id,
            dep_type=dep_type,
        )
        await self.client.add_dependency(params)

    async def get_ready_work(
        self,
        limit: int = 10,
        priority: Optional[int] = None,
    ) -> List[Issue]:
        """Get issues that are ready to work on (no open blockers).

        This is one of Beads' killer features - automatically finds work
        that can be started right now.

        Args:
            limit: Max number of issues to return
            priority: Filter by priority

        Returns:
            List of unblocked issues sorted by priority
        """
        params = ReadyWorkParams(limit=limit, priority=priority)
        return await self.client.ready(params)

    async def get_stats(self) -> Stats:
        """Get project statistics.

        Returns:
            Stats including total/open/closed/blocked issues and ready work count
        """
        return await self.client.stats()

    # Helper Methods
    async def get_epic_children(self, epic_id: str) -> List[Issue]:
        """Get all issues that are children of an epic.

        Args:
            epic_id: Epic ID

        Returns:
            List of child issues
        """
        epic = await self.get_issue(epic_id)
        # Beads stores dependents, children have parent-child relationship
        children = []
        for dependent in epic.dependents:
            # Check if it's a parent-child relationship
            full_issue = await self.get_issue(dependent.id)
            # If this issue has the epic as a dependency with parent-child type
            for dep in full_issue.dependencies:
                if dep.id == epic_id:
                    children.append(full_issue)
                    break
        return children

    async def get_blocked_issues(self) -> List[Issue]:
        """Get all blocked issues.

        Returns:
            List of issues in blocked status
        """
        return await self.list_issues(status="blocked")

    async def get_in_progress_issues(self) -> List[Issue]:
        """Get all in-progress issues.

        Returns:
            List of issues currently being worked on
        """
        return await self.list_issues(status="in_progress")


def get_beads_client(project_dir: Optional[str] = None) -> Optional[BeadsIntegration]:
    """Get Beads integration client.

    Args:
        project_dir: Project directory (auto-detected if None)

    Returns:
        BeadsIntegration instance or None if beads-mcp not available
    """
    if not BEADS_AVAILABLE:
        return None

    try:
        return BeadsIntegration(project_dir)
    except Exception:
        return None
