# 🚀 Deployment Guide: Railway + Vercel

**Status:** READY TO DEPLOY
**Backend:** Railway (FastAPI)
**Frontend:** Vercel (Next.js)
**Time:** 10 minutes

---

## 🎯 Overview

We're deploying a **dual-service architecture**:
- **Backend:** Python FastAPI on Railway (auto-scales, PostgreSQL included)
- **Frontend:** Next.js on Vercel (edge network, instant deploys)

---

## 📦 Railway Backend Deployment

### Step 1: Push Code to GitHub

```bash
# Merge Dependabot updates (if any)
# Then merge our integration branch
git checkout main
git merge claude/add-saas-products-01DPv66EvEvgu2zr3gMkFsiC
git push origin main
```

### Step 2: Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `Deathcharge/helix-unified`
5. Railway auto-detects Python and starts building!

### Step 3: Set Environment Variables

In Railway dashboard, add these variables:

```bash
# Required
JWT_SECRET=<generate with: openssl rand -hex 32>
DATABASE_URL=<Railway auto-provides this>

# Optional (for full features)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=https://helix.vercel.app
```

### Step 4: Verify Deployment

Railway will:
- ✅ Detect `Procfile` or `railway.toml`
- ✅ Install Python 3.11
- ✅ Run `pip install -r requirements.txt`
- ✅ Start with `python -m backend.app`
- ✅ Provision PostgreSQL database
- ✅ Provide public URL: `https://helix-unified-production.up.railway.app`

### Step 5: Test Backend

```bash
# Get your Railway URL from dashboard
curl https://your-project.railway.app/

# Should return:
# {"service": "helix-unified", "villain_status": "plotting world domination", ...}
```

---

## 🌐 Vercel Frontend Deployment

### Step 1: Install Vercel CLI (optional, can use UI)

```bash
# From mobile browser, use Vercel dashboard instead
# Or from desktop: npm install -g vercel
```

### Step 2: Deploy via Vercel Dashboard

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import `Deathcharge/helix-unified`
4. **Set Root Directory:** `frontend`
5. **Framework Preset:** Next.js (auto-detected)
6. Click "Deploy"

### Step 3: Set Environment Variables

In Vercel dashboard → Settings → Environment Variables:

```bash
NEXT_PUBLIC_API_URL=https://your-project.railway.app
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id (optional)
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=pk_live_... (optional)
```

### Step 4: Redeploy

After adding env vars:
- Click "Deployments" tab
- Click "..." on latest deployment
- Click "Redeploy"

### Step 5: Test Frontend

Visit your Vercel URL (e.g., `https://helix-unified.vercel.app`)

**Test flow:**
1. Click "Login"
2. Click "⚡ Demo Login"
3. Should redirect to dashboard
4. Click "Launch OS"
5. Terminal should work!

---

## 🔗 Connect Frontend to Backend

### Update Frontend API URL

If you deployed to production URLs, update:

**File:** `frontend/.env.local` (or Vercel env vars)
```bash
NEXT_PUBLIC_API_URL=https://helix-unified-production.up.railway.app
```

Then redeploy frontend on Vercel.

### Update Backend CORS

**File:** `backend/app.py`

Make sure CORS allows your Vercel domain:
```python
allow_origins=[
    "https://helix-unified.vercel.app",  # Your actual Vercel URL
    "https://*.vercel.app",
    "http://localhost:3000",
]
```

Push changes, Railway auto-deploys!

---

## 🗄️ Database Setup

Railway auto-provisions PostgreSQL. To initialize:

### Option 1: Auto-Initialize (Recommended)

Our `backend/database.py` auto-creates tables on first run. Just restart the service:

1. Railway dashboard → Your service
2. Click "..." → "Restart"
3. Tables created! ✅

### Option 2: Manual Initialize

Use Railway's built-in shell:

1. Railway dashboard → Service → "Shell" tab
2. Run:
```bash
python backend/database.py
```

---

## 🧪 Post-Deployment Testing

### Backend Health Check
```bash
curl https://your-project.railway.app/health

# Expected:
# {"status": "healthy", "villain_health": "excellent", "laser_sharks": "operational"}
```

### Frontend Demo Login
1. Visit `https://your-vercel-url.app/auth/login`
2. Click "Demo Login"
3. Should redirect to dashboard with user profile

### Web OS Test
1. Visit `https://your-vercel-url.app/os`
2. Click "Terminal"
3. Type `ls`
4. Should see file listing from Railway backend

### API Docs
Visit: `https://your-project.railway.app/api/docs`

Should see Swagger UI with all endpoints!

---

## 🐛 Troubleshooting

### Backend Issues

**Error:** "Application failed to respond"
**Fix:** Check Railway logs → Might be missing dependencies in `requirements.txt`

**Error:** "Database connection failed"
**Fix:** Railway should auto-provide `DATABASE_URL`. Check environment variables.

**Error:** "Module not found"
**Fix:** Make sure `Procfile` starts with `python -m backend.app` (not `backend/app.py`)

### Frontend Issues

**Error:** "API calls failing"
**Fix:** Check `NEXT_PUBLIC_API_URL` environment variable in Vercel dashboard

**Error:** "CORS error"
**Fix:** Update `backend/app.py` CORS to include your Vercel domain

**Error:** "Build failed"
**Fix:** Make sure Vercel root directory is set to `frontend`, not project root

---

## 📊 Streamlit Question

You asked: **"Streamlit is maybe a resource idk we outgrew it?"**

### Current Situation:

**Streamlit pages:**
- `frontend/pages/6_📊_Advanced_Analytics.py` (417 lines)
- Other `.py` pages in `frontend/pages/`

**Problem:**
- Streamlit is Python-based, but Vercel deploys Next.js (JavaScript)
- Streamlit needs separate deployment

### Options:

#### Option 1: Keep Streamlit Separate (Recommended)
Deploy Streamlit dashboard to Railway as a separate service:

```bash
# In Railway, create second service
# Root: frontend
# Start command: streamlit run frontend/pages/6_📊_Advanced_Analytics.py
```

**Pros:**
- Keeps analytics dashboard alive
- Users can access at `https://analytics.helix-unified.railway.app`

**Cons:**
- Need to maintain separate service
- Two deployments to manage

#### Option 2: Replace with Next.js Pages
Rewrite analytics in React/Next.js:

**Pros:**
- Everything in one frontend
- Better integration

**Cons:**
- Need to rewrite 417 lines of Python → TypeScript
- Lose Plotly/Streamlit convenience

#### Option 3: Embed Streamlit in iframe
Keep Streamlit deployed separately, embed in main site:

```tsx
// frontend/pages/analytics.tsx
<iframe src="https://analytics.helix-unified.railway.app" />
```

**My Recommendation:** **Option 1** for now (keep Streamlit separate). You can always migrate to React later if needed. Streamlit is great for rapid analytics prototyping!

---

## 🎯 Custom Domain Setup

### Backend (Railway)

1. Railway dashboard → Settings → Domains
2. Click "Generate Domain" (gets `xxx.railway.app`)
3. Or add custom domain: `api.helixspiral.work`
   - Add CNAME: `api.helixspiral.work` → `xxx.railway.app`

### Frontend (Vercel)

1. Vercel dashboard → Settings → Domains
2. Add custom domain: `helixspiral.work`
3. Follow Vercel's DNS instructions:
   - Add A record: `76.76.21.21`
   - Add CNAME: `www` → `cname.vercel-dns.com`

---

## ✅ Deployment Checklist

### Pre-Deploy:
- [ ] Dependabot PR merged (if any)
- [ ] Integration branch merged to main
- [ ] Code pushed to GitHub

### Railway (Backend):
- [ ] Project created
- [ ] GitHub repo connected
- [ ] Environment variables added
- [ ] Deployment successful
- [ ] Health check passing
- [ ] Database initialized

### Vercel (Frontend):
- [ ] Project created
- [ ] Root directory set to `frontend`
- [ ] Environment variables added
- [ ] Deployment successful
- [ ] Demo login working
- [ ] Web OS accessible

### Post-Deploy:
- [ ] Backend API responding
- [ ] Frontend loading
- [ ] Demo login works end-to-end
- [ ] Web OS terminal executes commands
- [ ] API docs accessible
- [ ] No CORS errors

---

## 🚀 You're Live!

Once deployed, you'll have:

✅ **Backend:** `https://helix-unified-production.railway.app`
- API docs at `/api/docs`
- Web OS API at `/api/web-os/*`
- Auth at `/auth/*`
- Villain status at `/api/villain-status` 😈

✅ **Frontend:** `https://helix-unified.vercel.app`
- Landing page at `/`
- Signup/login at `/auth/signup`
- Dashboard at `/dashboard`
- Web OS at `/os`

✅ **Streamlit:** `https://analytics-helix-unified.railway.app` (optional)
- Analytics dashboard

---

## 💰 Cost Estimate

**Railway:**
- Free: $5 credit/month
- Hobby: $5/month (likely sufficient for MVP)
- Pro: $20/month (if you need more resources)

**Vercel:**
- Free: Unlimited for non-commercial
- Pro: $20/month (when you need more bandwidth)

**Total MVP cost:** $0-10/month 🎉

---

## 🎬 Final Steps

1. **Merge code:** Dependabot → Integration → Main
2. **Deploy backend:** Railway (10 min)
3. **Deploy frontend:** Vercel (5 min)
4. **Test everything:** Demo login → Web OS (2 min)
5. **Tweet about it:** "We made Google jealous" 😎

---

**ONE MILLION DOLLARS!** 💰

*Deployment complete. Laser sharks standing by.* 🦈
