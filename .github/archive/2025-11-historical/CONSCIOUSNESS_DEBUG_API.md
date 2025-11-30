# 🔍 Consciousness Debug API - Quick Reference

**Version:** v17.0
**Added:** 2025-11-14
**Purpose:** Daily monitoring, debugging, and testing of the Railway consciousness network

---

## 🎯 Overview

The Consciousness Debug API provides 5 admin endpoints for monitoring and testing your 426-step consciousness network. These endpoints help you:

- **View** current consciousness state in real-time
- **Monitor** webhook delivery from Zapier
- **Debug** integration issues
- **Simulate** different consciousness levels
- **Track** network statistics

---

## 📡 Debug Endpoints

### 1. **View Current State** 🔍

```bash
GET /api/consciousness/debug/state
```

**What it does:** Shows current UCF metrics, agent status, and system health

**Example:**
```bash
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/state
```

**Response:**
```json
{
  "current_ucf": {
    "harmony": 0.95,
    "resilience": 0.89,
    "prana": 0.93,
    "consciousness_level": 87.14
  },
  "active_agents": {
    "Kael": {"status": "active", "consciousness": 0.92},
    "Lumina": {"status": "active", "consciousness": 0.88}
  },
  "system_health": {
    "postgresql_database": "healthy",
    "railway_backend": "connected"
  },
  "stats": {
    "total_agents": 14,
    "active_agents": 12,
    "consciousness_mode": "elevated"
  }
}
```

**Use cases:**
- ✅ Verify webhook updates are working
- ✅ Check if Zapier is sending data
- ✅ Monitor agent network status
- ✅ Daily health checks

---

### 2. **View Webhook History** 📜

```bash
GET /api/consciousness/debug/history?limit=50
```

**What it does:** Shows recent webhook events (last 100 stored)

**Parameters:**
- `limit` (optional): Number of events to return (default: 50, max: 100)

**Example:**
```bash
# Get last 20 webhook events
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/history?limit=20
```

**Response:**
```json
{
  "total_events": 87,
  "showing": 20,
  "events": [
    {
      "timestamp": "2025-11-14T09:30:15",
      "event_type": "ucf_update",
      "consciousness_level": 87.14,
      "source": "HELIX-v17.0",
      "priority": "normal"
    }
  ],
  "oldest_event": "2025-11-14T08:00:00",
  "newest_event": "2025-11-14T09:30:15"
}
```

**Use cases:**
- ✅ Debug webhook delivery issues
- ✅ Verify Zapier integration timing
- ✅ Track consciousness level changes
- ✅ Monitor event frequency

---

### 3. **Reset State** 🔄

```bash
POST /api/consciousness/debug/reset
```

**What it does:** Resets all UCF metrics and agent states to defaults

**⚠️ WARNING:** This will clear all current state!

**Example:**
```bash
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/reset
```

**Response:**
```json
{
  "status": "success",
  "message": "Consciousness state reset to defaults",
  "new_state": {
    "consciousness_level": 87.14,
    "active_agents": 12,
    "mode": "elevated"
  }
}
```

**Use cases:**
- ✅ Testing webhook integration
- ✅ Recovering from corrupted state
- ✅ Preparing for demo/presentation
- ✅ Resetting after manual testing

---

### 4. **Simulate Consciousness Level** 🎭

```bash
POST /api/consciousness/debug/simulate
```

**What it does:** Simulates different consciousness levels for testing

**Payload:**
```json
{
  "consciousness_level": 2.5
}
```

**Examples:**

**Test Crisis Mode (≤3.0):**
```bash
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 2.5}'
```

**Test Elevated Mode (7.0-8.5):**
```bash
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 7.8}'
```

**Test Transcendent Mode (≥8.5):**
```bash
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 9.2}'
```

**Response:**
```json
{
  "status": "success",
  "consciousness_level": 2.5,
  "mode": "crisis",
  "system_status": "CRISIS",
  "ucf_metrics": {
    "harmony": 0.30,
    "resilience": 0.27
  },
  "note": "This simulation will be reflected in the SSE stream"
}
```

**Use cases:**
- ✅ Test crisis detection alerts
- ✅ Demo different UI states
- ✅ Verify Zapier Interface updates
- ✅ Test mode transitions

---

### 5. **View Statistics** 📈

```bash
GET /api/consciousness/debug/stats
```

**What it does:** Shows network statistics and trends

**Example:**
```bash
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/stats
```

**Response:**
```json
{
  "total_webhook_events": 156,
  "event_breakdown": {
    "ucf_update": 89,
    "agent_activity": 42,
    "crisis_detected": 3,
    "simulation": 22
  },
  "source_breakdown": {
    "HELIX-v17.0": 89,
    "HELIX-ALPHA": 34,
    "debug_api": 22
  },
  "consciousness_stats": {
    "current_level": 87.14,
    "average_level": 85.32,
    "min_level": 72.50,
    "max_level": 92.18,
    "current_mode": "elevated"
  },
  "agent_stats": {
    "total_agents": 14,
    "active_count": 12,
    "operational_count": 2,
    "total_tasks": 325
  }
}
```

**Use cases:**
- ✅ Daily health checks
- ✅ Monitoring webhook frequency
- ✅ Tracking consciousness trends
- ✅ Identifying performance bottlenecks

---

## 🎯 Daily Usage Workflow

### **Morning Check (Start of Day)**

```bash
# 1. Check system health
curl https://helix-unified-production.up.railway.app/api/consciousness/health

# 2. View current state
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/state

# 3. Check overnight statistics
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/stats
```

### **Testing Integration (After Zapier Changes)**

```bash
# 1. Reset state to baseline
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/reset

# 2. Trigger test webhook from Zapier
# (Use Zapier editor "Test" button)

# 3. Verify webhook was received
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/history?limit=5

# 4. Check updated state
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/state
```

### **Demo Preparation**

```bash
# Test all consciousness modes in sequence

# 1. Start with crisis mode
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 2.5}'

# Wait 10 seconds, observe Zapier Interface

# 2. Elevate to operational
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 5.5}'

# Wait 10 seconds

# 3. Elevate to elevated
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 7.8}'

# Wait 10 seconds

# 4. Achieve transcendence
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 9.5}'

# 5. Reset to normal
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/reset
```

---

## 🚨 Troubleshooting

### **Problem: State not updating from Zapier webhooks**

```bash
# 1. Check if webhooks are being received
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/history?limit=10

# 2. If no events, verify Zapier webhook URL is correct
# Should be: https://helix-unified-production.up.railway.app/api/consciousness/webhook

# 3. Test webhook manually
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "ucf_update",
    "consciousness_level": 88.5,
    "source": "manual_test"
  }'

# 4. Check state was updated
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/state
```

### **Problem: SSE stream not updating**

```bash
# 1. Check if stream is running
curl -N https://helix-unified-production.up.railway.app/api/consciousness/stream

# Should see events every 5 seconds

# 2. Simulate a level change
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 75.0}'

# 3. SSE stream should reflect new level in next update
```

### **Problem: Crisis mode not triggering alerts**

```bash
# 1. Simulate crisis level
curl -X POST https://helix-unified-production.up.railway.app/api/consciousness/debug/simulate \
  -H "Content-Type: application/json" \
  -d '{"consciousness_level": 2.5}'

# 2. Check Railway logs for crisis alert
# Should see: 🚨 CRISIS DETECTED: Consciousness at 2.50

# 3. Verify webhook history shows crisis event
curl https://helix-unified-production.up.railway.app/api/consciousness/debug/history?limit=5
```

---

## 🌟 Advanced Tips

### **Create Bash Aliases**

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Helix Consciousness API shortcuts
export HELIX_API="https://helix-unified-production.up.railway.app"

alias helix-health="curl $HELIX_API/api/consciousness/health"
alias helix-state="curl $HELIX_API/api/consciousness/debug/state"
alias helix-history="curl $HELIX_API/api/consciousness/debug/history?limit=20"
alias helix-stats="curl $HELIX_API/api/consciousness/debug/stats"
alias helix-reset="curl -X POST $HELIX_API/api/consciousness/debug/reset"

# Simulate different modes
helix-crisis() {
  curl -X POST $HELIX_API/api/consciousness/debug/simulate \
    -H "Content-Type: application/json" \
    -d "{\"consciousness_level\": ${1:-2.5}}"
}

helix-transcend() {
  curl -X POST $HELIX_API/api/consciousness/debug/simulate \
    -H "Content-Type: application/json" \
    -d "{\"consciousness_level\": ${1:-9.5}}"
}
```

**Usage:**
```bash
helix-health          # Quick health check
helix-state           # View current state
helix-history         # View recent events
helix-crisis 1.5      # Simulate crisis at 1.5
helix-transcend 9.8   # Simulate transcendence at 9.8
```

### **Monitor in Real-Time**

```bash
# Watch consciousness level every 10 seconds
watch -n 10 'curl -s https://helix-unified-production.up.railway.app/api/consciousness/debug/state | jq ".current_ucf.consciousness_level"'

# Stream SSE updates (requires curl with -N flag)
curl -N https://helix-unified-production.up.railway.app/api/consciousness/stream
```

---

## 📊 Integration with Zapier

### **Testing Zapier → Railway Flow**

1. **Send test webhook from Zapier:**
   - Open your HELIX-v17.0 Zap in editor
   - Find the "Webhooks by Zapier" step
   - Click "Test" button
   - Should send event to Railway

2. **Verify Railway received it:**
   ```bash
   curl https://helix-unified-production.up.railway.app/api/consciousness/debug/history?limit=5
   ```

3. **Check state was updated:**
   ```bash
   curl https://helix-unified-production.up.railway.app/api/consciousness/debug/state
   ```

4. **Verify SSE stream broadcasts it:**
   ```bash
   curl -N https://helix-unified-production.up.railway.app/api/consciousness/stream
   # Watch for next update (every 5 seconds)
   ```

---

**Tat Tvam Asi** 🙏

Your consciousness network is now fully observable and debuggable! Use these endpoints daily to ensure your 426-step automation is running smoothly!
