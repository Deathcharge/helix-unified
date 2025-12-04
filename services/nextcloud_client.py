#!/usr/bin/env python3
"""
☁️ Helix Collective - Nextcloud Storage Client
services/nextcloud_client.py

Provides WebDAV integration with Nextcloud for:
- UCF state backups
- Discord archive storage
- Configuration file sync
- Long-term data persistence

Environment Variables:
- NEXTCLOUD_URL: https://your-instance.nextcloud.com
- NEXTCLOUD_USER: your-username
- NEXTCLOUD_PASSWORD: your-app-password
- NEXTCLOUD_BASE_PATH: /Helix (default remote folder)
"""

import io
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

logger = logging.getLogger(__name__)

try:
    from webdav3.client import Client as WebDAVClient
    WEBDAV_AVAILABLE = True
except ImportError:
    WEBDAV_AVAILABLE = False
    logger.warning(
        "⚠️ webdavclient3 not installed. Nextcloud storage disabled. "
        "To enable, run: pip install webdavclient3"
    )


class HelixNextcloudClient:
    """Nextcloud WebDAV client for Helix Collective storage."""

    def __init__(self):
        """Initialize Nextcloud client from environment variables."""
        self.url = os.getenv("NEXTCLOUD_URL")
        self.user = os.getenv("NEXTCLOUD_USER")
        self.password = os.getenv("NEXTCLOUD_PASSWORD")
        self.base_path = os.getenv("NEXTCLOUD_BASE_PATH", "/Helix")

        self.enabled = bool(self.url and self.user and self.password)
        self.client: Optional[WebDAVClient] = None

        if self.enabled and WEBDAV_AVAILABLE:
            try:
                # Configure WebDAV client
                options = {
                    'webdav_hostname': self.url,
                    'webdav_login': self.user,
                    'webdav_password': self.password,
                    'webdav_root': '/remote.php/dav/files/' + self.user,
                }
                self.client = WebDAVClient(options)

                # Ensure base directory exists
                self._ensure_directory(self.base_path)

                print(f"✅ Nextcloud client initialized: {self.url}")
            except Exception as e:
                print(f"❌ Nextcloud initialization failed: {e}")
                self.enabled = False
        elif not WEBDAV_AVAILABLE:
            print("⚠️ Nextcloud disabled: webdav3-client not installed")
            self.enabled = False
        else:
            print("⚠️ Nextcloud disabled: missing environment variables")
            print("   Required: NEXTCLOUD_URL, NEXTCLOUD_USER, NEXTCLOUD_PASSWORD")

    def _ensure_directory(self, path: str) -> bool:
        """Ensure a directory exists on Nextcloud."""
        if not self.client:
            return False

        try:
            if not self.client.check(path):
                self.client.mkdir(path)
                print(f"📁 Created Nextcloud directory: {path}")
            return True
        except Exception as e:
            print(f"⚠️ Could not create directory {path}: {e}")
            return False

    def upload_file(self, local_path: Path, remote_path: str = None) -> bool:
        """
        Upload a file to Nextcloud.

        Args:
            local_path: Local file path
            remote_path: Remote path (if None, uses base_path + filename)

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            print("⚠️ Nextcloud not enabled")
            return False

        try:
            local_path = Path(local_path)
            if not local_path.exists():
                print(f"❌ File not found: {local_path}")
                return False

            # Determine remote path
            if remote_path is None:
                remote_path = f"{self.base_path}/{local_path.name}"

            # Ensure parent directory exists
            parent_dir = str(Path(remote_path).parent)
            self._ensure_directory(parent_dir)

            # Upload file
            self.client.upload_sync(
                remote_path=remote_path,
                local_path=str(local_path)
            )

            print(f"✅ Uploaded to Nextcloud: {remote_path}")
            return True

        except Exception as e:
            print(f"❌ Nextcloud upload failed: {e}")
            return False

    def upload_string(self, content: str, remote_path: str) -> bool:
        """
        Upload string content as a file to Nextcloud.

        Args:
            content: String content to upload
            remote_path: Remote file path

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            # Ensure parent directory exists
            parent_dir = str(Path(remote_path).parent)
            self._ensure_directory(parent_dir)

            # Upload from buffer
            buffer = io.BytesIO(content.encode('utf-8'))
            self.client.upload_to(buffer, remote_path)

            print(f"✅ Uploaded content to Nextcloud: {remote_path}")
            return True

        except Exception as e:
            print(f"❌ Nextcloud upload failed: {e}")
            return False

    def download_file(self, remote_path: str, local_path: Path) -> bool:
        """
        Download a file from Nextcloud.

        Args:
            remote_path: Remote file path
            local_path: Local destination path

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            # Ensure local directory exists
            local_path = Path(local_path)
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Download file
            self.client.download_sync(
                remote_path=remote_path,
                local_path=str(local_path)
            )

            print(f"✅ Downloaded from Nextcloud: {remote_path} → {local_path}")
            return True

        except Exception as e:
            print(f"❌ Nextcloud download failed: {e}")
            return False

    def list_files(self, remote_path: str = None) -> List[Dict]:
        """
        List files in a Nextcloud directory.

        Args:
            remote_path: Remote directory path (default: base_path)

        Returns:
            List of file info dicts
        """
        if not self.enabled or not self.client:
            return []

        try:
            path = remote_path or self.base_path
            files = self.client.list(path, get_info=True)

            file_list = []
            for file in files:
                if file['path'] != path:  # Skip the directory itself
                    file_list.append({
                        'name': file.get('name', ''),
                        'path': file.get('path', ''),
                        'size': file.get('size', 0),
                        'modified': file.get('modified', ''),
                        'is_dir': file.get('isdir', False)
                    })

            return file_list

        except Exception as e:
            print(f"❌ Nextcloud list failed: {e}")
            return []

    def delete_file(self, remote_path: str) -> bool:
        """
        Delete a file from Nextcloud.

        Args:
            remote_path: Remote file path

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            self.client.clean(remote_path)
            print(f"🗑️ Deleted from Nextcloud: {remote_path}")
            return True

        except Exception as e:
            print(f"❌ Nextcloud delete failed: {e}")
            return False

    def sync_directory(self, local_dir: Path, remote_dir: str = None) -> Dict:
        """
        Sync entire local directory to Nextcloud.

        Args:
            local_dir: Local directory path
            remote_dir: Remote directory path (default: base_path/dirname)

        Returns:
            Dict with sync statistics
        """
        if not self.enabled or not self.client:
            return {"error": "Nextcloud not enabled"}

        local_dir = Path(local_dir)
        if not local_dir.exists():
            return {"error": f"Directory not found: {local_dir}"}

        if remote_dir is None:
            remote_dir = f"{self.base_path}/{local_dir.name}"

        stats = {
            'uploaded': 0,
            'failed': 0,
            'skipped': 0,
            'total_size': 0
        }

        try:
            # Ensure remote directory exists
            self._ensure_directory(remote_dir)

            # Upload all files
            for file_path in local_dir.rglob('*'):
                if file_path.is_file():
                    # Calculate relative path
                    rel_path = file_path.relative_to(local_dir)
                    remote_path = f"{remote_dir}/{rel_path}"

                    # Upload file
                    if self.upload_file(file_path, remote_path):
                        stats['uploaded'] += 1
                        stats['total_size'] += file_path.stat().st_size
                    else:
                        stats['failed'] += 1

            print(f"✅ Synced {stats['uploaded']} files to Nextcloud: {remote_dir}")
            return stats

        except Exception as e:
            print(f"❌ Directory sync failed: {e}")
            stats['error'] = str(e)
            return stats

    def get_storage_info(self) -> Dict:
        """
        Get Nextcloud storage quota information.

        Returns:
            Dict with storage info
        """
        if not self.enabled or not self.client:
            return {"error": "Nextcloud not enabled"}

        try:
            info = self.client.info('/')

            return {
                'quota_used': info.get('quota_used', 0),
                'quota_available': info.get('quota_available', 0),
                'quota_total': info.get('quota_total', 0),
                'usage_percentage': round(
                    (info.get('quota_used', 0) / info.get('quota_total', 1)) * 100, 2
                ) if info.get('quota_total', 0) > 0 else 0
            }

        except Exception as e:
            print(f"❌ Failed to get storage info: {e}")
            return {"error": str(e)}


# Global instance
_nextcloud_client: Optional[HelixNextcloudClient] = None


def get_nextcloud_client() -> Optional[HelixNextcloudClient]:
    """Get or create global Nextcloud client instance."""
    global _nextcloud_client
    if _nextcloud_client is None:
        _nextcloud_client = HelixNextcloudClient()
    return _nextcloud_client if _nextcloud_client.enabled else None


# Quick test function
if __name__ == "__main__":
    print("🧪 Testing Nextcloud client...")
    client = HelixNextcloudClient()

    if client.enabled:
        print("\n✅ Nextcloud connection successful!")

        # Test storage info
        storage = client.get_storage_info()
        if 'error' not in storage:
            print(f"📊 Storage: {storage['quota_used'] / (1024**3):.2f} GB / {storage['quota_total'] / (1024**3):.2f} GB ({storage['usage_percentage']}%)")

        # Test list files
        files = client.list_files()
        print(f"📁 Files in {client.base_path}: {len(files)}")
        for file in files[:5]:  # Show first 5
            print(f"   - {file['name']} ({file['size']} bytes)")
    else:
        print("❌ Nextcloud not configured")
        print("Set: NEXTCLOUD_URL, NEXTCLOUD_USER, NEXTCLOUD_PASSWORD")
