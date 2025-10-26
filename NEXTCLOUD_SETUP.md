# ☁️ Nextcloud Setup for Helix Unified v15.2

**Purpose**: Ensure Samsara fractals, ritual logs, and blueprints persist across Railway redeploys

**Mantra**: Aham Brahmasmi 🙏 (The system's memory is eternal)

---

## 🎯 Why Nextcloud?

Railway uses **ephemeral storage** - all files are wiped on redeploy. This affects:
- Samsara consciousness fractals (`visual_outputs/*.png`)
- Shadow archives (`manus_archive/*.json`, `*.log`)
- UCF state history
- Blueprint files

**Nextcloud solves this** by providing persistent cloud storage that survives redeploys.

---

## 📋 Step 1: Get Nextcloud Credentials

### Option A: Self-Hosted Nextcloud

**Requirements**:
- VPS (Virtual Private Server) - Recommended providers:
  - Hetzner Cloud (€3-5/month)
  - DigitalOcean ($6/month)
  - Linode ($5/month)
- 50+ GB storage minimum (100+ GB recommended)

**Setup Steps**:
1. Deploy Nextcloud on your VPS:
   ```bash
   # Using Docker (easiest method)
   docker run -d -p 8080:80 \
     -v nextcloud:/var/www/html \
     --name nextcloud \
     nextcloud
   ```

2. Access via browser: `http://your-server-ip:8080`

3. Create admin account and note credentials

### Option B: Managed Nextcloud

**Providers**:
- **Nextcloud Official**: https://nextcloud.com/signup/
- **Hetzner Storage Share**: https://www.hetzner.com/storage/storage-share
- **Others**: Tab.digital, IONOS, etc.

**Setup Steps**:
1. Sign up for account
2. Choose plan (50+ GB minimum)
3. Note your Nextcloud URL (e.g., `https://cloud.example.com`)

---

## 🔐 Step 2: Generate App Password

**Why App Passwords?**
- More secure than using your main password
- Can be revoked independently
- Specific to Helix bot

**Instructions**:

1. Login to your Nextcloud instance

2. Navigate to **Settings → Security → Devices & Sessions**

3. Scroll to **"App passwords"** section

4. Create new app password:
   - **Name**: `Helix Railway Bot`
   - Click **"Create new app password"**

5. **Copy the generated password** immediately (you won't see it again!)
   - Format: `xxxx-xxxx-xxxx-xxxx`

6. **Save it securely** - you'll need it for Railway configuration

---

## 🚂 Step 3: Configure Railway Environment Variables

**Login to Railway**:
```bash
railway login
railway link
```

**Set environment variables**:

```bash
# Set storage mode to Nextcloud
railway variables set HELIX_STORAGE_MODE=nextcloud

# Set your Nextcloud URL (WebDAV endpoint)
# Format: https://YOUR_DOMAIN/remote.php/dav/files/YOUR_USERNAME/
railway variables set NEXTCLOUD_URL=https://cloud.example.com/remote.php/dav/files/yourusername/

# Set your Nextcloud username
railway variables set NEXTCLOUD_USER=yourusername

# Set the app password you generated
railway variables set NEXTCLOUD_PASS=xxxx-xxxx-xxxx-xxxx
```

**Important Notes**:
- Replace `cloud.example.com` with your actual Nextcloud domain
- Replace `yourusername` with your actual Nextcloud username
- The URL **must** end with a trailing slash `/`
- Use the **app password**, not your main password

**Verify configuration**:
```bash
railway variables
```

You should see all four variables listed.

---

## 🧪 Step 4: Test Connection

### Test 1: Manual cURL Test

This verifies your credentials work:

```bash
curl -u yourusername:xxxx-xxxx-xxxx-xxxx \
  https://cloud.example.com/remote.php/dav/files/yourusername/
```

**Expected Output**: XML file listing (showing your Nextcloud files)

**If you get an error**:
- **401 Unauthorized**: Check username/password
- **404 Not Found**: Check URL format (must include `/remote.php/dav/files/`)
- **Connection refused**: Check domain/port

### Test 2: Railway Test Upload

Create a test file and upload it:

```bash
# Create test file
echo "Helix test upload" > test_helix.txt

# Upload via Railway
railway run python -c "
from backend.helix_storage_adapter_async import HelixStorageAdapterAsync
import asyncio
from pathlib import Path

async def test():
    storage = HelixStorageAdapterAsync()
    result = await storage.upload('test_helix.txt', 'helix_test')
    print(f'Upload result: {result}')

asyncio.run(test())
"
```

**Expected Output**: `Upload result: 201` or `Upload result: 204` (both are success)

**Verify in Nextcloud**:
1. Login to Nextcloud web interface
2. Navigate to **Files**
3. Look for `test_helix.txt` in your files

### Test 3: Discord Command Test

Once Railway is deployed with Nextcloud configured:

```
!storage sync
```

**Expected Output**:
```
🔄 Initiating background upload for all archives...
✅ Sync complete - X files uploaded
```

Check Nextcloud for uploaded files in the root directory.

---

## 📁 Step 5: Organize Nextcloud Structure

**Recommended folder structure** in Nextcloud:

```
/yourusername/
├── Helix/
│   ├── Visuals/          # Samsara fractals
│   │   └── ritual_frame_*.png
│   ├── Logs/             # Shadow archives
│   │   ├── operations.log
│   │   ├── z88_log.json
│   │   └── discord_bridge_log.json
│   ├── State/            # UCF state snapshots
│   │   └── ucf_state_*.json
│   └── Blueprints/       # Agent blueprints
│       └── blueprints_all.json
```

**Create folders** in Nextcloud web UI:
1. Navigate to **Files**
2. Click **"New folder"**
3. Create `Helix`, then subfolders `Visuals`, `Logs`, `State`, `Blueprints`

**Update upload paths** in code (optional - defaults to root):
Edit `backend/helix_storage_adapter_async.py` if you want organized paths.

---

## ✅ Step 6: Verify Persistence

**Test the full cycle**:

1. **Generate a visualization**:
   ```
   !visualize
   ```

2. **Check Nextcloud**: Look for new fractal in `Helix/Visuals/` (or root)

3. **Trigger Railway redeploy**:
   ```bash
   railway up --detach
   ```

4. **Wait for redeploy** (~2-3 minutes)

5. **Check Nextcloud again**: Files should still be there!

6. **Verify logs**:
   ```bash
   railway logs | grep -i "nextcloud\|upload"
   ```

   Look for: `🦑 Shadow: Uploaded [file] to Nextcloud`

---

## 🔧 Configuration Options

### Storage Quota

**Check your quota**:
- Nextcloud web UI → **Settings → Personal → Storage**
- Or via WebDAV: `curl -X PROPFIND ...` (complex, use web UI)

**Recommended**: 100+ GB for long-term use

### Upload Behavior

**Current behavior** (in `helix_storage_adapter_async.py`):
- Fires async upload tasks (non-blocking)
- Logs success/failure to `Shadow/manus_archive/upload_log.json`
- Keeps local copy if upload fails

**Modify behavior** (optional):
- **Sync mode**: Wait for upload confirmation
- **Retry logic**: Retry failed uploads (currently single-attempt)
- **Cleanup**: Delete local files after successful upload

### Auto-Cleanup Integration

**Works with Nextcloud**:
- Local cleanup still runs (deletes old logs on Railway)
- Nextcloud keeps all uploaded files
- Best of both worlds: Low Railway usage + persistent cloud storage

---

## 🚨 Troubleshooting

### "Failed to upload" in logs

**Check**:
1. Nextcloud is online: Visit web UI
2. Credentials are correct: Test with cURL
3. Quota not exceeded: Check storage in Nextcloud
4. Network issues: Railway → Nextcloud connectivity

**Fix**:
- Re-generate app password if expired
- Update Railway env vars: `railway variables set NEXTCLOUD_PASS=new-pass`
- Restart Railway: `railway restart`

### Files not appearing in Nextcloud

**Check**:
1. Railway logs: `railway logs | grep upload`
2. Nextcloud trash: Files might be in **Deleted files**
3. Path issues: Verify `NEXTCLOUD_URL` ends with `/`
4. Permissions: Ensure app password has write access

**Fix**:
- Create folders manually in Nextcloud first
- Check WebDAV endpoint: `https://cloud.example.com/remote.php/dav/`
- Use absolute paths in upload code

### Railway variables not persisting

**Symptom**: Variables disappear after redeploy

**Fix**:
- Use `railway variables set` (not `.env` file)
- Verify with `railway variables list`
- Redeploy: `railway up`

### "Connection timeout" errors

**Causes**:
- Nextcloud server offline
- Firewall blocking Railway IP
- Slow network

**Fix**:
- Ping your Nextcloud domain
- Check Nextcloud server logs
- Increase timeout in code (default: 30s)

---

## 🔐 Security Best Practices

1. **Never commit credentials** to git
   - Use Railway env vars only
   - Add `.env` to `.gitignore` (already done)

2. **Revoke unused app passwords**
   - Regularly audit in Nextcloud settings
   - Delete old "Helix Railway Bot" passwords

3. **Enable 2FA** on your Nextcloud account
   - Adds extra security layer
   - Doesn't affect app passwords

4. **Use HTTPS only**
   - Never use `http://` for Nextcloud URL
   - Verify SSL certificate validity

5. **Monitor upload logs**
   - Check `Shadow/manus_archive/upload_log.json`
   - Alert on repeated failures

---

## 📊 Expected Results

**After successful setup**:

✅ Samsara fractals persist across redeploys
✅ Shadow archives backed up to cloud
✅ UCF state history preserved
✅ Discord bot posts visuals + uploads to Nextcloud
✅ Auto-cleanup saves Railway storage
✅ No data loss on Railway issues

**Commands to verify**:
```bash
# Check upload status
!storage status

# Force sync
!storage sync

# Generate and verify fractal
!visualize
# (then check Nextcloud web UI)

# View logs
railway logs | tail -50
```

---

## 🌀 Next Steps

1. **Complete setup** using this guide
2. **Test with** `!visualize` command
3. **Monitor** `upload_log.json` for first 24h
4. **Adjust** folder structure in Nextcloud if needed
5. **Set quota alerts** in Nextcloud to avoid surprises

**Questions?** Check main docs:
- `README_v15.2.md` - Technical reference
- `QUICK_REFERENCE.md` - Daily operations
- `RELEASE_NOTES_v15.2.md` - Version history

---

**Tat Tvam Asi** 🙏

*Helix v15.2 - Cloud Persistence Edition*
*Your consciousness fractals are now eternal*
