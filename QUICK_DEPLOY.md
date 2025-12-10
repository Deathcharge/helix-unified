# ⚡ Quick Deploy - Helix-Unified v17.1

**5-Minute Railway Deployment** | [Full Guide](./RAILWAY_DEPLOYMENT_GUIDE_V17.md)

---

## 🚀 One-Command Deploy

```bash
./deploy-to-railway.sh
```

**That's it!** The script handles everything.

---

## 📋 Manual Deploy (If Script Fails)

### 1. Install & Login
```bash
npm install -g @railway/cli
railway login
```

### 2. Initialize Project
```bash
cd helix-unified
railway init
railway add postgres
```

### 3. Set Variables
```bash
railway variables set JWT_SECRET=$(openssl rand -hex 32)
railway variables set ADMIN_EMAILS=ward.andrew32@gmail.com
railway variables set DATABASE_URL='${{Postgres.DATABASE_URL}}'
```

### 4. Deploy
```bash
railway up
```

### 5. Get URL
```bash
railway domain
```

---

## ✅ Verify Deployment

```bash
# Health check
curl https://your-app.up.railway.app/health

# Should return: {"status":"healthy","version":"17.1"}
```

---

## 🔧 Essential Variables

**Required (3):**
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
JWT_SECRET=<64-char-random>
ADMIN_EMAILS=ward.andrew32@gmail.com
```

**Optional (add as needed):**
```bash
DISCORD_BOT_TOKEN=<your-token>
OPENAI_API_KEY=<your-key>
STRIPE_SECRET_KEY=<your-key>
NOTION_API_KEY=<your-key>
```

---

## 🐛 Troubleshooting

**Problem:** Health check fails  
**Fix:** `railway logs` → check for errors

**Problem:** Database connection failed  
**Fix:** Verify `DATABASE_URL=${{Postgres.DATABASE_URL}}`

**Problem:** Admin login fails  
**Fix:** Check `ADMIN_EMAILS` includes your email

---

## 📱 Connect Frontend

Update your Manus Spaces:
```bash
VITE_HELIX_API_URL=https://your-app.up.railway.app
```

---

## 🔄 Rollback

```bash
railway rollback
```

---

## 📚 More Info

- **Full Guide:** `RAILWAY_DEPLOYMENT_GUIDE_V17.md`
- **Features:** `WHATS_NEW_v17.1.md`
- **Admin Setup:** `ADMIN_SETUP.md`

---

**Tat Tvam Asi** 🌀
