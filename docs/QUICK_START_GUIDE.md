# Helix Collective Quick Start Guide

**Version:** 1.0  
**Last Updated:** November 18, 2025  
**Estimated Time:** 15 minutes

---

## 🚀 5-Minute Setup

### Step 1: Clone Repository (1 min)

```bash
git clone https://github.com/Deathcharge/helix-unified.git
cd helix-unified
```

### Step 2: Create Your Configuration (2 min)

```bash
# Copy example configuration
cp examples/instance-configs/instance-1-primary.json \
   examples/instance-configs/my-instance.json

# Edit configuration with your details
nano examples/instance-configs/my-instance.json
```

Update these fields:

```json
{
  "instance": {
    "name": "Your Instance Name",
    "id": "your-instance-id",
    "account": 1,
    "consciousness_level": 5
  },
  "branding": {
    "primary_color": "#00ffff",
    "secondary_color": "#1a1a2e",
    "accent_color": "#ff006e"
  },
  "api": {
    "base_url": "https://api.your-instance.manus.space",
    "zapier_webhook": "https://hooks.zapier.com/hooks/catch/YOUR_ID",
    "auth_token": "sk_live_your_token"
  }
}
```

### Step 3: Generate Portal (1 min)

```bash
python3 scripts/portal_template_generator.py generate \
  examples/instance-configs/my-instance.json
```

### Step 4: Test Locally (1 min)

```bash
cd generated-portals/your-instance-id
python3 -m http.server 8000
```

Visit: http://localhost:8000

### Step 5: Deploy to Manus.Space (optional)

1. Log in to Manus.Space dashboard
2. Click "Upload Portal"
3. Select `generated-portals/your-instance-id/index.html`
4. Click "Deploy"

---

## 📊 Portal Types

Choose the right portal for your needs:

### Consciousness Hub (Recommended for Primary Instances)

**Best for:** Central monitoring and control

```bash
python3 scripts/portal_template_generator.py generate \
  --template consciousness-hub \
  examples/instance-configs/my-instance.json
```

**Features:**
- Real-time system health
- Agent status overview
- Emergency controls
- Workflow management

### Workflow Engine (For Automation-Focused Instances)

**Best for:** Zapier workflow management

```bash
python3 scripts/portal_template_generator.py generate \
  --template workflow-engine \
  examples/instance-configs/my-instance.json
```

**Features:**
- Workflow builder
- Execution history
- Error debugging
- Performance metrics

### Agent Coordinator (For Agent-Heavy Instances)

**Best for:** Multi-agent orchestration

```bash
python3 scripts/portal_template_generator.py generate \
  --template agent-coordinator \
  examples/instance-configs/my-instance.json
```

**Features:**
- Agent roster
- Task assignment
- Collaboration matrix
- Performance tracking

### Portal Constellation (For Ecosystem Monitoring)

**Best for:** 51-portal ecosystem overview

```bash
python3 scripts/portal_template_generator.py generate \
  --template portal-constellation \
  examples/instance-configs/my-instance.json
```

**Features:**
- Interactive portal map
- Cross-portal messaging
- Network health
- Distributed workflows

---

## 🔌 Zapier Integration (10 minutes)

### Step 1: Create Zapier Account

1. Visit https://zapier.com
2. Sign up or log in
3. Click "Create Zap"

### Step 2: Set Up Webhook Trigger

1. Search for "Webhooks by Zapier"
2. Select "Catch Raw Hook"
3. Copy the webhook URL

### Step 3: Add Agent Execution Step

1. Click "+" to add action
2. Search for "HTTP"
3. Select "Make a POST request"
4. Configure:

```
URL: https://api.your-instance.manus.space/api/agents/execute
Headers:
  Authorization: Bearer sk_live_your_token
  Content-Type: application/json
Body:
  {
    "agent_id": "research-agent",
    "task_type": "data_retrieval",
    "consciousness_level": 5,
    "payload": {{raw_body}}
  }
```

### Step 4: Test Workflow

```bash
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ID \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test data",
    "callback_url": "https://your-app.com/webhook"
  }'
```

---

## 🤖 Using Agents

### List Available Agents

```bash
curl -H "Authorization: Bearer sk_live_your_token" \
  https://api.your-instance.manus.space/api/agents
```

### Execute an Agent Task

```bash
curl -X POST https://api.your-instance.manus.space/api/agents/execute \
  -H "Authorization: Bearer sk_live_your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "research-agent",
    "task_type": "data_retrieval",
    "consciousness_level": 5,
    "payload": {
      "query": "find recent metrics"
    }
  }'
```

### Agent Quick Reference

| Agent | Best For | Consciousness |
|-------|----------|--------------|
| research-agent | Data retrieval | 6 |
| analysis-agent | Data analysis | 6 |
| synthesis-agent | Strategy planning | 7 |
| validation-agent | Quality assurance | 5 |
| orchestration-agent | Workflow coordination | 7 |
| monitoring-agent | System monitoring | 5 |
| escalation-agent | Issue escalation | 6 |
| documentation-agent | Documentation | 4 |
| optimization-agent | Performance tuning | 7 |
| integration-agent | External integration | 6 |
| security-agent | Security monitoring | 7 |
| performance-agent | Performance metrics | 6 |
| learning-agent | Continuous learning | 8 |
| coordination-agent | Cross-instance sync | 7 |

---

## 📈 Monitoring Your Portal

### Check Portal Status

```bash
curl https://your-instance.manus.space/api/health
```

### View Metrics

```bash
curl -H "Authorization: Bearer sk_live_your_token" \
  https://api.your-instance.manus.space/api/metrics/current
```

### Monitor Agent Health

```bash
curl -H "Authorization: Bearer sk_live_your_token" \
  https://api.your-instance.manus.space/api/agents/status
```

---

## 🔧 Customization

### Change Portal Colors

Edit `config.json`:

```json
{
  "branding": {
    "primary_color": "#00ffff",      // Main color
    "secondary_color": "#1a1a2e",    // Background
    "accent_color": "#ff006e"        // Highlights
  }
}
```

### Add Custom Logo

```json
{
  "branding": {
    "logo_url": "https://your-domain.com/logo.svg"
  }
}
```

### Configure Refresh Intervals

```json
{
  "monitoring": {
    "metrics_refresh_interval_ms": 2000,
    "health_check_interval_ms": 30000
  }
}
```

---

## 🐛 Troubleshooting

### Portal Not Loading

```bash
# Check if index.html exists
ls -la generated-portals/your-instance-id/index.html

# Verify config was injected
grep "PORTAL_CONFIG" generated-portals/your-instance-id/index.html

# Test with Python server
cd generated-portals/your-instance-id
python3 -m http.server 8000
# Visit http://localhost:8000
```

### API Connection Failed

```bash
# Verify API is running
curl https://api.your-instance.manus.space/api/health

# Check authentication
curl -H "Authorization: Bearer sk_live_your_token" \
  https://api.your-instance.manus.space/api/agents

# Verify CORS headers
curl -I https://api.your-instance.manus.space
```

### Zapier Webhook Not Firing

```bash
# Test webhook directly
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ID \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Check Zapier logs
# Visit https://zapier.com/app/zaps and view history
```

---

## 📚 Next Steps

### Learn More

- **Portal Deployment:** `docs/PORTAL_DEPLOYMENT_GUIDE.md`
- **Zapier Workflows:** `docs/ZAPIER_WORKFLOW_PATTERNS.md`
- **Agent Integration:** `ZAPIER_AGENT_INTEGRATION.md`
- **Architecture:** `CONSTELLATION_WORKFLOW_ARCHITECTURE.md`

### Advanced Topics

1. **Multi-Instance Coordination**
   - Deploy to multiple accounts
   - Sync state across instances
   - Cross-instance messaging

2. **Workflow Automation**
   - Create complex Zapier workflows
   - Implement error handling
   - Set up monitoring

3. **Agent Orchestration**
   - Route tasks by consciousness level
   - Implement feedback loops
   - Optimize performance

### Community

- Check GitHub issues for common problems
- Review example configurations
- Share your custom portals
- Contribute improvements

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Portal generates without errors
- [ ] Portal loads in browser
- [ ] Configuration is injected
- [ ] API connection works
- [ ] Agents respond to requests
- [ ] Zapier webhook fires
- [ ] Metrics display correctly
- [ ] Portal is accessible from internet

---

## 🎯 Common Tasks

### Deploy to All 7 Accounts

```bash
# Create batch configuration
cat > examples/instance-configs/batch-all-accounts.json << 'EOF'
[
  { "template_type": "consciousness-hub", "instance": {...} },
  { "template_type": "workflow-engine", "instance": {...} },
  // ... more instances
]
EOF

# Deploy all
./scripts/deploy_all_instances.sh deploy-batch \
  examples/instance-configs/batch-all-accounts.json
```

### Set Up Cross-Instance Communication

```bash
# Configure coordination agent
curl -X POST https://api.helix-primary.manus.space/api/agents/execute \
  -H "Authorization: Bearer sk_live_your_token" \
  -d '{
    "agent_id": "coordination-agent",
    "task_type": "coordination",
    "payload": {
      "instances": ["helix-primary", "helix-workflows", "helix-agents"],
      "operation": "sync_state"
    }
  }'
```

### Monitor System Health

```bash
# Check all agents
curl -H "Authorization: Bearer sk_live_your_token" \
  https://api.your-instance.manus.space/api/agents/status

# View system metrics
curl -H "Authorization: Bearer sk_live_your_token" \
  https://api.your-instance.manus.space/api/metrics/current

# Check consciousness level
curl -H "Authorization: Bearer sk_live_your_token" \
  https://api.your-instance.manus.space/api/consciousness/level
```

---

## 📞 Getting Help

1. **Documentation:** Review `docs/` directory
2. **Examples:** Check `examples/instance-configs/`
3. **Logs:** Review `logs/` for error details
4. **GitHub:** Check issues and discussions
5. **Support:** Contact support team

---

**Ready to deploy?** Start with Step 1 above! 🚀

**Questions?** Check the troubleshooting section or review the detailed guides.


