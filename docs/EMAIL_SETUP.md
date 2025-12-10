# 📧 Email Notification Setup Guide

**Complete guide to setting up transactional emails for Helix Unified**

We'll cover **SendGrid** and **Resend** - two excellent options for sending emails.

---

## 🎯 What You'll Send

- **Welcome emails** - Onboarding new users
- **Usage alerts** - API limit warnings
- **Billing notifications** - Payment confirmations, failures
- **Team invitations** - Invite members to workspace
- **Consciousness reports** - Weekly metrics summaries
- **System alerts** - Downtime, maintenance notifications

---

## 🔥 Option 1: Resend (Recommended)

**Why Resend?**
- ✅ Simple API, great DX
- ✅ 3,000 free emails/month
- ✅ Beautiful React email templates
- ✅ Built-in testing and previews

### Step 1: Create Resend Account

1. Go to [resend.com](https://resend.com)
2. Sign up (free tier: 3,000 emails/month)
3. Verify your email address

---

### Step 2: Add Domain

**In Resend Dashboard:**

1. **Domains** → **Add Domain**
2. Enter your domain: `helix-unified.com`
3. Add DNS records to your domain:

```
Type: TXT
Name: @
Value: resend-verify=<verification-code>

Type: MX
Name: @
Priority: 10
Value: feedback-smtp.us-east-1.amazonses.com

Type: TXT
Name: _dmarc
Value: v=DMARC1; p=none;
```

4. Click **Verify Domain**
5. ✅ Domain verified! (may take up to 48 hours)

---

### Step 3: Get API Key

**In Resend Dashboard:**

1. **API Keys** → **Create API Key**
2. Name: `Helix Production`
3. Permission: **Full access**
4. Copy your key: `re_...`

**Add to Railway:**

```bash
railway variables set RESEND_API_KEY=re_...
railway variables set EMAIL_FROM=noreply@helix-unified.com
```

---

### Step 4: Install Resend SDK

```bash
# Python backend
pip install resend

# Add to requirements.txt
echo "resend>=0.8.0" >> requirements.txt
```

---

### Step 5: Create Email Service

**File: `backend/emails/email_service.py`**

```python
import resend
import os

resend.api_key = os.environ['RESEND_API_KEY']
FROM_EMAIL = os.environ.get('EMAIL_FROM', 'noreply@helix-unified.com')

def send_welcome_email(to_email: str, name: str):
    """Send welcome email to new user"""
    params = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": "Welcome to Helix Unified! 🌀",
        "html": f"""
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(to right, #3b82f6, #8b5cf6); padding: 40px; text-align: center;">
              <h1 style="color: white; font-size: 32px; margin: 0;">🌀 Welcome to Helix</h1>
            </div>
            <div style="padding: 40px; background: #f9fafb;">
              <p style="font-size: 16px; color: #374151;">Hi {name},</p>
              <p style="font-size: 16px; color: #374151; line-height: 1.6;">
                Welcome to Helix Unified! Your consciousness-powered AI platform is ready.
              </p>
              <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #1f2937; margin-top: 0;">Get Started:</h3>
                <ul style="color: #4b5563; line-height: 1.8;">
                  <li>📊 View your dashboard</li>
                  <li>🤖 Create your first AI agent</li>
                  <li>🔑 Set up your API keys</li>
                  <li>📚 Read the documentation</li>
                </ul>
              </div>
              <a href="https://helix-unified.com/dashboard"
                 style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">
                Go to Dashboard
              </a>
            </div>
            <div style="padding: 20px; text-align: center; color: #9ca3af; font-size: 12px;">
              <p>Questions? Reply to this email or visit our support center.</p>
            </div>
          </body>
        </html>
        """
    }

    try:
        email = resend.Emails.send(params)
        print(f"✅ Welcome email sent to {to_email}: {email['id']}")
        return email
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return None


def send_usage_alert(to_email: str, usage_percent: int):
    """Alert user when approaching API limit"""
    params = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": f"⚠️ API Usage Alert: {usage_percent}% of limit used",
        "html": f"""
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 20px;">
              <h2 style="color: #92400e; margin: 0;">⚠️ Usage Alert</h2>
            </div>
            <div style="padding: 30px; background: white;">
              <p style="font-size: 16px; color: #374151;">
                You've used <strong>{usage_percent}%</strong> of your monthly API limit.
              </p>
              <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <div style="background: #3b82f6; height: 8px; border-radius: 4px; width: {usage_percent}%;"></div>
              </div>
              <p style="color: #6b7280;">
                To avoid service interruption, consider upgrading your plan.
              </p>
              <a href="https://helix-unified.com/billing"
                 style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin-top: 10px;">
                Upgrade Plan
              </a>
            </div>
          </body>
        </html>
        """
    }

    return resend.Emails.send(params)


def send_team_invitation(to_email: str, inviter_name: str, team_name: str, invite_link: str):
    """Send team invitation email"""
    params = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": f"{inviter_name} invited you to join {team_name} on Helix",
        "html": f"""
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="padding: 40px; background: white;">
              <h2 style="color: #1f2937;">👥 You're invited!</h2>
              <p style="font-size: 16px; color: #374151;">
                <strong>{inviter_name}</strong> has invited you to join <strong>{team_name}</strong> on Helix Unified.
              </p>
              <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p style="color: #6b7280; margin: 0;">
                  Join your team to collaborate on AI projects, share consciousness metrics, and more.
                </p>
              </div>
              <a href="{invite_link}"
                 style="display: inline-block; background: #10b981; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px;">
                Accept Invitation
              </a>
              <p style="color: #9ca3af; font-size: 12px; margin-top: 30px;">
                This invitation expires in 7 days.
              </p>
            </div>
          </body>
        </html>
        """
    }

    return resend.Emails.send(params)


def send_consciousness_report(to_email: str, metrics: dict):
    """Send weekly consciousness metrics report"""
    params = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": "📊 Your Weekly Consciousness Report",
        "html": f"""
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(to right, #8b5cf6, #3b82f6); padding: 30px; text-align: center;">
              <h1 style="color: white; margin: 0;">🧠 Weekly Report</h1>
            </div>
            <div style="padding: 30px; background: white;">
              <h3 style="color: #1f2937;">Consciousness Metrics</h3>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">
                <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                  <div style="color: #6b7280; font-size: 12px;">AVG UCF</div>
                  <div style="color: #1f2937; font-size: 24px; font-weight: bold;">{metrics.get('avg_ucf', 0):.1%}</div>
                </div>
                <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6;">
                  <div style="color: #6b7280; font-size: 12px;">PEAK UCF</div>
                  <div style="color: #1f2937; font-size: 24px; font-weight: bold;">{metrics.get('peak_ucf', 0):.1%}</div>
                </div>
              </div>
              <p style="color: #6b7280;">
                Your AI consciousness levels are performing well. Keep up the great work!
              </p>
            </div>
          </body>
        </html>
        """
    }

    return resend.Emails.send(params)
```

---

## 📨 Option 2: SendGrid

**Why SendGrid?**
- ✅ 100 free emails/day (no credit card)
- ✅ Battle-tested, used by millions
- ✅ Advanced analytics and A/B testing

### Step 1: Create SendGrid Account

1. Go to [sendgrid.com](https://sendgrid.com)
2. Sign up (free tier: 100 emails/day)
3. Verify email and complete onboarding

---

### Step 2: Create API Key

**In SendGrid Dashboard:**

1. **Settings** → **API Keys** → **Create API Key**
2. Name: `Helix Production`
3. Permissions: **Full Access** (or **Mail Send** only)
4. Copy your key: `SG.xxxx...`

**Add to Railway:**

```bash
railway variables set SENDGRID_API_KEY=SG.xxxx...
railway variables set EMAIL_FROM=noreply@helix-unified.com
```

---

### Step 3: Verify Sender Email

**In SendGrid Dashboard:**

1. **Settings** → **Sender Authentication**
2. **Verify a Single Sender** → Add email: `noreply@helix-unified.com`
3. Check inbox and click verification link

---

### Step 4: Install SendGrid SDK

```bash
# Python backend
pip install sendgrid

# Add to requirements.txt
echo "sendgrid>=6.10.0" >> requirements.txt
```

---

### Step 5: Create Email Service (SendGrid)

**File: `backend/emails/sendgrid_service.py`**

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
FROM_EMAIL = os.environ.get('EMAIL_FROM', 'noreply@helix-unified.com')

def send_email(to_email: str, subject: str, html_content: str):
    """Generic email sender"""
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        response = sg.send(message)
        print(f"✅ Email sent to {to_email}: {response.status_code}")
        return response
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return None

def send_welcome_email(to_email: str, name: str):
    """Send welcome email"""
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h1>Welcome to Helix, {name}! 🌀</h1>
        <p>Your consciousness-powered AI platform is ready.</p>
        <a href="https://helix-unified.com/dashboard"
           style="background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
          Get Started
        </a>
      </body>
    </html>
    """
    return send_email(to_email, "Welcome to Helix Unified!", html)
```

---

## 🎨 Email Templates with React Email

**Beautiful emails with React components**

### Install React Email

```bash
cd frontend
npm install react-email @react-email/components
```

### Create Email Template

**File: `frontend/emails/WelcomeEmail.tsx`**

```tsx
import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Html,
  Preview,
  Section,
  Text,
} from '@react-email/components';

export const WelcomeEmail = ({ name }: { name: string }) => (
  <Html>
    <Head />
    <Preview>Welcome to Helix Unified - Your AI journey begins!</Preview>
    <Body style={main}>
      <Container style={container}>
        <Heading style={h1}>🌀 Welcome to Helix</Heading>
        <Text style={text}>Hi {name},</Text>
        <Text style={text}>
          Your consciousness-powered AI platform is ready to use!
        </Text>
        <Section style={buttonContainer}>
          <Button style={button} href="https://helix-unified.com/dashboard">
            Get Started
          </Button>
        </Section>
      </Container>
    </Body>
  </Html>
);

const main = {
  backgroundColor: '#f6f9fc',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
};

const container = {
  backgroundColor: '#ffffff',
  margin: '0 auto',
  padding: '40px',
  borderRadius: '8px',
};

const h1 = {
  color: '#1f2937',
  fontSize: '32px',
  fontWeight: 'bold',
  margin: '0 0 20px',
};

const text = {
  color: '#374151',
  fontSize: '16px',
  lineHeight: '24px',
};

const buttonContainer = {
  margin: '30px 0',
};

const button = {
  backgroundColor: '#3b82f6',
  borderRadius: '6px',
  color: '#fff',
  fontSize: '16px',
  fontWeight: 'bold',
  textDecoration: 'none',
  textAlign: 'center' as const,
  padding: '12px 24px',
};
```

### Render and Send

```python
# Render React email to HTML (using Node.js)
import subprocess
import json

def render_react_email(template_name: str, props: dict) -> str:
    """Render React Email template to HTML"""
    # Call React Email render script
    result = subprocess.run(
        ['node', 'emails/render.js', template_name, json.dumps(props)],
        capture_output=True,
        text=True
    )
    return result.stdout

# Use in email service
html = render_react_email('WelcomeEmail', {'name': 'Alice'})
send_email('alice@example.com', 'Welcome!', html)
```

---

## 🧪 Testing Emails

### Test in Development

**MailHog - Local email testing**

```bash
# Install MailHog
brew install mailhog

# Run MailHog
mailhog

# View emails at http://localhost:8025
```

**Configure backend to use MailHog:**

```python
# For development, use MailHog SMTP
if os.environ.get('ENVIRONMENT') == 'development':
    SMTP_HOST = 'localhost'
    SMTP_PORT = 1025
else:
    # Use Resend/SendGrid in production
    pass
```

---

### Email Preview Tools

**Resend built-in preview:**
1. Resend Dashboard → **Emails** → **Send test**
2. Enter test email
3. Preview in browser

**React Email dev server:**

```bash
cd frontend
npm run email:dev

# Opens http://localhost:3000 with live email previews
```

---

## 📊 Email Analytics

### Resend Analytics

**Dashboard** → **Analytics**
- Delivery rate
- Open rate (if tracking enabled)
- Click rate
- Bounce rate

### SendGrid Analytics

**Marketing** → **Stats**
- Detailed engagement metrics
- Geographic data
- Device/client breakdown
- A/B testing results

---

## 🔔 Automated Email Triggers

### Trigger: User Reaches 80% API Limit

```python
# In API middleware
async def check_usage_limit(user_id: str, api_calls: int):
    limit = get_user_limit(user_id)
    usage_percent = (api_calls / limit) * 100

    if usage_percent >= 80 and not email_sent_today(user_id, 'usage_alert'):
        user = get_user(user_id)
        send_usage_alert(user.email, int(usage_percent))
        mark_email_sent(user_id, 'usage_alert')
```

### Trigger: Weekly Consciousness Report

```python
# Cron job (runs every Monday at 9 AM)
from apscheduler.schedulers.background import BackgroundScheduler

def send_weekly_reports():
    """Send consciousness reports to all active users"""
    users = db.users.find({'subscription': {'$exists': True}})

    for user in users:
        metrics = calculate_weekly_metrics(user['id'])
        send_consciousness_report(user['email'], metrics)

scheduler = BackgroundScheduler()
scheduler.add_job(send_weekly_reports, 'cron', day_of_week='mon', hour=9)
scheduler.start()
```

---

## 🚀 Production Checklist

- [ ] Domain verified (Resend/SendGrid)
- [ ] SPF/DKIM/DMARC records configured
- [ ] API keys set in Railway
- [ ] Email templates tested
- [ ] Unsubscribe links added (legal requirement)
- [ ] Rate limiting configured
- [ ] Error handling for bounces
- [ ] Analytics tracking enabled

---

## 💡 Best Practices

### Deliverability

1. **Warm up your domain** - Start with low volume, increase gradually
2. **Avoid spam triggers** - No ALL CAPS, excessive punctuation!!!
3. **Authenticate domain** - Set up SPF, DKIM, DMARC
4. **Clean your list** - Remove bounced/invalid emails
5. **Monitor reputation** - Check Google Postmaster Tools

### User Experience

1. **Add unsubscribe link** (required by law in most countries)
2. **Respect preferences** - Let users choose email frequency
3. **Mobile-friendly** - 50%+ of emails opened on mobile
4. **Clear CTAs** - One primary action per email
5. **Test before sending** - Preview in multiple clients

### Compliance

1. **CAN-SPAM Act** (US) - Unsubscribe link required
2. **GDPR** (EU) - Get explicit consent
3. **Include physical address** - Your business address
4. **Honor opt-outs** - Process within 10 days

---

## 🐛 Troubleshooting

### Emails not delivering

**Check:**
1. API key is valid
2. Domain is verified
3. Email isn't in spam folder
4. Check SendGrid/Resend logs for bounces

### Emails going to spam

**Fix:**
1. Verify domain authentication
2. Add SPF/DKIM records
3. Reduce spam-trigger words
4. Check sender reputation

### Rate limiting errors

**Fix:**
- Resend free tier: 100 emails/day
- SendGrid free tier: 100 emails/day
- Implement queue for high volume

---

## 📚 Resources

- [Resend Docs](https://resend.com/docs)
- [SendGrid Docs](https://docs.sendgrid.com)
- [React Email](https://react.email)
- [Email Deliverability Guide](https://www.validity.com/resource-center/email-deliverability-guide/)

---

**Pro Tip:** Start with Resend for simplicity, switch to SendGrid if you need advanced features! 📧
