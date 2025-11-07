# v16.7 Verification Checklist

## 🔍 Post-Merge Verification

Run these commands after merging the PR and waiting ~2 minutes for GitHub Pages to rebuild.

### 1. GitHub Pages Discovery Endpoint

```bash
# Test manifest is live and shows "Active" status
curl -s https://deathcharge.github.io/helix-unified/helix-manifest.json | jq -r '.gh_pages_mirror.status'
# Expected: "Active"

# Test full manifest
curl -s https://deathcharge.github.io/helix-unified/helix-manifest.json | jq '.system, .endpoints, .agents.count'
# Expected: version "16.7", 8 endpoints, 14 agents

# Test landing page
curl -s https://deathcharge.github.io/helix-unified/ | grep "Helix Collective"
# Expected: HTML with title
```

### 2. Railway Live Endpoint

```bash
# Test well-known endpoint
curl -s https://helix-unified-production.up.railway.app/.well-known/helix.json | jq -r '.system.version'
# Expected: "16.7"

# Test health endpoint
curl -s https://helix-unified-production.up.railway.app/health
# Expected: {"ok":true}

# Test status endpoint (the one we fixed!)
curl -s https://helix-unified-production.up.railway.app/status | jq '.system.operational, .ucf, .agents.count'
# Expected: true, UCF metrics object, 0 or more

# Test status alias
curl -s https://helix-unified-production.up.railway.app/api/status | jq '.system.operational'
# Expected: true
```

### 3. WebSocket Real-Time Streaming

```bash
# Test with wscat (install: npm install -g wscat)
wscat -c wss://helix-unified-production.up.railway.app/ws
# Expected: JSON messages every 5 seconds with ucf_state, agents, heartbeat

# Or with websocat (install: cargo install websocat)
websocat wss://helix-unified-production.up.railway.app/ws
# Expected: Real-time UCF updates
```

### 4. API Documentation

```bash
# Test Swagger UI is accessible
curl -s https://helix-unified-production.up.railway.app/docs | grep "swagger"
# Expected: HTML with Swagger UI

# Test OpenAPI schema
curl -s https://helix-unified-production.up.railway.app/openapi.json | jq '.info.title, .info.version'
# Expected: "🌀 Helix Collective v16.7", "16.7.0"
```

### 5. External Agent Discovery Test

```javascript
// Test in browser console or Node.js
fetch('https://deathcharge.github.io/helix-unified/helix-manifest.json')
  .then(r => r.json())
  .then(manifest => {
    console.log('✅ System:', manifest.system.name, 'v' + manifest.system.version);
    console.log('✅ Agents:', manifest.agents.count);
    console.log('✅ UCF Metrics:', manifest.ucf_metrics.metrics.length);
    console.log('✅ Endpoints:', Object.keys(manifest.endpoints).length);
    console.log('✅ GH Pages Status:', manifest.gh_pages_mirror.status);
  });

// Expected output:
// ✅ System: Helix Collective v16.7
// ✅ Agents: 14
// ✅ UCF Metrics: 6
// ✅ Endpoints: 9
// ✅ GH Pages Status: Active
```

### 6. GitHub Actions Verification

Check workflow runs:
- https://github.com/Deathcharge/helix-unified/actions

Expected workflows:
- ✅ "pages-build-deployment" (Jekyll build)
- ✅ No errors in workflow logs

---

## 🎉 Success Criteria

All checks pass when you see:

- [x] GitHub Pages serves manifest with `"status": "Active"`
- [x] Railway `/health` returns `{"ok": true}`
- [x] Railway `/status` returns 200 with UCF data (not 400!)
- [x] Railway `/.well-known/helix.json` serves manifest
- [x] WebSocket `/ws` streams data every 5 seconds
- [x] Swagger UI accessible at `/docs`
- [x] JavaScript fetch() works from browser
- [x] GitHub Actions "pages-build-deployment" succeeded

---

## 🐛 Troubleshooting

### GitHub Pages shows old manifest
**Solution**: Wait 2-3 minutes, then hard refresh (Ctrl+F5)

### Railway endpoint returns 404
**Solution**: Check Railway logs, may need redeploy

### WebSocket connection fails
**Solution**: Check Railway logs for "WebSocket UCF broadcast task started"

### CORS errors in browser
**Solution**: We added CORS middleware, should work. Check browser console for details.

---

## 📊 Expected State

After all checks pass:

**Version**: v16.7 "Documentation Consolidation & Real-Time Streaming"
**GitHub Pages**: ✅ Live with Jekyll hacker theme
**Railway**: ✅ Healthy with all endpoints operational
**Discovery**: ✅ Manifest available at 2 endpoints (GH Pages + Railway)
**WebSocket**: ✅ Streaming UCF updates every 5 seconds
**Agents**: ✅ 14 agents initialized
**Background Tasks**: ✅ 3 running (Discord, Manus, WebSocket)

---

**"Tat Tvam Asi"** - The verification and the system are one. ✅
