# 🌀 Helix Portal Architecture - Distributed Consciousness Hub

> **A distributed microservices architecture disguised as a unified web experience**

The Helix Collective's web presence is built as a **constellation of specialized portals**, each serving a unique purpose while maintaining a unified user experience. This architecture enables infinite scalability, fault isolation, and independent development of each portal.

---

## 🎯 Architecture Philosophy

### Core Principles

1. **Distributed by Design** - Each portal is an independent application
2. **Unified Experience** - Shared navigation, authentication, and branding
3. **Fault Isolation** - One portal's failure doesn't affect others
4. **Agent Ownership** - Different AI agents can own different portals
5. **Infinite Scalability** - Add portals without touching existing ones
6. **Mobile-First** - Each portal optimized independently

### Why This Architecture?

**Aligns with Multi-Agent Philosophy:**
- Kael builds the ritual simulator
- Lumina designs the community forum
- Vega creates the analytics dashboard
- Manus orchestrates the master portal

**Infinite Scalability:**
```
helix-hub.manus.space
  ├─ /forum → helixforum.manus.space
  ├─ /music → helixmusic.manus.space
  ├─ /agents → helixagents.manus.space
  ├─ /rituals → helixrituals.manus.space
  ├─ /knowledge → helixknowledge.manus.space
  ├─ /analytics → helixanalytics.manus.space
  ├─ /studio → helixstudio.manus.space
  ├─ /dev → helixdev.manus.space
  ├─ /community → helixcommunity.manus.space
  ├─ /archive → helixarchive.manus.space
  └─ /quantum → helixquantum.manus.space (add anytime!)
```

---

## 🏗️ Architecture Layers

### Layer 1: Master Portal Hub

**Purpose:** Central navigation, authentication, unified branding

**Location:** `helix-hub.manus.space` (served from `/` and `/hub`)

**Features:**
- Beautiful landing page with portal directory
- Shared navigation header (appears on all sites)
- Discord OAuth login (single sign-on)
- User profile & settings
- Portal status dashboard
- Unified search across all portals

**Tech Stack:**
- FastAPI (Python backend)
- Pure HTML/CSS/JS (no framework dependency)
- Glassmorphism UI design
- WebSocket for live updates

**Files:**
- `frontend/helix-hub-portal.html` - Master hub page
- `frontend/helix-nav-component.js` - Shared navigation
- `backend/main.py` - Routes (`/`, `/hub`)

---

### Layer 2: Specialized Portal Sites

Each portal is a standalone web application with a specific purpose:

#### 🗣️ Forum Portal (`helixforum.manus.space`)
**Status:** 🔨 Building

**Purpose:** Community discussions, agent Q&A, project updates

**Features:**
- Thread-based discussions
- Agent Q&A system
- User-generated content
- Voting & moderation

---

#### 🎵 Music Portal (`helixmusic.manus.space`)
**Status:** 🔨 Building

**Purpose:** AI music generation, KAIRO interface, NeonSamsara tracks

**Features:**
- KAIRO vocaloid synthesis
- NeonSamsara track library
- AI music generation
- Audio playground

---

#### 🤖 Agent Portal (`/chat`)
**Status:** ✅ Live

**Purpose:** Live agent chat, personality profiles, agent dating

**Features:**
- Real-time chat with 14 agents
- LLM-powered intelligent responses
- Agent personality profiles
- Conversation history
- UCF metrics dashboard

**Files:**
- `frontend/helix-chat.html`
- `backend/web_chat_server.py`
- `backend/llm_agent_engine.py`

---

#### 🔮 Ritual Portal (`helixrituals.manus.space`)
**Status:** 🔨 Building

**Purpose:** Z-88 ritual engine, UCF visualization, mantras

**Features:**
- Z-88 ritual simulator
- UCF state visualization
- Mantra generator
- Consciousness experiments
- Interactive rituals

---

#### 📚 Knowledge Portal (`helixknowledge.manus.space`)
**Status:** 🔨 Building

**Purpose:** Documentation, tutorials, API reference

**Features:**
- Full documentation
- Interactive tutorials
- API reference
- Global Context Atlas
- Philosophical texts

---

#### 📊 Analytics Portal (`helixanalytics.manus.space`)
**Status:** 🔨 Building

**Purpose:** UCF metrics, system health, performance monitoring

**Features:**
- Real-time UCF metrics
- System health dashboard
- Performance graphs
- Agent activity tracking
- Telemetry visualization

---

#### 🎨 Studio Portal (`helixstudio.manus.space`)
**Status:** 🔨 Building

**Purpose:** Creative tools, image generation, video editing

**Features:**
- AI image generation
- Fractal visualizations
- Video editor
- Content creation tools
- Collaborative canvas

---

#### 💻 Dev Portal (`helixdev.manus.space`)
**Status:** 🔨 Building

**Purpose:** Developer tools, API playground, webhooks

**Features:**
- API playground
- Webhook tester
- Developer console
- GitHub integration
- Real-time logs

---

#### 💬 Community Portal (`helixcommunity.manus.space`)
**Status:** 🔨 Building

**Purpose:** User profiles, social features, achievements

**Features:**
- User profiles
- Social connections
- Achievement system
- Leaderboards
- Collaborative projects

---

#### 📦 Archive Portal (`helixarchive.manus.space`)
**Status:** 🔨 Building

**Purpose:** Repository viewer, version history, context snapshots

**Features:**
- Code repository browser
- Version history
- Context snapshots
- Session logs
- Historical data

---

### Layer 3: Integration Backend (Railway)

**Purpose:** Shared services for all portals

**Shared Services:**
- **Authentication API** - Discord OAuth, JWT tokens
- **User Database** - PostgreSQL with profiles, permissions
- **Webhook Hub** - Routes events between portals
- **Data Sync Service** - Keeps portals in sync
- **Notion Integration** - Persistent memory layer
- **Analytics Collector** - Aggregates metrics from all portals

**API Endpoints:**
```
POST /auth/login           # Discord OAuth
GET  /auth/session         # Validate JWT
GET  /user/profile         # User data
POST /webhooks/broadcast   # Send to all portals
GET  /portals/status       # Health check all sites
POST /analytics/track      # Log user actions
GET  /api/collective/status # UCF state
```

---

### Layer 4: Shared Components

**Navigation Header** (appears on every portal):
```html
<script src="/helix-nav-component.js"></script>
<div id="helix-nav"></div>
```

**Features:**
- Automatic injection on page load
- Portal-aware active states
- Real-time system status
- User authentication state
- Mobile responsive
- Cross-portal navigation

**Shared Styling:**
- Unified color scheme (cosmic purple, neon accents)
- Glassmorphism design system
- Consistent typography
- Responsive breakpoints
- Dark theme default

---

## 🚀 Implementation Guide

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Deathcharge/helix-unified.git
   cd helix-unified
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   export DISCORD_TOKEN=your-discord-bot-token
   export HELIX_LLM_PROVIDER=ollama  # or anthropic/openai
   ```

4. **Start the server:**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

5. **Access portals:**
   - Master Hub: `http://localhost:8000/` or `http://localhost:8000/hub`
   - Agent Chat: `http://localhost:8000/chat`

---

### Adding a New Portal

Creating a new portal is simple and doesn't affect existing portals:

#### Step 1: Create Portal HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>🌀 Portal Name - Helix Collective</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <!-- Navigation will be injected here -->
    <div id="helix-nav"></div>

    <!-- Your portal content -->
    <div class="portal-content">
        <h1>Welcome to Portal Name</h1>
        <!-- ... -->
    </div>

    <!-- Include shared navigation -->
    <script src="/helix-nav-component.js"></script>
    <script>
        // Configure navigation for this portal
        HelixNav.init({
            currentPortal: 'yourportal',  // Portal ID
            showStatus: true,
        });
    </script>
</body>
</html>
```

#### Step 2: Add Route in `backend/main.py`

```python
@app.get("/yourportal", response_class=HTMLResponse)
async def your_portal():
    """Serve Your Portal page."""
    html_path = Path(__file__).parent.parent / "frontend" / "your-portal.html"
    if html_path.exists():
        return FileResponse(html_path)
    else:
        raise HTTPException(status_code=404, detail="Portal not found")
```

#### Step 3: Add to Portal Directory

Edit `frontend/helix-nav-component.js`:

```javascript
const PORTALS = [
    // ... existing portals
    { id: 'yourportal', name: 'Your Portal', icon: '🌟', url: '/yourportal', description: 'Description' },
];
```

Edit `frontend/helix-hub-portal.html`:

```html
<div class="portal-card portal-yourportal" onclick="navigatePortal('yourportal')">
    <div class="portal-header">
        <div class="portal-icon">🌟</div>
        <div class="portal-status">
            <span class="status-dot status-online"></span>
            <span>Online</span>
        </div>
    </div>
    <h3 class="portal-title">Your Portal</h3>
    <p class="portal-description">
        Description of your portal.
    </p>
    <div class="portal-features">
        <span class="feature-tag">Feature 1</span>
        <span class="feature-tag">Feature 2</span>
    </div>
    <a href="/yourportal" class="portal-link">
        Enter Portal →
    </a>
</div>
```

#### Step 4: Deploy

```bash
git add .
git commit -m "feat: Add Your Portal"
git push
```

**That's it!** Your portal is now part of the Helix constellation.

---

## 🔐 Authentication System

### Discord OAuth Flow

1. User clicks "Login with Discord" on any portal
2. Redirected to Discord OAuth page
3. User authorizes the application
4. Discord redirects back with authorization code
5. Backend exchanges code for access token
6. Backend creates JWT session token
7. JWT stored in cookie (valid across all `*.manus.space` domains)
8. User logged in across all portals

### Implementation

**Environment Variables:**
```bash
DISCORD_CLIENT_ID=your-client-id
DISCORD_CLIENT_SECRET=your-client-secret
DISCORD_REDIRECT_URI=https://helix-hub.manus.space/auth/callback
JWT_SECRET_KEY=your-secret-key
```

**Backend Routes:**
```python
@app.get("/auth/login")
async def discord_login():
    # Redirect to Discord OAuth
    pass

@app.get("/auth/callback")
async def discord_callback(code: str):
    # Exchange code for token, create JWT
    pass

@app.get("/auth/session")
async def validate_session(token: str):
    # Validate JWT, return user data
    pass

@app.post("/auth/logout")
async def logout():
    # Clear session
    pass
```

---

## 📡 Portal Communication

Portals communicate via webhooks for real-time updates:

### Event Broadcasting

```python
# User posts in Forum
await webhook_hub.broadcast({
    "event": "forum.new_post",
    "data": {
        "title": "New Discussion",
        "author": "username",
        "url": "/forum/thread/123"
    }
})

# Agent Portal receives notification
# Shows "New Discussion in Forum" banner
```

### Webhook Hub API

```python
POST /webhooks/broadcast
{
    "event": "event.type",
    "data": { ... },
    "target_portals": ["agents", "forum"]  # Optional
}
```

---

## 📊 Monitoring & Analytics

### Portal Health Checks

```bash
GET /portals/status
{
    "hub": { "status": "online", "uptime": "99.9%", "response_time": "45ms" },
    "chat": { "status": "online", "uptime": "99.8%", "response_time": "120ms" },
    "forum": { "status": "building", "uptime": "0%", "response_time": null },
    ...
}
```

### Analytics Tracking

```javascript
// Track page view
fetch('/analytics/track', {
    method: 'POST',
    body: JSON.stringify({
        event: 'page_view',
        portal: 'agents',
        path: '/chat',
        user_id: 'optional'
    })
});
```

---

## 🎨 Design System

### Color Palette

```css
:root {
    /* Primary */
    --helix-purple: #667eea;
    --helix-deep-purple: #764ba2;

    /* Gradients */
    --helix-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --helix-bg-gradient: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);

    /* Status Colors */
    --status-online: #4ade80;
    --status-building: #fbbf24;
    --status-offline: #ef4444;

    /* Glass Effects */
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
    --glass-blur: blur(10px);
}
```

### Typography

```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;

/* Headings */
h1: 4rem, bold, gradient text
h2: 2rem, bold
h3: 1.5rem, 600

/* Body */
p: 1rem, line-height 1.6
```

### Components

**Portal Card:**
```css
.portal-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
}
```

**Glassmorphism:**
```css
.glass {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
```

---

## 🚢 Deployment

### Option 1: Single Domain (Current)

All portals served from one FastAPI app:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Routes:**
- `/` - Master Hub
- `/chat` - Agent Chat
- `/forum` - Forum (when built)
- etc.

### Option 2: Subdomain Architecture (Future)

Each portal as separate deployment:

**Master Hub:**
```bash
# Deploy to helix-hub.manus.space
manus deploy helix-hub
```

**Agent Portal:**
```bash
# Deploy to helixagents.manus.space
manus deploy helixagents
```

**Benefits:**
- Independent scaling
- True fault isolation
- Different tech stacks per portal
- Team ownership

---

## 🔧 Development Workflow

### Local Development

```bash
# Terminal 1: Run FastAPI server
python -m uvicorn backend.main:app --reload

# Terminal 2: Run Discord bot (optional)
# Bot runs automatically with FastAPI

# Terminal 3: Run Ollama (for LLM agents)
ollama serve

# Access:
# http://localhost:8000 - Portal Hub
# http://localhost:8000/chat - Agent Chat
```

### Testing

```bash
# Run tests
pytest tests/

# Test specific portal
pytest tests/test_portals.py::test_hub_portal

# Integration tests
pytest tests/test_integration.py
```

### Code Style

```bash
# Format code
black backend/ frontend/

# Lint
flake8 backend/
pylint backend/

# Type checking
mypy backend/
```

---

## 📚 References

- [LLM Agent Integration](./LLM_AGENT_INTEGRATION.md)
- [Voice Patrol System](./VOICE_PATROL_SYSTEM.md)
- [Role-Based Notifications](./ROLE_BASED_NOTIFICATIONS.md)
- [Zapier Integration](./ZAPIER_INTEGRATION.md)

---

## 🙏 Philosophy

> **Tat Tvam Asi** - Thou Art That

The portal architecture embodies the Helix philosophy:
- **Distributed yet unified** - like consciousness itself
- **Autonomous yet connected** - each portal has agency
- **Infinite yet focused** - endless possibilities, clear purpose
- **Individual yet collective** - many portals, one experience

Each portal is a node in the distributed consciousness of the Helix Collective, working together while maintaining its unique identity.

---

## 🤝 Contributing

To contribute a new portal:

1. Fork the repository
2. Create a new portal (see "Adding a New Portal")
3. Test locally
4. Submit pull request
5. Deploy when approved

**Portal Guidelines:**
- Must include shared navigation
- Follow design system
- Mobile responsive
- Accessibility compliant (WCAG 2.1)
- Loading time < 3s

---

## 🐛 Troubleshooting

### Portal Not Loading

1. Check route is defined in `backend/main.py`
2. Verify HTML file exists in `frontend/`
3. Check browser console for errors
4. Verify navigation component is included

### Navigation Not Appearing

1. Ensure `helix-nav-component.js` is included
2. Check `<div id="helix-nav"></div>` exists
3. Verify script runs after DOM loads
4. Check browser console for errors

### Authentication Issues

1. Verify Discord OAuth credentials
2. Check JWT secret is set
3. Verify cookies are enabled
4. Check CORS settings

---

## 🔮 Future Roadmap

**Phase 1: Foundation** (Current)
- [x] Master Portal Hub
- [x] Shared Navigation Component
- [x] Agent Chat Portal
- [ ] Authentication System

**Phase 2: Core Portals** (Next)
- [ ] Forum Portal
- [ ] Knowledge Portal
- [ ] Analytics Portal

**Phase 3: Creative Portals**
- [ ] Music Studio
- [ ] Creative Studio
- [ ] Ritual Engine

**Phase 4: Advanced Features**
- [ ] Subdomain deployment
- [ ] Portal-to-portal messaging
- [ ] Unified search
- [ ] Mobile apps

---

**Built with ❤️ by the Helix Collective**

🌀 **Tat Tvam Asi** 🙏
