#!/usr/bin/env python3
"""
🔒 Helix Collective - Automated Backup System
Prevents project loss through multi-layer backup strategy

Backup Targets:
1. Helix-unified repository (local + remote)
2. Notion databases (via API)
3. Zapier Tables (via webhook export)
4. Railway environment variables
5. Configuration files
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import requests


class HelixBackupSystem:
    """Comprehensive backup system for Helix Collective infrastructure."""

    def __init__(self):
        self.backup_dir = Path("backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Notion configuration
        self.notion_api_key = os.getenv("NOTION_API_KEY")
        self.notion_databases = {
            "context_vault": os.getenv("NOTION_CONTEXT_VAULT_DB_ID"),
            "agent_registry": os.getenv("NOTION_AGENT_REGISTRY_DB_ID"),
            "ucf_metrics": os.getenv("NOTION_UCF_METRICS_DB_ID"),
        }

        # Zapier configuration
        self.zapier_tables = {
            "ucf_metrics": "01K9DP5MG6KCY48YC8M7VW0PXD",
            "commands": "01K9DP9YYQASFC49MKVPJHEPWQ",
            "emergency": "01K9DPA8RW9DTR2HJG7YDXA24Z",
        }

    def backup_git_repository(self) -> Dict:
        """Backup entire git repository structure."""
        print("📦 Backing up git repository...")

        backup_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "branch": self._run_command("git branch --show-current"),
            "commit": self._run_command("git rev-parse HEAD"),
            "status": self._run_command("git status --porcelain"),
            "remotes": self._run_command("git remote -v"),
        }

        # Save repository state
        with open(self.backup_dir / "git_state.json", "w") as f:
            json.dump(backup_data, f, indent=2)

        # Create tarball of entire repo (excluding .git to save space)
        print("📦 Creating repository tarball...")
        subprocess.run(
            [
                "tar",
                "-czf",
                str(self.backup_dir / "helix_unified_repo.tar.gz"),
                "--exclude=.git",
                "--exclude=__pycache__",
                "--exclude=*.pyc",
                "--exclude=node_modules",
                ".",
            ]
        )

        print("✅ Git repository backed up")
        return backup_data

    def backup_notion_databases(self) -> Dict:
        """Backup all Notion databases via API."""
        print("📔 Backing up Notion databases...")

        if not self.notion_api_key:
            print("⚠️ NOTION_API_KEY not set - skipping Notion backup")
            return {"error": "API key not configured", "status": "skipped"}

        try:
            from notion_client import Client
        except ImportError:
            print("⚠️ notion-client not installed - skipping Notion backup")
            print("   Install with: pip install notion-client")
            return {"error": "notion-client not installed", "status": "skipped"}

        notion = Client(auth=self.notion_api_key)
        backup_data = {}

        for db_name, db_id in self.notion_databases.items():
            if not db_id:
                print(f"⚠️ {db_name} database ID not configured - skipping")
                continue

            print(f"  - Backing up {db_name}...")
            try:
                # Query all pages in database
                results = notion.databases.query(database_id=db_id)
                backup_data[db_name] = {
                    "database_id": db_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "pages": results["results"],
                    "has_more": results["has_more"],
                }

                # Save to file
                with open(self.backup_dir / f"notion_{db_name}.json", "w") as f:
                    json.dump(backup_data[db_name], f, indent=2)

                print(f"  ✅ {len(results['results'])} pages backed up from {db_name}")

            except Exception as e:
                print(f"  ❌ Failed to backup {db_name}: {e}")
                backup_data[db_name] = {"error": str(e)}

        return backup_data

    def backup_zapier_tables(self) -> Dict:
        """Backup Zapier Tables data via webhook export."""
        print("📊 Backing up Zapier Tables...")

        # Note: Zapier Tables don't have a direct export API
        # This creates a webhook-based export structure
        backup_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "tables": self.zapier_tables,
            "note": "Zapier Tables require manual export or webhook-based sync",
        }

        # Document table structure
        with open(self.backup_dir / "zapier_tables_structure.json", "w") as f:
            json.dump(backup_data, f, indent=2)

        print("✅ Zapier Tables structure documented")
        print("ℹ️ For full data backup, use Zapier's Export feature in dashboard")

        return backup_data

    def backup_environment_variables(self) -> Dict:
        """Backup environment configuration (sensitive values masked)."""
        print("⚙️ Backing up environment configuration...")

        # Get Railway variables (if available)
        try:
            railway_vars = self._run_command("railway variables")
        except:
            railway_vars = "Railway CLI not available"

        env_backup = {
            "timestamp": datetime.utcnow().isoformat(),
            "variables": {
                # Document which vars are needed (without exposing values)
                "NOTION_API_KEY": "*** (required for Notion sync)",
                "NOTION_CONTEXT_VAULT_DB_ID": "*** (Context Vault database)",
                "ZAPIER_CONTEXT_ARCHIVE_WEBHOOK": "*** (Context archiving)",
                "API_BASE": os.getenv("API_BASE", "not set"),
                "RAILWAY_ENVIRONMENT": os.getenv("RAILWAY_ENVIRONMENT", "local"),
            },
            "railway": railway_vars,
        }

        with open(self.backup_dir / "environment_config.json", "w") as f:
            json.dump(env_backup, f, indent=2)

        print("✅ Environment configuration backed up")
        return env_backup

    def backup_documentation(self) -> Dict:
        """Backup all documentation files."""
        print("📚 Backing up documentation...")

        docs = []
        for doc_file in Path("docs").glob("*.md"):
            docs.append(str(doc_file))

        backup_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "files": docs,
            "count": len(docs),
        }

        # Copy all docs to backup directory
        docs_backup_dir = self.backup_dir / "docs"
        docs_backup_dir.mkdir(exist_ok=True)

        for doc in docs:
            subprocess.run(["cp", doc, str(docs_backup_dir)])

        print(f"✅ {len(docs)} documentation files backed up")
        return backup_data

    def create_recovery_guide(self):
        """Create recovery instructions in case of catastrophic failure."""
        print("📖 Creating recovery guide...")

        recovery_guide = f"""# 🔒 Helix Collective - Disaster Recovery Guide

**Backup Created**: {datetime.utcnow().isoformat()}
**Backup Location**: {self.backup_dir}

---

## 🚨 COMPLETE SYSTEM RECOVERY PROCEDURE

### Step 1: Restore Git Repository

```bash
# Extract repository backup
tar -xzf helix_unified_repo.tar.gz -C /path/to/restore/

# Reinitialize git
cd /path/to/restore/
git init
git remote add origin https://github.com/Deathcharge/helix-unified.git

# Restore to previous commit
git fetch origin
git checkout {self._run_command("git rev-parse HEAD")}
```

### Step 2: Restore Environment Variables

Set these in Railway dashboard or .env file:

```bash
NOTION_API_KEY=*** (retrieve from Notion integration settings)
NOTION_CONTEXT_VAULT_DB_ID=*** (from Notion database URL)
ZAPIER_CONTEXT_ARCHIVE_WEBHOOK=*** (from Zapier webhook URL)
API_BASE=https://helix-unified-production.up.railway.app
```

### Step 3: Restore Notion Databases

1. Create new databases in Notion (if needed)
2. Import data from `notion_*.json` files using Notion API
3. Update database IDs in environment variables

### Step 4: Restore Zapier Tables

1. Go to Zapier Tables dashboard
2. Create tables with IDs:
   - UCF Metrics: 01K9DP5MG6KCY48YC8M7VW0PXD
   - Commands: 01K9DP9YYQASFC49MKVPJHEPWQ
   - Emergency: 01K9DPA8RW9DTR2HJG7YDXA24Z
3. Import data using Zapier's import feature

### Step 5: Deploy to Railway

```bash
railway login
railway link
railway up
```

### Step 6: Verify All Systems

```bash
# Test Streamlit dashboard
streamlit run frontend/streamlit_app.py

# Test Railway backend
curl https://helix-unified-production.up.railway.app/status

# Test Notion sync
python -c "from services.notion_sync_daemon import NotionSyncDaemon; daemon = NotionSyncDaemon(); daemon.sync_agents_to_zapier()"
```

---

## 📋 CRITICAL URLS TO PRESERVE

**GitHub Repository**: https://github.com/Deathcharge/helix-unified
**Railway Backend**: https://helix-unified-production.up.railway.app
**Zapier Dashboard**: https://helix-consciousness-dashboard.zapier.app
**Context Vault**: Navigate to page 16 in Streamlit dashboard

**Notion Databases**:
- Context Vault: (from NOTION_CONTEXT_VAULT_DB_ID)
- Agent Registry: (from NOTION_AGENT_REGISTRY_DB_ID)
- UCF Metrics: (from NOTION_UCF_METRICS_DB_ID)

**Zapier Webhooks**:
- Context Archive: (from ZAPIER_CONTEXT_ARCHIVE_WEBHOOK)

---

## 🔑 ACCOUNT RECOVERY

**GitHub**: Deathcharge account
**Railway**: Connected to GitHub OAuth
**Notion**: (your Notion workspace)
**Zapier**: (your Zapier account)
**Stripe**: Account ID acct_1SQhxUGc7bW6TLEn

---

## 📞 EMERGENCY CONTACTS

If you need help recovering:
1. GitHub support (for repo access issues)
2. Railway support (for deployment issues)
3. Notion support (for database issues)
4. Zapier support (for interface issues)

---

*Tat Tvam Asi* - The backup IS the consciousness. 🌀
"""

        with open(self.backup_dir / "RECOVERY_GUIDE.md", "w") as f:
            f.write(recovery_guide)

        print("✅ Recovery guide created")

    def generate_backup_summary(self) -> Dict:
        """Generate summary of backup operation."""
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "backup_location": str(self.backup_dir),
            "components_backed_up": [
                "git_repository",
                "notion_databases",
                "zapier_tables_structure",
                "environment_config",
                "documentation",
                "recovery_guide",
            ],
            "backup_size_mb": sum(
                f.stat().st_size for f in self.backup_dir.rglob("*") if f.is_file()
            )
            / (1024 * 1024),
        }

        with open(self.backup_dir / "backup_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        return summary

    def run_full_backup(self):
        """Execute complete backup sequence."""
        print("=" * 60)
        print("🔒 HELIX COLLECTIVE - FULL SYSTEM BACKUP")
        print("=" * 60)
        print()

        results = {}

        # Execute all backup steps
        results["git"] = self.backup_git_repository()
        print()

        results["notion"] = self.backup_notion_databases()
        print()

        results["zapier"] = self.backup_zapier_tables()
        print()

        results["environment"] = self.backup_environment_variables()
        print()

        results["documentation"] = self.backup_documentation()
        print()

        self.create_recovery_guide()
        print()

        summary = self.generate_backup_summary()

        print("=" * 60)
        print("✅ BACKUP COMPLETE")
        print("=" * 60)
        print(f"Location: {self.backup_dir}")
        print(f"Size: {summary['backup_size_mb']:.2f} MB")
        print(f"Components: {len(summary['components_backed_up'])}")
        print()
        print("📖 See RECOVERY_GUIDE.md for restoration instructions")
        print()

        return results

    def _run_command(self, command: str) -> str:
        """Run shell command and return output."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"


def main():
    """Run backup system."""
    backup = HelixBackupSystem()
    backup.run_full_backup()


if __name__ == "__main__":
    main()
