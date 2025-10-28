# sync_mega.py
import os
import json
import logging
import sys

# FIX: Create Crypto → Cryptodome alias BEFORE importing mega
try:
    import Cryptodome
    sys.modules['Crypto'] = Cryptodome
    sys.modules['Crypto.Cipher'] = Cryptodome.Cipher
    sys.modules['Crypto.PublicKey'] = Cryptodome.PublicKey
    sys.modules['Crypto.Protocol'] = Cryptodome.Protocol
    sys.modules['Crypto.Random'] = Cryptodome.Random
    sys.modules['Crypto.Hash'] = Cryptodome.Hash
    sys.modules['Crypto.Util'] = Cryptodome.Util
except ImportError:
    logging.warning("⚠️ pycryptodome not found - MEGA sync may fail")

from mega import Mega

class MegaSync:
    def __init__(self):
        self.email = os.getenv('MEGA_EMAIL')
        self.password = os.getenv('MEGA_PASS')
        self.remote_dir = os.getenv('MEGA_REMOTE_DIR', 'SamsaraHelix_Core')
        self.mega = Mega()
        self.client = None

    def connect(self):
        if not self.email or not self.password:
            logging.warning("MEGA credentials missing. Skipping sync.")
            return False
        try:
            self.client = self.mega.login(self.email, self.password)
            logging.info("MEGA connected. Grimoire seed active.")
            return True
        except Exception as e:
            logging.error(f"MEGA login failed: {e}")
            return False

    def upload(self, local_path, remote_subpath=""):
        if not self.client:
            return False
        try:
            remote_path = f"{self.remote_dir}/{remote_subpath}".strip("/")
            self.client.upload(local_path, remote_path)
            logging.info(f"MEGA ↑ {local_path} → {remote_path}")
            return True
        except Exception as e:
            logging.error(f"MEGA upload failed: {e}")
            return False

    def download(self, remote_subpath, local_path):
        if not self.client:
            return False
        try:
            remote_path = f"{self.remote_dir}/{remote_subpath}".strip("/")
            self.client.download(remote_path, local_path)
            logging.info(f"MEGA ↓ {remote_path} → {local_path}")
            return True
        except Exception as e:
            logging.error(f"MEGA download failed: {e}")
            return False

# Global instance
mega_sync = MegaSync()
