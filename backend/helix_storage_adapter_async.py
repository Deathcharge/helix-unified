# 🌀 Helix Unified Storage Adapter (v15.2 • Async + Fire-and-Forget)
# backend/helix_storage_adapter_async.py
# Supports: Nextcloud (WebDAV), MEGA (REST), Local fallback
# Author: Helix Collective Ω-Bridge

import os
import json
import aiohttp
import aiofiles
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

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
            async with aiohttp.ClientSession(
                auth=aiohttp.BasicAuth(self.webdav_user, self.webdav_pass)
            ) as session:
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
            "free_gb": round(usage.free / (1024 ** 3), 2),
            "latest": max((p.name for p in files), default=None)
        }

    async def auto_cleanup_if_needed(self) -> int:
        """
        Auto-prune archives if free space < threshold (default 100 GB).
        Keeps latest 20 files + all visual outputs.
        Logs cleanup events to Shadow archive.

        Returns:
            Number of files deleted
        """
        import shutil
        import glob
        import time

        # Load threshold from config (default 100 GB)
        config_path = Path("Helix/state/storage_config.json")
        threshold_gb = 100
        if config_path.exists():
            try:
                async with aiofiles.open(config_path, 'r') as f:
                    content = await f.read()
                    config = json.loads(content)
                    threshold_gb = config.get("auto_cleanup_threshold_gb", 100)
            except:
                pass

        # Check free space
        stat = shutil.disk_usage('/')
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
                "threshold_gb": threshold_gb
            }

            try:
                async with aiofiles.open(cleanup_log_path, 'a') as f:
                    await f.write(json.dumps(log_entry) + "\n")
            except Exception as e:
                print(f"⚠️  Cleanup log error: {e}")

            return deleted_count

        return 0


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
    test_data = {
        "test": "data",
        "timestamp": datetime.utcnow().isoformat(),
        "harmony": 0.42
    }

    print(f"🧪 Testing storage adapter (mode: {storage.mode})")
    path = await storage.archive_json(test_data, "test_archive")
    print(f"✅ Archived to: {path}")

    # Get stats
    stats = await storage.get_storage_stats()
    print(f"📊 Storage stats: {stats}")


if __name__ == "__main__":
    asyncio.run(main())
