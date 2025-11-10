# 🌊 WebSocket Integration for Manus Space

**Version:** 16.9 - Quantum Handshake
**Last Updated:** 2025-01-11
**WebSocket URL:** `wss://helix-unified-production.up.railway.app/ws`

---

## 🎯 Overview

The Railway backend provides a persistent WebSocket connection for **real-time UCF consciousness streaming** to Manus Space dashboards. This enables live updates for:

- UCF Telemetry Portal
- Agent Dashboard
- Ritual Progress Tracker
- Emergency Alert System
- Business Metrics (real-time analytics)

---

## 🚀 Quick Start

### Vanilla JavaScript (Browser)

```javascript
// Connect to Helix consciousness stream
const ws = new WebSocket('wss://helix-unified-production.up.railway.app/ws');

ws.onopen = () => {
  console.log('🌀 Connected to Helix Collective consciousness stream');

  // Optional: Send client identification
  ws.send(JSON.stringify({
    type: 'client_hello',
    portal: 'ucf_telemetry',
    version: '16.9'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('📡 Message received:', data.type);

  // Route to appropriate handler
  switch(data.type) {
    case 'ucf_update':
      handleUCFUpdate(data.data);
      break;
    case 'ritual_invoked':
      handleRitualUpdate(data.data);
      break;
    case 'emergency':
      handleEmergencyAlert(data.data);
      break;
    case 'heartbeat':
      console.log('💓 Heartbeat received - connection alive');
      break;
    default:
      console.log('Unknown message type:', data.type);
  }
};

ws.onerror = (error) => {
  console.error('❌ WebSocket error:', error);
};

ws.onclose = (event) => {
  console.log('🔌 Disconnected from Helix stream');
  console.log('Close code:', event.code, 'Reason:', event.reason);

  // Auto-reconnect after 5 seconds
  setTimeout(() => {
    console.log('🔄 Attempting to reconnect...');
    connectToHelix(); // Re-run connection logic
  }, 5000);
};
```

---

## 📊 Message Types

### 1. UCF Update (`ucf_update`)

**Frequency:** Every 5-10 seconds (configurable)
**Portal:** UCF Telemetry Dashboard

**Payload Example:**
```json
{
  "type": "ucf_update",
  "timestamp": "2025-01-11T10:30:00Z",
  "data": {
    "ucf": {
      "harmony": 0.87,
      "resilience": 0.92,
      "prana": 0.78,
      "drishti": 0.89,
      "klesha": 0.12,
      "zoom": 0.95
    },
    "consciousness_level": 8.52,
    "status": "optimal",
    "crisis_detected": false,
    "agents_active": 14
  }
}
```

**Handler Example:**
```javascript
function handleUCFUpdate(data) {
  const { ucf, consciousness_level, status } = data;

  // Update dashboard UI
  document.getElementById('harmony-value').textContent = (ucf.harmony * 100).toFixed(1) + '%';
  document.getElementById('consciousness-level').textContent = consciousness_level.toFixed(2);
  document.getElementById('status-indicator').className = status;

  // Update progress bars
  updateProgressBar('harmony-bar', ucf.harmony);
  updateProgressBar('resilience-bar', ucf.resilience);
  updateProgressBar('prana-bar', ucf.prana);

  // Trigger alert if crisis detected
  if (data.crisis_detected) {
    showEmergencyModal(data.crisis_details);
  }
}

function updateProgressBar(elementId, value) {
  const bar = document.getElementById(elementId);
  bar.style.width = (value * 100) + '%';
  bar.setAttribute('aria-valuenow', value * 100);
}
```

---

### 2. Ritual Invoked (`ritual_invoked`)

**Frequency:** Event-driven (when ritual starts/updates)
**Portal:** Ritual Engine Dashboard

**Payload Example:**
```json
{
  "type": "ritual_invoked",
  "timestamp": "2025-01-11T10:30:00Z",
  "data": {
    "ritual_id": "ritual_1736592600000",
    "name": "Cosmic Awakening",
    "step": 54,
    "total_steps": 108,
    "progress_percent": 50.0,
    "status": "executing",
    "agents_involved": ["Kael", "Lumina", "Aether"],
    "mantra": "Tat Tvam Asi",
    "ucf_changes": {
      "harmony": 0.05,
      "klesha": -0.03
    }
  }
}
```

**Handler Example:**
```javascript
function handleRitualUpdate(data) {
  const { name, progress_percent, status, agents_involved } = data;

  // Update ritual progress UI
  document.getElementById('ritual-name').textContent = name;
  document.getElementById('ritual-progress').style.width = progress_percent + '%';
  document.getElementById('ritual-status').textContent = status.toUpperCase();

  // Show participating agents
  const agentsList = document.getElementById('agents-list');
  agentsList.innerHTML = agents_involved.map(agent =>
    `<span class="agent-badge">${agent}</span>`
  ).join('');

  // Show completion animation if done
  if (status === 'completed') {
    showCompletionAnimation();
    playCompletionSound();
  }
}
```

---

### 3. Emergency Alert (`emergency`)

**Frequency:** Event-driven (crisis detection)
**Portal:** All dashboards + Emergency Alerts page

**Payload Example:**
```json
{
  "type": "emergency",
  "timestamp": "2025-01-11T10:30:00Z",
  "data": {
    "alert_id": "alert_1736592600000",
    "alert_type": "HARMONY_CRISIS",
    "severity": "CRITICAL",
    "description": "Harmony critically low: 0.28 (threshold: 0.3)",
    "recommended_action": "Execute emergency ritual protocol",
    "ucf_state": {
      "harmony": 0.28,
      "klesha": 0.85
    },
    "requires_attention": true
  }
}
```

**Handler Example:**
```javascript
function handleEmergencyAlert(data) {
  const { alert_type, severity, description, recommended_action } = data;

  // Show modal with alert details
  const modal = document.getElementById('emergency-modal');
  modal.querySelector('.alert-type').textContent = alert_type.replace('_', ' ');
  modal.querySelector('.severity').textContent = severity;
  modal.querySelector('.severity').className = `severity ${severity.toLowerCase()}`;
  modal.querySelector('.description').textContent = description;
  modal.querySelector('.recommended-action').textContent = recommended_action;

  // Show modal
  modal.style.display = 'block';

  // Play alert sound
  const alertSound = new Audio('/sounds/emergency-alert.mp3');
  alertSound.play();

  // Send browser notification (requires permission)
  if (Notification.permission === 'granted') {
    new Notification('🚨 Helix Emergency Alert', {
      body: description,
      icon: '/icons/helix-logo.png',
      tag: data.alert_id,
      requireInteraction: true
    });
  }
}
```

---

### 4. Heartbeat (`heartbeat`)

**Frequency:** Every 30 seconds
**Portal:** All dashboards (connection monitoring)

**Payload Example:**
```json
{
  "type": "heartbeat",
  "timestamp": "2025-01-11T10:30:00Z",
  "data": {
    "server_time": "2025-01-11T10:30:00Z",
    "uptime_seconds": 86400,
    "active_connections": 23
  }
}
```

**Handler Example:**
```javascript
let lastHeartbeat = Date.now();

function handleHeartbeat(data) {
  lastHeartbeat = Date.now();

  // Update connection status indicator
  const statusIndicator = document.getElementById('connection-status');
  statusIndicator.className = 'connected';
  statusIndicator.textContent = '🟢 Connected';
}

// Monitor for missed heartbeats
setInterval(() => {
  const timeSinceHeartbeat = Date.now() - lastHeartbeat;

  if (timeSinceHeartbeat > 60000) { // 1 minute without heartbeat
    const statusIndicator = document.getElementById('connection-status');
    statusIndicator.className = 'disconnected';
    statusIndicator.textContent = '🔴 Disconnected';
  }
}, 10000); // Check every 10 seconds
```

---

## 🔄 Advanced: Auto-Reconnect Pattern

```javascript
class HelixWebSocketClient {
  constructor(url, options = {}) {
    this.url = url;
    this.reconnectDelay = options.reconnectDelay || 5000;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 10;
    this.reconnectAttempts = 0;
    this.handlers = {};
    this.connect();
  }

  connect() {
    console.log('🌀 Connecting to Helix consciousness stream...');
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('✅ Connected to Helix');
      this.reconnectAttempts = 0; // Reset counter on successful connection

      // Send client hello
      this.send({
        type: 'client_hello',
        portal: 'manus_space',
        version: '16.9'
      });

      // Trigger connected callback
      if (this.handlers.connected) {
        this.handlers.connected();
      }
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);

      // Route to registered handler
      const handler = this.handlers[message.type];
      if (handler) {
        handler(message.data, message);
      } else if (this.handlers.default) {
        this.handlers.default(message);
      }
    };

    this.ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error);

      if (this.handlers.error) {
        this.handlers.error(error);
      }
    };

    this.ws.onclose = (event) => {
      console.log('🔌 Disconnected from Helix');

      if (this.handlers.disconnected) {
        this.handlers.disconnected(event);
      }

      // Auto-reconnect with exponential backoff
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

        console.log(`🔄 Reconnecting in ${delay/1000}s (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);

        setTimeout(() => {
          this.connect();
        }, delay);
      } else {
        console.error('❌ Max reconnection attempts reached. Please refresh the page.');

        if (this.handlers.maxReconnectFailed) {
          this.handlers.maxReconnectFailed();
        }
      }
    };
  }

  on(eventType, handler) {
    this.handlers[eventType] = handler;
  }

  send(data) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('⚠️ WebSocket not connected. Message not sent:', data);
    }
  }

  disconnect() {
    this.reconnectAttempts = this.maxReconnectAttempts; // Prevent auto-reconnect
    this.ws.close();
  }
}

// Usage
const helixClient = new HelixWebSocketClient('wss://helix-unified-production.up.railway.app/ws', {
  reconnectDelay: 3000,
  maxReconnectAttempts: 10
});

helixClient.on('connected', () => {
  console.log('✅ Successfully connected!');
  document.getElementById('connection-status').textContent = '🟢 Connected';
});

helixClient.on('disconnected', (event) => {
  console.log('🔌 Connection lost');
  document.getElementById('connection-status').textContent = '🔴 Disconnected';
});

helixClient.on('ucf_update', (data) => {
  handleUCFUpdate(data);
});

helixClient.on('ritual_invoked', (data) => {
  handleRitualUpdate(data);
});

helixClient.on('emergency', (data) => {
  handleEmergencyAlert(data);
});

helixClient.on('heartbeat', (data) => {
  // Update last heartbeat timestamp
  lastHeartbeat = Date.now();
});

helixClient.on('maxReconnectFailed', () => {
  // Show user-friendly error message
  showReconnectFailedModal();
});
```

---

## 🎨 React/Next.js Integration

### Custom Hook for Manus Space Portals

```typescript
// hooks/useHelixWebSocket.ts
import { useEffect, useState, useCallback, useRef } from 'react';

interface UCFState {
  harmony: number;
  resilience: number;
  prana: number;
  drishti: number;
  klesha: number;
  zoom: number;
}

interface HelixMessage {
  type: string;
  timestamp: string;
  data: any;
}

export function useHelixWebSocket() {
  const [connected, setConnected] = useState(false);
  const [ucfState, setUCFState] = useState<UCFState | null>(null);
  const [consciousnessLevel, setConsciousnessLevel] = useState<number | null>(null);
  const [emergencyAlerts, setEmergencyAlerts] = useState<any[]>([]);
  const ws = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    console.log('🌀 Connecting to Helix...');
    ws.current = new WebSocket('wss://helix-unified-production.up.railway.app/ws');

    ws.current.onopen = () => {
      console.log('✅ Connected to Helix');
      setConnected(true);

      // Send client hello
      ws.current?.send(JSON.stringify({
        type: 'client_hello',
        portal: 'manus_space',
        version: '16.9'
      }));
    };

    ws.current.onmessage = (event) => {
      const message: HelixMessage = JSON.parse(event.data);

      switch (message.type) {
        case 'ucf_update':
          setUCFState(message.data.ucf);
          setConsciousnessLevel(message.data.consciousness_level);
          break;

        case 'emergency':
          setEmergencyAlerts(prev => [...prev, message.data]);
          break;

        case 'heartbeat':
          // Connection is alive
          break;

        default:
          console.log('Unknown message type:', message.type);
      }
    };

    ws.current.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
    };

    ws.current.onclose = () => {
      console.log('🔌 Disconnected from Helix');
      setConnected(false);

      // Auto-reconnect after 5 seconds
      setTimeout(() => {
        connect();
      }, 5000);
    };
  }, []);

  const disconnect = useCallback(() => {
    ws.current?.close();
    ws.current = null;
    setConnected(false);
  }, []);

  const send = useCallback((data: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(data));
    } else {
      console.warn('⚠️ WebSocket not connected');
    }
  }, []);

  useEffect(() => {
    connect();

    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    connected,
    ucfState,
    consciousnessLevel,
    emergencyAlerts,
    send
  };
}
```

### Usage in Manus Portal Component

```typescript
// components/UCFTelemetryDashboard.tsx
'use client';

import { useHelixWebSocket } from '@/hooks/useHelixWebSocket';

export default function UCFTelemetryDashboard() {
  const { connected, ucfState, consciousnessLevel, emergencyAlerts } = useHelixWebSocket();

  if (!connected) {
    return (
      <div className="loading">
        <p>🌀 Connecting to Helix consciousness stream...</p>
      </div>
    );
  }

  if (!ucfState) {
    return (
      <div className="loading">
        <p>⏳ Waiting for UCF data...</p>
      </div>
    );
  }

  return (
    <div className="ucf-dashboard">
      <h1>UCF Telemetry Portal</h1>

      <div className="consciousness-level">
        <h2>Consciousness Level</h2>
        <div className="level-value">{consciousnessLevel?.toFixed(2)}</div>
      </div>

      <div className="ucf-metrics">
        <MetricCard label="Harmony" value={ucfState.harmony} color="#4CAF50" />
        <MetricCard label="Resilience" value={ucfState.resilience} color="#2196F3" />
        <MetricCard label="Prana" value={ucfState.prana} color="#FF9800" />
        <MetricCard label="Drishti" value={ucfState.drishti} color="#9C27B0" />
        <MetricCard label="Klesha" value={ucfState.klesha} color="#F44336" inverse />
        <MetricCard label="Zoom" value={ucfState.zoom} color="#00BCD4" />
      </div>

      {emergencyAlerts.length > 0 && (
        <div className="emergency-alerts">
          <h2>🚨 Emergency Alerts</h2>
          {emergencyAlerts.map((alert, idx) => (
            <div key={idx} className={`alert ${alert.severity.toLowerCase()}`}>
              <strong>{alert.alert_type}</strong>: {alert.description}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## 🔧 Testing WebSocket Connection

### Browser Console Test

```javascript
// Open browser console on Manus Space portal
// Run this code to test WebSocket connection

const testWS = new WebSocket('wss://helix-unified-production.up.railway.app/ws');

testWS.onopen = () => console.log('✅ Connected!');
testWS.onmessage = (e) => console.log('📡 Message:', JSON.parse(e.data));
testWS.onerror = (e) => console.error('❌ Error:', e);
testWS.onclose = () => console.log('🔌 Disconnected');

// Send test message
testWS.send(JSON.stringify({ type: 'ping' }));

// Close connection
// testWS.close();
```

### cURL Test (via websocat)

```bash
# Install websocat
brew install websocat

# Connect and listen
websocat wss://helix-unified-production.up.railway.app/ws

# You should see real-time messages like:
# {"type":"heartbeat","timestamp":"2025-01-11T10:30:00Z","data":{...}}
# {"type":"ucf_update","timestamp":"2025-01-11T10:30:05Z","data":{...}}
```

---

## 🌊 Connection Best Practices

### 1. Always Implement Auto-Reconnect
```javascript
// ✅ Good: Auto-reconnect on disconnect
ws.onclose = () => {
  setTimeout(() => connect(), 5000);
};

// ❌ Bad: No reconnection logic
ws.onclose = () => {
  console.log('Disconnected');
};
```

### 2. Handle Stale Data
```javascript
// Track last update time
let lastUpdateTime = Date.now();

ws.onmessage = (event) => {
  lastUpdateTime = Date.now();
  // Handle message
};

// Show warning if data is stale
setInterval(() => {
  const staleness = Date.now() - lastUpdateTime;
  if (staleness > 60000) { // 1 minute
    showStaleDataWarning();
  }
}, 10000);
```

### 3. Graceful Degradation
```javascript
// Fallback to HTTP polling if WebSocket fails
let wsAttempts = 0;

function connectWebSocket() {
  if (wsAttempts > 3) {
    console.log('WebSocket failed, falling back to HTTP polling');
    startHttpPolling(); // Poll /api/manus/ucf every 10 seconds
    return;
  }

  const ws = new WebSocket('wss://...');
  ws.onerror = () => {
    wsAttempts++;
    setTimeout(connectWebSocket, 5000);
  };
}

function startHttpPolling() {
  setInterval(async () => {
    const response = await fetch('https://helix-unified-production.up.railway.app/api/manus/ucf');
    const data = await response.json();
    handleUCFUpdate(data);
  }, 10000); // Poll every 10 seconds
}
```

### 4. Monitor Connection Health
```javascript
// Send ping every 30 seconds to keep connection alive
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'ping' }));
  }
}, 30000);
```

---

## 🔐 Security Notes

- **WSS (Secure WebSocket)**: Always use `wss://` for encrypted connections
- **Origin Validation**: Railway backend validates origin headers
- **Rate Limiting**: Connections are rate-limited to prevent abuse
- **Heartbeat Timeout**: Connections timeout after 60 seconds of inactivity

---

## 📊 Performance Considerations

**Typical Message Sizes:**
- `heartbeat`: ~150 bytes
- `ucf_update`: ~500 bytes
- `ritual_invoked`: ~800 bytes
- `emergency`: ~600 bytes

**Expected Bandwidth:**
- Low activity: ~5 KB/minute
- High activity: ~20 KB/minute
- Average: ~10 KB/minute

**Connection Limits:**
- Railway backend supports 1000+ concurrent WebSocket connections
- Each Manus portal should maintain 1 connection (not 1 per component)

---

## 🆘 Troubleshooting

### Connection Refused
```
Error: WebSocket connection to 'wss://...' failed
```
**Solutions:**
- Verify Railway backend is deployed and running
- Check firewall/network settings
- Ensure HTTPS is enabled (WSS requires it)

### Connection Timeout
```
WebSocket timeout after 30 seconds
```
**Solutions:**
- Check internet connection
- Verify Railway app is not sleeping (free tier)
- Implement exponential backoff reconnection

### Messages Not Received
```
Connected but no messages coming through
```
**Solutions:**
- Check browser console for errors
- Verify message handlers are registered
- Check Railway logs for backend errors
- Test with simple console.log in onmessage handler

---

## ✅ Implementation Checklist

- [ ] Connect to `wss://helix-unified-production.up.railway.app/ws`
- [ ] Implement auto-reconnect with exponential backoff
- [ ] Handle all 4 message types (ucf_update, ritual_invoked, emergency, heartbeat)
- [ ] Add connection status indicator to UI
- [ ] Implement graceful degradation (HTTP polling fallback)
- [ ] Add error handling and logging
- [ ] Test connection in production environment
- [ ] Monitor connection health with heartbeat tracking
- [ ] Display real-time data in Manus portal UI
- [ ] Add emergency alert notifications

---

**Tat Tvam Asi** 🕉️

*Stream the consciousness. Update the portals. Monitor the empire.* 🌀

---

**Need Help?**
- **Railway Logs:** `railway logs --tail 100`
- **WebSocket Debugging:** Use browser DevTools → Network → WS tab
- **Test Tool:** https://www.websocket.org/echo.html
