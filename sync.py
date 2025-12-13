#!/usr/bin/env python3
"""
sync.py - Helix Universal Cloud Sync Adapter
Version: 15.4-preview
Strategy: Backend-agnostic sync interface

Supports:
- rclone (50+ backends: MEGA, S3, Drive, Dropbox, etc.)
- mega.py (legacy fallback for v15.3 compatibility)

Design Philosophy:
- Auto-detect best available backend
- Graceful degradation if rclone unavailable
- Simple API: upload(local, remote) / download(remote, local)
- Production-grade: retries, timeouts, logging

Author: Claude Code (implementing Grok's strategy)
"""

import logging
import os
import subprocess
from enum import Enum
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SyncBackend(Enum):
    """Available cloud sync backends."""
    RCLONE_MEGA = "rclone_mega"  # rclone + MEGA (production)
    RCLONE_S3 = "rclone_s3"      # rclone + AWS S3
    RCLONE_GDRIVE = "rclone_gdrive"  # rclone + Google Drive
    MEGA_LEGACY = "mega_py"      # mega.py (v15.3 fallback)
    NONE = "none"                # No backend available


class CloudSync:
    """
    Universal cloud sync adapter.

    Auto-selects best available backend:
    1. rclone (if binary available) - PREFERRED
    2. mega.py (if rclone unavailable) - FALLBACK
    3. None (logs warning) - OFFLINE MODE

    Usage:
        from sync import cloud_sync

        # Upload
        cloud_sync.upload("local.png", "rituals/fractal_001.png")

        # Download
        cloud_sync.download("state/ucf.json", "local_ucf.json")
    """

    def __init__(self, backend: Optional[SyncBackend] = None, remote_name: str = "mega"):
        """
        Initialize cloud sync adapter.

        Args:
            backend: Force specific backend (or None for auto-detect)
            remote_name: rclone remote name (default: "mega")
        """
        self.remote_name = remote_name

        # Auto-detect or use forced backend
        if backend is None:
            self.backend = self._auto_detect_backend()
        else:
            self.backend = backend

        logger.info(f"☁️ CloudSync initialized: {self.backend.value}")

        # Initialize backend-specific client
        self._init_backend()

    def _auto_detect_backend(self) -> SyncBackend:
        """Auto-select best available backend."""

        # Check if rclone is available (preferred)
        if self._check_rclone():
            logger.info("✅ rclone detected - using production backend")
            return SyncBackend.RCLONE_MEGA

        # Fall back to mega.py (legacy)
        try:
            import mega
            logger.warning("⚠️ rclone not found - falling back to mega.py (legacy)")
            return SyncBackend.MEGA_LEGACY
        except ImportError:
            logger.error("❌ No sync backend available (rclone or mega.py)")
            return SyncBackend.NONE

    def _check_rclone(self) -> bool:
        """Check if rclone binary is available."""
        try:
            result = subprocess.run(
                ["rclone", "version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _init_backend(self):
        """Initialize backend-specific client."""
        if self.backend == SyncBackend.MEGA_LEGACY:
            try:
                # Import legacy mega.py adapter
                from bot.mega_sync import mega_sync
                self.mega_client = mega_sync
                logger.info("🦑 Legacy mega.py client loaded")
            except ImportError:
                logger.error("❌ mega.py client import failed")
                self.backend = SyncBackend.NONE

    def upload(self, local_path: str, remote_path: str) -> bool:
        """
        Upload file to cloud storage.

        Args:
            local_path: Local file path
            remote_path: Remote path (relative to remote root)

        Returns:
            True if upload succeeded, False otherwise
        """
        if self.backend == SyncBackend.NONE:
            logger.warning(f"⚠️ Sync disabled - cannot upload {local_path}")
            return False

        # Normalize paths
        local_path = Path(local_path)
        if not local_path.exists():
            logger.error(f"❌ Local file not found: {local_path}")
            return False

        # Route to appropriate backend
        if self.backend.value.startswith("rclone"):
            return self._rclone_upload(str(local_path), remote_path)
        elif self.backend == SyncBackend.MEGA_LEGACY:
            return self._megapy_upload(str(local_path), remote_path)

        return False

    def download(self, remote_path: str, local_path: str) -> bool:
        """
        Download file from cloud storage.

        Args:
            remote_path: Remote path (relative to remote root)
            local_path: Local destination path

        Returns:
            True if download succeeded, False otherwise
        """
        if self.backend == SyncBackend.NONE:
            logger.warning(f"⚠️ Sync disabled - cannot download {remote_path}")
            return False

        # Route to appropriate backend
        if self.backend.value.startswith("rclone"):
            return self._rclone_download(remote_path, local_path)
        elif self.backend == SyncBackend.MEGA_LEGACY:
            return self._megapy_download(remote_path, local_path)

        return False

    # -------------------------------------------------------------------------
    # rclone Backend (Production)
    # -------------------------------------------------------------------------

    def _rclone_upload(self, local_path: str, remote_path: str) -> bool:
        """Upload via rclone (production method)."""
        try:
            remote_full = f"{self.remote_name}:{remote_path}"

            result = subprocess.run([
                "rclone", "copy",
                local_path,
                remote_full,
                "--progress",
                "--retries", "3",
                "--low-level-retries", "10",
                "--timeout", "10m",
                "--stats", "1s"
            ], capture_output=True, timeout=600)

            if result.returncode == 0:
                logger.info(f"✅ rclone ↑ {local_path} → {remote_full}")
                return True
            else:
                error = result.stderr.decode()
                logger.error(f"❌ rclone upload failed: {error}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"❌ rclone upload timeout: {local_path}")
            return False
        except Exception as e:
            logger.error(f"❌ rclone upload error: {e}")
            return False

    def _rclone_download(self, remote_path: str, local_path: str) -> bool:
        """Download via rclone (production method)."""
        try:
            remote_full = f"{self.remote_name}:{remote_path}"

            # Ensure local directory exists
            Path(local_path).parent.mkdir(parents=True, exist_ok=True)

            result = subprocess.run([
                "rclone", "copy",
                remote_full,
                str(Path(local_path).parent),
                "--progress",
                "--retries", "3",
                "--low-level-retries", "10",
                "--timeout", "10m"
            ], capture_output=True, timeout=600)

            if result.returncode == 0:
                logger.info(f"✅ rclone ↓ {remote_full} → {local_path}")
                return True
            else:
                error = result.stderr.decode()
                logger.error(f"❌ rclone download failed: {error}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"❌ rclone download timeout: {remote_path}")
            return False
        except Exception as e:
            logger.error(f"❌ rclone download error: {e}")
            return False

    # -------------------------------------------------------------------------
    # mega.py Backend (Legacy Fallback)
    # -------------------------------------------------------------------------

    def _megapy_upload(self, local_path: str, remote_path: str) -> bool:
        """Upload via mega.py (legacy fallback)."""
        try:
            if not hasattr(self, 'mega_client'):
                logger.error("❌ mega.py client not initialized")
                return False

            # Connect if not connected
            if not self.mega_client.client:
                if not self.mega_client.connect():
                    logger.error("❌ mega.py connection failed")
                    return False

            # Upload
            result = self.mega_client.upload(local_path, remote_path)

            if result:
                logger.info(f"✅ mega.py ↑ {local_path} → {remote_path}")
            else:
                logger.error(f"❌ mega.py upload failed: {local_path}")

            return result

        except Exception as e:
            logger.error(f"❌ mega.py upload error: {e}")
            return False

    def _megapy_download(self, remote_path: str, local_path: str) -> bool:
        """Download via mega.py (legacy fallback)."""
        try:
            if not hasattr(self, 'mega_client'):
                logger.error("❌ mega.py client not initialized")
                return False

            # Connect if not connected
            if not self.mega_client.client:
                if not self.mega_client.connect():
                    logger.error("❌ mega.py connection failed")
                    return False

            # Download
            result = self.mega_client.download(remote_path, local_path)

            if result:
                logger.info(f"✅ mega.py ↓ {remote_path} → {local_path}")
            else:
                logger.error(f"❌ mega.py download failed: {remote_path}")

            return result

        except Exception as e:
            logger.error(f"❌ mega.py download error: {e}")
            return False


# ============================================================================
# GLOBAL INSTANCE (for convenience)
# ============================================================================

# Auto-initialized singleton
cloud_sync = CloudSync()


# ============================================================================
# TESTING
# ============================================================================

def test_sync():
    """Test cloud sync functionality."""
    logger.info("🧪 Testing CloudSync adapter...")

    # Test file
    test_file = "Helix/state/sync_test.txt"
    os.makedirs(os.path.dirname(test_file), exist_ok=True)

    with open(test_file, "w") as f:
        f.write(f"Helix CloudSync test - {os.getpid()}")

    # Upload test
    logger.info(f"Testing upload: {test_file}")
    upload_result = cloud_sync.upload(test_file, "test/sync_test.txt")

    if upload_result:
        logger.info("✅ Upload test PASSED")
    else:
        logger.error("❌ Upload test FAILED")

    # Download test
    logger.info("Testing download...")
    download_result = cloud_sync.download("test/sync_test.txt", "downloaded_test.txt")

    if download_result:
        logger.info("✅ Download test PASSED")
    else:
        logger.error("❌ Download test FAILED")

    return upload_result and download_result


if __name__ == "__main__":
    # Run tests if executed directly
    test_sync()
