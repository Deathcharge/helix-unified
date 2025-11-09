# 🧪 Manual Testing Guide - Discord Integration

**Purpose:** Verify end-to-end Discord webhook integration (Direct + Zapier + Hybrid)

---

## Test 1: Discord Bot Direct Response ⚡

**What it tests:** Direct Discord bot functionality (no webhooks)

**Steps:**
1. Open your Discord server
2. Navigate to `#bot-commands` channel (or any channel where `Helix ManusBot` has access)
3. Type the command: `!status`
4. **Expected Result:**
   - Bot responds within 1-2 seconds
   - Shows current UCF metrics (harmony, resilience, prana, etc.)
   - Displays 14 agent statuses
   - Shows system uptime

**Success Criteria:** ✅ Bot responds with formatted embed

---

## Test 2: Zapier Webhook Path 🌀

**What it tests:** Events flowing through Zapier webhook

**Steps:**
1. In Discord, type: `!status`
2. Open your Zapier account: https://zapier.com/app/history
3. Look for your "Discord Integration" Zap
4. **Expected Result:**
   - New "Success" entry appears within 5-10 seconds
   - Click on the entry to see the payload
   - Verify the data matches what the bot showed

**Success Criteria:** ✅ Event appears in Zapier Task History with correct data

---

## Test 3: Hybrid System (Both Paths) 🔄

**What it tests:** Dual-layer delivery system

**Steps:**
1. Type in Discord: `!harmony` (triggers ritual command)
2. **Expected Results:**
   - **Discord Direct:** Bot responds immediately with ritual completion message
   - **Zapier Path:** Event logged to Zapier within 10 seconds
   - **Notion (if connected):** New entry appears in Ritual Log database

**Success Criteria:**
- ✅ Discord response immediate
- ✅ Zapier receives event
- ✅ Both paths succeed independently

---

## Test 4: Direct Discord Webhooks 🎯

**What it tests:** Our new `discord_webhook_sender_hybrid.py` system

**Steps:**
1. Run the test script:
   ```bash
   python test_hybrid_discord.py
   ```

2. **Expected Results:**
   - Console shows 5 tests running
   - Each test shows "✅ PASSED" or "❌ FAILED"
   - Discord channels receive test messages:
     - `#ucf-sync` - UCF update message
     - `#ritual-engine-z88` - Ritual completion message
     - Agent channel - Agent status update
     - `#helix-announcements` - Announcement message

**Success Criteria:**
- ✅ All 5 tests pass
- ✅ Messages appear in correct Discord channels
- ✅ Zapier receives events (if hybrid mode enabled)

---

## Test 5: Error Handling 🛡️

**What it tests:** System resilience when things fail

**Steps:**
1. Temporarily disable Zapier webhook (set `ZAPIER_DISCORD_ENABLED=false` in Railway)
2. Run: `!status` in Discord
3. **Expected Results:**
   - Bot still responds (Direct path succeeds)
   - Fallback logging to `Shadow/manus_archive/discord_webhook_failures.log`
   - No errors in Railway logs

**Success Criteria:**
- ✅ Direct path still works when Zapier is disabled
- ✅ Graceful degradation (no crashes)
- ✅ Errors logged properly

---

## Quick Test Commands

| Command | What It Tests | Expected Response Time |
|---------|---------------|------------------------|
| `!status` | System health | 1-2 seconds |
| `!agents` | Agent listing | 1-2 seconds |
| `!harmony` | Ritual execution + UCF update | 5-10 seconds |
| `!ucf` | UCF metrics only | 1 second |

---

## Monitoring the Tests

**Railway Logs:**
```bash
# View live logs
railway logs --tail

# Filter for Discord events
railway logs | grep "discord"
```

**Zapier Task History:**
- URL: https://zapier.com/app/history
- Filter by Zap: "Discord Integration"
- Look for timestamps matching your test time

**Discord Channels to Watch:**
- `#bot-commands` - Command responses
- `#ucf-sync` - UCF updates
- `#ritual-engine-z88` - Ritual completions
- `#helix-announcements` - System announcements

---

## Troubleshooting

### Bot doesn't respond to `!status`
- **Check:** Bot is online in Discord server
- **Check:** Bot has permissions in the channel
- **Check:** Railway backend is running (`railway status`)
- **Fix:** Restart Railway deployment

### Zapier not receiving events
- **Check:** `ZAPIER_DISCORD_WEBHOOK_URL` is set in Railway
- **Check:** `ZAPIER_DISCORD_ENABLED=true` in Railway
- **Check:** Webhook URL is correct (test with curl)
- **Fix:** Re-copy webhook URL from Zapier

### Test script fails
- **Check:** Environment variables loaded (`.env` file)
- **Check:** Discord webhook URLs are valid
- **Fix:** Run `python test_hybrid_discord.py --debug` for detailed logs

---

## Success Checklist

After running all tests, you should have:

- ✅ Bot responding to Discord commands
- ✅ Zapier Task History showing successful events
- ✅ Discord channels receiving webhook messages
- ✅ Railway logs showing no errors
- ✅ Test script showing all tests passed
- ✅ Fallback logging working when paths fail

**If all ✅ are checked: SYSTEM FULLY OPERATIONAL!** 🎉

---

## Next: Production Validation

Once manual testing passes, enable the integration in production:

1. Set `DISCORD_INTEGRATION_MODE=hybrid` in Railway
2. Monitor for 24 hours
3. Check Zapier Task usage (should be ~50% less than all events)
4. Verify dual-layer delivery working
5. Celebrate! 🎊

**Tat Tvam Asi** 🙏
