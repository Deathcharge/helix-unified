# Helix Unified Deployment Guide

## Quick Reference
- **Repository**: https://github.com/Deathcharge/helix-unified
- **Backend**: Railway (https://helix-unified-production.up.railway.app)
- **Docs**: GitHub Pages (auto-deployed on push to main)
- **Version**: v16.9

## Architecture

### Backend (Railway)
- FastAPI/Python backend
- PostgreSQL database
- WebSocket support for real-time updates
- Deployed via Railway CLI or GitHub integration

### Frontend/Docs (GitHub Pages)
- Static documentation site
- Auto-deployed via GitHub Actions
- Cross-linked with portal constellation

## Automated Workflows

### 1. Deploy Workflow (`.github/workflows/deploy.yml`)
Triggers on:
- Push to `main` branch
- Manual workflow dispatch

Actions:
- Installs Python dependencies
- Builds static documentation
- Deploys to GitHub Pages

### 2. Sync Documentation (`.github/workflows/sync-docs.yml`)
Triggers on:
- Changes to `docs/**` or `README.md`
- Manual workflow dispatch

Actions:
- Updates portal constellation links
- Cross-links all Helix repositories
- Commits changes back to repository

## Manual Deployment

### Backend to Railway
```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login
railway login

# Deploy
railway up
```

### Docs to GitHub Pages
```bash
# Build docs
mkdir -p docs/_build
cp -r docs/* docs/_build/

# Push to main (triggers auto-deploy)
git add .
git commit -m "Update documentation"
git push origin main
```

## Environment Variables

Set these in Railway dashboard:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection (optional)
- `SECRET_KEY` - API secret key
- `ZAPIER_WEBHOOK_URL` - Webhook for Zapier integration

## GitHub Pages Setup (When Ready)

1. Go to: https://github.com/Deathcharge/helix-unified/settings/pages
2. Under "Build and deployment":
   - Source: **GitHub Actions**
3. Workflow will handle the rest automatically

## Cross-Repository Navigation

All Helix repositories include standardized `docs/PORTAL_LINKS.md` with links to:
- Core portals (Hub, Unified Hub, Collective Web)
- Specialized portals (Creative Studio, Agent Codex, etc.)
- Hub constellation (Forum, Music, Analytics, etc.)
- Backend infrastructure

## Troubleshooting

### Workflow Fails
- Check GitHub Actions logs
- Verify permissions: Settings → Actions → General → Workflow permissions
- Ensure "Read and write permissions" enabled

### Pages Not Deploying
- Verify Pages is enabled in repo settings
- Check that workflow completed successfully
- Wait 1-2 minutes for DNS propagation

### Railway Deployment Issues
- Check Railway logs: `railway logs`
- Verify environment variables set
- Check Procfile exists and is correct

## Links
- [Portal Constellation Links](./PORTAL_LINKS.md)
- [Architecture Docs](../README.md)
- [Railway Dashboard](https://railway.app/dashboard)
