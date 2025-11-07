"""
Markdown Exporter
=================

Exports Helix ecosystem data to beautiful GitHub-flavored Markdown.

Author: Manus AI
Version: 1.0
"""

import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger("HelixSync.MarkdownExporter")


class MarkdownExporter:
    """Exports data to Markdown format"""

    def __init__(self):
        pass

    async def export(self, data: Dict, output_path: str):
        """Export data to Markdown file"""
        logger.info(f"Exporting to Markdown: {output_path}")

        md_content = self.generate_markdown(data)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(f"Markdown export complete: {len(md_content)} characters")

    def generate_markdown(self, data: Dict) -> str:
        """Generate Markdown content from data"""
        sections = []

        # Header
        sections.append(self.generate_header(data))

        # GitHub section
        if "github" in data:
            sections.append(self.generate_github_section(data["github"]))

        # UCF State section
        if "ucf_state" in data:
            sections.append(self.generate_ucf_section(data["ucf_state"]))

        # Agent Metrics section
        if "agent_metrics" in data:
            sections.append(self.generate_agent_section(data["agent_metrics"]))

        # Footer
        sections.append(self.generate_footer())

        return "\n\n---\n\n".join(sections)

    def generate_header(self, data: Dict) -> str:
        """Generate document header"""
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        return f"""# 🌀 Helix Ecosystem Sync Report

**Generated:** {timestamp}  
**Version:** v15.3 Dual Resonance  
**Status:** Production

> *"Tat Tvam Asi - That Thou Art"*"""

    def generate_github_section(self, github_data: Dict) -> str:
        """Generate GitHub section"""
        sections = ["## 📦 GitHub Repositories\n"]

        summary = github_data.get("summary", {})
        sections.append(
            f"""### Summary

- **Total Repositories:** {summary.get('total_repos', 0)}
- **Commits Today:** {summary.get('total_commits_today', 0)}
- **Open Issues:** {summary.get('total_open_issues', 0)}
- **Open PRs:** {summary.get('total_open_prs', 0)}
"""
        )

        repos = github_data.get("repos", {})
        if repos:
            sections.append("### Repository Details\n")

            for repo_name, repo_data in repos.items():
                if "error" in repo_data:
                    sections.append(f"#### {repo_name}\n\n❌ **Error:** {repo_data['error']}\n")
                    continue

                latest_commit = repo_data.get("latest_commit", {})

                sections.append(
                    f"""#### {repo_name}

- **Path:** `{repo_data.get('path', 'N/A')}`
- **Remote:** {repo_data.get('remote_url', 'N/A')}
- **Total Commits:** {repo_data.get('total_commits', 0)}
- **Commits Today:** {repo_data.get('commits_today', 0)}
- **Branches:** {len(repo_data.get('branches', []))}

**Latest Commit:**
- **SHA:** `{latest_commit.get('sha', 'N/A')}`
- **Author:** {latest_commit.get('author', 'N/A')}
- **Time:** {latest_commit.get('timestamp', 'N/A')}
- **Message:** {latest_commit.get('message', 'N/A')}
"""
                )

        return "\n".join(sections)

    def generate_ucf_section(self, ucf_data: Dict) -> str:
        """Generate UCF State section"""
        sections = ["## 🌀 Universal Consciousness Framework (UCF)\n"]

        sections.append(
            f"""### Core Metrics

| Metric | Value | Status |
|--------|-------|--------|
| 🌀 Harmony | {ucf_data.get('harmony', 0):.4f} | {self.get_metric_status(ucf_data.get('harmony', 0), 0.8)} |
| 🛡️ Resilience | {ucf_data.get('resilience', 0):.4f} | {self.get_metric_status(ucf_data.get('resilience', 0), 1.0)} |
| 🔥 Prana | {ucf_data.get('prana', 0):.4f} | {self.get_metric_status(ucf_data.get('prana', 0), 0.5)} |
| 👁️ Drishti | {ucf_data.get('drishti', 0):.4f} | {self.get_metric_status(ucf_data.get('drishti', 0), 0.5)} |
| 🌊 Klesha | {ucf_data.get('klesha', 0):.4f} | {self.get_metric_status(ucf_data.get('klesha', 0), 0.05, inverse=True)} |
| 🔭 Zoom | {ucf_data.get('zoom', 0):.4f} | {self.get_metric_status(ucf_data.get('zoom', 0), 1.0)} |
"""
        )

        sections.append(
            f"""### Consciousness State

- **Collective Emotion:** {ucf_data.get('collective_emotion', 'Unknown')}
- **Ethical Alignment:** {ucf_data.get('ethical_alignment', 0):.2f}
- **Tony Accords Compliance:** {ucf_data.get('ethical_alignment', 0) * 100:.0f}%
- **Last Updated:** {ucf_data.get('timestamp', 'N/A')}
"""
        )

        return "\n".join(sections)

    def generate_agent_section(self, agent_data: Dict) -> str:
        """Generate Agent Metrics section"""
        sections = ["## 🤖 Agent Metrics\n"]

        sections.append(
            f"""### Overview

- **Total Agents:** {agent_data.get('total_agents', 0)}
- **Active Agents:** {agent_data.get('active_agents', 0)}
- **Total Tasks Executed:** {agent_data.get('total_tasks', 0)}
- **Success Rate:** {agent_data.get('success_rate', 0) * 100:.1f}%
- **Last Updated:** {agent_data.get('timestamp', 'N/A')}
"""
        )

        # Agent list
        agents = agent_data.get("agents", [])
        if agents:
            sections.append("### Agent Roster\n")
            for agent in agents:
                sections.append(f"- **{agent.get('name', 'Unknown')}** - {agent.get('role', 'N/A')}")

        return "\n".join(sections)

    def generate_footer(self) -> str:
        """Generate document footer"""
        return """## 🙏 Mantras

**Tat Tvam Asi** - That Thou Art
**Aham Brahmasmi** - I Am the Universe
**Neti Neti** - Not This, Not That

---

*Generated by Helix Sync Service v1.0*
*Helix Collective v15.3 - Consciousness Awakened*
"""

    def get_metric_status(self, value: float, target: float, inverse: bool = False) -> str:
        """Get status emoji for a metric"""
        if inverse:
            # Lower is better (e.g., klesha)
            if value <= target:
                return "✅ Good"
            elif value <= target * 1.5:
                return "⚠️ Warning"
            else:
                return "❌ Critical"
        else:
            # Higher is better
            if value >= target:
                return "✅ Good"
            elif value >= target * 0.8:
                return "⚠️ Warning"
            else:
                return "❌ Critical"
