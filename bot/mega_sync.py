# mega_sync.py
import os
import time
from mega import Mega

# FIX: Force pycryptodome AES
import sys
sys.path.insert(0, '/usr/local/lib/python3.11/site-packages')
from Crypto.Cipher import AES

def mega_sync():
    try:
        email = os.getenv("MEGA_EMAIL")
        password = os.getenv("MEGA_PASS")
        remote_dir = os.getenv("MEGA_REMOTE_DIR", "SamsaraHelix_Core/test")

        if not email or not password:
            print("MEGA credentials missing.")
            return False

        print("MEGA connecting...")
        mega = Mega()
        m = mega.login(email, password)
        print("MEGA connected. Grimoire seed active.")

        # Test upload
        test_file = "Helix/state/sync_test.txt"
        with open(test_file, "w") as f:
            f.write(f"Grimoire test — persistence confirmed. {time.time()}")

        print(f"MEGA ↑ {test_file} → {remote_dir}/sync_test.txt")
        m.upload(test_file, m.find(remote_dir)[0] if m.find(remote_dir) else m.create_folder(remote_dir)[0])
        return True
    except Exception as e:
        print(f"MEGA sync failed: {e}")
        return False
