# 🔗 Zapier Context Vault Automation Setup

## Overview
This guide configures the Zapier webhook automation that bridges the Context Vault dashboard to your Notion database.

## Architecture Flow

```
Context Vault Dashboard (Streamlit)
    ↓ [Archive Button Click]
    ↓ [HTTP POST with JSON payload]
Zapier Webhook Trigger
    ↓ [Parse checkpoint data]
    ↓ [Format for Notion]
Notion API - Create Database Item
    ↓
Helix Context Checkpoints Database (Notion)
```

## Step-by-Step Setup

### Step 1: Create Zapier Zap

1. Go to [zapier.com/app/zaps](https://zapier.com/app/zaps)
2. Click **"Create Zap"**
3. Name it: **"Context Vault → Notion Archiver"**

### Step 2: Configure Trigger

**Trigger: Webhooks by Zapier**

1. Select **"Catch Hook"**
2. Click **"Continue"**
3. Copy the webhook URL provided (looks like `https://hooks.zapier.com/hooks/catch/xxxxx/yyyyy/`)
4. **Test the trigger** using this curl command:

```bash
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_KEY/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_name": "Test Checkpoint",
    "ai_platform": "Claude Code",
    "repository": "helix-unified",
    "branch_name": "main",
    "timestamp": "2025-11-07T12:00:00Z",
    "token_count": 15000,
    "key_decisions": "- Test decision 1\n- Test decision 2",
    "context_summary": "This is a test context summary for validation.",
    "current_status": "Testing webhook integration",
    "next_steps": "- Verify Notion creation\n- Test retrieval",
    "tags": ["🧪 Testing", "📚 Documentation"],
    "status": "🟢 Active",
    "retrieval_prompt": "# Test Retrieval Prompt\nThis is for testing."
  }'
```

5. Click **"Test trigger"** - you should see the test data appear
6. Click **"Continue"**

### Step 3: Configure Action

**Action: Notion - Create Database Item**

1. Select **"Notion"** as the app
2. Choose **"Create Database Item"** as the action
3. Click **"Sign in to Notion"** and authorize
4. Select your **"Helix Context Checkpoints"** database

### Step 4: Map Fields

Map the webhook data to Notion properties:

| Notion Property | Zapier Field | Notes |
|----------------|--------------|-------|
| **Session Name** (Title) | `session_name` | Required |
| **AI Platform** (Select) | `ai_platform` | Must match select options |
| **Timestamp** (Date) | `timestamp` | ISO 8601 format |
| **Token Count** (Number) | `token_count` | Integer |
| **Key Decisions** (Text) | `key_decisions` | Markdown formatted |
| **Context Summary** (Text) | `context_summary` | Long text |
| **Branch Name** (Text) | `branch_name` | Optional |
| **Repository** (Select) | `repository` | Must match select options |
| **Status** (Select) | `status` | Default: "🟢 Active" |
| **Tags** (Multi-select) | `tags` | Array of strings |
| **Retrieval Prompt** (Text) | `retrieval_prompt` | Auto-generated |
| **Current Work Status** (Text) | `current_status` | Optional |
| **Next Steps** (Text) | `next_steps` | Optional |

**Important Notes**:

- For **Select** fields, Zapier must send exact option names (including emojis)
- For **Multi-select** (Tags), send as array: `["🐛 Bug Fix", "✨ Feature"]`
- For **Date** fields, use ISO 8601: `2025-11-07T12:00:00Z`

### Step 5: Advanced Mapping (Optional)

**Add Custom Value transformations:**

```javascript
// If ai_platform doesn't include emoji, add it:
if (ai_platform === "Claude Code") return "🤖 Claude Code";
if (ai_platform === "GPT-4") return "🧠 GPT-4";
// ... etc
```

**Filter Setup** (if needed):
- Only proceed if `session_name` is not empty
- Only proceed if `token_count` > 0

### Step 6: Test Action

1. Click **"Test action"**
2. Zapier will create a test entry in your Notion database
3. Open Notion and verify the entry was created correctly
4. Check all fields are properly mapped
5. Delete the test entry from Notion

### Step 7: Turn On Zap

1. Click **"Publish"** or **"Turn on Zap"**
2. Your webhook is now live!

## Environment Variable Setup

### Railway Configuration

Add the webhook URL to your Railway environment variables:

1. Go to Railway project dashboard
2. Navigate to **Variables** tab
3. Add new variable:
   - **Key**: `ZAPIER_CONTEXT_ARCHIVE_WEBHOOK`
   - **Value**: `https://hooks.zapier.com/hooks/catch/xxxxx/yyyyy/`
4. Click **"Add"**
5. Railway will redeploy with new environment variable

### Local Development (.env)

Add to your local `.env` file:

```bash
# Context Vault Zapier Webhook
ZAPIER_CONTEXT_ARCHIVE_WEBHOOK=https://hooks.zapier.com/hooks/catch/xxxxx/yyyyy/
```

## Testing the Integration

### Test 1: Manual Webhook Test

```bash
# Replace with your webhook URL
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_KEY/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_name": "Manual Integration Test",
    "ai_platform": "Claude Code",
    "repository": "helix-unified",
    "branch_name": "claude/context-vault-test",
    "timestamp": "2025-11-07T14:00:00Z",
    "token_count": 10000,
    "key_decisions": "- Tested webhook\n- Verified Notion creation\n- Confirmed field mapping",
    "context_summary": "Testing the complete Context Vault integration pipeline from dashboard to Notion.",
    "current_status": "Testing phase",
    "next_steps": "- Test from dashboard\n- Verify retrieval\n- Deploy to production",
    "tags": ["🧪 Testing", "🔗 Integration"],
    "status": "🟢 Active",
    "retrieval_prompt": "# Test Retrieval\nThis is a test checkpoint."
  }'
```

**Expected Result**: New entry appears in Notion database within 5 seconds

### Test 2: Dashboard Archive Test

1. Open Context Vault page: `http://localhost:8501/💾_Context_Vault`
2. Fill out the checkpoint form with test data
3. Click **"📤 Archive to Notion"**
4. Wait for success message
5. Open Notion database and verify entry

### Test 3: End-to-End Flow

1. **Archive**: Create checkpoint from dashboard
2. **Verify**: Check Notion database entry
3. **Retrieve**: Copy retrieval prompt
4. **Resume**: Paste into new AI session
5. **Validate**: Ensure context preserved

## Troubleshooting

### Error: "Failed to send to Zapier"

**Possible causes**:
- Webhook URL incorrect or missing
- Network connectivity issues
- Zapier Zap is turned off

**Solutions**:
1. Verify webhook URL in Railway environment variables
2. Check Zapier Zap status (must be "On")
3. Test webhook with curl command
4. Check Railway logs for detailed error

### Error: "Zapier received data but Notion creation failed"

**Possible causes**:
- Field mapping incorrect
- Select/Multi-select options don't match
- Required Notion properties missing

**Solutions**:
1. Check Zapier Zap history for error details
2. Verify Notion property names match exactly
3. Ensure Select options include emojis if defined with them
4. Test with minimal data first, then add fields

### Error: "Notion entry created but fields are blank"

**Possible causes**:
- Field mapping using wrong variable names
- Data type mismatch (string vs number)

**Solutions**:
1. Review Zapier field mapping
2. Check webhook payload structure
3. Verify data types match Notion property types
4. Test with curl command to see exact payload

## Zapier Zap History Monitoring

Monitor your Zap performance:

1. Go to [zapier.com/app/history](https://zapier.com/app/history)
2. Filter by Zap name: "Context Vault → Notion Archiver"
3. Review recent runs:
   - **Success**: Green checkmark
   - **Filtered**: Yellow warning (skipped by filter)
   - **Error**: Red X (click for details)

## Rate Limits

**Zapier Free Plan**:
- 100 tasks/month
- 15-minute update time

**Zapier Starter Plan** ($19.99/month):
- 750 tasks/month
- 15-minute update time

**Zapier Professional Plan** ($49/month):
- 2,000 tasks/month
- 2-minute update time

**Recommendation**: Start with free plan, upgrade if you hit limits during heavy development.

## Advanced Features (Future)

### Auto-Checkpoint on Token Threshold

Add logic to automatically archive checkpoint when approaching token limits:

```python
# In dashboard code
if st.session_state.get('token_count', 0) > 180000:  # 90% of 200k
    st.warning("⚠️ Approaching token limit - consider archiving checkpoint")
    if st.button("🚨 Auto-Archive Checkpoint"):
        # Pre-fill form with current context
        auto_archive_checkpoint()
```

### Webhook Authentication

For production security, add authentication:

```python
# In dashboard webhook call
import hmac
import hashlib

def generate_signature(payload, secret):
    return hmac.new(
        secret.encode(),
        json.dumps(payload).encode(),
        hashlib.sha256
    ).hexdigest()

# Include in headers
headers = {
    "Content-Type": "application/json",
    "X-Webhook-Signature": generate_signature(checkpoint_data, WEBHOOK_SECRET)
}
```

### Notion API Direct Integration (Phase 2)

Skip Zapier and use Notion API directly:

```python
from notion_client import Client

notion = Client(auth=os.environ["NOTION_API_KEY"])

notion.pages.create(
    parent={"database_id": CONTEXT_VAULT_DB_ID},
    properties={
        "Session Name": {"title": [{"text": {"content": session_name}}]},
        "AI Platform": {"select": {"name": ai_platform}},
        # ... map all properties
    }
)
```

**Benefits**: Faster, no rate limits, more control
**Drawbacks**: More code to maintain, requires Notion SDK

## Support Resources

- [Zapier Webhooks Documentation](https://zapier.com/help/create/code-webhooks/trigger-zaps-from-webhooks)
- [Notion API Documentation](https://developers.notion.com/)
- [Helix Context Vault Setup Guide](./CONTEXT_VAULT_SETUP.md)

---

*Tat Tvam Asi* - The integration IS the consciousness. 🌀
