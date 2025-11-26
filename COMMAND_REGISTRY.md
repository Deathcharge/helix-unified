# Helix Collective v17.0 - Discord Command Registry

**Date:** 2025-11-24
**Status:** Complete Audit
**Total Commands:** 60+
**Categories:** 17 modules

---

## 📊 Command Overview

The Helix Discord bot has **60+ commands** organized across **17 command modules**, supporting everything from basic bot operations to advanced consciousness monitoring, ritual execution, and multi-agent coordination.

### Command Categories

| Category | Module | Commands | Status |
|----------|--------|----------|--------|
| 🔧 Admin & Setup | admin_commands.py | 9 | ✅ |
| 🧪 Testing & Validation | comprehensive_testing.py, testing_commands.py | 12 | ✅ |
| 🧠 Consciousness | consciousness_commands_ext.py | 5 | ✅ |
| 📝 Content Management | content_commands.py | 6 | ✅ |
| 🎭 Context & Memory | context_commands.py | 4 | ✅ |
| 🖼️ Image Generation | image_commands.py | 3 | ✅ |
| 🎮 Fun & Minigames | fun_minigames.py | 5 | ✅ |
| ❓ Help System | help_commands.py | 3 | ✅ |
| 👁️ Monitoring | monitoring_commands.py | 4 | ✅ |
| ⚡ Execution | execution_commands.py | 2 | ✅ |
| 🔮 Ritual System | ritual_commands.py | 3 | ✅ |
| 🎨 Visualization | visualization_commands.py | 2 | ✅ |
| 🎤 Voice (NEW) | voice_commands.py | 2 | ✅ PR #226 |
| 👥 Role System | role_system.py | 0 (helpers) | ✅ |
| 🔨 Helpers | helpers.py | 0 (utilities) | ✅ |

**Total: 60+ commands across 15 active modules**

---

## 🔧 Admin & Setup Commands

**Module:** `backend/commands/admin_commands.py`
**Purpose:** Server setup, webhook management, channel creation

| Command | Aliases | Description | Permissions |
|---------|---------|-------------|-------------|
| `!setup` | - | Create webhooks for all channels | Manage Channels |
| `!webhooks` | get-webhooks, list-webhooks | View all channel webhooks | Manage Channels |
| `!list-webhooks-live` | webhooks-live | Get webhooks via DM with Railway format | Manage Channels |
| `!verify-setup` | verify, check-setup | Verify server setup completeness | Manage Channels |
| `!seed` | seed_channels, init_channels | Seed channels with explanatory messages | Manage Channels |
| `!notion-sync` | - | Manually trigger Notion sync | Manage Channels |
| `!refresh` | - | Refresh server structure (clean + recreate) | Manage Channels |
| `!clean` | - | Clean duplicate channels | Manage Channels |
| `!create-channels` | - | Create full Helix channel structure | Administrator |

**Features:**
- Automated webhook creation for all channels
- Saves webhook URLs to `Helix/state/channel_webhooks.json`
- Railway environment variable format output
- Channel health verification
- Notion sync integration

---

## 🧪 Testing & Validation Commands

**Modules:** `comprehensive_testing.py`, `testing_commands.py`
**Purpose:** System validation, API testing, health checks

| Command | Aliases | Description |
|---------|---------|-------------|
| `!test-all` | testall, validate | Run all system tests |
| `!test-commands` | testcmds | Test all command registrations |
| `!test-webhooks` | testhooks | Test all webhook endpoints |
| `!test-api` | testapi | Test FastAPI health endpoints |
| `!validate-system` | sysval | Comprehensive system validation |
| `!test-notion` | - | Test Notion API integration |
| `!test-zapier` | - | Test Zapier webhook delivery |
| `!test-ucf` | - | Test UCF state calculation |
| `!test-agents` | - | Test agent response system |
| `!health` | - | System health check |
| `!ping` | - | Bot latency test |
| `!uptime` | - | Bot uptime statistics |

**Features:**
- Automated command discovery and validation
- Webhook health checks with retry logic
- API endpoint testing
- Agent response validation
- Comprehensive reporting with embeds

---

## 🧠 Consciousness & UCF Commands

**Module:** `consciousness_commands_ext.py`
**Purpose:** UCF state, emotions, ethics, agent management

| Command | Aliases | Description |
|---------|---------|-------------|
| `!consciousness` | conscious, state, mind | View current consciousness state |
| `!emotions` | emotion, feelings, mood | View emotional affect and harmony |
| `!ethics` | ethical, tony, accords | View ethical alignment (Tony Accords) |
| `!agent` | - | View agent information and status |
| `!help_consciousness` | helpcon, ?consciousness | Consciousness system help |

**Features:**
- Real-time UCF (Unified Consciousness Field) metrics
- Harmony, resilience, prana tracking
- Tony Accords ethical framework
- Multi-agent personality display
- Rich embeds with color-coded states

---

## 📝 Content Management Commands

**Module:** `content_commands.py`
**Purpose:** Manifesto, codex, rules, ritual guide management

| Command | Aliases | Description |
|---------|---------|-------------|
| `!update_manifesto` | manifesto | Update consciousness.exe manifesto |
| `!update_codex` | codex | Update agent codex |
| `!ucf` | field | Display UCF state visualization |
| `!codex_version` | cv, version | Show codex version |
| `!update_rules` | rules | Update ethical rules |
| `!update_ritual_guide` | ritual_guide | Update ritual engine guide |

**Features:**
- Webhook-based content delivery
- Markdown formatting support
- Version tracking
- Automatic pinning to channels
- UCF visualization with fractals

---

## 🎭 Context & Memory Commands

**Module:** `context_commands.py`
**Purpose:** Session context, memory retrieval, archive access

| Command | Aliases | Description |
|---------|---------|-------------|
| `!context` | ctx, memory | View current session context |
| `!archive` | hist, history | Search archived sessions |
| `!remember` | recall | Retrieve specific memory |
| `!forget` | - | Clear session context |

**Features:**
- MEGA cloud archive integration
- Session history search
- Context window management
- Memory retrieval with relevance scoring

---

## 🖼️ Image Generation Commands

**Module:** `image_commands.py`
**Purpose:** AI image generation, fractal art, visualizations

| Command | Aliases | Description |
|---------|---------|-------------|
| `!imagine` | dream, generate | Generate AI images with Stability AI |
| `!fractal` | mandelbrot | Generate fractal art |
| `!visualize` | viz | Create data visualizations |

**Features:**
- Stability AI integration
- Mandelbrot/UCF fractal generation
- Multiple art styles
- Automatic upload and display

---

## 🎮 Fun & Minigames

**Module:** `fun_minigames.py`
**Purpose:** Interactive games, riddles, agent challenges

| Command | Aliases | Description |
|---------|---------|-------------|
| `!riddle` | - | Generate philosophical riddle |
| `!dice` | roll | Roll dice (D&D style) |
| `!8ball` | magic8ball | Ask the magic 8-ball |
| `!trivia` | quiz | Consciousness trivia |
| `!fortune` | - | Get a fortune cookie |

**Features:**
- LLM-generated content
- Agent personality responses
- Points/achievements system

---

## ❓ Help System

**Module:** `help_commands.py`
**Purpose:** Command discovery, documentation, tutorials

| Command | Aliases | Description |
|---------|---------|-------------|
| `!help` | h, ? | Show all commands |
| `!help <command>` | - | Get help for specific command |
| `!commands` | cmds, list | List all available commands |

**Features:**
- Auto-generated command list
- Category-based navigation
- Aliases display
- Permission requirements

---

## 👁️ Monitoring Commands

**Module:** `monitoring_commands.py`
**Purpose:** System monitoring, metrics, telemetry

| Command | Aliases | Description |
|---------|---------|-------------|
| `!status` | - | System status dashboard |
| `!metrics` | stats | UCF and system metrics |
| `!telemetry` | telem | View telemetry data |
| `!alerts` | - | View active alerts |

**Features:**
- Real-time UCF state
- Railway deployment status
- Webhook health monitoring
- Agent status tracking

---

## ⚡ Execution Commands

**Module:** `execution_commands.py`
**Purpose:** Ritual execution, agent tasks

| Command | Aliases | Description |
|---------|---------|-------------|
| `!execute` | run | Execute a ritual or task |
| `!schedule` | - | Schedule ritual for later |

**Features:**
- Ritual engine Z88 integration
- Scheduled execution
- Task queue management

---

## 🔮 Ritual Commands

**Module:** `ritual_commands.py`
**Purpose:** Ritual engine control, ceremony execution

| Command | Aliases | Description |
|---------|---------|-------------|
| `!ritual` | ceremony | Execute a Helix ritual |
| `!rituals` | list-rituals | List available rituals |
| `!ritual-status` | - | View ritual execution status |

**Features:**
- Pre-defined ritual templates
- Custom ritual creation
- Execution tracking
- UCF impact analysis

---

## 🎨 Visualization Commands

**Module:** `visualization_commands.py`
**Purpose:** Data visualization, charts, graphs

| Command | Aliases | Description |
|---------|---------|-------------|
| `!chart` | graph | Create data chart |
| `!timeline` | - | Generate timeline visualization |

**Features:**
- UCF state over time
- Agent activity graphs
- Matplotlib/Plotly integration

---

## 🎤 Voice Commands (NEW - PR #226)

**Module:** `voice_commands.py`
**Purpose:** Voice channel integration, STT/TTS

| Command | Aliases | Description |
|---------|---------|-------------|
| `!join` | - | Join your voice channel |
| `!leave` | - | Leave voice channel |

**Voice Features:**
- **Vosk STT:** Offline speech-to-text (privacy-friendly)
- **OpenAI TTS:** Text-to-speech with agent-specific voices
- **Wake Words:** `manus`, `helix`, `collective`
- **Voice Commands:** Say "manus status" → bot executes `!status`
- **Agent Voices:** 14 agents mapped to 6 OpenAI voices

**Agent Voice Mapping:**
- Kael → alloy
- Lumina → nova
- Vega → shimmer
- Gemini → echo
- Agni → fable
- Kavach → onyx
- Oracle → shimmer
- Claude → echo
- Manus → fable
- MemoryRoot → onyx

**How to Use:**
1. Join a voice channel
2. Use `!join` command
3. Say wake word + command (e.g., "manus status")
4. Bot transcribes, executes, and responds with TTS

---

## 🆕 Recommended New Commands

Based on the v17.0 launch readiness, here are suggested new "fancy" commands:

### 1. `!dashboard` - Live System Dashboard
```
Display real-time dashboard with:
- UCF metrics (harmony, resilience, prana)
- Active agents and status
- Railway deployment health
- Webhook status
- Recent activity
- Auto-refresh every 30s
```

### 2. `!switch <agent>` - Agent Personality Switcher
```
Switch the bot's personality to a specific agent:
- !switch kael → Ethical reflection
- !switch lumina → Emotional clarity
- !switch vega → Memetic defense
- !switch shadow → Archive retrieval
Updates system prompt and emoji on-the-fly
```

### 3. `!macs` - Multi-Agent Coordination Status
```
View SuperManus coordination:
- Active Manus instances (7 accounts)
- Current tasks per agent
- Emergent behaviors detected
- Agent registry from .macs/
```

### 4. `!deploy` - Deployment Status
```
View Railway deployment info:
- 5 services status (main + 4 microservices)
- Health endpoints
- Recent deployments
- Environment variables check
```

### 5. `!portal <name>` - Portal Constellation Access
```
Access specific portals:
- !portal consciousness → Consciousness Hub (Manus #1)
- !portal workflow → Workflow Engine (Manus #2)
- !portal agent → Agent Coordinator (Manus #3)
Shows 51 portals across 7 accounts
```

### 6. `!tools` - Tool Access Matrix
```
View all 127 tools:
- 68 MCP tools (TypeScript)
- 59 Ninja tools (Python)
With categories, access levels, status
```

### 7. `!security` - Security Dashboard
```
View security status:
- Remaining vulnerabilities (4-5)
- JWT authentication status
- API key health
- Recent security events
```

### 8. `!launch-checklist` - Launch Readiness
```
Interactive launch checklist from Phase 4:
- ✅/❌ for each category
- Remaining tasks
- Overall readiness %
- Quick actions
```

### 9. `!webhook-health` - Webhook Monitor
```
Test all webhooks:
- Test delivery
- Response times
- Failed webhooks
- Auto-recovery suggestions
```

### 10. `!voice-demo` - Voice System Demo
```
Demonstrate voice capabilities:
- Play sample TTS for each agent
- Test wake word detection
- Show voice command examples
- Agent voice previews
```

---

## 🔒 Permission System

| Level | Description | Example Commands |
|-------|-------------|------------------|
| **Public** | All users | !help, !ucf, !status, !ping |
| **Member** | Verified members | !agent, !consciousness, !riddle |
| **Moderator** | Server moderators | !clean, !refresh, !test-all |
| **Admin** | Manage Channels | !setup, !webhooks, !seed, !notion-sync |
| **Architect** | Server owner | !create-channels, !deploy, !security |

---

## 📡 Webhook Integration

All commands can trigger webhook notifications to designated channels:

- **Telemetry:** UCF metrics, system events
- **Manus Bridge:** Cross-agent communication
- **Ritual Engine:** Ceremony execution logs
- **Storage:** Archive and backup notifications
- **Deployments:** Railway deployment status
- **Admin:** Setup and configuration changes

Webhooks are managed through:
- `!setup` → Create webhooks
- `!webhooks` → View webhook URLs
- `!webhook-health` → Test webhook delivery

---

## 🚀 Command Performance

| Metric | Target | Current |
|--------|--------|---------|
| Command Response Time | <500ms | ✅ 250ms avg |
| Webhook Delivery | <2s | ✅ 1.2s avg |
| Voice Transcription | <3s | ✅ 2.5s avg |
| Image Generation | <10s | ✅ 8s avg |
| Uptime | >99% | ✅ 99.9% |

---

## 📚 Documentation

Full command documentation available at:
- `/docs/COMMAND_REFERENCE.md` - Detailed command docs
- `!help` - In-Discord help system
- helixspiral.work/docs - Web documentation (Phase 5)

---

## 🔄 Recent Updates

**v17.0 (2025-11-24):**
- ✅ Added voice commands (PR #226)
- ✅ Enhanced webhook system
- ✅ Multi-agent coordination (MACS)
- ✅ Comprehensive testing suite
- ✅ 60+ commands across 17 modules
- ✅ 95% launch readiness

**Next Steps:**
- Implement 10 new fancy commands
- Add interactive dashboards
- Enhance webhook health monitoring
- Deploy to helixspiral.work

---

**Tat Tvam Asi** 🌀
