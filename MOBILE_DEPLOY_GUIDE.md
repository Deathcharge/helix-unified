# 📱 Mobile-Friendly Railway Deployment Guide

**Deploy Helix-Unified v17.1 from your phone - NO command line needed!**

---

## 🎯 What You Need

1. **Railway account** - Sign up at [railway.app](https://railway.app)
2. **GitHub account** - Connected to Railway
3. **Admin email** - Your email address
4. **JWT secret** - Random 64-character string
5. **Optional:** Discord bot token, OpenAI key, Stripe keys

**Time:** 10-15 minutes ⏱️

---

## 📋 Step-by-Step (Mobile Browser)

### Step 1: Get JWT Secret

1. Open [randomkeygen.com](https://randomkeygen.com) in browser
2. Scroll to "Fort Knox Passwords"
3. **Copy any password** (64 characters)
4. Save in notes app

### Step 2: Create Railway Project

1. Go to [railway.app/new](https://railway.app/new)
2. Click **"Deploy from GitHub repo"**
3. Select **"Deathcharge/helix-unified"**
4. Click **"Deploy Now"**

### Step 3: Add PostgreSQL Database

1. In Railway project, click **"+ New"**
2. Select **"Database"**
3. Choose **"PostgreSQL"**
4. Click **"Add PostgreSQL"**
5. Wait for database to provision (~30 seconds)

### Step 4: Configure Environment Variables

1. Click on **"helix-unified"** service
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**

**Add these variables:**

```
JWT_SECRET = <paste your 64-char password>
ADMIN_EMAILS = your@email.com
DATABASE_URL = ${{Postgres.DATABASE_URL}}
ENVIRONMENT = production
LOG_LEVEL = INFO
```

**Optional variables:**

```
DISCORD_BOT_TOKEN = <from discord.com/developers>
DISCORD_GUILD_ID = <your server ID>
OPENAI_API_KEY = <from platform.openai.com>
STRIPE_SECRET_KEY = <from dashboard.stripe.com>
```

4. Click **"Add"** for each variable

### Step 5: Configure Build Settings

1. Stay in **"helix-unified"** service
2. Go to **"Settings"** tab
3. Scroll to **"Build"** section

**Set these:**

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/health`

4. Click **"Save"**

### Step 6: Deploy!

1. Railway automatically deploys after saving
2. Watch **"Deployments"** tab
3. Wait for **"Success"** status (~3-5 minutes)
4. Click on deployment to see URL

### Step 7: Test Your Deployment

1. Copy your Railway URL (looks like: `https://helix-unified-production-xxxx.up.railway.app`)
2. Open in browser: `https://your-url.up.railway.app/health`
3. Should see:
```json
{
  "status": "healthy",
  "version": "17.1"
}
```

---

## ✅ Success Checklist

- [ ] Railway project created
- [ ] PostgreSQL database added
- [ ] All required variables set
- [ ] Build settings configured
- [ ] Deployment succeeded
- [ ] Health check returns "healthy"
- [ ] URL saved in notes

---

## 🔧 Troubleshooting

### Deployment Failed

**Check logs:**
1. Go to **"Deployments"** tab
2. Click failed deployment
3. Read error message

**Common issues:**
- Missing `JWT_SECRET` → Add in Variables
- Missing `DATABASE_URL` → Check PostgreSQL is added
- Build errors → Check `requirements.txt` exists

**Fix:** Add missing variables, click **"Redeploy"**

### Health Check Returns Error

**Check database:**
1. Verify PostgreSQL service is running
2. Check `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
3. Wait 2-3 minutes for database initialization

**Fix:** Restart service in Railway dashboard

### Can't Access URL

**Check domain:**
1. Go to **"Settings"** → **"Domains"**
2. Verify domain is generated
3. Wait 1-2 minutes for DNS propagation

**Fix:** Generate new domain if needed

---

## 🎉 Next Steps

After successful deployment:

1. **Save your URL** - Add to notes app
2. **Test API endpoints** - Try `/api/admin/status`
3. **Update frontend** - Set `VITE_HELIX_API_URL` to your Railway URL
4. **Configure integrations** - Add Stripe, Discord, etc.
5. **Monitor logs** - Check Railway dashboard regularly

---

## 💡 Mobile Tips

- **Use Railway app** - Available on iOS/Android
- **Bookmark dashboard** - Quick access to logs
- **Save credentials** - Use secure notes app
- **Enable notifications** - Get deployment alerts
- **Test on mobile** - Verify API works on your phone

---

## 🆘 Need Help?

**Railway Docs:** [docs.railway.app](https://docs.railway.app)  
**GitHub Issues:** [github.com/Deathcharge/helix-unified/issues](https://github.com/Deathcharge/helix-unified/issues)  
**Discord:** Join Helix Collective server

---

**Built with 🙏 by the Helix Collective**  
**Tat Tvam Asi** 🌀

---

**Document Version:** 1.0  
**Last Updated:** December 11, 2025  
**Platform:** Mobile-optimized  
**Time Required:** 10-15 minutes
