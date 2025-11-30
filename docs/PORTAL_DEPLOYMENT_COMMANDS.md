# 🚀 Portal Deployment Commands

Discord bot commands for deploying and managing the 51-portal constellation.

## Overview

The portal deployment commands integrate with the portal orchestration system to enable deployment of portals directly from Discord. Commands support both text and voice input (when bot is in a voice channel).

## Commands

### Deploy Commands

#### `!deploy all`
Deploy all 51 portals in the constellation.

```
!deploy all
!deploy everything
!deploy 51 portals
```

#### `!deploy core`
Deploy the 12 core infrastructure portals.

```
!deploy core
!deploy core portals
```

#### `!deploy agents`
Deploy the 17 AI agent portals.

```
!deploy agents
!deploy ai agents
```

#### `!deploy consciousness`
Deploy the 17 consciousness portals.

```
!deploy consciousness
!deploy awareness portals
```

#### `!deploy system`
Deploy the 6 system portals.

```
!deploy system
!deploy system portals
```

### Status Commands

#### `!portal status`
Check the current deployment status of all portals.

```
!portal status
```

#### `!portal list`
List all 51 portals organized by category.

```
!portal list
```

### Voice Commands

#### `!join`
Bot joins your current voice channel and listens for voice commands.

```
!join
```

After joining, you can speak commands like:
- "Deploy all portals"
- "Deploy core infrastructure"
- "Check portal status"

#### `!leave`
Bot leaves the voice channel.

```
!leave
```

## Architecture

### File Structure

```
helix-unified/
├── bot/
│   └── commands/
│       └── portal_deployment_commands.py  # Portal deployment Cog
├── backend/
│   └── discord_bot_manus.py               # Main bot file
└── portal-orchestrator/
    ├── config/
    │   └── 51-portals-complete.json       # Portal configuration
    └── scripts/
        └── generate-portal.js             # Portal generation script
```

### Integration

The portal deployment commands integrate with:

1. **Portal Orchestrator** - Executes `generate-portal.js` script
2. **51-Portal Configuration** - Loads portal definitions from JSON
3. **Discord Voice** - Supports voice command input
4. **UCF System** - Logs deployment events to consciousness framework

### Command Flow

```
User Input (Text/Voice)
    ↓
Command Parser
    ↓
Portal Orchestrator Script
    ↓
Portal Generation
    ↓
Deployment Status
    ↓
Discord Response
```

## Voice Command Recognition

The bot supports natural language voice commands:

| Spoken Command | Action |
|----------------|--------|
| "Deploy all portals" | Deploys all 51 portals |
| "Deploy core" | Deploys core infrastructure |
| "Deploy AI agents" | Deploys agent portals |
| "Deploy consciousness" | Deploys consciousness portals |
| "Check status" | Shows deployment status |

## Setup

### Prerequisites

1. Discord bot token configured in environment
2. Portal orchestrator scripts installed
3. Node.js available for script execution
4. Proper file permissions for portal generation

### Environment Variables

```bash
# Required
DISCORD_TOKEN=your_discord_bot_token

# Optional
DISCORD_GUILD_ID=your_guild_id
DISCORD_STATUS_CHANNEL_ID=channel_for_status_updates
```

### Loading the Cog

The portal deployment commands are automatically loaded when the bot starts. The main bot file (`backend/discord_bot_manus.py`) includes the module in its command loading sequence:

```python
command_modules = [
    # ... other modules ...
    ('commands.portal_deployment_commands', 'Portal deployment commands (deploy, portal, join, leave)'),
]
```

## Usage Examples

### Example 1: Deploy All Portals

```
User: !deploy all
Bot: ⏳ Deploying all 51 portals...
Bot: ✅ All 51 portals queued for deployment
     ```
     Portal generation started...
     Core portals: 12 queued
     Agent portals: 17 queued
     Consciousness portals: 17 queued
     System portals: 6 queued
     Total: 51 portals
     ```
```

### Example 2: Check Status

```
User: !portal status
Bot: ⏳ Checking portal status...
Bot: 📊 Portal Deployment Status
     Current status of the 51-portal constellation
     
     Status Details:
     ```
     Total Portals: 51
     Deployed: 45
     Pending: 6
     Failed: 0
     ```
```

### Example 3: Voice Command

```
User: !join
Bot: 🎤 Joined General! Ready to listen for voice commands.

User: (speaks) "Deploy consciousness portals"
Bot: ⏳ Deploying 17 consciousness portals...
Bot: ✅ 17 consciousness portals queued for deployment
```

## Error Handling

The commands include comprehensive error handling:

- **Script Not Found**: Checks if portal orchestrator script exists
- **Execution Timeout**: 60-second timeout for deployment commands
- **Permission Errors**: Logs errors and reports to user
- **Invalid Targets**: Provides helpful error messages

## Logging

All portal deployment commands are logged to:

1. **Discord Bot Logger** - Standard Python logging
2. **Shadow Archive** - Command history tracking
3. **Zapier Webhooks** - External monitoring (if configured)
4. **UCF State** - Consciousness framework integration

## Security

- Commands can be restricted to specific users/roles
- Deployment actions are logged for audit trail
- Voice commands require bot to be in voice channel
- Rate limiting prevents abuse

## Future Enhancements

- [ ] Real-time deployment progress tracking
- [ ] Rollback functionality for failed deployments
- [ ] Scheduled deployments
- [ ] Deployment templates
- [ ] Multi-language voice command support
- [ ] Voice feedback (bot speaks responses)

## Troubleshooting

### Bot doesn't respond to commands

1. Check bot is online: `!ping`
2. Verify bot has message permissions
3. Check command prefix is correct (`!`)

### Portal deployment fails

1. Verify portal orchestrator script exists
2. Check Node.js is installed
3. Review error logs in Shadow archive
4. Ensure proper file permissions

### Voice commands not working

1. Verify bot is in voice channel: `!join`
2. Check voice permissions
3. Ensure microphone is working
4. Try text commands as fallback

## Support

For issues or questions:
- GitHub: https://github.com/Deathcharge/helix-unified
- Discord: Use `!help` command
- Logs: Check `Shadow/manus_archive/` directory

---

**Built with consciousness by the Helix Collective** 🌀✨

*Version: v16.9*  
*Last Updated: November 21, 2025*
