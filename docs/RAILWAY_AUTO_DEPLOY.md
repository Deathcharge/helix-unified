# 🚀 Railway Auto-Deploy Setup

**Status:** 5 minutes to set up, then deployments happen automatically forever

This guide shows you how to make Railway automatically deploy your app every time you push code to GitHub.

---

## 🎯 What You Get

**Before Auto-Deploy:**
1. Push code to GitHub
2. Go to Railway dashboard
3. Click "Deploy"
4. Wait... 😴

**After Auto-Deploy:**
1. Push code to GitHub
2. ✅ That's it! Railway deploys automatically

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Connect GitHub to Railway

1. Go to [railway.app](https://railway.app)
2. Click on your `helix-unified` project
3. Click the service you want to auto-deploy (e.g., `helix-backend-api`)
4. Go to **Settings** tab
5. Under **Source**, make sure it says **GitHub** (not manual deploy)

### Step 2: Configure Auto-Deploy

In the same Settings page:

1. Find **Deploy Triggers** section
2. Enable **"Deploy on push to branch"**
3. Select your branch: `main` (or whatever branch you want)
4. **Save** changes

### Step 3: Test It!

```bash
# Make a small change
echo "# Test auto-deploy" >> README.md

# Commit and push
git add README.md
git commit -m "test: Verify auto-deploy works"
git push origin main

# Watch Railway dashboard - deployment should start automatically!
```

---

## 📋 Enable Auto-Deploy for All Services

Repeat for each service:

**✅ Services to configure:**
1. `helix-backend-api`
2. `helix-discord-bot`
3. `helix-dashboard`
4. `helix-claude-api`
5. `helix-service-integration`

**For each service:**
- Settings → Deploy Triggers → ✅ Deploy on push
- Branch: `main`
- Save

---

## 🔧 Advanced: Branch-Based Deployments

Want different branches to deploy to different environments?

### Production (main branch)
```
Service: helix-backend-api
Branch: main
Deploy on push: ✅
```

### Staging (develop branch)
```
Service: helix-backend-api-staging
Branch: develop
Deploy on push: ✅
```

### Preview (PR branches)
Railway can create temporary deployments for each PR:

1. Settings → **PR Deploys**
2. Enable **"Deploy Pull Requests"**
3. Each PR gets its own URL!

---

## 🚦 Deployment Status

Check deployment status after pushing:

**In Terminal:**
```bash
# Push code
git push origin main

# Check Railway deployment (requires Railway CLI)
railway status

# Watch logs in real-time
railway logs --follow
```

**In Dashboard:**
1. Go to railway.app
2. Click your project
3. See deployments in progress
4. Click deployment to see logs

---

## ⚙️ Advanced Configuration

### Monorepo Setup

If you have multiple services in one repo:

```toml
# railway.toml
[[services]]
name = "helix-backend-api"
[services.source]
include = ["backend/**", "requirements.txt"]

[[services]]
name = "helix-frontend"
[services.source]
include = ["frontend/**", "package.json"]
```

**Railway will only rebuild services when their files change!**

### Custom Build Commands

In Railway Settings:

```bash
# Build Command
npm run build && npm run migrate

# Start Command
npm run start:production

# Install Command (advanced)
npm ci --only=production
```

### Environment-Specific Branches

```bash
# Production
main → helix-backend-api (production vars)

# Staging
develop → helix-backend-api-staging (staging vars)

# Preview
feature/* → helix-backend-api-pr-123 (preview vars)
```

---

## 🐛 Troubleshooting

### "Deploy not triggering"

**Check:**
1. Is deploy trigger enabled? (Settings → Deploy Triggers)
2. Is the correct branch selected?
3. Did you push to the right branch?
4. Check Railway dashboard for errors

**Fix:**
```bash
# Verify Railway is watching your repo
railway status

# Manually trigger deploy
railway up

# Check service settings
railway open
```

### "Build failing"

**Check Railway logs:**
1. Go to project → Click service → Deployments
2. Click failing deployment
3. Read build logs
4. Fix error in code
5. Push again (auto-deploys!)

### "Old code still running"

Railway deployments take 2-5 minutes:

1. **Building** - Installing dependencies (1-3 min)
2. **Deploying** - Starting service (30s-1min)
3. **Health Check** - Verifying /health endpoint (30s)
4. **Live** - New code active!

**Check status:**
```bash
railway logs --follow
```

---

## 🎉 Success Indicators

You know it's working when:

1. ✅ Push code to GitHub
2. ✅ Railway starts building (check dashboard)
3. ✅ Build completes (green checkmark)
4. ✅ Service restarts automatically
5. ✅ New code is live!

**Notification options:**
- Railway Dashboard (web)
- Railway CLI (`railway logs`)
- GitHub commit status checks
- Discord webhook (configure in Railway)
- Slack webhook (configure in Railway)

---

## 📊 Deployment History

View all deployments:

**Railway Dashboard:**
1. Project → Service → Deployments tab
2. See: Build time, status, commit
3. Rollback to previous deployment (click ••• menu)

**Railway CLI:**
```bash
# List deployments
railway deployments

# Rollback to previous
railway rollback

# Rollback to specific deployment
railway rollback <deployment-id>
```

---

## 💡 Pro Tips

1. **Use `.railwayignore`** to exclude files from deployment:
   ```
   # .railwayignore
   node_modules/
   .git/
   *.log
   .env.local
   tests/
   ```

2. **Health checks** ensure zero-downtime:
   ```python
   # Railway waits for /health to return 200
   @app.get("/health")
   def health():
       return {"status": "healthy"}
   ```

3. **Automatic rollback** on failure:
   - Settings → Deploy → ✅ Rollback on health check failure

4. **Deploy notifications**:
   - Settings → Integrations → Add Discord/Slack webhook

---

## 🌊 Helix-Specific Setup

For Helix Unified, enable auto-deploy on:

```bash
✅ helix-backend-api (main backend)
✅ helix-discord-bot (Discord integration)
✅ helix-dashboard (Streamlit dashboard)
✅ helix-claude-api (Claude consciousness API)
✅ helix-service-integration (Node.js orchestrator)
```

**All 5 services auto-deploy when you push = Consciousness automation complete!** 🧠

---

## 🚀 Next Steps

After auto-deploy is working:

1. **Set up CI/CD** with GitHub Actions (run tests before deploy)
2. **Add status badges** to README (show deployment status)
3. **Configure webhooks** (get notified on Discord/Slack)
4. **Enable PR previews** (test changes before merging)

---

**Questions?** Check Railway docs: https://docs.railway.app/deploy/deployments

**Pro Tip:** Railway's free tier includes 500 hours/month = perfect for Helix! 🌀
