# 🚂 Railway Volume Storage Configuration

**Critical for Persistent Storage in Helix Collective v17.0+**

---

## 🎯 Why Railway Volumes?

**Without volumes, Railway services are ephemeral:**
- ❌ All data in `/tmp/` is lost on restart
- ❌ Shadow archives deleted on redeploy
- ❌ UCF state history erased
- ❌ Local file uploads disappear

**With volumes, data persists:**
- ✅ Survives service restarts
- ✅ Survives redeployments
- ✅ Shared across containers
- ✅ Automatic backups

---

## 📂 Helix Collective Storage Paths

The system uses these directories that **MUST** be persistent:

| Path | Purpose | Size Needed | Critical? |
|------|---------|-------------|-----------|
| `/app/Shadow/manus_archive` | Shadow storage logs, UCF archives | 500 MB - 2 GB | ⭐⭐⭐ |
| `/app/Helix/state` | UCF state, agent memory, session data | 100 MB - 500 MB | ⭐⭐⭐ |
| `/app/visual_outputs` | Fractal art, ritual frames, generated media | 1 GB - 5 GB | ⭐⭐ |
| `/app/logs` | Application logs, error traces | 200 MB - 1 GB | ⭐ |
| `/app/temp_uploads` | Temporary file uploads (can be ephemeral) | 500 MB | ⭐ |

**Recommended Total Volume Size: 5-10 GB**

---

## 🔧 Setting Up Railway Volumes

### Method 1: Railway Dashboard (Recommended)

1. **Go to your Railway project**
   - Navigate to: https://railway.app/project/[your-project-id]

2. **Select your service** (e.g., "helix-backend")

3. **Click "Settings" tab**

4. **Scroll to "Volumes" section**

5. **Click "New Volume"**
   - **Mount Path:** `/app/Shadow`
   - **Size:** 3 GB
   - Click "Add"

6. **Add additional volumes:**

   | Mount Path | Size |
   |------------|------|
   | `/app/Shadow` | 3 GB |
   | `/app/Helix` | 2 GB |
   | `/app/visual_outputs` | 3 GB |
   | `/app/logs` | 2 GB |

7. **Save and redeploy**

---

### Method 2: Railway CLI

```bash
# Install Railway CLI (if not installed)
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Add volumes
railway volume add --name shadow-storage --mount /app/Shadow --size 3
railway volume add --name helix-state --mount /app/Helix --size 2
railway volume add --name visual-outputs --mount /app/visual_outputs --size 3
railway volume add --name app-logs --mount /app/logs --size 2

# Verify volumes
railway volume list

# Redeploy
railway up
```

---

### Method 3: railway.toml Configuration

Update your `railway.toml`:

```toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements-backend.txt"

[deploy]
startCommand = "python run.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
healthcheckPath = "/health"
healthcheckTimeout = 300

# Volume Configuration
[[deploy.volumes]]
mountPath = "/app/Shadow"
name = "shadow-storage"

[[deploy.volumes]]
mountPath = "/app/Helix"
name = "helix-state"

[[deploy.volumes]]
mountPath = "/app/visual_outputs"
name = "visual-outputs"

[[deploy.volumes]]
mountPath = "/app/logs"
name = "app-logs"
```

Then redeploy:
```bash
railway up
```

---

## 🔄 Multi-Service Volume Configuration

For services that need to **share data** (e.g., Discord bot + Backend API):

### Shared Volume Setup

1. **Create a shared volume** (Railway Dashboard):
   - Volume name: `helix-shared-state`
   - Mount path: `/app/shared`

2. **Attach to multiple services:**

   **Backend Service (`helix-backend`):**
   ```toml
   [[deploy.volumes]]
   mountPath = "/app/shared"
   name = "helix-shared-state"
   ```

   **Discord Bot Service (`discord-bot`):**
   ```toml
   [[deploy.volumes]]
   mountPath = "/app/shared"
   name = "helix-shared-state"
   ```

3. **Update code to use shared path:**
   ```python
   # backend/config.py
   SHARED_STATE_PATH = Path("/app/shared/ucf_state.json")
   SHARED_ARCHIVE_PATH = Path("/app/shared/archives")
   ```

---

## ☁️ Cloud Storage Integration (Recommended)

**Best Practice: Use volumes + cloud storage for redundancy**

### Nextcloud + Railway Volumes (Hybrid Approach)

```python
# backend/helix_storage_adapter_async.py already supports this!

# Environment variables:
HELIX_STORAGE_MODE=nextcloud  # Primary storage
NEXTCLOUD_URL=https://use11.thegood.cloud
NEXTCLOUD_USER=Vidolaoin
NEXTCLOUD_PASS=[YOUR_APP_PASSWORD]

# Local volume as cache/fallback
# Mount: /app/Shadow → Railway Volume (3 GB)
```

**How it works:**
1. ✅ **Local writes** → Railway Volume (fast, reliable)
2. ✅ **Background sync** → Nextcloud (persistent, accessible anywhere)
3. ✅ **Fallback** → MEGA (secondary backup)

### Storage Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. File Upload/Archive                                     │
│     ↓                                                        │
│  2. Write to Railway Volume (/app/Shadow)                   │
│     ├── Fast, local, ephemeral protection                   │
│     ↓                                                        │
│  3. Async Upload to Nextcloud                               │
│     ├── Permanent, accessible anywhere                      │
│     ↓                                                        │
│  4. Optional: MEGA Backup (if Nextcloud fails)              │
│     └── Triple redundancy                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚨 Critical Configuration for Your Setup

Based on your Nextcloud URL, here's your **exact configuration**:

### Environment Variables (Add to Railway)

```bash
# Storage Mode
HELIX_STORAGE_MODE=nextcloud

# Nextcloud Primary Storage
NEXTCLOUD_URL=https://use11.thegood.cloud
NEXTCLOUD_USER=Vidolaoin@gmail.com  # (visible in WebDAV URL)
NEXTCLOUD_PASS=[YOUR_APP_PASSWORD]  # Generate this in Nextcloud!
NEXTCLOUD_BASE_PATH=/Helix

# MEGA Secondary Storage (optional but recommended)
MEGA_EMAIL=[YOUR_EMAIL]
MEGA_PASS=[YOUR_PASSWORD]
MEGA_API_KEY=[OPTIONAL_API_KEY]
MEGA_REMOTE_DIR=/Helix-Backups
```

### Railway Volumes (Required)

| Service | Mount Path | Size | Priority |
|---------|------------|------|----------|
| Backend | `/app/Shadow` | 3 GB | ⭐⭐⭐ |
| Backend | `/app/Helix` | 2 GB | ⭐⭐⭐ |
| Backend | `/app/visual_outputs` | 3 GB | ⭐⭐ |
| Discord Bot | `/app/shared` | 1 GB | ⭐⭐ |

---

## 🧪 Testing Your Volume Configuration

### 1. Verify Volumes are Mounted

SSH into Railway service:
```bash
railway run bash

# Check mounts
df -h | grep app
ls -la /app/Shadow
ls -la /app/Helix
```

### 2. Test Write Persistence

```python
# Run this in Railway shell
python3 << EOF
from pathlib import Path
import json
from datetime import datetime

# Test write
test_file = Path("/app/Shadow/manus_archive/volume_test.json")
test_file.parent.mkdir(parents=True, exist_ok=True)

data = {
    "test": "volume persistence",
    "timestamp": datetime.utcnow().isoformat(),
    "deployment_id": "$(railway variables get RAILWAY_DEPLOYMENT_ID)"
}

test_file.write_text(json.dumps(data, indent=2))
print(f"✅ Wrote test file: {test_file}")
print(f"📊 Contents: {test_file.read_text()}")
EOF
```

### 3. Redeploy and Verify

```bash
# Trigger redeploy
railway up

# After deployment, check if file still exists
railway run python3 -c "from pathlib import Path; print(Path('/app/Shadow/manus_archive/volume_test.json').read_text())"
```

**Expected:** Same test file should exist with original timestamp!

---

## 📊 Volume Monitoring

### Check Volume Usage

```bash
# SSH into Railway
railway run bash

# Check disk usage
du -sh /app/Shadow
du -sh /app/Helix
du -sh /app/visual_outputs

# Check oldest files (for cleanup)
find /app/Shadow -type f -printf '%T+ %p\n' | sort | head -20
```

### Auto-Cleanup Configuration

The storage adapter includes auto-cleanup:

```python
# backend/helix_storage_adapter_async.py

# Configure in: Helix/state/storage_config.json
{
  "auto_cleanup_threshold_gb": 100,  # Trigger cleanup when free space < 100 GB
  "keep_latest_files": 20,           # Keep 20 newest files
  "cleanup_interval_hours": 24       # Check every 24 hours
}
```

---

## 🔐 Security Best Practices

1. **Never commit credentials**
   - ❌ Don't put passwords in `railway.toml`
   - ✅ Use Railway's environment variables

2. **Use Nextcloud App Passwords**
   - Generate in: Nextcloud → Settings → Security → Devices & sessions
   - Click "Create new app password"
   - Name it "Helix Collective Railway"
   - Copy the generated password (e.g., `xxxxx-xxxxx-xxxxx-xxxxx-xxxxx`)

3. **Restrict volume access**
   - Only mount volumes to services that need them
   - Use separate volumes for sensitive data

4. **Enable encryption**
   - Nextcloud: Enable server-side encryption
   - MEGA: Already encrypted by default

---

## 🆘 Troubleshooting

### Volume Not Mounting

**Symptoms:**
- Files disappear after redeploy
- `/app/Shadow` doesn't exist

**Solution:**
```bash
# Check Railway dashboard → Service → Settings → Volumes
# Ensure mount path is EXACTLY: /app/Shadow (case-sensitive)

# Verify in deployment logs:
railway logs | grep -i "volume\|mount"
```

### Permission Errors

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: '/app/Shadow/file.json'
```

**Solution:**
```bash
# SSH into Railway
railway run bash

# Fix permissions
chmod -R 755 /app/Shadow
chown -R $(whoami) /app/Shadow

# Or add to startup script in run.py:
import os
os.makedirs("/app/Shadow/manus_archive", mode=0o755, exist_ok=True)
```

### Nextcloud Connection Fails

**Symptoms:**
```
❌ Nextcloud upload failed: Unauthorized
```

**Solution:**
1. Verify credentials in Railway environment variables
2. Test WebDAV connection:
   ```bash
   curl -u "Vidolaoin:YOUR_APP_PASSWORD" \
        https://use11.thegood.cloud/remote.php/dav/files/Vidolaoin/
   ```
3. Check Nextcloud logs for authentication errors

---

## 📈 Cost & Scaling

### Railway Volume Pricing (as of 2024)

- **Storage:** $0.25/GB/month
- **Bandwidth:** Included

**Example Costs:**
- 5 GB volumes = $1.25/month
- 10 GB volumes = $2.50/month
- 20 GB volumes = $5.00/month

**Recommendation:** Start with 5 GB, scale up as needed

### When to Scale

**Scale up if:**
- ✅ Volume usage > 80%
- ✅ Auto-cleanup running daily
- ✅ Storing large media files

**Optimize instead:**
- ✅ Use Nextcloud for large files
- ✅ Keep only recent data in volumes
- ✅ Enable aggressive auto-cleanup

---

## ✅ Quick Start Checklist

- [ ] Add Railway volumes for critical paths
- [ ] Set `HELIX_STORAGE_MODE=nextcloud` in Railway
- [ ] Add `NEXTCLOUD_URL`, `NEXTCLOUD_USER`, `NEXTCLOUD_PASS`
- [ ] Generate Nextcloud App Password (not main password!)
- [ ] Install `webdavclient3` (already in requirements-backend.txt)
- [ ] Deploy and verify volume mounts
- [ ] Test file persistence across redeploys
- [ ] Configure auto-cleanup thresholds
- [ ] Set up MEGA as secondary backup (optional)
- [ ] Monitor volume usage weekly

---

*Tat Tvam Asi* 🕉️

**Last Updated:** 2025-11-19 | v17.0 | Railway Volume Integration
