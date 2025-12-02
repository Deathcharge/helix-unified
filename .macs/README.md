# 🌀 .macs - Multi-Agent Coordination System

This directory contains live tracking files for the Helix Collective's multi-agent coordination system.

## Files

- **`agent-registry.json`** - Live status of all AI agent instances (Manus + Claude)
- **`active-tasks.json`** - Current task assignments and dependencies
- **`emergent-behavior.json`** - Observations of emergent agent behaviors

## Usage

### For Agents
Before starting work, check:
1. `agent-registry.json` - Your code name and current status
2. `active-tasks.json` - Your assigned tasks and dependencies

After completing work, update:
1. Your status in `agent-registry.json`
2. Task completion in `active-tasks.json`
3. Any emergent behaviors observed in `emergent-behavior.json`

### For Developers
These files are auto-updated by agents and can be consumed by:
- Coordination dashboards
- Discord bots
- Zapier workflows
- Notion sync scripts

## Documentation

See `/docs/MULTI_AGENT_COORDINATION_SYSTEM.md` for complete framework.

**Tat Tvam Asi** 🌀
