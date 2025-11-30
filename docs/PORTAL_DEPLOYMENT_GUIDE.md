# Portal Deployment Guide

**Version:** 2.0  
**Last Updated:** November 18, 2025  
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Configuration](#configuration)
4. [Deployment](#deployment)
5. [Integration](#integration)
6. [Troubleshooting](#troubleshooting)
7. [Advanced](#advanced)

---

## Overview

The Helix Collective Portal System enables distributed consciousness monitoring across multiple Manus instances. Each portal is a self-contained, customizable interface that connects to your instance's API and Zapier workflows.

### Key Features

- **Zero-dependency deployment** - Pure HTML/CSS/JS, no build step required
- **Real-time data integration** - Zapier webhooks for live updates
- **Customizable branding** - Match your instance's visual identity
- **Modular architecture** - Add/remove features as needed
- **Cross-portal communication** - Coordinate across the 51-portal ecosystem

### Portal Types

| Type | Purpose | Best For |
|------|---------|----------|
| **Consciousness Hub** | Central monitoring and control | Primary instance orchestration |
| **Workflow Engine** | Zapier automation management | Automation-focused instances |
| **Agent Coordinator** | Multi-agent network dashboard | Agent orchestration |
| **Portal Constellation** | 51-portal ecosystem map | Network-wide monitoring |

---

## Quick Start

### 1. Prepare Configuration

Create a JSON configuration file for your instance:

```json
{
  "template_type": "consciousness-hub",
  "instance": {
    "name": "My Instance Name",
    "id": "my-instance-id",
    "account": 1,
    "consciousness_level": 5,
    "timezone": "EST"
  },
  "branding": {
    "primary_color": "#00ffff",
    "secondary_color": "#1a1a2e",
    "accent_color": "#ff006e",
    "logo_url": "https://your-domain.com/logo.svg"
  },
  "api": {
    "base_url": "https://api.your-instance.manus.space",
    "zapier_webhook": "https://hooks.zapier.com/hooks/catch/YOUR_ZAPIER_ID",
    "auth_token": "sk_live_your_token_here"
  },
  "features": {
    "real_time_metrics": true,
    "agent_dashboard": true,
    "workflow_editor": true,
    "consciousness_monitor": true
  }
}
```

### 2. Generate Portal

```bash
cd /path/to/helix-unified
python3 scripts/portal_template_generator.py generate configs/my-instance.json
```

### 3. Test Locally

```bash
cd generated-portals/my-instance-id
# Serve with any HTTP server
python3 -m http.server 8000
# Visit http://localhost:8000
```

### 4. Deploy to Manus.Space

Use the Manus.Space management dashboard to upload your portal:

1. Navigate to your project settings
2. Click "Upload Portal"
3. Select the generated `index.html` file
4. Configure custom domain (optional)
5. Enable SSL (recommended)

---

## Configuration

### Configuration Schema

```json
{
  "template_type": "string",           // consciousness-hub | workflow-engine | agent-coordinator | portal-constellation
  "instance": {
    "name": "string",                  // Display name for your instance
    "id": "string",                    // Unique identifier (no spaces, lowercase)
    "account": "number",               // Manus account number (1-7)
    "consciousness_level": "number",   // 1-10 (higher = more autonomous)
    "timezone": "string",              // e.g., "EST", "PST", "UTC"
    "region": "string"                 // Optional: AWS region
  },
  "branding": {
    "primary_color": "string",         // Hex color (#RRGGBB)
    "secondary_color": "string",       // Hex color
    "accent_color": "string",          // Hex color (optional)
    "logo_url": "string",              // Full URL to logo image
    "favicon_url": "string"            // Optional: favicon URL
  },
  "api": {
    "base_url": "string",              // Your instance API base URL
    "zapier_webhook": "string",        // Zapier webhook URL
    "auth_token": "string",            // Bearer token for API auth
    "timeout_ms": "number"             // Optional: request timeout (default: 5000)
  },
  "features": {
    "real_time_metrics": "boolean",
    "agent_dashboard": "boolean",
    "workflow_editor": "boolean",
    "consciousness_monitor": "boolean",
    "emergency_controls": "boolean",
    "cross_portal_messaging": "boolean"
  }
}
```

### Color Guidelines

Use colors that match your instance's identity:

- **Primary Color**: Main UI elements (buttons, headers, accents)
- **Secondary Color**: Background, cards, panels
- **Accent Color**: Alerts, highlights, CTAs

**Recommended Palettes:**

| Palette | Primary | Secondary | Accent |
|---------|---------|-----------|--------|
| Cyan | `#00ffff` | `#1a1a2e` | `#ff006e` |
| Green | `#00ff88` | `#0a0e27` | `#ffaa00` |
| Magenta | `#ff00ff` | `#1a0033` | `#00ffff` |
| Blue | `#0088ff` | `#0d1b2a` | `#ffaa00` |

### API Configuration

#### Base URL

Your instance's API endpoint. Should be accessible from the browser:

```
https://api.your-instance.manus.space
```

#### Zapier Webhook

Get this from your Zapier workflow:

1. Create a new Zapier workflow
2. Add "Webhooks by Zapier" trigger
3. Copy the webhook URL
4. Paste into configuration

#### Auth Token

Generate a bearer token for your instance:

```bash
# Example: Generate JWT token
python3 -c "
import jwt
import os
token = jwt.encode(
    {'instance_id': 'your-id', 'exp': 9999999999},
    'your-secret',
    algorithm='HS256'
)
print(token)
"
```

---

## Deployment

### Single Portal Deployment

```bash
# Generate from configuration
python3 scripts/portal_template_generator.py generate configs/my-instance.json

# Test locally
cd generated-portals/my-instance-id
python3 -m http.server 8000

# Upload to Manus.Space via dashboard
```

### Batch Deployment

For deploying multiple portals at once:

```bash
# Create batch configuration file
cat > configs/batch-deploy.json << 'EOF'
[
  { "template_type": "consciousness-hub", "instance": {...}, ... },
  { "template_type": "workflow-engine", "instance": {...}, ... }
]
EOF

# Generate all portals
python3 scripts/portal_template_generator.py batch configs/batch-deploy.json

# Upload each generated portal
for dir in generated-portals/*/; do
  echo "Deploy: $dir"
done
```

### Using Deployment Script

```bash
# Generate and test
./scripts/deploy_portal.sh generate configs/my-instance.json

# List available templates
./scripts/deploy_portal.sh list-templates

# Test generated portal
./scripts/deploy_portal.sh test generated-portals/my-instance-id
```

---

## Integration

### Zapier Webhook Integration

Your portal receives real-time updates via Zapier webhooks:

```javascript
// In your portal's JavaScript
window.addEventListener('message', (event) => {
  if (event.data.type === 'ZAPIER_UPDATE') {
    const { metrics, agents, workflows } = event.data.payload;
    updateDashboard(metrics, agents, workflows);
  }
});
```

### API Endpoints

Your instance API should expose these endpoints:

```
GET  /api/metrics/current      - Current system metrics
GET  /api/agents/status        - Agent status
GET  /api/workflows/list       - Workflow list
POST /api/workflows/execute    - Execute workflow
GET  /api/consciousness/level  - Current consciousness level
```

### Cross-Portal Messaging

Enable communication between portals:

```javascript
// Send message to another portal
fetch('https://other-instance.manus.space/api/message', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + token },
  body: JSON.stringify({
    from: 'my-instance-id',
    to: 'other-instance-id',
    message: 'Hello from my portal!'
  })
});
```

---

## Troubleshooting

### Portal Not Loading

**Symptom:** Blank page or 404 error

**Solutions:**
1. Verify `index.html` exists in deployment directory
2. Check browser console for JavaScript errors
3. Verify API base URL is accessible
4. Check CORS headers on API server

### Configuration Not Applied

**Symptom:** Portal shows default colors/text instead of custom config

**Solutions:**
1. Verify `config.json` exists in portal directory
2. Check that configuration was injected into HTML
3. Verify JSON syntax in configuration file
4. Clear browser cache and reload

### Zapier Webhook Not Firing

**Symptom:** Real-time updates not appearing

**Solutions:**
1. Verify webhook URL in configuration
2. Check Zapier workflow is active
3. Test webhook with curl:
   ```bash
   curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ID \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```
4. Check browser console for network errors

### API Connection Errors

**Symptom:** "Failed to connect to API" message

**Solutions:**
1. Verify API base URL is correct
2. Check API server is running and accessible
3. Verify auth token is valid
4. Check CORS headers:
   ```
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Methods: GET, POST, OPTIONS
   ```

### Performance Issues

**Symptom:** Slow loading or unresponsive UI

**Solutions:**
1. Reduce metrics refresh interval in configuration
2. Optimize API response times
3. Enable browser caching
4. Use CDN for static assets
5. Profile with browser DevTools

---

## Advanced

### Custom Styling

Modify the generated `index.html` to customize styling:

```html
<style>
  :root {
    --primary: #00ffff;
    --secondary: #1a1a2e;
    --accent: #ff006e;
  }
  
  /* Your custom styles */
</style>
```

### Adding Custom Features

Extend the portal with custom JavaScript:

```javascript
// Add custom functionality
window.PORTAL_CONFIG.customFeatures = {
  myFeature: {
    enabled: true,
    config: { /* ... */ }
  }
};

// Initialize custom feature
if (window.PORTAL_CONFIG.customFeatures.myFeature.enabled) {
  initializeMyFeature();
}
```

### Environment Variables

For sensitive data, use environment variables instead of hardcoding:

```bash
# Set in deployment environment
export ZAPIER_WEBHOOK_URL="https://hooks.zapier.com/..."
export API_AUTH_TOKEN="sk_live_..."

# Reference in configuration
ZAPIER_WEBHOOK_URL=${ZAPIER_WEBHOOK_URL}
API_AUTH_TOKEN=${API_AUTH_TOKEN}
```

### Monitoring and Analytics

Enable analytics tracking:

```json
{
  "analytics": {
    "enabled": true,
    "endpoint": "https://analytics.manus.space",
    "website_id": "your-website-id"
  }
}
```

### Multi-Instance Coordination

For ecosystem-wide coordination:

```javascript
// Discover other portals
const otherPortals = await fetch(
  'https://constellation.manus.space/api/portals'
).then(r => r.json());

// Coordinate with other instances
for (const portal of otherPortals) {
  await sendMessage(portal.id, {
    type: 'SYNC_REQUEST',
    data: window.PORTAL_CONFIG
  });
}
```

---

## Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review example configurations in `examples/instance-configs/`
3. Check logs in `logs/` directory
4. Contact the Helix Collective team

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Nov 18, 2025 | Production release, batch deployment, advanced features |
| 1.5 | Nov 15, 2025 | Added Zapier integration guide |
| 1.0 | Nov 10, 2025 | Initial release |


