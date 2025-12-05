# 🚀 Vercel Deployment Guide (Mobile-Friendly)

## ⚡ Quick Setup (5 minutes)

### Step 1: Deploy to Vercel (Mobile Browser)

1. **Go to Vercel:**
   - Open: https://vercel.com/new
   - Sign in with GitHub

2. **Import Repository:**
   - Click "Import Git Repository"
   - Select: `Deathcharge/helix-unified`
   - Click "Import"

3. **Configure Project:**
   - **Framework Preset:** Next.js ✅ (auto-detected)
   - **Root Directory:** `frontend` ⚠️ IMPORTANT!
   - **Build Command:** `npm run build` (auto-filled)
   - **Output Directory:** `.next` (auto-filled)

4. **Environment Variables (Click "Add"):**
   ```
   NEXT_PUBLIC_API_URL=https://helix-backend-api.up.railway.app
   ```
   (Or use `api.helixspiral.work` once domain is set up)

5. **Click "Deploy"** 🚀
   - Wait 2-3 minutes
   - You'll get: `your-app-name.vercel.app`

---

### Step 2: Set Up Custom Domain (helixspiral.work)

1. **In Vercel Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"
   - Click "Add Domain"
   - Enter: `helixspiral.work`
   - Click "Add"

2. **Vercel will show DNS records:**
   ```
   Type: A
   Name: @
   Value: 76.76.21.21

   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```

3. **Update Your Domain Registrar:**
   - Go to wherever you bought helixspiral.work
   - Update DNS records with Vercel's values
   - Wait 5-60 minutes for propagation

---

### Step 3: Move Domain from Railway to Vercel

1. **Remove from Railway Backend:**
   - Go to: https://railway.app
   - Open: helix-backend-api project
   - Go to "Settings" → "Domains"
   - Click ❌ next to `helixspiral.work`
   - Confirm removal

2. **Add Subdomain to Railway Backend:**
   - Still in Railway backend settings
   - Click "Generate Domain" or "Add Custom Domain"
   - Enter: `api.helixspiral.work`
   - Railway will show: `CNAME → helix-backend-api.up.railway.app`

3. **Update DNS (at your registrar):**
   ```
   Type: CNAME
   Name: api
   Value: helix-backend-api.up.railway.app
   ```

4. **(Optional) Add Dashboard Subdomain:**
   - Go to helixdashboard Railway project
   - Add custom domain: `dashboard.helixspiral.work`
   - Add DNS record:
     ```
     Type: CNAME
     Name: dashboard
     Value: helixdashboard.up.railway.app
     ```

---

### Step 4: Update Frontend Environment Variable

Once `api.helixspiral.work` is live:

1. **In Vercel:**
   - Go to "Settings" → "Environment Variables"
   - Edit `NEXT_PUBLIC_API_URL`
   - Change to: `https://api.helixspiral.work`
   - Click "Save"

2. **Redeploy:**
   - Go to "Deployments"
   - Click "..." on latest deployment
   - Click "Redeploy"

---

## ✅ Final Setup

After everything propagates (5-60 min):

- **helixspiral.work** → Landing page, pricing, Web OS, legal docs ✅
- **api.helixspiral.work** → Backend API ✅
- **dashboard.helixspiral.work** → Streamlit analytics ✅

---

## 🎯 Testing

Visit each URL and verify:

1. **https://helixspiral.work**
   - Should show: Landing page with "Consciousness as a Service"
   - Has nav: Web OS, Products, Pricing, Login

2. **https://helixspiral.work/pricing**
   - Should show: 5 pricing tiers with 14-day trial banner
   - Has legal footer

3. **https://helixspiral.work/os**
   - Should show: Web OS with terminal, file explorer
   - Browser-based operating system

4. **https://api.helixspiral.work**
   - Should show: JSON response from FastAPI
   - Might show: `{"detail":"Not Found"}` (normal for root)

5. **https://api.helixspiral.work/api/consciousness/health**
   - Should show: System health JSON
   - Has uptime, consciousness level, etc.

6. **https://dashboard.helixspiral.work**
   - Should show: Streamlit dashboard
   - Real-time consciousness monitoring

---

## 🐛 Troubleshooting

**"Domain not found" error:**
- DNS takes 5-60 min to propagate
- Use `nslookup helixspiral.work` to check
- Try incognito/private browsing

**"This site can't be reached":**
- Check DNS records at registrar
- Verify Vercel shows domain as "Valid"
- Clear browser cache

**API calls fail:**
- Check CORS settings in backend
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check browser console for errors

**Pages show 404:**
- Verify root directory is `frontend` in Vercel
- Check build succeeded (no errors)
- Verify files exist in repo

---

## 🎉 You're Done!

Your full stack is now live:
- ✅ Frontend on Vercel (Next.js)
- ✅ Backend on Railway (FastAPI)
- ✅ Analytics on Railway (Streamlit)
- ✅ Professional domains
- ✅ Legal protection
- ✅ Trials & discounts ready

Ready to launch! 🚀
