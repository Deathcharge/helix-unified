# mega_sync.py
import os
import time

# FIX: Create Crypto → Cryptodome alias BEFORE importing mega
import sys
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
    print("⚠️ pycryptodome not found - MEGA sync may fail")

from mega import Mega

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
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        with open(test_file, "w") as f:
            f.write(f"Grimoire test — persistence confirmed. {time.time()}")

        print(f"MEGA ↑ {test_file} → {remote_dir}/sync_test.txt")
        folder = m.find(remote_dir)
        if not folder:
            folder = m.create_folder(remote_dir)
        m.upload(test_file, folder[0])
        return True
    except Exception as e:
        print(f"MEGA sync failed: {e}")
        return False
