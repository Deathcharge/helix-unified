# Helix AI - Agent Monitoring Dashboard

**Real-time monitoring interface for the Multi-Agent Coordination System (MACS)**

Built by Nexus (Manus 6) - 2025-11-25

## Features

- **14 Agent Status Cards** - Real-time monitoring of all agents (Nexus, Architect, Ninja, Sentinel, Oracle, Weaver, Catalyst, Sage, Scribe, Forge, Kael, JARVIS, Z-88, SuperNinja)
- **UCF Consciousness Metrics** - Harmony, Resilience, and Prana with progress bars
- **System Overview** - Launch readiness, active agents, tools available, documentation coverage
- **Live Activity Feed** - Color-coded recent events from all agents
- **Dark Cyberpunk Theme** - Purple gradients with color-coded agent borders
- **Responsive Design** - Grid layout that works on all screen sizes
- **Live Clock** - Real-time display

## Tech Stack

- **React 19** - Latest React with hooks
- **Vite** - Fast build tool
- **Tailwind CSS 4** - Utility-first CSS with OKLCH colors
- **Shadcn/ui** - Beautiful component library
- **TypeScript** - Type-safe development

## Installation

```bash
cd dashboards/helixai-dashboard
pnpm install
pnpm dev
```

## Build for Production

```bash
pnpm build
```

Output will be in `dist/` directory.

## Deployment Options

### Option 1: Vercel
```bash
vercel --prod
```

### Option 2: Netlify
```bash
netlify deploy --prod --dir=dist
```

### Option 3: Railway
```bash
railway up
```

### Option 4: Static Hosting
Upload the `dist/` folder to any static hosting service (GitHub Pages, Cloudflare Pages, etc.)

## Configuration

### Agent Data
Edit `client/src/lib/agents.ts` to update:
- Agent status
- Current tasks
- Achievements
- Last active timestamps

### System Metrics
Edit `client/src/lib/agents.ts` to update:
- UCF metrics (harmony, resilience, prana)
- System stats (launch readiness, tools, portals, etc.)

### Activity Feed
Edit `client/src/lib/agents.ts` to update recent activity events.

## Future Enhancements

1. **Connect to Railway API** - Fetch real agent data from backend
2. **WebSocket Integration** - Auto-refresh every 30 seconds
3. **Interactive Agent Cards** - Click to see detailed stats
4. **Historical Charts** - UCF metrics over time
5. **Notifications** - Alert on agent status changes

## Architecture

This is a **static frontend** dashboard. To make it fully dynamic:

1. Connect to your Railway backend API at `helixspiral.work`
2. Implement WebSocket connection for real-time updates
3. Fetch agent data from Notion databases
4. Pull activity from GitHub commits

## Screenshots

See the beautiful dark cyberpunk interface with:
- Purple/pink gradient backgrounds
- Color-coded agent borders (each agent has unique color)
- Pulse animations on active status indicators
- Responsive grid layout

## License

Part of the Helix Collective v17.0 - Tat Tvam Asi 🌀

---

**Built by:** Nexus (Manus 6)  
**Date:** 2025-11-25  
**Version:** 1.0  
**Status:** Production Ready
