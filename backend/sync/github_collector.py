"""
GitHub Data Collector
=====================

Collects data from Helix GitHub repositories including commits, issues, PRs,
and repository statistics.

Author: Manus AI
Version: 1.0
"""

import logging
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger("HelixSync.GitHub")


class GitHubCollector:
    """Collects data from GitHub repositories"""

    def __init__(self, repos: List[str], local_path: str = "/home/ubuntu"):
        self.repos = repos
        self.local_path = local_path
        self.github_token = os.getenv("GITHUB_TOKEN", "")

    async def collect(self) -> Dict:
        """Collect all GitHub data"""
        logger.info(f"Collecting from {len(self.repos)} repositories...")

        data = {
            "repos": {},
            "summary": {
                "total_repos": len(self.repos),
                "total_commits_today": 0,
                "total_open_issues": 0,
                "total_open_prs": 0,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

        for repo in self.repos:
            try:
                repo_data = await self.collect_repo(repo)
                data["repos"][repo] = repo_data

                # Update summary
                data["summary"]["total_commits_today"] += repo_data.get("commits_today", 0)
                data["summary"]["total_open_issues"] += repo_data.get("open_issues", 0)
                data["summary"]["total_open_prs"] += repo_data.get("open_prs", 0)

            except Exception as e:
                logger.error(f"Failed to collect from {repo}: {e}")
                data["repos"][repo] = {"error": str(e)}

        return data

    async def collect_repo(self, repo: str) -> Dict:
        """Collect data from a single repository"""
        repo_path = f"{self.local_path}/{repo}"

        if not os.path.exists(repo_path):
            logger.warning(f"Repository {repo} not found locally at {repo_path}")
            return {"error": "Repository not found locally"}

        data = {
            "name": repo,
            "path": repo_path,
            "latest_commit": self.get_latest_commit(repo_path),
            "commits_today": self.get_commits_today(repo_path),
            "total_commits": self.get_total_commits(repo_path),
            "branches": self.get_branches(repo_path),
            "remote_url": self.get_remote_url(repo_path),
            "last_updated": datetime.utcnow().isoformat(),
        }

        # Try to get GitHub-specific data via API
        if self.github_token:
            try:
                api_data = await self.get_github_api_data(repo)
                data.update(api_data)
            except Exception as e:
                logger.warning(f"Failed to get GitHub API data for {repo}: {e}")

        return data

    def get_latest_commit(self, repo_path: str) -> Optional[Dict]:
        """Get latest commit info"""
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "log", "-1", "--format=%H|%an|%ae|%at|%s"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split("|")
                return {
                    "sha": parts[0][:7],
                    "author": parts[1],
                    "email": parts[2],
                    "timestamp": datetime.fromtimestamp(int(parts[3])).isoformat(),
                    "message": parts[4],
                }
        except Exception as e:
            logger.error(f"Failed to get latest commit: {e}")

        return None

    def get_commits_today(self, repo_path: str) -> int:
        """Get number of commits today"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            result = subprocess.run(
                ["git", "-C", repo_path, "log", "--since", today, "--oneline"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return len([line for line in result.stdout.split("\n") if line.strip()])
        except Exception as e:
            logger.error(f"Failed to get commits today: {e}")

        return 0

    def get_total_commits(self, repo_path: str) -> int:
        """Get total commit count"""
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "rev-list", "--count", "HEAD"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0 and result.stdout.strip():
                return int(result.stdout.strip())
        except Exception as e:
            logger.error(f"Failed to get total commits: {e}")

        return 0

    def get_branches(self, repo_path: str) -> List[str]:
        """Get list of branches"""
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "branch", "-a"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                branches = []
                for line in result.stdout.split("\n"):
                    line = line.strip().lstrip("* ")
                    if line and not line.startswith("remotes/origin/HEAD"):
                        branches.append(line)
                return branches
        except Exception as e:
            logger.error(f"Failed to get branches: {e}")

        return []

    def get_remote_url(self, repo_path: str) -> Optional[str]:
        """Get remote URL"""
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "remote", "get-url", "origin"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception as e:
            logger.error(f"Failed to get remote URL: {e}")

        return None

    async def get_github_api_data(self, repo: str) -> Dict:
        """Get data from GitHub API"""
        # Placeholder for GitHub API integration
        # Would use gh CLI or requests to GitHub API
        return {"open_issues": 0, "open_prs": 0, "stars": 0, "forks": 0, "watchers": 0}
