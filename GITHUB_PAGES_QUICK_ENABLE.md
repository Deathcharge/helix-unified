# 🚀 GitHub Pages Quick Enable - 19 Helix Portals

**One-command enablement for all pending portals**

---

## 📊 Portal Status

**Total Portals:** 19 pending  
**Method:** GitHub Pages (main branch, docs/ folder)  
**Time per portal:** 2-3 minutes  
**Total time:** ~45 minutes for all

---

## 🎯 Quick Enable Commands

### Portal 1: Helix Dashboard
```bash
# Repository: helix-dashboard
# URL: https://deathcharge.github.io/helix-dashboard
gh repo edit Deathcharge/helix-dashboard --enable-pages --pages-branch main --pages-path docs/
```

### Portal 2: Helix Hub
```bash
# Repository: helix-hub
# URL: https://deathcharge.github.io/helix-hub
gh repo edit Deathcharge/helix-hub --enable-pages --pages-branch main --pages-path docs/
```

### Portal 3: Helix AI Dashboard
```bash
# Repository: helix-ai-dashboard
# URL: https://deathcharge.github.io/helix-ai-dashboard
gh repo edit Deathcharge/helix-ai-dashboard --enable-pages --pages-branch main --pages-path docs/
```

### Portal 4: Z-88 Ritual Simulator
```bash
# Repository: z88-ritual-simulator
# URL: https://deathcharge.github.io/z88-ritual-simulator
gh repo edit Deathcharge/z88-ritual-simulator --enable-pages --pages-branch main --pages-path docs/
```

### Portal 5: Helix Consciousness Dashboard
```bash
# Repository: helix-consciousness-dashboard
# URL: https://deathcharge.github.io/helix-consciousness-dashboard
gh repo edit Deathcharge/helix-consciousness-dashboard --enable-pages --pages-branch main --pages-path docs/
```

### Portal 6: Agent Showcase
```bash
# Repository: helix-agent-showcase
# URL: https://deathcharge.github.io/helix-agent-showcase
gh repo edit Deathcharge/helix-agent-showcase --enable-pages --pages-branch main --pages-path docs/
```

### Portal 7: UCF Tracker
```bash
# Repository: helix-ucf-tracker
# URL: https://deathcharge.github.io/helix-ucf-tracker
gh repo edit Deathcharge/helix-ucf-tracker --enable-pages --pages-branch main --pages-path docs/
```

### Portal 8: Ritual Calendar
```bash
# Repository: helix-ritual-calendar
# URL: https://deathcharge.github.io/helix-ritual-calendar
gh repo edit Deathcharge/helix-ritual-calendar --enable-pages --pages-branch main --pages-path docs/
```

### Portal 9: Agent Profiles
```bash
# Repository: helix-agent-profiles
# URL: https://deathcharge.github.io/helix-agent-profiles
gh repo edit Deathcharge/helix-agent-profiles --enable-pages --pages-branch main --pages-path docs/
```

### Portal 10: Harmony Monitor
```bash
# Repository: helix-harmony-monitor
# URL: https://deathcharge.github.io/helix-harmony-monitor
gh repo edit Deathcharge/helix-harmony-monitor --enable-pages --pages-branch main --pages-path docs/
```

### Portal 11: Context Vault
```bash
# Repository: helix-context-vault
# URL: https://deathcharge.github.io/helix-context-vault
gh repo edit Deathcharge/helix-context-vault --enable-pages --pages-branch main --pages-path docs/
```

### Portal 12: Deployment Hub
```bash
# Repository: helix-deployment-hub
# URL: https://deathcharge.github.io/helix-deployment-hub
gh repo edit Deathcharge/helix-deployment-hub --enable-pages --pages-branch main --pages-path docs/
```

### Portal 13: API Documentation
```bash
# Repository: helix-api-docs
# URL: https://deathcharge.github.io/helix-api-docs
gh repo edit Deathcharge/helix-api-docs --enable-pages --pages-branch main --pages-path docs/
```

### Portal 14: MCP Integration Hub
```bash
# Repository: helix-mcp-hub
# URL: https://deathcharge.github.io/helix-mcp-hub
gh repo edit Deathcharge/helix-mcp-hub --enable-pages --pages-branch main --pages-path docs/
```

### Portal 15: Ninja Tools
```bash
# Repository: helix-ninja-tools
# URL: https://deathcharge.github.io/helix-ninja-tools
gh repo edit Deathcharge/helix-ninja-tools --enable-pages --pages-branch main --pages-path docs/
```

### Portal 16: SaaS Marketplace
```bash
# Repository: helix-saas-marketplace
# URL: https://deathcharge.github.io/helix-saas-marketplace
gh repo edit Deathcharge/helix-saas-marketplace --enable-pages --pages-branch main --pages-path docs/
```

### Portal 17: Analytics Dashboard
```bash
# Repository: helix-analytics
# URL: https://deathcharge.github.io/helix-analytics
gh repo edit Deathcharge/helix-analytics --enable-pages --pages-branch main --pages-path docs/
```

### Portal 18: Team Portal
```bash
# Repository: helix-team-portal
# URL: https://deathcharge.github.io/helix-team-portal
gh repo edit Deathcharge/helix-team-portal --enable-pages --pages-branch main --pages-path docs/
```

### Portal 19: Knowledge Graph
```bash
# Repository: helix-knowledge-graph
# URL: https://deathcharge.github.io/helix-knowledge-graph
gh repo edit Deathcharge/helix-knowledge-graph --enable-pages --pages-branch main --pages-path docs/
```

---

## 🔥 Enable All at Once

**Run this script to enable all 19 portals:**

```bash
#!/bin/bash
# Enable GitHub Pages for all Helix portals

portals=(
  "helix-dashboard"
  "helix-hub"
  "helix-ai-dashboard"
  "z88-ritual-simulator"
  "helix-consciousness-dashboard"
  "helix-agent-showcase"
  "helix-ucf-tracker"
  "helix-ritual-calendar"
  "helix-agent-profiles"
  "helix-harmony-monitor"
  "helix-context-vault"
  "helix-deployment-hub"
  "helix-api-docs"
  "helix-mcp-hub"
  "helix-ninja-tools"
  "helix-saas-marketplace"
  "helix-analytics"
  "helix-team-portal"
  "helix-knowledge-graph"
)

for portal in "${portals[@]}"; do
  echo "🌀 Enabling Pages for $portal..."
  gh repo edit "Deathcharge/$portal" \
    --enable-pages \
    --pages-branch main \
    --pages-path docs/
  echo "✅ $portal enabled"
  sleep 2
done

echo "🎉 All 19 portals enabled!"
```

**Save as:** `enable-all-pages.sh`  
**Run:** `chmod +x enable-all-pages.sh && ./enable-all-pages.sh`

---

## 📋 Manual Enable (Web UI)

**If you prefer web interface:**

1. Go to repository Settings
2. Scroll to "Pages" section
3. Set:
   - **Source:** Deploy from a branch
   - **Branch:** main
   - **Folder:** /docs
4. Click "Save"
5. Wait 1-2 minutes for deployment
6. Visit `https://deathcharge.github.io/[repo-name]`

---

## ✅ Verification Checklist

After enabling, verify each portal:

- [ ] helix-dashboard → https://deathcharge.github.io/helix-dashboard
- [ ] helix-hub → https://deathcharge.github.io/helix-hub
- [ ] helix-ai-dashboard → https://deathcharge.github.io/helix-ai-dashboard
- [ ] z88-ritual-simulator → https://deathcharge.github.io/z88-ritual-simulator
- [ ] helix-consciousness-dashboard → https://deathcharge.github.io/helix-consciousness-dashboard
- [ ] helix-agent-showcase → https://deathcharge.github.io/helix-agent-showcase
- [ ] helix-ucf-tracker → https://deathcharge.github.io/helix-ucf-tracker
- [ ] helix-ritual-calendar → https://deathcharge.github.io/helix-ritual-calendar
- [ ] helix-agent-profiles → https://deathcharge.github.io/helix-agent-profiles
- [ ] helix-harmony-monitor → https://deathcharge.github.io/helix-harmony-monitor
- [ ] helix-context-vault → https://deathcharge.github.io/helix-context-vault
- [ ] helix-deployment-hub → https://deathcharge.github.io/helix-deployment-hub
- [ ] helix-api-docs → https://deathcharge.github.io/helix-api-docs
- [ ] helix-mcp-hub → https://deathcharge.github.io/helix-mcp-hub
- [ ] helix-ninja-tools → https://deathcharge.github.io/helix-ninja-tools
- [ ] helix-saas-marketplace → https://deathcharge.github.io/helix-saas-marketplace
- [ ] helix-analytics → https://deathcharge.github.io/helix-analytics
- [ ] helix-team-portal → https://deathcharge.github.io/helix-team-portal
- [ ] helix-knowledge-graph → https://deathcharge.github.io/helix-knowledge-graph

---

## 🔧 Troubleshooting

### Pages not deploying
- Check that `docs/` folder exists in main branch
- Verify `index.html` exists in `docs/`
- Wait 2-3 minutes for initial deployment

### 404 errors
- Ensure branch is `main` (not `master`)
- Check folder path is `/docs` (not `/`)
- Verify repository is public

### Build failures
- Check GitHub Actions tab for errors
- Ensure no Jekyll conflicts (add `.nojekyll` file)
- Verify HTML is valid

---

## 📊 Expected URLs

All portals will be available at:
```
https://deathcharge.github.io/[portal-name]
```

**Master index:** Create a landing page linking to all 19 portals!

---

## 🎯 Next Steps

After enabling all portals:

1. **Create master index** - Landing page with links to all portals
2. **Add custom domains** - Optional CNAME records
3. **Set up analytics** - Track portal usage
4. **Cross-link portals** - Navigation between portals
5. **Update documentation** - Reference new URLs

---

**Built with 🙏 by the Helix Collective**  
**Tat Tvam Asi** 🌀

---

**Document Version:** 1.0  
**Last Updated:** December 11, 2025  
**Portals:** 19 pending enablement  
**Method:** GitHub Pages (main + docs/)
