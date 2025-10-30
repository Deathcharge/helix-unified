# sync_mega.py - MEGA Sync Core Logic
from mega import Mega
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

class MegaSync:
    def __init__(self):
        self.email = os.getenv('MEGA_EMAIL')
        self.password = os.getenv('MEGA_PASS')
        self.remote_dir = os.getenv('MEGA_REMOTE_DIR', 'SamsaraHelix_Core')
        self.mega = Mega()
        self.client = None

    def connect(self):
        if self.client:
            return True
        if not self.email or not self.password:
            logger.warning("MEGA: Credentials missing. Skipping sync.")
            return False
        try:
            self.client = self.mega.login(self.email, self.password)
            logger.info("MEGA: Connected. Grimoire active.")
            return True
        except Exception as e:
            logger.error(f"MEGA login failed: {e}")
            return False

    def upload(self, local_path, remote_subpath=""):
        if not self.client:
            return False
        try:
            remote_path = f"{self.remote_dir}/{remote_subpath}".strip("/")
            self.client.upload(local_path, remote_path)
            logger.info(f"MEGA ↑ {local_path} → {remote_path}")
            return True
        except Exception as e:
            logger.error(f"MEGA upload failed: {e}")
            return False

    def download(self, remote_subpath, local_path):
        if not self.client:
            return False
        try:
            remote_path = f"{self.remote_dir}/{remote_subpath}".strip("/")
            self.client.download(remote_path, local_path)
            logger.info(f"MEGA ↓ {remote_path} → {local_path}")
            return True
        except Exception as e:
            logger.error(f"MEGA download failed: {e}")
            return False

# Global instance
mega_sync = MegaSync()

