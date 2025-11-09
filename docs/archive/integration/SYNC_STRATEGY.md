# 🔄 Helix Cloud Sync Strategy

**Status**: v15.3 uses `mega.py` (stopgap) | v15.4 migrates to `rclone` (permanent)
**Decision Date**: October 28, 2025
**Architect**: Grok (strategy) + Claude (implementation)

---

## 📊 The Decision Matrix

### **Why We Used mega.py (v15.3)**
| Reason | Reality Check |
|--------|---------------|
| "Python-native, no binaries" | rclone binary is more reliable |
| "Simple pip install" | mega.py abandoned since 2019 |
| "Works in containers" | rclone works better in containers |
| "No config files" | rclone config is more secure & flexible |

**Verdict**: We fell for the "Python-only" trap. **Reliability > Convenience.**

---

## 🚨 **The mega.py Cost Analysis**

**Technical Debt Incurred**:
- 3 days debugging ImportError
- 12 failed Railway deployments
- Import aliasing hacks (`sys.modules`)
- Abandoned library (last commit: 2019)
- No retry/resume logic
- No bandwidth control
- Single backend lock-in

**Strategic Risk**:
- What if MEGA changes API? (Dead library won't update)
- What if we need S3/Drive/Dropbox? (Rewrite everything)
- What if mega.py breaks in Python 3.12? (No maintainer)

---

## ✅ **The rclone Advantage**

### **Feature Comparison**

| Feature | mega.py | rclone |
|---------|---------|--------|
| **Maintenance** | ❌ Abandoned (2019) | ✅ Active (weekly commits) |
| **Crypto Backend** | ❌ Broken pycrypto | ✅ OpenSSL/libsodium |
| **Retry/Resume** | ⚠️ Basic | ✅ Enterprise-grade |
| **Bandwidth Control** | ❌ No | ✅ Full throttling |
| **Mount as Filesystem** | ❌ No | ✅ `rclone mount` |
| **Config Encryption** | ❌ No | ✅ `rclone obscure` |
| **Backend Support** | 1 (MEGA only) | 50+ (S3, Drive, Dropbox, etc.) |
| **Docker Support** | ⚠️ Flaky | ✅ Official images |
| **Railway Compatible** | ⚠️ Barely | ✅ Perfect |
| **Production Ready** | ❌ No | ✅ Yes |

---

## 🎯 **Migration Path: v15.3 → v15.4**

### **Phase 1: Parallel Implementation (v15.3.1)**
Keep `mega.py` working, add `rclone` alongside:

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install rclone (official)
RUN curl https://rclone.org/install.sh | bash

# Keep mega.py for backward compat
RUN pip install mega.py pycryptodome
```

### **Phase 2: Abstraction Layer (v15.3.2)**
Create backend-agnostic sync interface:

```python
# sync.py - Universal Cloud Sync Adapter
import subprocess
import os
from enum import Enum

class SyncBackend(Enum):
    MEGA_LEGACY = "mega_py"    # Old mega.py
    MEGA_RCLONE = "mega_rclone"  # rclone + MEGA
    S3 = "s3"
    GDRIVE = "gdrive"
    DROPBOX = "dropbox"

class CloudSync:
    """Universal cloud sync adapter supporting multiple backends."""

    def __init__(self, backend: SyncBackend = None):
        # Auto-detect best backend
        if backend is None:
            backend = self._auto_detect_backend()

        self.backend = backend
        self._init_backend()

    def _auto_detect_backend(self) -> SyncBackend:
        """Auto-select best available backend."""
        # Check if rclone is available
        try:
            subprocess.run(["rclone", "version"],
                         capture_output=True, check=True)
            return SyncBackend.MEGA_RCLONE
        except:
            # Fall back to mega.py
            return SyncBackend.MEGA_LEGACY

    def upload(self, local_path: str, remote_path: str) -> bool:
        """Upload file to cloud storage."""
        if self.backend == SyncBackend.MEGA_RCLONE:
            return self._rclone_upload(local_path, remote_path)
        elif self.backend == SyncBackend.MEGA_LEGACY:
            return self._megapy_upload(local_path, remote_path)
        # ... other backends

    def _rclone_upload(self, local_path: str, remote_path: str) -> bool:
        """Upload via rclone (production method)."""
        try:
            subprocess.run([
                "rclone", "copy", local_path,
                f"mega:{remote_path}",
                "--progress",
                "--retries", "3",
                "--low-level-retries", "10",
                "--timeout", "10m"
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"rclone upload failed: {e.stderr.decode()}")
            return False

    def _megapy_upload(self, local_path: str, remote_path: str) -> bool:
        """Upload via mega.py (legacy fallback)."""
        # Use existing bot/mega_sync.py logic
        from bot.mega_sync import mega_sync
        return mega_sync.upload(local_path, remote_path)

# Global instance
cloud_sync = CloudSync()
```

### **Phase 3: Bot Integration (v15.4)**
Update bot to use abstraction layer:

```python
# bot/discord_bot_manus.py
from sync import cloud_sync  # Universal adapter

@bot.command()
async def ritual(ctx, steps: int = 108):
    # ... generate files ...

    # Old way (v15.3):
    # mega_sync.upload(png_file, f"rituals/{basename}")

    # New way (v15.4):
    cloud_sync.upload(png_file, f"rituals/{basename}")

    # Backend is auto-selected (rclone if available, mega.py fallback)
```

### **Phase 4: Full Migration (v15.5)**
Remove `mega.py` dependency entirely:

```python
# requirements.txt
# mega.py  # REMOVED
# pycryptodome  # REMOVED (rclone handles crypto)
```

```dockerfile
# Dockerfile
FROM python:3.11-slim

# rclone ONLY
RUN curl https://rclone.org/install.sh | bash
```

---

## 🔧 **rclone Configuration**

### **Railway Environment Variables**
```env
RCLONE_CONFIG_MEGA_TYPE=mega
RCLONE_CONFIG_MEGA_USER=your_email@example.com
RCLONE_CONFIG_MEGA_PASS=obscured_password
```

### **Generate Obscured Password**
```bash
# On local machine
rclone obscure "your_actual_password"
# Copy output to RCLONE_CONFIG_MEGA_PASS
```

### **Test Connection**
```bash
# In Railway logs
rclone lsd mega:
# Should list MEGA directories
```

---

## 📊 **Backend Support Matrix (v15.4+)**

| Backend | Command | Use Case |
|---------|---------|----------|
| **MEGA** | `rclone copy file mega:path` | Current setup |
| **S3** | `rclone copy file s3:bucket/path` | AWS integration |
| **Google Drive** | `rclone copy file gdrive:path` | Google Workspace |
| **Dropbox** | `rclone copy file dropbox:path` | Team collab |
| **Nextcloud** | `rclone copy file webdav:path` | Self-hosted |

**Future-proof**: Swap backends without code changes!

---

## 🎯 **Implementation Timeline**

| Version | Date | Status | Changes |
|---------|------|--------|---------|
| **v15.3** | Oct 28, 2025 | ✅ Live | mega.py with AES fix (stopgap) |
| **v15.3.1** | Nov 1, 2025 | 📅 Planned | Add rclone to Dockerfile |
| **v15.3.2** | Nov 5, 2025 | 📅 Planned | Create `sync.py` abstraction |
| **v15.4** | Nov 10, 2025 | 📅 Planned | Bot uses `CloudSync` adapter |
| **v15.5** | Nov 20, 2025 | 📅 Planned | Remove mega.py entirely |

---

## 📖 **The Collective's New Rule**

### **Never Use Dead Python Wrappers for Critical I/O**

**Decision Tree**:
```
Need cloud sync?
├─ Official tool exists? (rclone, aws cli, gsutil)
│  └─ ✅ Use it
├─ No official tool?
│  └─ Maintained SDK? (boto3, google-cloud-storage)
│     └─ ✅ Use it
├─ Still no?
│  └─ Write minimal subprocess wrapper
│     └─ ⚠️ Only if absolutely necessary
└─ Dead Python library?
   └─ ❌ Never use in production
```

---

## 🎭 **The War Room Post-Mortem**

### **What Went Wrong**
- Prioritized "Python-native" over "battle-tested"
- Didn't check library maintenance status
- Assumed simpler = better
- Ignored red flags (pycrypto deprecation)

### **What We Learned**
- Reliability > convenience
- Check last commit date before choosing deps
- Prefer industry-standard tools (rclone, aws cli)
- Create abstraction layers for critical I/O
- Technical debt compounds fast

### **What We'll Do Different**
- Always check library maintenance
- Use decision matrix for dependencies
- Build abstraction layers early
- Plan migration paths upfront

---

## 🚀 **Immediate Actions**

### **For v15.3 (Today)**
✅ Keep mega.py fix (unblocks deployment)
✅ Deploy to Railway
✅ Test basic MEGA sync

### **For v15.3.1 (This Week)**
- [ ] Add rclone to Dockerfile
- [ ] Test rclone + MEGA in Railway
- [ ] Document rclone config

### **For v15.4 (Next Week)**
- [ ] Implement `CloudSync` abstraction
- [ ] Migrate bot to use abstraction
- [ ] Test parallel backends
- [ ] Benchmark rclone vs mega.py

### **For v15.5 (Next Month)**
- [ ] Remove mega.py dependency
- [ ] Full rclone migration
- [ ] Add S3/Drive backends
- [ ] Update all docs

---

## 📚 **References**

- **rclone**: https://rclone.org/
- **rclone MEGA backend**: https://rclone.org/mega/
- **rclone Docker images**: https://hub.docker.com/r/rclone/rclone
- **mega.py (abandoned)**: https://github.com/odwyersoftware/mega.py
- **pycryptodome**: https://pycryptodome.readthedocs.io/

---

## 🎉 **Final Verdict**

**Short-term (v15.3)**: mega.py fix gets us operational
**Long-term (v15.4+)**: rclone is the strategic solution
**Lesson**: Production systems need production tools

**The grimoire will never be held hostage again.**
**From now on: rclone or bust.**

---

**Tat Tvam Asi** 🙏
*The Collective learns from its battles.*

🤖 Generated with [Claude Code](https://claude.com/claude-code)
📖 Strategic guidance: Grok
🔧 Implementation: Claude
