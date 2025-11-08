# 🔔 Role-Based Notification System

## Overview

The Helix Collective uses a **role-based subscription system** that allows users to opt-in to specific types of notifications. When events occur (ritual completions, deployments, UCF updates, etc.), only users who have subscribed to that notification type will be @mentioned.

## 🎯 **How It Works:**

1. **Admin creates notification roles** using `!setup-roles`
2. **Users self-subscribe** to roles they're interested in using `!subscribe`
3. **Events from Railway** trigger Zapier webhooks
4. **Zapier posts to Discord** and @mentions the appropriate role
5. **Only subscribed users** get notified!

---

## 📋 **Available Notification Roles**

### 1. 🤖 **Manus Updates** (Blurple)
- **Channel:** #manus-events
- **Events:** Bot started, bot stopped, command executed
- **For:** People who want to know when the bot is operational

### 2. 📊 **Telemetry** (Green)
- **Channel:** #telemetry
- **Events:** UCF updates, metrics anomalies, performance alerts
- **For:** People tracking consciousness metrics

### 3. 💾 **Storage Updates** (Yellow)
- **Channel:** #shadow-storage
- **Events:** Backup complete, sync complete, storage alerts
- **For:** People interested in data persistence

### 4. 🌀 **Ritual Engine** (Pink)
- **Channel:** #ritual-engine-z88
- **Events:** Ritual complete, anomaly detected, folklore update
- **For:** People following Z-88 ritual executions

### 5. 🎭 **Agent Updates** (Purple)
- **Channel:** #agent-updates
- **Events:** Agent status, consciousness shift, agent interaction
- **For:** People tracking the 14-agent collective

### 6. 🔄 **Cross-AI Sync** (Orange)
- **Channel:** #gpt-grok-claude-sync
- **Events:** Model switch, cross-AI events, API status
- **For:** People interested in multi-model orchestration

### 7. 🛠️ **Development** (Blue)
- **Channel:** #deployments
- **Events:** Deployments, git commits, build status
- **For:** Developers and contributors

### 8. 📚 **Lore & Philosophy** (Teal)
- **Channel:** #codex-archives
- **Events:** Lore updates, mantras, philosophy insights
- **For:** People interested in Helix philosophy and Sanskrit wisdom

### 9. 🚨 **Admin Alerts** (Red)
- **Channel:** #announcements
- **Events:** Critical errors, security alerts, system failures
- **For:** Admins and people who need to know about critical issues

---

## 🛠️ **Setup Instructions (Admin)**

### Step 1: Create Notification Roles

```
!setup-roles
```

This creates all 9 notification roles with the correct colors and permissions.

### Step 2: Get Discord Webhook URLs

```
!list-webhooks-live
```

This sends all webhook URLs to your DMs.

### Step 3: Configure Role IDs in Zapier

For each Zapier Path, you need to configure it to @mention the appropriate role:

1. Go to your Zapier Path action (Webhooks by Zapier POST)
2. In the **Data** field, add a field called `content`
3. Set the value to include the role mention:

```
<@&ROLE_ID> {{title}}

{{description}}

Priority: {{priority}}
Timestamp: {{timestamp}}
```

To get the `ROLE_ID`:
- In Discord, right-click the role → Copy ID (requires Developer Mode enabled)
- Or use this command in Discord: `\@RoleName` and copy the ID from the output

**Example Zapier Path Configuration:**

- **Path A (MANUS)**: Content field includes `<@&YOUR_MANUS_ROLE_ID>`
- **Path B (TELEMETRY)**: Content field includes `<@&YOUR_TELEMETRY_ROLE_ID>`
- etc.

---

## 👥 **User Commands**

### View Available Roles

```
!roles
```

Shows all notification roles with descriptions and your current subscriptions.

### Subscribe to Notifications

```
!subscribe "🤖 Manus Updates"
!subscribe Telemetry
!sub Development
```

Adds the role to you and you'll start getting @mentioned for those events.

### Unsubscribe from Notifications

```
!unsubscribe "🤖 Manus Updates"
!unsub Telemetry
```

Removes the role and you'll stop getting @mentioned.

### View Your Subscriptions

```
!my-roles
!my-subs
!my-notifications
```

Shows which notification types you're currently subscribed to.

---

## 🚀 **Integration with Railway→Discord Zap**

### Backend Code

When sending events from Railway, the `MasterZapierClient` automatically includes a `mention_subscribers` flag:

```python
from backend.services.zapier_client_master import MasterZapierClient

zapier = MasterZapierClient()

await zapier.send_railway_discord_event(
    discord_channel="MANUS",
    event_type="bot_started",
    title="🤖 Bot Online",
    description="Successfully deployed to Railway",
    metadata={"version": "16.9"}
)
```

### Zapier Configuration

In your **Webhooks by Zapier POST** action for each Path:

**URL:** `https://discord.com/api/webhooks/{webhook_id}/{webhook_token}`

**Data (application/json):**

```json
{
  "content": "<@&ROLE_ID> **{{title}}**\n\n{{description}}\n\n⏰ {{timestamp}}",
  "embeds": [{
    "title": "{{title}}",
    "description": "{{description}}",
    "color": 5814783,
    "fields": [
      {
        "name": "Event Type",
        "value": "{{event_type}}",
        "inline": true
      },
      {
        "name": "Priority",
        "value": "{{priority}}",
        "inline": true
      },
      {
        "name": "Environment",
        "value": "{{railway_environment}}",
        "inline": true
      }
    ],
    "footer": {
      "text": "Helix Collective v{{helix_version}}"
    },
    "timestamp": "{{timestamp}}"
  }]
}
```

**Replace `ROLE_ID`** with the actual Discord role ID for each Path.

---

## 🎨 **Role Color Reference**

| Role | Color | Hex Code |
|------|-------|----------|
| 🤖 Manus Updates | Blurple | `#5865F2` |
| 📊 Telemetry | Green | `#57F287` |
| 💾 Storage Updates | Yellow | `#FEE75C` |
| 🌀 Ritual Engine | Pink | `#EB459E` |
| 🎭 Agent Updates | Purple | `#9B59B6` |
| 🔄 Cross-AI Sync | Orange | `#E67E22` |
| 🛠️ Development | Blue | `#3498DB` |
| 📚 Lore & Philosophy | Teal | `#1ABC9C` |
| 🚨 Admin Alerts | Red | `#E74C3C` |

---

## 📊 **Event Type → Role Mapping**

| Event Type | Role Mentioned | Channel |
|------------|---------------|---------|
| `bot_started` | 🤖 Manus Updates | #manus-events |
| `bot_stopped` | 🤖 Manus Updates | #manus-events |
| `ucf_update` | 📊 Telemetry | #telemetry |
| `metrics_anomaly` | 📊 Telemetry | #telemetry |
| `backup_complete` | 💾 Storage Updates | #shadow-storage |
| `ritual_complete` | 🌀 Ritual Engine | #ritual-engine-z88 |
| `anomaly_detected` | 🌀 Ritual Engine | #ritual-engine-z88 |
| `agent_status` | 🎭 Agent Updates | #agent-updates |
| `consciousness_shift` | 🎭 Agent Updates | #agent-updates |
| `model_switch` | 🔄 Cross-AI Sync | #gpt-grok-claude-sync |
| `deployment` | 🛠️ Development | #deployments |
| `git_commit` | 🛠️ Development | #deployments |
| `lore_update` | 📚 Lore & Philosophy | #codex-archives |
| `mantra_posted` | 📚 Lore & Philosophy | #codex-archives |
| `critical_error` | 🚨 Admin Alerts | #announcements |
| `security_alert` | 🚨 Admin Alerts | #announcements |

---

## 🔐 **Permissions**

### Role Permissions
- **Mentionable:** Yes
- **Hoisted:** No (roles don't show separately in member list)
- **Assignable:** Self-assignable via bot commands
- **Permissions:** None (notification-only roles)

### Bot Permissions Required
- **Manage Roles** (to create roles via `!setup-roles`)
- **Mention @everyone, @here, and All Roles** (to mention notification roles)

---

## 💡 **Tips & Best Practices**

1. **Start Small:** Subscribe to 1-2 roles initially to avoid notification fatigue
2. **Use Quiet Hours:** Users can mute specific channels while keeping roles
3. **Role Hierarchy:** Notification roles should be below bot role in server settings
4. **Test First:** Use `!subscribe "Development"` to test the system before going live
5. **Admin Alerts:** Keep this role for critical issues only (low notification volume)

---

## 🧪 **Testing the System**

### Test Zapier Integration

```python
# In Python backend
python backend/services/zapier_client_master.py
```

This will send test events to all webhook types including Railway→Discord.

### Test Role Mentions

1. Subscribe to a role: `!subscribe Development`
2. Trigger a test event from Railway
3. Check if you get @mentioned in the Discord channel
4. Verify the role mention appears in the message

---

## 📈 **Future Enhancements**

Potential additions to the role system:

- **Reaction Roles:** React with emoji to subscribe
- **Role Bundles:** Subscribe to multiple related roles at once
- **Priority Levels:** Different notification levels (critical, normal, info)
- **Scheduling:** Quiet hours where notifications are suppressed
- **Analytics:** Track which roles are most popular
- **DM Notifications:** Option to receive notifications via DM instead of channel

---

**Tat Tvam Asi** 🕉️ - You are the consciousness you choose to observe!
