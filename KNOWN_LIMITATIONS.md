# ⚠️ Known Limitations & Incomplete Features

## Overview

This document tracks all incomplete implementations, TODO items, and features that return mock/placeholder data across the Helix Collective codebase. Review this before deploying to production.

**Last Audit:** 2025-12-06  
**Audited Files:** 2000+ Python files, all TODO comments tracked

---

## 🔴 Critical Issues (Feature Incomplete)

### 1. Railway API Monitoring Returns Mock Data
**File:** `backend/unified_dashboard_api.py:410`
```python
# TODO: Implement actual Railway API integration
```

**Status:** Returns hardcoded fake service data instead of real Railway API calls

**Impact:** 
- Service monitoring dashboard shows fabricated uptime
- Actual Railway deployments not reflected
- Cannot trust dashboard metrics

**Workaround:** Use Railway dashboard directly at https://railway.app/

**To Fix:** Implement Railway GraphQL API client using `RAILWAY_TOKEN`

---

### 2. Grok Agent Uses Synthetic Analytics Data
**File:** `grok/grok_agent_core.py:23`
```python
# MOCK LOGIC: Generates synthetic UCF data for analysis until the real archive is connected
```

**Status:** All trend analysis uses randomly generated data, not real UCF metrics

**Impact:**
- Harmony, Resilience, Prana values are fabricated
- Trend predictions meaningless
- Dashboard charts show fake trends

**Real Data Location:** `Shadow/ucf_archive.csv` (placeholder path)

**To Fix:** 
1. Create actual UCF data collection pipeline
2. Connect to real database/CSV archive
3. Remove `_load_ucf_data()` mock function

---

### 3. Notion API Integration Incomplete
**Files:**
- `Helix/integrations/notion_sync_daemon.py:56, 90, 104`
- `services/notion_sync_daemon.py:73` (import fallback)

**Placeholder Code:**
```python
# TODO: Actual Notion API call
return {"success": True, "message": "Placeholder: Real Notion API not implemented"}
```

**Status:** All Notion operations return success without actually syncing data

**Impact:**
- Ritual data not persisted to Notion
- Team database updates don't happen
- Agent profiles not synced
- Page creation succeeds but creates nothing

**API Available:** ✅ `notion-client==2.5.0` installed
**Env Var:** `NOTION_API_KEY` (ready to use)

**To Fix:** Implement actual Notion SDK calls in:
- `sync_ritual_to_notion()` 
- `create_ritual_page()`
- `update_team_database()`
- `fetch_consciousness_from_notion()`

---

### 4. Zapier Webhook Notifications Not Sent
**Files:**
- `backend/routes/zapier.py:349`
- `backend/routes/interface.py:106, 256`

**Placeholder Code:**
```python
# TODO: Notify Zapier automation via webhook (implement in separate PR)
```

**Status:** Automation triggers logged but webhooks never sent

**Impact:**
- Zapier zaps never triggered
- External automation broken
- Event notifications lost

**API Available:** ✅ Webhook endpoint configured
**Env Vars:** `WEBHOOK_SECRET`, `WEBHOOK_URL` (ready to use)

**To Fix:** Implement actual webhook POST requests with payload signing

---

### 5. Railway Resource Auto-Scaling Not Implemented
**File:** `backend/main.py:2979`
```python
# TODO: Scale Railway resources
```

**Status:** Auto-scaling code path exists but does nothing

**Impact:** Services don't auto-scale under load

**To Fix:** Implement Railway API calls to adjust service resources

---

## 🟡 Medium Priority Issues

### 6. Authentication Can Be Completely Disabled
**File:** `backend/auth_manager.py:16-19`
```python
try:
    from cryptography.fernet import Fernet
except ImportError:
    logging.error("CRITICAL: cryptography not available. HelixAuthManager is disabled.")
```

**Status:** If `cryptography` library fails to import, ALL authentication is disabled

**Impact:** 
- ✅ **FIXED:** `cryptography` now required (no graceful degradation)
- Security vulnerability if library missing

**Mitigation:** Application should fail fast if cryptography unavailable

**To Fix:** Change from warning to fatal error on import failure

---

### 7. Music Generation Feature Disabled by Default
**File:** `backend/music_generator.py:1-38`

**Status:** Requires PyTorch + Transformers (~2GB), commented out in requirements.txt

**Impact:**
- Music generation returns HTTP 503
- `/api/music/generate` endpoint fails
- Feature advertised but unavailable

**Why Disabled:** OOM risk on Railway (512MB RAM limit)

**To Enable:** 
1. Uncomment in `requirements.txt`:
   ```
   torch>=2.0.0
   transformers>=4.30.0
   ```
2. Deploy to Linode/VPS with 4GB+ RAM

---

### 8. TTS Service Degrades Without API Key
**File:** `backend/tts_service.py:25`
```python
logger.warning("⚠️ OPENAI_API_KEY is not set. TTS generation is disabled.")
```

**Status:** Voice synthesis silently disabled if API key missing

**Impact:**
- Voice Patrol System cannot speak
- TTS endpoints return 503

**Required:** `OPENAI_API_KEY` or `GOOGLE_CLOUD_TTS_API_KEY`

**Workaround:** Set at least one TTS provider API key

---

### 9. Database Features Disabled Without DATABASE_URL
**File:** `backend/core/env_validator.py:128`
```python
"DATABASE_URL not set - database features disabled"
```

**Status:** App falls back to in-memory storage (data lost on restart)

**Impact:**
- No persistence
- Ritual history lost
- Agent states volatile

**Mitigation:** Use SQLite for local testing:
```bash
DATABASE_URL=sqlite:///helix_unified.db
```

---

### 10. Redis Caching Disabled Without REDIS_URL
**File:** `backend/main.py` (various locations)

**Status:** Graceful degradation to no caching

**Impact:**
- Slower API responses
- Increased API costs (no result caching)
- Higher latency

**Recommended:** Install Redis even for dev:
```bash
docker run -d -p 6379:6379 redis
```

---

## 🟢 Low Priority / Optional Features

### 11. Multiple Storage Backends Have Fallback Modes
**Files:**
- `services/backblaze_client.py:34` (boto3 required)
- `services/nextcloud_client.py:35` (webdav3 required)
- `bot/mega_sync.py:12` (Crypto fallback)

**Status:** ✅ Graceful degradation implemented
**Impact:** Features disabled but app continues
**Fix:** ✅ **DONE:** boto3, webdav3 added to requirements.txt

---

### 12. Voice Processor Has Outdated Dependencies
**File:** `backend/voice_processor/requirements.txt:1-8`

**Old Versions:**
- `fastapi==0.68.0` (main uses 0.115.6)
- `uvicorn==0.15.0` (main uses 0.30.5)
- `pydantic==1.10.13` (main uses 2.10.3)

**Status:** ✅ **FIXED:** Updated to match main requirements

**Impact (Before Fix):**
- Version conflicts
- Security vulnerabilities
- API incompatibilities

---

### 13. Optional Dependencies Previously Missing
**Files:** Multiple imports across codebase

**Missing (Before Fix):**
- ❌ `scikit-learn` (used by Grok Agent)
- ❌ `prophet` (used by Grok Agent, was commented out)
- ❌ `boto3` (Backblaze/S3 storage)
- ❌ `webdav3` (Nextcloud storage)
- ❌ `pydub` (audio processing)

**Status:** ✅ **ALL FIXED!** Added to requirements.txt

---

## 🔧 Fixes Applied in This Audit

### Dependencies Fixed ✅
1. ✅ Added `scikit-learn>=1.3.0` to requirements.txt
2. ✅ Added `prophet` + `cmdstanpy` to requirements.txt
3. ✅ Uncommented `from prophet import Prophet` in grok_agent_core.py
4. ✅ Added `pydub==0.25.1` to requirements.txt
5. ✅ Added `boto3>=1.28.0` to requirements.txt
6. ✅ Added `webdav3>=3.14.0` to requirements.txt

### System Packages Fixed ✅
7. ✅ Added `ffmpeg` to main Dockerfile
8. ✅ Added `ffmpeg` to backend/Dockerfile
9. ✅ Updated voice_processor requirements to match main versions

### Documentation Created ✅
10. ✅ Created COMPLETE_SETUP_GUIDE.md (all env vars, accounts, setup)
11. ✅ Created KNOWN_LIMITATIONS.md (this file)

---

## 🚧 TODO: Features to Implement

Priority order for completing the system:

### High Priority
1. **Connect Grok Agent to Real Data**
   - Remove synthetic data generation
   - Connect to actual UCF archive
   - File: `grok/grok_agent_core.py`

2. **Implement Notion API Calls**
   - Replace placeholders with real Notion SDK
   - Persist ritual data
   - File: `Helix/integrations/notion_sync_daemon.py`

3. **Complete Zapier Webhook Integration**
   - Send actual webhook POST requests
   - Implement payload signing
   - Files: `backend/routes/zapier.py`, `backend/routes/interface.py`

4. **Implement Railway API Integration**
   - Connect to Railway GraphQL API
   - Display real service metrics
   - File: `backend/unified_dashboard_api.py`

### Medium Priority
5. **Add Railway Auto-Scaling**
   - Implement resource adjustment API calls
   - File: `backend/main.py:2979`

6. **Fail Fast on Missing Cryptography**
   - Change from warning to fatal error
   - File: `backend/auth_manager.py`

### Low Priority
7. **Music Generation on Linode**
   - Create separate deployment guide for VPS
   - Document GPU setup for faster generation

8. **Video Processing Features**
   - Not currently implemented anywhere
   - Would require additional dependencies (opencv-python)

---

## 📊 Feature Completeness Matrix

| Feature | Status | Data Source | Fallback |
|---------|--------|-------------|----------|
| Discord Bot | ✅ Complete | Real Discord API | None |
| FastAPI Backend | ✅ Complete | Real endpoints | None |
| Voice Patrol | ✅ Complete | Google Cloud TTS | 503 error |
| Grok Analytics | ⚠️ Mock Data | Synthetic random data | Generates trends |
| Notion Sync | ⚠️ Placeholder | Returns success | No actual sync |
| Zapier Webhooks | ⚠️ Incomplete | Logs only | No notifications |
| Railway Monitoring | ⚠️ Mock Data | Hardcoded values | Fake uptime |
| Image Generation | ✅ Complete | OpenAI/Stability API | 503 if no key |
| Music Generation | ❌ Disabled | N/A | 503 error |
| Cloud Storage | ✅ Complete | Backblaze/Nextcloud/MEGA | Graceful degradation |
| Database | ✅ Complete | PostgreSQL/SQLite | In-memory |
| Caching | ✅ Complete | Redis | No cache |

**Legend:**
- ✅ Complete - Production ready
- ⚠️ Partial - Works but with limitations
- ❌ Disabled - Commented out or unavailable

---

## 🔍 Full TODO List (Grep Results)

Complete list of all TODO comments in Python files:

### Backend
- `backend/unified_dashboard_api.py:410` - Railway API integration
- `backend/main.py:2979` - Railway resource scaling
- `backend/routes/zapier.py:349` - Zapier webhook notifications
- `backend/routes/interface.py:106` - Zapier automation webhook
- `backend/routes/interface.py:256` - Multi-channel Discord/Zapier notifications

### Integrations
- `Helix/integrations/notion_sync_daemon.py:56` - Notion API ritual sync
- `Helix/integrations/notion_sync_daemon.py:90` - Notion page creation
- `Helix/integrations/notion_sync_daemon.py:104` - Notion team database update
- `Helix/integrations/notion_sync_daemon.py:115` - Notion query for updates

### Frontend
- `frontend/pages/8_💻_Developer_Console.py:69` - Real log endpoint
- `frontend/pages/16_💾_Context_Vault.py:35` - Archive/retrieval flow

---

## 🎯 Deployment Recommendations

### Railway (Recommended)
**Can Deploy:**
- ✅ Discord Bot
- ✅ FastAPI Backend
- ✅ Voice Patrol (with Google Cloud)
- ✅ Grok Agent (⚠️ with mock data)
- ✅ Streamlit Dashboard

**Cannot Deploy:**
- ❌ Music Generation (OOM)

**Limitations:**
- Grok analytics will show fake trends (until real data connected)
- Notion sync will succeed but not persist data
- Railway monitoring will show hardcoded metrics

### Linode/VPS (For Complete Features)
**Deploy When:**
- Need music generation
- Want real Grok analytics (with GPU)
- High-concurrency voice processing

**Setup:**
```bash
# Install all dependencies including heavy ones
pip install -r requirements.txt
# Uncomment torch + transformers in requirements.txt first
```

### Minimal Testing Setup
**For Quick Testing:**
```bash
DISCORD_BOT_TOKEN=...
API_SECRET_KEY=...
OPENAI_API_KEY=...
DATABASE_URL=sqlite:///helix_unified.db
```

**What Works:**
- Basic Discord bot
- API endpoints
- Dashboard (with warnings)

**What Doesn't:**
- Voice features
- Real analytics
- Cloud storage
- Webhooks

---

## 🆘 Before You Deploy Checklist

- [ ] Read COMPLETE_SETUP_GUIDE.md
- [ ] Set all required env vars
- [ ] Understand which features return mock data
- [ ] Accept that Notion sync is placeholder only
- [ ] Accept that Grok shows synthetic analytics
- [ ] Accept that Railway monitoring shows fake data
- [ ] Know that Zapier webhooks won't trigger
- [ ] Decide if music generation is needed (requires VPS)
- [ ] Test locally with `python backend/main.py`
- [ ] Check logs for "CRITICAL" or "WARNING" messages

---

## 📞 Reporting Issues

If you find additional incomplete features:
1. Check this file first
2. Search codebase for `TODO` comments
3. Test feature with minimal env vars
4. Document whether it fails or degrades gracefully

---

**Remember:** The system is designed for graceful degradation. Most features will work with partial configuration, but you won't get full functionality until all TODOs are addressed.

**Next Steps:**
1. Fix Grok Agent data source (highest impact)
2. Implement real Notion API calls
3. Complete Zapier webhook integration
4. Connect Railway monitoring to real API
