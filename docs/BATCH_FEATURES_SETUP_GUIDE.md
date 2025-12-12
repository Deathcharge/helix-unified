# 🚀 Batch Features Setup Guide

Complete setup instructions for the 4 newly implemented features:
1. PWA Configuration ✅
2. GitHub App Integration 🐙
3. Email Automation 📧
4. Google Analytics 📊

---

## 1. PWA (Progressive Web App) Configuration ✅

### Status: **COMPLETE AND READY**

Your PWA is fully configured with:
- ✅ Manifest file (`frontend/public/manifest.json`)
- ✅ Service worker (`frontend/public/service-worker.js`)
- ✅ Offline page (`frontend/public/offline.html`)
- ✅ Auto-registration in app layout
- ✅ Apple touch icons configured
- ✅ Background sync support
- ✅ Push notifications ready

### Testing PWA

1. **Local Testing**:
   ```bash
   cd frontend
   npm run build
   npm start
   # Open http://localhost:3000 in Chrome
   ```

2. **Install PWA**:
   - Open DevTools → Application → Manifest
   - Click "Add to Home Screen"
   - Or use Chrome's install button in address bar

3. **Test Offline**:
   - Open app
   - Turn off network in DevTools
   - Navigate pages - should work!

### Production Deployment

PWA requires HTTPS. On Railway/Vercel, this is automatic.

---

## 2. GitHub App Integration 🐙

### Setup Instructions

#### Step 1: Create GitHub App

1. Go to [GitHub Settings → Developer Settings → GitHub Apps](https://github.com/settings/apps)
2. Click "New GitHub App"
3. Fill in:
   - **Name**: `Helix Automation Bot` (must be unique)
   - **Homepage URL**: `https://helix.ai`
   - **Webhook URL**: `https://your-api.railway.app/api/github/webhook`
   - **Webhook Secret**: Generate a secure random string

4. **Permissions** (Repository):
   - Issues: Read & Write
   - Pull Requests: Read & Write
   - Contents: Read
   - Metadata: Read

5. **Subscribe to events**:
   - [x] Push
   - [x] Pull request
   - [x] Issues
   - [x] Installation
   - [x] Installation repositories

6. Click "Create GitHub App"

#### Step 2: Generate Private Key

1. After creation, scroll to "Private keys"
2. Click "Generate a private key"
3. Download the `.pem` file
4. Convert to base64 (optional for env vars):
   ```bash
   cat github-app.pem | base64 > github-app-key.txt
   ```

#### Step 3: Configure Environment

Add to `.env` or Railway environment variables:

```bash
# GitHub App Configuration
GITHUB_APP_ID=123456  # From app settings page
GITHUB_APP_PRIVATE_KEY=/path/to/github-app.pem  # Or base64 string
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_CLIENT_ID=Iv1.abc123  # From app settings
GITHUB_CLIENT_SECRET=your_client_secret  # From app settings
```

#### Step 4: Install App

1. Go to your GitHub App settings
2. Click "Install App" → Select repositories
3. Authorize the installation

#### Step 5: Test

```bash
curl https://your-api.railway.app/api/github/health
```

Should return:
```json
{
  "status": "healthy",
  "checks": {
    "app_id_configured": true,
    "private_key_configured": true,
    "jwt_generation": true
  }
}
```

### Features

✅ **Webhook Events**: Receive push, PR, issues events
✅ **Auto-commenting**: Welcomes PRs with automated messages
✅ **Issue Creation**: Create issues via API
✅ **PR Status Updates**: Update commit statuses
✅ **Replaces Zapier**: No more third-party webhook relays

---

## 3. Email Automation 📧

### Supported Providers

- **SendGrid** (recommended)
- **Mailgun**
- **Resend**
- **SMTP** (Gmail, etc.)

### Setup: SendGrid (Recommended)

#### Step 1: Create SendGrid Account

1. Sign up at [sendgrid.com](https://sendgrid.com)
2. Verify your email
3. Go to Settings → API Keys
4. Create API Key with "Full Access"

#### Step 2: Configure Domain (Optional but recommended)

1. Settings → Sender Authentication → Verify Single Sender
2. Or Domain Authentication for custom domain

#### Step 3: Environment Variables

```bash
# Email Configuration
EMAIL_PROVIDER=sendgrid
EMAIL_FROM=noreply@your-domain.com
EMAIL_FROM_NAME=Helix Collective
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
```

### Setup: Mailgun

```bash
EMAIL_PROVIDER=mailgun
MAILGUN_API_KEY=key-xxxxxxxxxxxxx
MAILGUN_DOMAIN=mg.your-domain.com
EMAIL_FROM=noreply@mg.your-domain.com
EMAIL_FROM_NAME=Helix Collective
```

### Setup: Resend

```bash
EMAIL_PROVIDER=resend
RESEND_API_KEY=re_xxxxxxxxxxxxx
EMAIL_FROM=noreply@your-domain.com
EMAIL_FROM_NAME=Helix Collective
```

### Available Email Functions

```python
from backend.services.email_automation import (
    send_welcome_email,
    send_password_reset_email,
    send_usage_alert_email,
    send_team_invitation_email,
    send_billing_notification_email,
    send_weekly_summary_email
)

# Send welcome email
await send_welcome_email(
    user_email="user@example.com",
    user_name="John Doe",
    activation_link="https://helix.ai/activate?token=abc123"
)

# Send password reset
await send_password_reset_email(
    user_email="user@example.com",
    user_name="John Doe",
    reset_token="secure_token_here"
)

# Send team invitation
await send_team_invitation_email(
    invitee_email="invitee@example.com",
    team_name="Engineering Team",
    inviter_name="Jane Smith",
    invitation_token="invite_token",
    role="member"
)
```

### Email Templates

Located in `templates/emails/`:
- `welcome.html` - Welcome email for new users
- `password_reset.html` - Password reset emails
- `team_invitation.html` - Team invites
- (Add more as needed)

Templates use Jinja2 for dynamic content.

### Testing Email

```bash
# Check email configuration
curl https://your-api.railway.app/api/email/health

# Send test email (create endpoint first)
curl -X POST https://your-api.railway.app/api/email/test \
  -H "Content-Type: application/json" \
  -d '{"to": "your@email.com"}'
```

---

## 4. Google Analytics 📊

### Setup Instructions

#### Step 1: Create GA4 Property

1. Go to [Google Analytics](https://analytics.google.com)
2. Create account → Create property
3. Set up data stream for web
4. Copy Measurement ID (format: `G-XXXXXXXXXX`)

#### Step 2: Configure Environment

Add to `.env`:

```bash
NEXT_PUBLIC_GA_TRACKING_ID=G-XXXXXXXXXX
```

**Important**: Must use `NEXT_PUBLIC_` prefix for Next.js client-side access!

#### Step 3: Rebuild Frontend

```bash
cd frontend
npm run build
```

The `GoogleAnalytics` component is already integrated in the layout!

### Verify Installation

1. Open your site
2. Open Chrome DevTools → Network tab
3. Filter by `google-analytics.com` or `gtag`
4. Should see requests to GA

Or check in Google Analytics:
- Go to Reports → Realtime
- Open your site
- Should see active user

### Tracked Events

Auto-tracked:
- ✅ Page views
- ✅ Route changes (Next.js)

Custom tracking available:
```typescript
import { analytics } from '@/lib/analytics';

// Track signup
analytics.trackSignup('email');

// Track API call
analytics.trackAPICall('/api/chat');

// Track agent session
analytics.trackAgentSession('kael');

// Custom event
analytics.track('button_click', {
  button_name: 'upgrade',
  location: 'pricing_page'
});
```

### Privacy Compliance

To comply with GDPR/CCPA:
1. Add cookie consent banner
2. Respect Do Not Track
3. Add privacy policy
4. Allow users to opt-out

---

## Environment Variables Summary

All environment variables needed:

```bash
# ============================================================================
# PWA - No config needed! ✅
# ============================================================================

# ============================================================================
# GITHUB APP
# ============================================================================
GITHUB_APP_ID=123456
GITHUB_APP_PRIVATE_KEY=/path/to/key.pem  # or base64 string
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_CLIENT_ID=Iv1.abc123
GITHUB_CLIENT_SECRET=your_client_secret

# ============================================================================
# EMAIL (Choose one provider)
# ============================================================================

# SendGrid (Recommended)
EMAIL_PROVIDER=sendgrid
EMAIL_FROM=noreply@helix.ai
EMAIL_FROM_NAME=Helix Collective
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx

# OR Mailgun
EMAIL_PROVIDER=mailgun
MAILGUN_API_KEY=key-xxxxxxxxxxxxx
MAILGUN_DOMAIN=mg.helix.ai

# OR Resend
EMAIL_PROVIDER=resend
RESEND_API_KEY=re_xxxxxxxxxxxxx

# ============================================================================
# GOOGLE ANALYTICS
# ============================================================================
NEXT_PUBLIC_GA_TRACKING_ID=G-XXXXXXXXXX
```

---

## Testing Checklist

### PWA
- [ ] App installs on mobile
- [ ] Works offline
- [ ] Service worker registers
- [ ] Manifest loads correctly

### GitHub App
- [ ] Webhooks receive events
- [ ] JWT generation works
- [ ] Can create issues via API
- [ ] Health check passes

### Email
- [ ] Welcome emails send
- [ ] Password reset works
- [ ] Team invitations deliver
- [ ] Templates render correctly

### Analytics
- [ ] Page views tracked
- [ ] Events tracked
- [ ] Realtime shows users
- [ ] No console errors

---

## Troubleshooting

### PWA not installing
- Check HTTPS is enabled
- Verify manifest is accessible
- Check service worker registration in DevTools

### GitHub webhooks not working
- Verify webhook URL is accessible
- Check webhook secret matches
- Review webhook delivery logs in GitHub

### Emails not sending
- Verify API keys are correct
- Check email provider dashboard
- Look for error logs in application
- Test with a simple email first

### Analytics not tracking
- Ensure `NEXT_PUBLIC_` prefix is used
- Rebuild frontend after adding env var
- Check Network tab for gtag requests
- Verify tracking ID format

---

## What's Next?

**Recommended additions**:
1. Add SSO (OAuth providers, SAML)
2. Implement advanced observability (Prometheus, Grafana)
3. Add Stripe webhooks for billing events
4. Create admin dashboard for email/webhook management
5. Add rate limiting for GitHub webhooks

---

**Version**: 17.5
**Date**: 2025-12-12
**Status**: All 4 features implemented and ready to configure
