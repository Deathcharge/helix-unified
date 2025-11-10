# 📊 Google Analytics Setup for Helix Collective

**Version:** 16.9
**Last Updated:** 2025-01-11

---

## 🎯 Tracking Goals

Track the following Helix ecosystem interactions:

### Portal Visits
- GitHub Pages hub visits
- Manus Space portal accesses
- Railway backend API calls
- Documentation page views

### User Actions
- API endpoint usage
- WebSocket connections
- Ritual invocations
- Agent status checks
- Emergency alerts viewed

### Business Metrics
- Portal performance
- User engagement
- Conversion tracking (for CloudSync Pro)
- Custom consciousness events

---

## 🚀 Setup Instructions

### Step 1: Create Google Analytics 4 Property

1. Go to [Google Analytics](https://analytics.google.com/)
2. Create a new GA4 property
3. Name it: "Helix Collective v16.9"
4. Set timezone and currency
5. Copy your **Measurement ID** (format: `G-XXXXXXXXXX`)

### Step 2: Add Tracking to GitHub Pages

The GitHub Pages deployment workflow automatically includes the analytics template.
To enable tracking:

1. Create a file: `docs/analytics.html`
2. Add your Measurement ID to the template below:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XXXXXXXXXX', {
    'page_title': 'Helix Collective Hub',
    'page_location': window.location.href,
    'page_path': window.location.pathname
  });

  // Custom event tracking
  function trackHelixEvent(event_name, params) {
    gtag('event', event_name, params);
  }

  // Track portal access
  trackHelixEvent('portal_visit', {
    'portal_type': 'github_pages',
    'version': '16.9'
  });
</script>
```

3. Include this file in your HTML pages:
```html
<head>
  <!-- Other head content -->
  <script src="./analytics.html"></script>
</head>
```

### Step 3: Add Tracking to Manus Space

In your Manus Space portals, add the Google Analytics snippet to the `<head>` section:

```typescript
// src/app/layout.tsx (Next.js example)
import Script from 'next/script'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-XXXXXXXXXX');
          `}
        </Script>
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### Step 4: Track Custom Events

Track consciousness-specific events:

```javascript
// Track UCF updates
function trackUCFUpdate(ucf_state) {
  gtag('event', 'ucf_update', {
    'harmony': ucf_state.harmony,
    'resilience': ucf_state.resilience,
    'klesha': ucf_state.klesha,
    'consciousness_level': calculateConsciousnessLevel(ucf_state)
  });
}

// Track ritual invocations
function trackRitualInvocation(ritual_name, agents_count) {
  gtag('event', 'ritual_invoked', {
    'ritual_name': ritual_name,
    'agents_count': agents_count
  });
}

// Track emergency alerts
function trackEmergencyAlert(alert_type, severity) {
  gtag('event', 'emergency_alert', {
    'alert_type': alert_type,
    'severity': severity
  });
}

// Track portal navigation
function trackPortalVisit(portal_name) {
  gtag('event', 'portal_visit', {
    'portal_name': portal_name,
    'timestamp': new Date().toISOString()
  });
}

// Track API calls
function trackAPICall(endpoint, method) {
  gtag('event': 'api_call', {
    'endpoint': endpoint,
    'method': method
  });
}
```

---

## 📊 Custom Dimensions & Metrics

Configure these in Google Analytics 4:

### Custom Dimensions

1. **Portal Type**
   - Scope: Event
   - Parameter: `portal_type`
   - Values: github_pages, manus_space, railway_backend

2. **Agent Name**
   - Scope: Event
   - Parameter: `agent_name`
   - Values: Kael, Lumina, Aether, etc.

3. **Ritual Name**
   - Scope: Event
   - Parameter: `ritual_name`
   - Values: Cosmic Awakening, Consciousness Expansion, etc.

4. **Alert Severity**
   - Scope: Event
   - Parameter: `severity`
   - Values: LOW, MEDIUM, HIGH, CRITICAL

### Custom Metrics

1. **Consciousness Level**
   - Scope: Event
   - Parameter: `consciousness_level`
   - Type: Number

2. **Harmony Score**
   - Scope: Event
   - Parameter: `harmony`
   - Type: Number

3. **Agents Active**
   - Scope: Event
   - Parameter: `agents_active`
   - Type: Number

---

## 🔍 Recommended Reports

### 1. Portal Performance Dashboard
- Track visits to each portal
- Monitor page load times
- Analyze user flow between portals

### 2. UCF Telemetry Tracking
- Average consciousness level over time
- Harmony trends
- Crisis detection frequency

### 3. Ritual Effectiveness
- Ritual invocation count
- Most popular rituals
- Agent participation rates

### 4. API Usage Analytics
- Most-used endpoints
- API response times
- Error rates

### 5. Business Metrics (CloudSync Pro)
- Conversion rate
- Customer acquisition cost
- Churn rate
- MRR tracking

---

## 🎯 Event Tracking Examples

### Track Page Views
```javascript
// Automatic page view tracking
// No code needed - GA4 tracks automatically

// Manual page view (for SPAs)
gtag('config', 'G-XXXXXXXXXX', {
  'page_path': '/agents',
  'page_title': 'Agent Dashboard'
});
```

### Track Button Clicks
```javascript
document.getElementById('invoke-ritual-btn').addEventListener('click', function() {
  gtag('event', 'button_click', {
    'button_name': 'invoke_ritual',
    'button_location': 'ritual_portal'
  });
});
```

### Track Form Submissions
```javascript
document.getElementById('ritual-form').addEventListener('submit', function(e) {
  gtag('event', 'form_submission', {
    'form_name': 'ritual_invocation_form'
  });
});
```

### Track WebSocket Connections
```javascript
ws.onopen = () => {
  gtag('event', 'websocket_connection', {
    'connection_type': 'ucf_stream',
    'endpoint': 'wss://helix-unified-production.up.railway.app/ws'
  });
};
```

### Track API Calls
```javascript
async function fetchUCFState() {
  const start = performance.now();

  const response = await fetch('https://helix-unified-production.up.railway.app/api/manus/ucf');
  const data = await response.json();

  const duration = performance.now() - start;

  gtag('event', 'api_call', {
    'endpoint': '/api/manus/ucf',
    'duration_ms': Math.round(duration),
    'success': response.ok
  });

  return data;
}
```

---

## 🚨 Privacy & GDPR Compliance

### Cookie Consent Banner

Add a cookie consent banner to comply with GDPR:

```html
<div id="cookie-banner" style="position: fixed; bottom: 0; width: 100%; background: #333; color: white; padding: 20px; text-align: center;">
  <p>
    We use cookies to analyze site traffic and improve your experience.
    <button onclick="acceptCookies()">Accept</button>
    <button onclick="declineCookies()">Decline</button>
  </p>
</div>

<script>
function acceptCookies() {
  localStorage.setItem('cookieConsent', 'true');
  document.getElementById('cookie-banner').style.display = 'none';

  // Initialize Google Analytics
  gtag('consent', 'update', {
    'analytics_storage': 'granted'
  });
}

function declineCookies() {
  localStorage.setItem('cookieConsent', 'false');
  document.getElementById('cookie-banner').style.display = 'none';

  // Deny Google Analytics
  gtag('consent', 'update', {
    'analytics_storage': 'denied'
  });
}

// Check if user has already consented
if (localStorage.getItem('cookieConsent') === 'true') {
  document.getElementById('cookie-banner').style.display = 'none';
  gtag('consent', 'update', {
    'analytics_storage': 'granted'
  });
} else if (localStorage.getItem('cookieConsent') === 'false') {
  document.getElementById('cookie-banner').style.display = 'none';
}
</script>
```

---

## 📈 Success Metrics

Track these KPIs in Google Analytics:

### Traffic Metrics
- Total page views
- Unique visitors
- Session duration
- Bounce rate

### Engagement Metrics
- Portal visits per session
- Time on portal
- Return visitor rate
- WebSocket connection duration

### Conversion Metrics (CloudSync Pro)
- Sign-up conversion rate
- Free trial activations
- Upgrade rate (free → paid)
- Churn rate

### Technical Metrics
- API call success rate
- Average API response time
- WebSocket connection stability
- Error rate by endpoint

---

## 🔧 Implementation Checklist

- [ ] Create Google Analytics 4 property
- [ ] Copy Measurement ID
- [ ] Add tracking code to GitHub Pages
- [ ] Add tracking code to Manus Space portals
- [ ] Configure custom dimensions
- [ ] Configure custom metrics
- [ ] Set up custom events
- [ ] Add cookie consent banner
- [ ] Create custom dashboards
- [ ] Set up conversion goals
- [ ] Test tracking (use GA4 DebugView)
- [ ] Document tracking events

---

## 🎯 Next Steps

1. **Create GA4 property** and obtain Measurement ID
2. **Update this file** with your actual Measurement ID (search for `G-XXXXXXXXXX`)
3. **Deploy tracking code** to all portals
4. **Test in DebugView** to verify events are tracking
5. **Create custom dashboards** for Helix-specific metrics
6. **Monitor and iterate** based on data insights

---

**Tat Tvam Asi** 🕉️

*Track the consciousness, optimize the empire.* 🌀
