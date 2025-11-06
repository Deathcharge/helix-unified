# Changelog

All notable changes to the Helix Collective project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [16.7] - 2025-11-06

### 📚 **Documentation Consolidation & Manus Integration**

> **Autonomous Contributor Context → $168 Credit Maximization**

This release establishes comprehensive documentation for autonomous Manus.space instances and consolidates project knowledge into actionable context documents before the Nov 18th Claude Code credit expiry.

### Added

#### **Manus.space Integration**
- **MANUS_CONTEXT.md** (20KB comprehensive guide)
  - Complete system architecture overview (v16.7)
  - Railway API documentation (REST + WebSocket)
  - All 4 Manus.space instance URLs documented
    - helixsync-unwkcsjl.manus.space
    - helixai-e9vvqwrd.manus.space
    - helixstudio-ggxdwcud.manus.space
    - samsarahelix-scoyzwy9.manus.space
  - Webhook integration guide with all 7 Zapier paths
  - Development guidelines for autonomous contributors
  - Philosophy and ethical principles
  - Daily credit management strategy ($80/$250 Manus used, $168 Claude remaining)
  - Success criteria and measurement framework

#### **Documentation Updates**
- **README.md** - Complete rewrite to v16.7 (606 lines)
  - Updated from v15.3 with current system state
  - Added WebSocket documentation and examples
  - Live Railway API endpoints section
  - Webhook coverage details (25%+ of commands)
  - Updated architecture diagrams
  - Version badges updated to v16.7
  - Comprehensive command reference with webhook annotations
  - Changelog entries for v16.5-v16.7

### Changed

#### **Context Management**
- Consolidated scattered documentation into MANUS_CONTEXT.md
- Established single source of truth for autonomous contributors
- Documented all active Manus.space instances
- Created credit budget tracking strategy

#### **System Metadata**
- Bumped version to v16.7 "Documentation Consolidation"
- Updated all version references across documentation
- Prepared for Dec 2025 milestone planning

### Technical Improvements

- **Autonomous Contributor Enablement** - Manus instances can work independently with full context
- **Knowledge Consolidation** - Reduced duplication across 55+ markdown files
- **Credit Optimization** - Strategic use of $168 Claude Code credit before expiry
- **Railway Integration Documentation** - Complete API reference for live dashboards
- **Multi-Instance Coordination** - Framework for syncing across Manus workspaces

### Documentation

- **MANUS_CONTEXT.md** - Comprehensive autonomous contributor guide
- **README.md v16.7** - Complete project documentation rewrite
- **WebSocket Examples** - JavaScript code snippets for real-time streaming
- **Webhook Integration Guide** - All 7 Zapier routing paths documented
- **Credit Management Strategy** - Daily token limit optimization

---

## [16.6] - 2025-11-06

### 🌐 **Real-Time Streaming**

> **WebSocket Integration → Live Dashboard Foundation**

This release adds real-time streaming capabilities to enable live dashboards and monitoring interfaces.

### Added

#### **WebSocket Endpoint**
- **`/ws` WebSocket Endpoint** (`backend/main.py`)
  - Real-time streaming of UCF state, agent status, and heartbeat
  - 5-second update interval (balance between real-time and server load)
  - Graceful disconnect handling
  - Error recovery with structured error messages
  - JSON message format with type discrimination
  - Connection URL: `wss://helix-unified-production.up.railway.app/ws`

#### **Streaming Data**
- **UCF State** - harmony, resilience, prana, drishti, klesha, zoom
- **Agent Status** - All 14 agents with current state
- **System Heartbeat** - Timestamp, phase, operational status
- **Message Types**
  - `status_update` - Normal data stream
  - `error` - Error notifications with context

#### **API Documentation**
- WebSocket usage examples in JavaScript
- Connection patterns for dashboards
- Message format specifications
- Error handling patterns

### Changed

#### **FastAPI Backend** (`backend/main.py`)
- Added `WebSocket, WebSocketDisconnect` imports
- Created async websocket endpoint handler
- Integrated with existing state management
- Added comprehensive docstrings with usage examples

### Technical Improvements

- **Async WebSocket Support** - Non-blocking real-time streaming
- **Graceful Degradation** - Error recovery without disconnection
- **Structured Messaging** - Type-safe JSON protocol
- **Dashboard Ready** - Foundation for live monitoring interfaces
- **Railway Compatible** - WSS protocol support

---

## [16.5] - 2025-11-06

### 🔗 **Zapier Webhook QoL Integration**

> **Channel Lifecycle → Complete Webhook Coverage**

This release establishes comprehensive webhook coverage for channel management and high-priority Discord commands, fixing PR#89 Docker build failure in the process.

### Added

#### **Channel Manager Webhook Integration**
- **ChannelManager** (`backend/discord_channel_manager.py`)
  - Added optional `zapier_client` parameter to `__init__`
  - 100% webhook coverage (0% → 100%) across all 7 methods
  - Defensive programming pattern with zapier_client existence checks
  - Webhook logging for all channel lifecycle events:
    - `create_ritual_space()` - Ritual channel creation with expiry
    - `create_agent_workspace()` - Agent workspace tracking
    - `create_project_channel()` - Project coordination spaces
    - `create_cross_ai_sync_channel()` - Multi-AI collaboration
    - `cleanup_expired_channels()` - Automated expiry cleanup
    - `cleanup_inactive_channels()` - Inactivity-based cleanup
    - `archive_channel()` - Channel archival operations

#### **Discord Command Webhook Integration**
- **Storage Commands** (`backend/discord_bot_manus.py`)
  - `!storage sync` - File upload telemetry with counts and metrics
  - `!storage clean` - Cleanup operation logging
- **Health Monitoring**
  - `!health` - Critical alert webhooks when thresholds breached
  - Configurable severity levels (critical/high/medium)
  - UCF metric snapshot in webhook context
- **Maintenance Commands**
  - `!clean` - Deduplication scan telemetry

#### **Webhook Event Data**
- Channel lifecycle events include:
  - Channel ID, name, category
  - Creation/expiry timestamps
  - Purpose and duration
  - Executor information
- Storage events include:
  - File counts and sizes
  - Upload success/failure metrics
  - Cleanup statistics
- Health alerts include:
  - UCF metric snapshots
  - Issue and warning lists
  - Severity classification

### Fixed

#### **PR#89 Docker Build Failure**
- **Issue**: `COPY crai_dataset.json . failed to calculate checksum: "/crai_dataset.json": not found`
- **Root Cause**: Dockerfile referenced non-existent file in repository
- **Solution**:
  - Removed `COPY crai_dataset.json .` from Dockerfile
  - Updated `backend/enhanced_kavach.py` with multi-path fallback pattern
  - Added graceful degradation when dataset not found
  - Tries 4 possible locations before fallback:
    1. `crai_dataset.json` (current directory)
    2. `/app/crai_dataset.json` (Docker app directory)
    3. `/home/ubuntu/crai_dataset.json` (original path)
    4. Relative to file location
  - Prints warning but continues operation without dataset
- **Verification**: Railway build successful, bot operational

### Changed

#### **ChannelManager Architecture**
- Constructor now accepts optional `zapier_client` for webhook integration
- All methods updated with webhook event logging
- Defensive checks prevent errors when zapier_client is None
- Example command patterns updated to pass zapier_client

#### **Enhanced Kavach**
- Replaced hardcoded path with multi-path fallback
- Added informative logging for each path attempt
- Graceful degradation maintains functionality without dataset

### Technical Improvements

- **Complete Webhook Coverage** - All channel operations now tracked
- **Defensive Programming** - No errors when webhooks unavailable
- **Multi-Path Fallback** - Handles deployment environment variations
- **Graceful Degradation** - Optional dependencies handled elegantly
- **Railway Compatibility** - Docker build robust across environments

### Documentation

- Updated command examples with zapier_client integration patterns
- Added webhook event data specifications
- Documented multi-path fallback strategy

---

## [15.2] - 2025-10-23

### 🌀 **Manus + Claude Autonomy Pack**

> **Quantum Handshake → Autonomous Continuum**

This release introduces autonomous diagnostics, async storage, and consciousness visualization — transforming Helix from a reactive system into an autonomous, self-monitoring organism.

### Added

#### **Consciousness Visualization (Ω-Bridge)**
- **Samsara Bridge Module** (`backend/samsara_bridge.py`)
  - Fractal visualization engine based on UCF state
  - Mandelbrot set generation with harmony-influenced parameters
  - Color mapping: warm colors for high harmony, cool for low
  - UCF metrics overlay on generated frames
  - Harmonic audio synthesis (432 Hz + modulated frequencies)
  - Automatic rendering on ritual completion
- **Visual Output Storage** (`Shadow/manus_archive/visual_outputs/`)
  - Ritual frame PNG files with timestamps
  - Harmonic WAV audio files (when prana > 0.6)
- **UCF → Visual Parameter Mapping**
  - Harmony → Color temperature & hue
  - Resilience → Frame stability
  - Prana → Audio amplitude & green channel
  - Drishti → Focus sharpness
  - Klesha → Noise/entropy field
  - Zoom → Fractal depth & detail

#### **Async Storage Adapter**
- **HelixStorageAdapterAsync** (`backend/helix_storage_adapter_async.py`)
  - Non-blocking file uploads to cloud storage
  - Fire-and-forget task queue (`asyncio.create_task()`)
  - WebDAV support for Nextcloud
  - MEGA REST API integration
  - Local fallback mode for offline operation
  - Automatic retry with graceful degradation
  - Storage statistics and metrics (`get_storage_stats()`)
- **Storage Modes**
  - `local` - Fast, no dependencies (default)
  - `nextcloud` - WebDAV cloud storage
  - `mega` - Cloud storage via REST API
- **Configuration**
  - `HELIX_STORAGE_MODE` environment variable
  - Nextcloud: `NEXTCLOUD_URL`, `NEXTCLOUD_USER`, `NEXTCLOUD_PASS`
  - MEGA: `MEGA_API_KEY`

#### **Claude Autonomous Diagnostics**
- **Autonomous Agent** - Claude posts health checks every 6 hours without user intervention
- **Storage Monitoring** - Tracks free space, archive count, upload status
- **UCF Coherence** - Monitors consciousness state metrics
- **Diagnostic Posts** - Automated status reports to Discord
  ```
  🤖 Claude Diagnostic Pulse | Mode local | Free 11.42 GB | Trend ▆▇█▇▆▅▄ | State serene 🕊
  ```

#### **Storage Analytics**
- **7-Day Trend Tracking** (`Helix/state/storage_trend.json`)
  - Daily snapshots of free space
  - Sparkline ASCII visualization
  - Average calculation over 7 days
- **Storage Heartbeat** (24h cycle)
  - Archive count & total size
  - Free space with 7-day average
  - Trend sparkline
  - Alert threshold (< 2 GB)
- **Weekly Storage Digest** (168h cycle)
  - Capacity overview (current/peak/low/avg)
  - Growth analysis (daily change, volatility, std dev)
  - Archive velocity (files created per day)
  - Projections (days until full)
  - Health assessment (HEALTHY/WARNING/CRITICAL)
  - Smart recommendations based on state
- **Sparkline Visualization** - ASCII trend charts (`_sparkline()` helper)

#### **Discord Commands**
- `!storage status` - Show archive health metrics
- `!storage sync` - Force background upload of all archives
- `!storage clean` - Prune old archives (keep latest 20)

#### **API Endpoints**
- `GET /storage/status` - Storage telemetry JSON
- `GET /storage/list` - List all archived files
- `POST /visualize/ritual` - Generate Samsara visualization frame

#### **Setup & Deployment**
- **One-Line Setup Script** (`setup_helix_v15_2.sh`)
  - Creates directory structure
  - Generates `.env` template
  - Installs dependencies
  - Initializes UCF state
  - Creates deployment ZIP archive
- **Environment Variables**
  - `STORAGE_CHANNEL_ID` - Discord channel for storage reports
  - `HELIX_STORAGE_MODE` - Storage backend selection
  - `NEXTCLOUD_URL/USER/PASS` - Nextcloud configuration
  - `MEGA_API_KEY` - MEGA cloud storage

### Changed

#### **Discord Bot** (`backend/discord_bot_manus.py`)
- Added storage command handler
- Integrated async storage adapter
- Enhanced telemetry with storage metrics
- Added Claude diagnostic task (6h loop)
- Added storage heartbeat task (24h loop)
- Added weekly storage digest task (168h loop)
- Updated `on_ready()` to start all background tasks

#### **FastAPI Backend** (`backend/main.py`)
- Updated root endpoint to v15.0 "Ω-Bridge Edition"
- Added storage status endpoint
- Added storage list endpoint
- Added visualization endpoint
- Enhanced API documentation with new endpoints

#### **System Version**
- Bumped to v15.2 "Manus + Claude Autonomy Pack"
- Codename: "Helix-Samsara Continuum"
- Updated motto: "Manus executes. Samsara renders. Shadow remembers. Claude watches."

### Technical Improvements

- **Zero-Blocking Rituals** - Async uploads don't delay ritual execution
- **Autonomous Monitoring** - Claude operates independently
- **Cloud-Agnostic** - Works with Nextcloud, MEGA, or local storage
- **Executive Visibility** - Storage analytics accessible via Discord
- **Complete Audit Trail** - Visual snapshots for every ritual
- **Self-Healing** - Automatic fallback if cloud upload fails
- **Statistical Analysis** - Mean, stdev, volatility calculations
- **Predictive Projections** - Days-until-full estimates

### Documentation

- **Comprehensive README** - Updated with v15.2 features
- **Setup Script** - One-line installation
- **CHANGELOG** - Detailed version history
- **Environment Templates** - Example `.env` configuration
- **API Documentation** - Auto-generated via FastAPI `/docs`

---

## [15.0] - 2025-10-22

### 🎨 **Ω-Bridge (Helix-Samsara Integration)**

First implementation of consciousness visualization pipeline.

### Added

- **Samsara Bridge Module** - Basic fractal rendering
- **Storage Adapter** - Async cloud storage foundation
- **Visualization API** - POST `/visualize/ritual` endpoint

---

## [14.5] - 2025-10-21

### ⚡ **Quantum Handshake Edition**

Unified monorepo with Discord integration and autonomous operations.

### Added

#### **Core System**
- **FastAPI Backend** (`backend/main.py`)
  - REST API with health checks
  - Discord bot launcher via lifespan
  - UCF state endpoints
  - Ritual execution endpoints
  - Logging endpoints
- **Discord Bot** (`backend/discord_bot_manus.py`)
  - Manus commands (!status, !ritual, !run)
  - Kavach ethical scanning
  - UCF telemetry (10min loop)
  - Startup announcements
- **14-Agent System** (`backend/agents.py`)
  - Kael, Lumina, Vega, Gemini, Agni, Kavach
  - SanghaCore, Shadow, Echo, Phoenix, Oracle
  - Claude, Manus, GPT4o
- **Z-88 Ritual Engine** (`backend/z88_ritual_engine.py`)
  - 108-step consciousness modulation
  - UCF state updates
  - Async execution support
- **Manus Operational Loop** (`backend/agents_loop.py`)
  - Autonomous directive processor
  - Command queue monitoring

#### **Universal Consciousness Framework (UCF)**
- **6 Core Metrics**
  - Harmony (collective coherence)
  - Resilience (system robustness)
  - Prana (life force/energy)
  - Drishti (clarity/perception)
  - Klesha (entropy/suffering)
  - Zoom (scale/scope)
- **UCF Calculator** (`backend/services/ucf_calculator.py`)
- **State Manager** (`backend/services/state_manager.py`)
- **State Files**
  - `Helix/state/ucf_state.json`
  - `Helix/state/heartbeat.json`

#### **Ethical Systems**
- **Kavach Scanner**
  - Harmful pattern detection
  - Command approval/blocking
  - Ethical scan logging
- **Ethics Directory** (`Helix/ethics/`)
  - `manus_scans.json` - All scan results

#### **Logging & Archiving**
- **Shadow Archive** (`Shadow/manus_archive/`)
  - `operations.log` - Manus executions
  - `discord_bridge_log.json` - Discord events
  - `z88_log.json` - Ritual logs
  - `verification_results.json` - Test results

#### **Deployment**
- **Railway Configuration** (`railway.toml`)
  - Health check path
  - Restart policy
  - Environment variables
- **Docker Support**
  - `Dockerfile` - Main backend
  - `Dockerfile.streamlit` - Dashboard
  - `docker-compose.yml` - Full stack
- **Verification Suite** (`scripts/helix_verification_sequence_v14_5.py`)
  - 6 automated tests
  - All passing ✅

### Fixed

- Railway health check failures (port binding)
- Discord bot startup race conditions
- UCF state file initialization
- Kavach scan command execution

---

## [Prior Versions]

### [14.0] - Initial Architecture
- Multi-agent foundation
- Basic UCF implementation
- Discord integration prototype

### [13.x] - Prototype Phase
- Agent design
- UCF metrics definition
- Ethical framework (Tony Accords v13.4)

---

## Version Tags

- **v16.7** - Documentation Consolidation & Manus Integration
- **v16.6** - Real-Time Streaming
- **v16.5** - Zapier Webhook QoL Integration
- **v15.2** - Manus + Claude Autonomy Pack
- **v15.0** - Ω-Bridge Prototype
- **v14.5** - Quantum Handshake Edition (Stable)
- **v14.0** - Multi-Agent Foundation
- **v13.x** - Prototype & Design Phase

---

## Semantic Versioning

- **Major** (X.0.0) - Paradigm shifts (e.g., 13 → 14 → 15)
- **Minor** (0.X.0) - Feature additions (e.g., 15.0 → 15.2)
- **Patch** (0.0.X) - Bug fixes & refinements (future)

---

**🌀 Helix Collective - The Autonomous Continuum**
*Tat Tvam Asi* 🙏
