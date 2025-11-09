# mega_sync.py - Helix v15.3 MEGA Integration
import os
import time
import logging
import sys

# FIX: Verify pycryptodome is installed (installs as 'Crypto', not 'Cryptodome')
try:
    import Crypto
    from Crypto.Cipher import AES
    logging.info(f"✅ pycryptodome found (version {Crypto.__version__}) - MEGA sync enabled")
except ImportError:
    logging.warning("⚠️ pycryptodome not found - MEGA sync may fail")
    Crypto = None

from mega import Mega

class MegaSync:
    """MEGA cloud storage adapter for Helix Collective."""

    def __init__(self):
        self.email = os.getenv('MEGA_EMAIL')
        self.password = os.getenv('MEGA_PASS')
        self.remote_dir = os.getenv('MEGA_REMOTE_DIR', 'SamsaraHelix_Core')
        self.mega = Mega()
        self.client = None

    def connect(self):
        """Connect to MEGA cloud storage."""
        if not self.email or not self.password:
            logging.warning("MEGA credentials missing. Skipping sync.")
            return False
        try:
            self.client = self.mega.login(self.email, self.password)
            logging.info("🌀 MEGA connected. Grimoire seed active.")
            return True
        except Exception as e:
            logging.error(f"MEGA login failed: {e}")
            return False

    def upload(self, local_path, remote_subpath=""):
        """Upload file to MEGA."""
        if not self.client:
            logging.warning("MEGA not connected. Cannot upload.")
            return False
        try:
            # Build remote path
            remote_path = f"{self.remote_dir}/{remote_subpath}".strip("/")

            # Find or create folder
            folder = self.client.find(remote_path)
            if not folder:
                # Create folder hierarchy
                folder = self.client.create_folder(remote_path)

            # Upload file
            self.client.upload(local_path, folder[0] if isinstance(folder, list) else folder)
            logging.info(f"🌀 MEGA ↑ {local_path} → {remote_path}")
            return True
        except Exception as e:
            logging.error(f"MEGA upload failed: {e}")
            return False

    def download(self, remote_subpath, local_path):
        """Download file from MEGA."""
        if not self.client:
            logging.warning("MEGA not connected. Cannot download.")
            return False
        try:
            remote_path = f"{self.remote_dir}/{remote_subpath}".strip("/")
            file = self.client.find(remote_path)
            if file:
                self.client.download(file, local_path)
                logging.info(f"🌀 MEGA ↓ {remote_path} → {local_path}")
                return True
            else:
                logging.warning(f"MEGA file not found: {remote_path}")
                return False
        except Exception as e:
            logging.error(f"MEGA download failed: {e}")
            return False

# Global instance for bot to use
mega_sync = MegaSync()
