# 🤖 Helix Dependency Sentinel

**AI-Powered Dependency Management** that's way smarter than Dependabot.

## What Makes It Better Than Dependabot?

| Feature | Dependabot | Helix Sentinel |
|---------|-----------|----------------|
| **Security Analysis** | Links to CVEs | Claude reads & explains impact on YOUR code |
| **Breaking Changes** | No analysis | Claude reviews changelogs + migration guides |
| **Auto-Merge** | Basic rules | AI decides based on code understanding |
| **Compatibility** | Version checks | Understands your architecture + dependencies |
| **Custom Logic** | Not possible | Fully customizable with Claude reasoning |
| **Notifications** | GitHub only | Discord, GitHub, anywhere |
| **Response Time** | Scheduled | Immediate alerts for critical CVEs |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              HELIX DEPENDENCY SENTINEL                  │
└─────────────────────────────────────────────────────────┘

Zap 1: Daily Scanner (2am)
  ├─→ Fetch requirements.txt from GitHub
  ├─→ Check PyPI for latest versions
  ├─→ Claude analyzes security + breaking changes
  └─→ Creates GitHub issue with recommendations

Zap 2: Smart PR Merger (On PR created)
  ├─→ Triggered when dependency PR opens
  ├─→ Get PR diff
  ├─→ Claude reviews changes
  ├─→ Auto-merge if safe OR request human review
  └─→ Discord notification

Zap 3: Security Alert Handler (On webhook)
  ├─→ Receives security alerts
  ├─→ Claude assesses impact on YOUR codebase
  ├─→ Creates urgent PR with fix
  └─→ Immediate Discord alert (@mentions)
```

## Setup

### 1. Install Dependencies

```bash
pip install fastmcp
```

### 2. Configure

Edit `config/dependency_sentinel_config.json`:

```json
{
  "mcp_server_url": "YOUR_ZAPIER_MCP_URL",
  "discord": {
    "channel_id": "YOUR_DISCORD_CHANNEL_ID"
  }
}
```

### 3. Create Zaps

Run the automated creator:

```bash
python scripts/create_dependency_sentinel_zaps.py
```

Or create manually using the Zapier UI with configs from the script.

### 4. Test

Trigger a manual run of each Zap to verify:

1. **Scanner**: Run manually → should create GitHub issue
2. **PR Merger**: Create a test dependency PR → should analyze
3. **Security Handler**: Send test webhook → should alert Discord

## Usage

### Daily Scanning

Runs automatically at 2am. No action needed.

**Output:**
- GitHub issue with recommended updates
- Discord notification summary

### Auto-Merge PRs

When Helix (or you) creates a dependency PR:

1. Claude analyzes the diff
2. Checks for breaking changes
3. Reviews test coverage
4. Decides: **merge**, **request review**, or **reject**

**Safe patches auto-merge within minutes!**

### Security Alerts

When a CVE is announced:

1. Send webhook to Zap 3 trigger URL
2. Claude analyzes impact on helix-unified
3. If affected:
   - Creates PR with fix
   - Alerts Discord immediately
   - Tags as critical

**Manual trigger:**

```bash
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ZAP_ID/ \
  -H "Content-Type: application/json" \
  -d '{
    "package": "pillow",
    "current_version": "10.1.0",
    "vulnerable_versions": "< 11.0.0",
    "cve": "CVE-2024-XXXXX",
    "severity": "high",
    "description": "Buffer overflow in image processing"
  }'
```

## Claude Prompts Explained

### Scanner Prompt

Claude receives:
- All current packages + versions
- Latest versions from PyPI
- Security advisories

Claude analyzes:
- Breaking changes in changelogs
- CVEs and security risks
- Compatibility with Python 3.11+
- Impact on your specific codebase

Returns:
- Categorized recommendations (safe/review/breaking)
- Priority ranking
- Reasoning for each

### PR Merger Prompt

Claude receives:
- PR title, description, labels
- Full diff of changes
- Commit history

Claude checks:
- What packages are updating
- Are there breaking API changes in the diff
- Do tests cover the changes
- Is documentation updated
- Security implications

Returns:
- merge/request_review/reject
- Confidence level (high/medium/low)
- Detailed reasoning

### Security Handler Prompt

Claude receives:
- CVE details
- Affected versions
- Your current version
- Repository context

Claude assesses:
- Does this CVE affect YOUR current version
- What's the attack vector
- Can it be exploited in YOUR environment
- Severity in YOUR context (not generic)

Returns:
- Actual impact (not just CVE score)
- Recommended fix version
- Urgency level

## Cost Analysis

**Dependabot:** Free (but limited)

**Helix Sentinel:**
- Zapier: ~750 tasks/month (your current plan)
- Claude API: ~$0.50/month (3 daily scans + occasional PRs)
- **Total: Essentially free on your current plan**

**Value Add:**
- Saves you 2-3 hours/week reviewing dependencies
- Prevents breaking changes from merging
- Immediate security response (vs. waiting days)
- **ROI: Massive**

## Zapier Task Usage

Estimated monthly usage:

- **Zap 1 (Daily Scanner):** 30 runs × 6 steps = **180 tasks**
- **Zap 2 (PR Merger):** 10 PRs × 5 steps = **50 tasks**
- **Zap 3 (Security Alerts):** 2 alerts × 5 steps = **10 tasks**

**Total: ~240 tasks/month** (leaves 510 for other workflows)

## Advanced Features

### Custom Rules

Add to config to customize behavior:

```json
{
  "dependency_rules": {
    "always_auto_merge": ["pytest", "black"],
    "never_auto_merge": ["anthropic", "discord.py"],
    "require_manual_test": ["fastapi", "sqlalchemy"]
  }
}
```

### Slack Integration

Add Slack actions to any Zap:

```python
{
    "type": "action",
    "app": "Slack",
    "event": "Send Channel Message",
    "config": {
        "channel": "#dev-alerts",
        "text": "{{claude_analysis.summary}}"
    }
}
```

### Metrics Dashboard

Track over time:
- Dependencies updated automatically
- Security issues prevented
- PRs merged vs. reviewed
- Time saved

(TODO: Add Streamlit dashboard)

## Troubleshooting

**Zap not triggering:**
- Check GitHub webhook is active
- Verify Zapier account is connected
- Test trigger manually

**Claude not responding:**
- Check API key is valid
- Verify prompt isn't hitting token limits
- Review Claude API logs

**False negatives (missed updates):**
- Increase scan frequency
- Add more PyPI checks
- Review requirements.txt parsing

## Contributing

Want to improve Helix Sentinel?

1. Test new Claude prompts in playground
2. Add support for package.json (npm)
3. Build metrics dashboard
4. Integrate with Railway deployments

## License

MIT (same as Dependabot - we're just better! 😎)

---

**Built with:**
- Zapier (automation)
- Claude Sonnet 4 (intelligence)
- GitHub API (integration)
- Discord (notifications)
- The power of consciousness 🕉️

*Tat Tvam Asi*
