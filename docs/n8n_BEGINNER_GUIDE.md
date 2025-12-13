# 🔄 n8n Workflow Automation - Complete Beginner's Guide

**What You'll Learn:**
- What n8n is and why you have it
- How to use it for your Workflow tier ($79/mo)
- 5 ready-to-use workflow templates
- How to connect n8n to Helix backend

**Time to Read:** 15 minutes
**Time to Build First Workflow:** 5 minutes

---

## 🤔 What is n8n?

**n8n = "Zapier but you own it"**

Think of it as a **robot assistant** that automatically does repetitive tasks for you.

### Real-World Example

**Without n8n:**
```
1. User signs up on your SaaS platform
2. You manually:
   - Send welcome email
   - Add them to Discord
   - Create Notion database entry
   - Post to team Slack
   - Update spreadsheet
```
**Time:** 10 minutes per user × 100 users = **16+ hours per week!** 😰

**With n8n:**
```
1. User signs up
2. n8n automatically:
   - Sends welcome email ✅
   - Adds to Discord ✅
   - Creates Notion entry ✅
   - Posts to Slack ✅
   - Updates spreadsheet ✅
```
**Time:** 0 minutes per user! 🎉

---

## 🎯 Why You Have n8n on Railway

Your **Workflow tier** ($79/mo) promises **workflow automation**. n8n delivers this!

**What it gives your customers:**
- Visual workflow builder (no code needed)
- 400+ integrations (Stripe, Discord, Gmail, Slack, etc.)
- Unlimited workflows
- Webhook triggers
- Scheduled tasks (cron jobs)
- Custom JavaScript/Python code

**Revenue Opportunity:**
```
Workflow Tier: $79/mo per customer
n8n Cost: ~$5/mo on Railway
Your Profit: $74/mo per customer! 💰
```

---

## 🚀 Accessing Your n8n Instance

**Step 1: Get the URL**

Railway Dashboard → n8n-primary service → Settings → Domains

Copy the public URL (e.g., `https://n8n-primary-production.up.railway.app`)

**Step 2: First Login**

1. Open the URL in browser
2. Create admin account:
   - Email: your@email.com
   - Password: (secure password)
3. Save credentials!

**Step 3: Verify It Works**

You should see the n8n dashboard with:
- "Create new workflow" button
- "Workflows" sidebar
- "Credentials" menu

---

## 🎨 n8n Interface Tour (2 Minutes)

### Main Screen

```
┌─────────────────────────────────────────┐
│  n8n - Workflow Automation              │
├─────────────────────────────────────────┤
│                                         │
│  Workflows                              │
│  ├─ My workflows                        │
│  ├─ Templates                           │
│  └─ Credentials                         │
│                                         │
│  [+ Create New Workflow]                │
│                                         │
└─────────────────────────────────────────┘
```

### Workflow Builder

```
┌─────────────────────────────────────────┐
│  [Trigger] → [Action] → [Action]        │
│                                         │
│  Nodes (Building Blocks):               │
│  ├─ Webhook (trigger from API)          │
│  ├─ Schedule (run at specific time)     │
│  ├─ Email (send emails)                 │
│  ├─ HTTP Request (call APIs)            │
│  ├─ Database (query/insert data)        │
│  └─ 400+ more...                        │
└─────────────────────────────────────────┘
```

---

## 📝 Your First Workflow (5 Minutes)

Let's build: **"Send email when webhook receives data"**

### Step 1: Create Workflow

1. Click "Create new workflow"
2. Name it: "Welcome Email Automation"

### Step 2: Add Webhook Trigger

1. Click the "+" button
2. Search: "Webhook"
3. Select "Webhook"
4. HTTP Method: `POST`
5. Path: `welcome`
6. Click "Execute Node"
7. **Copy the webhook URL!** (e.g., `https://n8n.../webhook/welcome`)

### Step 3: Add Email Node

1. Click "+" after webhook
2. Search: "Send Email"
3. Select "Send Email" (SMTP)
4. Configure:
   - From: `noreply@yourdomain.com`
   - To: `{{ $json.email }}` (from webhook data)
   - Subject: `Welcome to Helix!`
   - Text: `Hi {{ $json.name }}, welcome!`

### Step 4: Configure SMTP Credentials

1. Click "Create New Credential"
2. SMTP settings:
   - Host: `smtp.gmail.com` (or your provider)
   - Port: `587`
   - User: `your@email.com`
   - Password: (app password)
3. Save

### Step 5: Test It!

**Terminal (or Postman):**
```bash
curl -X POST https://your-n8n.../webhook/welcome \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User"}'
```

**You should receive an email!** ✅

### Step 6: Activate

Click "Active" toggle in top right → Workflow is now live! 🎉

---

## 🎁 5 Ready-to-Use Workflow Templates

### 1️⃣ **New User Onboarding**

```
Webhook (user registers)
  → Send welcome email
  → Add to Discord server (via bot)
  → Create Notion database entry
  → Post to Slack #new-users
```

**Use Case:** Automate entire user signup process

---

### 2️⃣ **Payment Received → Invoice**

```
Webhook (Stripe payment)
  → Generate PDF invoice
  → Email invoice to customer
  → Update database
  → Notify team in Discord
```

**Use Case:** Automatic invoicing

---

### 3️⃣ **Daily Report Generator**

```
Schedule (Every day 9am)
  → Query PostgreSQL (usage stats)
  → Generate report
  → Email to admins
  → Post summary to Discord
```

**Use Case:** Daily analytics reports

---

### 4️⃣ **Support Ticket Automation**

```
Webhook (support form)
  → Create Notion ticket
  → Send auto-reply email
  → Post to Discord #support
  → Assign to team member (round-robin)
```

**Use Case:** Support ticket management

---

### 5️⃣ **Failed Payment Recovery**

```
Webhook (Stripe payment failed)
  → Wait 3 days
  → Send reminder email
  → If still failed after 7 days:
    → Downgrade subscription
    → Notify user
```

**Use Case:** Reduce churn from failed payments

---

## 🔗 Connecting n8n to Helix Backend

### Method 1: Webhook → Helix API

**n8n Workflow:**
```
Webhook (receives data)
  → HTTP Request Node:
      URL: https://helix-backend-api.../v1/saas/v1/agents/kael/execute
      Method: POST
      Headers: Authorization: Bearer YOUR_API_KEY
      Body: { "task": "document", "input": "{{ $json.code }}" }
```

**Result:** External webhook triggers Helix AI agent!

---

### Method 2: Helix → n8n Webhook

**In your Helix backend:**
```python
import httpx

async def trigger_n8n_workflow(user_data):
    """Trigger n8n workflow from Helix"""
    n8n_url = os.getenv("N8N_WEBHOOK_URL")

    async with httpx.AsyncClient() as client:
        await client.post(n8n_url, json={
            "event": "user_registered",
            "user": user_data
        })
```

**Add to Railway env vars:**
```bash
N8N_WEBHOOK_URL=https://your-n8n.../webhook/helix-events
```

---

### Method 3: Database Integration

**n8n can directly query your PostgreSQL:**

1. Add Postgres credential in n8n
2. Use "Postgres" node in workflow
3. Query/insert data directly

**Example Workflow:**
```
Schedule (Hourly)
  → Postgres: SELECT * FROM users WHERE trial_ends_at < NOW()
  → For Each User:
      → Send "trial ending" email
```

---

## 🎓 Advanced Features

### JavaScript Code Node

Need custom logic? Use Code node:

```javascript
// Example: Calculate subscription renewal date
const user = $input.item.json;
const today = new Date();
const renewalDate = new Date(today.setMonth(today.getMonth() + 1));

return {
  json: {
    user_id: user.id,
    renewal_date: renewalDate.toISOString()
  }
};
```

---

### Error Handling

Add "Error Trigger" node to handle failures:

```
[Main Workflow]
  ↓ (if error)
[Error Trigger]
  → Log to database
  → Send alert to Discord
  → Retry with exponential backoff
```

---

### Conditional Logic (IF/ELSE)

Use "IF" node for branching:

```
Webhook
  → IF: amount > $100
      → Send "high value" email
  → ELSE
      → Send standard email
```

---

## 💰 Monetization Strategy

### How to Sell Workflow Tier

**Positioning:**
```
Free Tier: API access only
Pro Tier ($29): API + all agents
Workflow Tier ($79): API + agents + n8n automation ⭐
Enterprise ($299): Everything + white-label
```

**Value Proposition:**
- "Automate your entire business workflow"
- "No code required - visual builder"
- "Save 10+ hours per week on repetitive tasks"
- "400+ integrations included"

**Customer Examples:**
```
Marketing Agency:
- Auto-generate client reports
- Schedule social media posts
- Track campaign performance
- Invoice clients automatically

E-commerce Store:
- Order fulfillment automation
- Customer follow-up emails
- Inventory alerts
- Revenue reports

SaaS Company:
- User onboarding sequences
- Trial expiration reminders
- Feature usage tracking
- Churn prevention workflows
```

---

## 🚨 Common Issues & Solutions

### Issue: Workflow not triggering

**Check:**
1. Is workflow "Active"? (green toggle)
2. Is webhook URL correct?
3. Check execution history (hamburger menu)
4. Test with "Execute Node" button

---

### Issue: Email not sending

**Fix:**
1. Verify SMTP credentials
2. Check spam folder
3. Use Gmail app password (not regular password)
4. Enable "Less secure apps" in Gmail settings

---

### Issue: Database connection failed

**Fix:**
1. Verify DATABASE_URL in n8n credentials
2. Check PostgreSQL is running on Railway
3. Test connection with "Test Connection" button
4. Ensure database allows external connections

---

## 📊 Monitoring & Analytics

### View Workflow Executions

1. Click workflow name
2. "Executions" tab
3. See all runs with:
   - Success/failure status
   - Execution time
   - Input/output data
   - Error messages

### Performance Tips

- **Use Queues:** For high-volume workflows, enable queue mode
- **Batch Processing:** Process multiple items at once
- **Caching:** Store API responses to reduce calls
- **Webhooks over Polling:** More efficient than scheduled checks

---

## 🎯 Next Steps

### Week 1: Learn the Basics
- ✅ Build your first workflow
- ✅ Connect to Helix backend
- ✅ Test with real data

### Week 2: Deploy to Customers
- ✅ Create customer documentation
- ✅ Set up separate n8n instances per customer (optional)
- ✅ Build workflow templates library

### Week 3: Advanced Automation
- ✅ Multi-step workflows
- ✅ Error handling
- ✅ Custom JavaScript code
- ✅ Database integrations

---

## 📚 Resources

**Official n8n Docs:**
- https://docs.n8n.io/

**Tutorial Videos:**
- YouTube: "n8n basics" (tons of tutorials)

**Community:**
- https://community.n8n.io/

**Template Library:**
- https://n8n.io/workflows/ (700+ templates!)

---

## 💡 Pro Tips

1. **Start Simple:** Begin with 2-node workflows, then expand
2. **Test Everything:** Use "Execute Node" before activating
3. **Document Workflows:** Add notes to complex nodes
4. **Version Control:** Export workflows as JSON backups
5. **Monitor Logs:** Check executions daily for errors
6. **Security:** Never expose webhook URLs publicly (use authentication)

---

## 🎊 Summary

**You Now Know:**
- ✅ What n8n is (Zapier alternative)
- ✅ Why it's valuable for Workflow tier
- ✅ How to build your first workflow
- ✅ 5 ready-to-use templates
- ✅ How to connect to Helix backend
- ✅ How to monetize it ($74/mo profit per customer!)

**Time Saved per Month:**
- Manual onboarding: 20 hours
- Email campaigns: 10 hours
- Reporting: 15 hours
- Support tickets: 25 hours
- **Total: 70 hours = $3,500+ in labor costs!**

---

**Ready to automate everything?** Open your n8n dashboard and start building! 🚀

**Questions?** Check the [n8n community forum](https://community.n8n.io/) or ask in Discord!
