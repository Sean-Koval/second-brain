"""Jira integration client."""

import os
from typing import Optional, List, Dict, Any
from jira import JIRA
from jira.exceptions import JIRAError


class JiraClient:
    """Client for interacting with Jira API."""

    def __init__(
        self,
        server: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
    ):
        """
        Initialize Jira client.

        Args:
            server: Jira server URL (e.g., https://company.atlassian.net)
            email: User email for authentication
            api_token: API token for authentication

        If not provided, will attempt to read from environment variables:
        - JIRA_SERVER
        - JIRA_EMAIL
        - JIRA_API_TOKEN
        """
        self.server = server or os.getenv("JIRA_SERVER")
        self.email = email or os.getenv("JIRA_EMAIL")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN")

        if not all([self.server, self.email, self.api_token]):
            raise ValueError(
                "Jira credentials not provided. Set JIRA_SERVER, JIRA_EMAIL, "
                "and JIRA_API_TOKEN environment variables or pass them to the constructor."
            )

        self.client = JIRA(server=self.server, basic_auth=(self.email, self.api_token))

    def test_connection(self) -> bool:
        """Test if the Jira connection is working."""
        try:
            self.client.myself()
            return True
        except JIRAError:
            return False

    def get_project_issues(
        self, project_key: str, status: Optional[str] = None, max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get issues for a specific project.

        Args:
            project_key: Jira project key (e.g., 'PROJ')
            status: Filter by status (optional)
            max_results: Maximum number of results to return

        Returns:
            List of issue dictionaries
        """
        jql = f"project = {project_key}"
        if status:
            jql += f" AND status = '{status}'"

        jql += " ORDER BY updated DESC"

        try:
            issues = self.client.search_issues(jql, maxResults=max_results)
            return [self._format_issue(issue) for issue in issues]
        except JIRAError as e:
            print(f"Error fetching issues: {e}")
            return []

    def get_assigned_issues(
        self, assignee: Optional[str] = None, status: Optional[str] = None, max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get issues assigned to a user.

        Args:
            assignee: Username or email (defaults to current user)
            status: Filter by status (optional)
            max_results: Maximum number of results

        Returns:
            List of issue dictionaries
        """
        if not assignee:
            assignee = "currentUser()"
        else:
            assignee = f'"{assignee}"'

        jql = f"assignee = {assignee}"
        if status:
            jql += f" AND status = '{status}'"

        jql += " ORDER BY updated DESC"

        try:
            issues = self.client.search_issues(jql, maxResults=max_results)
            return [self._format_issue(issue) for issue in issues]
        except JIRAError as e:
            print(f"Error fetching assigned issues: {e}")
            return []

    def get_issue(self, issue_key: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific issue by key.

        Args:
            issue_key: Issue key (e.g., 'PROJ-123')

        Returns:
            Issue dictionary or None if not found
        """
        try:
            issue = self.client.issue(issue_key)
            return self._format_issue(issue)
        except JIRAError:
            return None

    def _format_issue(self, issue) -> Dict[str, Any]:
        """Format a Jira issue into a dictionary."""
        return {
            "key": issue.key,
            "id": issue.id,
            "summary": issue.fields.summary,
            "description": issue.fields.description or "",
            "status": issue.fields.status.name,
            "priority": issue.fields.priority.name if issue.fields.priority else None,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
            "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
            "created": issue.fields.created,
            "updated": issue.fields.updated,
            "project_key": issue.fields.project.key,
            "issue_type": issue.fields.issuetype.name,
            "labels": issue.fields.labels if hasattr(issue.fields, "labels") else [],
        }

    def update_issue_status(self, issue_key: str, status: str) -> bool:
        """
        Update the status of an issue.

        Note: This requires the transition to be valid for the current status.

        Args:
            issue_key: Issue key
            status: Target status name

        Returns:
            True if successful
        """
        try:
            issue = self.client.issue(issue_key)
            transitions = self.client.transitions(issue)

            # Find the transition that matches the target status
            for transition in transitions:
                if transition["name"].lower() == status.lower():
                    self.client.transition_issue(issue, transition["id"])
                    return True

            print(f"No valid transition found to status: {status}")
            return False
        except JIRAError as e:
            print(f"Error updating issue status: {e}")
            return False

    def add_comment(self, issue_key: str, comment: str) -> bool:
        """
        Add a comment to an issue.

        Args:
            issue_key: Issue key
            comment: Comment text

        Returns:
            True if successful
        """
        try:
            self.client.add_comment(issue_key, comment)
            return True
        except JIRAError as e:
            print(f"Error adding comment: {e}")
            return False
