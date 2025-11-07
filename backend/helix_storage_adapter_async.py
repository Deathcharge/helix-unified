# 🌀 Helix Unified Storage Adapter (v15.2 • Async + Fire-and-Forget)
# backend/helix_storage_adapter_async.py
# Supports: Nextcloud (WebDAV), MEGA (REST), Local fallback
# Author: Helix Collective Ω-Bridge

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import aiofiles
import aiohttp


class HelixStorageAdapterAsync:
    """Non-blocking cloud/local archive handler for Shadow persistence."""

    def __init__(self):
        self.mode = os.getenv("HELIX_STORAGE_MODE", "local")  # nextcloud | mega | local
        self.root = Path("Shadow/manus_archive")
        self.root.mkdir(parents=True, exist_ok=True)

        # Nextcloud / WebDAV configuration
        self.webdav_url = os.getenv("NEXTCLOUD_URL", "")
        self.webdav_user = os.getenv("NEXTCLOUD_USER", "")
        self.webdav_pass = os.getenv("NEXTCLOUD_PASS", "")

        # MEGA configuration
        self.mega_token = os.getenv("MEGA_API_KEY", "")

    async def upload(self, file_path: str, remote_dir: str = "helix_uploads") -> Optional[int]:
        """
        Upload file to configured cloud storage (non-blocking).

        Args:
            file_path: Local file path to upload
            remote_dir: Remote directory name

        Returns:
            HTTP status code or 200 for local storage
        """
        path = Path(file_path)
        if not path.exists():
            print(f"❌ Missing file {path}")
            return None

        if self.mode == "nextcloud" and self.webdav_url:
            return await self._upload_nextcloud(path, remote_dir)
        elif self.mode == "mega" and self.mega_token:
            return await self._upload_mega(path, remote_dir)
        else:
            return await self._upload_local(path, remote_dir)

    async def _upload_nextcloud(self, path: Path, remote_dir: str) -> int:
        """Upload to Nextcloud via WebDAV."""
        target = f"{self.webdav_url.rstrip('/')}/{remote_dir}/{path.name}"

        try:
            async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.webdav_user, self.webdav_pass)) as session:
                async with aiofiles.open(path, "rb") as f:
                    data = await f.read()
                    async with session.put(target, data=data) as response:
                        print(f"☁️ Nextcloud → {response.status} ({path.name})")
                        return response.status
        except Exception as e:
            print(f"⚠️  Nextcloud upload failed: {e}")
            return await self._upload_local(path, remote_dir)

    async def _upload_mega(self, path: Path, remote_dir: str) -> int:
        """Upload to MEGA via REST API."""
        endpoint = "https://api.mega.nz/v2/files/upload"
        headers = {"Authorization": self.mega_token}

        try:
            async with aiohttp.ClientSession() as session:
                async with aiofiles.open(path, "rb") as f:
                    data = await f.read()
                    form = aiohttp.FormData()
                    form.add_field("file", data, filename=path.name)

                    async with session.post(endpoint, headers=headers, data=form) as response:
                        print(f"☁️ MEGA → {response.status} ({path.name})")
                        return response.status
        except Exception as e:
            print(f"⚠️  MEGA upload failed: {e}")
            return await self._upload_local(path, remote_dir)

    async def _upload_local(self, path: Path, remote_dir: str) -> int:
        """Local fallback storage."""
        local_target = self.root / f"{remote_dir}_{path.name}"

        try:
            async with aiofiles.open(path, "rb") as src:
                async with aiofiles.open(local_target, "wb") as dst:
                    await dst.write(await src.read())
            print(f"💾 Local → {local_target}")
            return 200
        except Exception as e:
            print(f"❌ Local storage error: {e}")
            return 500

    async def archive_json(self, data: Dict[str, Any], name: str) -> Path:
        """
        Save JSON data to archive and queue for upload.

        Args:
            data: Dictionary to save as JSON
            name: Base filename (timestamp will be added)

        Returns:
            Path to saved file
        """
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = self.root / f"{name}_{ts}.json"

        # Save locally
        async with aiofiles.open(filename, "w") as f:
            await f.write(json.dumps(data, indent=2))

        print(f"🦑 Archived {filename}")

        # Queue upload in background (fire-and-forget)
        asyncio.create_task(self.upload(str(filename)))

        return filename

    async def list_archives(self) -> list:
        """List all JSON archives in Shadow directory."""
        return [p.name for p in self.root.glob("*.json")]

    async def retrieve_archive(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Load JSON archive from Shadow directory.

        Args:
            filename: Archive filename (e.g., "manus_log_20250130_123456.json")

        Returns:
            Parsed JSON data or None if file not found/invalid
        """
        file_path = self.root / filename

        if not file_path.exists():
            print(f"⚠️ Archive not found: {filename}")
            return None

        try:
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
                data = json.loads(content)
                print(f"📂 Retrieved archive: {filename}")
                return data
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {filename}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            return None

    async def search_archives(self, pattern: str = "*", limit: int = 10) -> list[Dict[str, Any]]:
        """
        Search for archives matching a pattern and return their metadata.

        Args:
            pattern: Glob pattern (e.g., "manus_log_*", "context_*")
            limit: Maximum number of results to return

        Returns:
            List of archive metadata sorted by modification time (newest first)
        """
        files = list(self.root.glob(f"{pattern}.json"))
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        results = []
        for file_path in files[:limit]:
            try:
                stat = file_path.stat()
                results.append(
                    {
                        "filename": file_path.name,
                        "size_kb": round(stat.st_size / 1024, 2),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "path": str(file_path),
                    }
                )
            except Exception as e:
                print(f"⚠️ Error reading metadata for {file_path.name}: {e}")

        return results

    async def get_latest_archive(self, name_prefix: str) -> Optional[Dict[str, Any]]:
        """
        Get the most recent archive matching a name prefix.

        Args:
            name_prefix: Archive name prefix (e.g., "manus_log", "context_memes")

        Returns:
            Parsed JSON data from latest archive or None if not found
        """
        files = list(self.root.glob(f"{name_prefix}_*.json"))

        if not files:
            # Try exact match (e.g., "context_memes.json" without timestamp)
            exact_match = self.root / f"{name_prefix}.json"
            if exact_match.exists():
                return await self.retrieve_archive(exact_match.name)

            print(f"⚠️ No archives found matching: {name_prefix}")
            return None

        # Get latest by modification time
        latest = max(files, key=lambda p: p.stat().st_mtime)
        return await self.retrieve_archive(latest.name)

    async def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        import shutil

        files = list(self.root.glob("*.json"))
        total_size = sum(p.stat().st_size for p in files)
        usage = shutil.disk_usage(self.root)

        return {
            "mode": self.mode,
            "archive_count": len(files),
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "free_gb": round(usage.free / (1024**3), 2),
            "latest": max((p.name for p in files), default=None),
        }

    async def auto_cleanup_if_needed(self) -> int:
        """
        Auto-prune archives if free space < threshold (default 100 GB).
        Keeps latest 20 files + all visual outputs.
        Logs cleanup events to Shadow archive.

        Returns:
            Number of files deleted
        """
        import glob
        import shutil

        # Load threshold from config (default 100 GB)
        config_path = Path("Helix/state/storage_config.json")
        threshold_gb = 100
        if config_path.exists():
            try:
                async with aiofiles.open(config_path, "r") as f:
                    content = await f.read()
                    config = json.loads(content)
                    threshold_gb = config.get("auto_cleanup_threshold_gb", 100)
            except Exception:
                pass

        # Check free space
        stat = shutil.disk_usage("/")
        free_gb = stat.free / (1024**3)

        if free_gb < threshold_gb:
            # Get all log files (excluding visual outputs)
            log_files = []
            for ext in ["*.log", "*.json"]:
                for f in glob.glob(str(self.root / ext)):
                    if "visual_outputs" not in f and "cleanup_log" not in f:
                        log_files.append(f)

            # Sort by modification time (oldest first)
            log_files.sort(key=os.path.getmtime)

            # Keep latest 20, delete rest
            deleted_count = 0
            if len(log_files) > 20:
                to_delete = log_files[:-20]
                for file in to_delete:
                    try:
                        os.remove(file)
                        print(f"🧹 Auto-cleanup: Deleted {file}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"⚠️  Cleanup error for {file}: {e}")

            # Log to Shadow archive
            cleanup_log_path = self.root / "cleanup_log.json"
            log_entry = {
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "deleted_files": deleted_count,
                "free_space_gb": round(free_gb, 2),
                "threshold_gb": threshold_gb,
            }

            try:
                async with aiofiles.open(cleanup_log_path, "a") as f:
                    await f.write(json.dumps(log_entry) + "\n")
            except Exception as e:
                print(f"⚠️  Cleanup log error: {e}")

            return deleted_count

        return 0


# ============================================================================
# SAMSARA ASSET UPLOADER (Manus Pass v15.2)
# ============================================================================


async def upload_samsara_asset(file_path: Path, metadata: dict) -> bool:
    """
    Upload Samsara assets to Nextcloud with UCF metadata.
    Supports ritual_frame_*.png, kairobyte_om_*.mp3/wav, ucf_state.json.

    Args:
        file_path: Path to asset file
        metadata: UCF state and other context

    Returns:
        True if upload successful, False otherwise
    """
    import logging
    import time

    storage_mode = os.getenv("HELIX_STORAGE_MODE", "local")

    if storage_mode != "nextcloud":
        logging.info(f"🦑 Shadow: Nextcloud disabled (mode={storage_mode}); falling back to local")
        return False

    nextcloud_url = os.getenv("NEXTCLOUD_URL", "")
    nextcloud_user = os.getenv("NEXTCLOUD_USER", "")
    nextcloud_pass = os.getenv("NEXTCLOUD_PASS", "")

    if not all([nextcloud_url, nextcloud_user, nextcloud_pass]):
        logging.warning("⚠️  Nextcloud credentials incomplete")
        return False

    if not file_path.exists():
        logging.error(f"❌ File not found: {file_path}")
        return False

    # Build WebDAV URL
    url = f"{nextcloud_url.rstrip('/')}/{file_path.name}"

    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as f:
                auth = aiohttp.BasicAuth(nextcloud_user, nextcloud_pass)
                async with session.put(url, data=f, auth=auth) as resp:
                    success = resp.status in (201, 204)
                    status = "success" if success else f"failed ({resp.status})"

                    log_entry = {
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "file": str(file_path),
                        "status": status,
                        "metadata": metadata,
                    }

                    logging.info(f"🦑 Shadow: Uploaded {file_path.name} - {status}")

                    # Log upload
                    archive_path = Path("Shadow/manus_archive/upload_log.json")
                    archive_path.parent.mkdir(parents=True, exist_ok=True)

                    async with aiofiles.open(archive_path, "a") as log:
                        await log.write(json.dumps(log_entry) + "\n")

                    return success

    except Exception as e:
        logging.error(f"❌ Samsara upload failed: {e}")
        return False


# ============================================================================
# PUBLIC API
# ============================================================================


async def get_storage_adapter() -> HelixStorageAdapterAsync:
    """Get singleton storage adapter instance."""
    return HelixStorageAdapterAsync()


# ============================================================================
# TESTING
# ============================================================================


async def main():
    """Test the storage adapter."""
    storage = HelixStorageAdapterAsync()

    # Test archiving
    test_data = {"test": "data", "timestamp": datetime.utcnow().isoformat(), "harmony": 0.42}

    print(f"🧪 Testing storage adapter (mode: {storage.mode})")
    path = await storage.archive_json(test_data, "test_archive")
    print(f"✅ Archived to: {path}")

    # Get stats
    stats = await storage.get_storage_stats()
    print(f"📊 Storage stats: {stats}")


if __name__ == "__main__":
    asyncio.run(main())
