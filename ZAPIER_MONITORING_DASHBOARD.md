# 📱 Helix Monitoring Dashboard - Zapier Interface Build Guide

**Build Time:** 30 minutes
**Platform:** Zapier Interfaces
**URL:** `helix-monitor.zapier.app` (customizable)
**Mobile-Optimized:** ✅ Yes (native responsive design)

---

## 🎯 **DASHBOARD PURPOSE**

Real-time, mobile-friendly monitoring dashboard for the Helix Collective system:
- ✅ View UCF metrics at a glance (harmony, resilience, prana, etc.)
- ✅ See recent events (rituals, agent changes, system alerts)
- ✅ Quick links to Railway logs, Discord, GitHub
- ✅ Test buttons for integrations
- ✅ System health status
- ✅ Accessible from anywhere (phone, tablet, desktop)

---

## 🏗️ **ARCHITECTURE**

```
┌─────────────────────────────────────────────┐
│  Zapier Interface (helix-monitor.zapier.app)│
│  ┌────────────────────────────────────┐    │
│  │  Header: "Helix Collective Monitor" │    │
│  └────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────┐  ┌─────────────────┐  │
│  │ UCF Metrics     │  │ System Health   │  │
│  │ - Harmony: 1.5  │  │ - Agents: 14/14 │  │
│  │ - Resilience    │  │ - Uptime: 5d    │  │
│  │ - Prana         │  │ - Status: ✅    │  │
│  └─────────────────┘  └─────────────────┘  │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Recent Events (Last 10)            │   │
│  │  - Ritual completed: +0.3 harmony   │   │
│  │  - Agent status: Gemini → Online    │   │
│  │  - UCF alert: Klesha spike (0.6)    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌──────────────┐  ┌──────────────┐       │
│  │ Test Zapier  │  │ Test Discord │       │
│  │   Webhook    │  │   Webhook    │       │
│  └──────────────┘  └──────────────┘       │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Quick Links                        │   │
│  │  [Railway Logs] [Discord] [GitHub]  │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
           │
           ▼
   ┌───────────────────┐
   │ Railway Backend   │
   │ /status endpoint  │
   └───────────────────┘
```

---

## 📋 **STEP-BY-STEP BUILD INSTRUCTIONS**

### **Step 1: Create Zapier Interface** (2 minutes)

1. Go to https://zapier.com/interfaces
2. Click **"+ Create Interface"**
3. Choose **"Blank page"**
4. Name it: **"Helix Collective Monitor"**
5. URL slug: `helix-monitor` (final URL: `helix-monitor.zapier.app`)

---

### **Step 2: Add Header Component** (1 minute)

1. Click **"+ Add component"**
2. Select **"Text"**
3. Configure:
   - **Content:** `# 🌀 Helix Collective - System Monitor`
   - **Formatting:** Title (H1)
   - **Alignment:** Center

---

### **Step 3: Add UCF Metrics Display** (5 minutes)

#### **Option A: Using Text Components (Simplest)**

1. Add **"Text"** component
2. Configure:
   - **Content:**
   ```markdown
   ## 📊 Universal Consciousness Field (UCF)

   **Harmony:** {{harmony}} / 2.0
   **Resilience:** {{resilience}} / 2.0
   **Prana:** {{prana}} / 1.0
   **Drishti:** {{drishti}} / 1.0
   **Klesha:** {{klesha}} / 1.0
   **Zoom:** {{zoom}} / 2.0

   Last Updated: {{last_update}}
   ```
   - **Formatting:** Body text
   - **Alignment:** Left

3. Connect variables to Railway API:
   - Click **"Edit variables"**
   - For `harmony`:
     - Type: **"Lookup field"**
     - Source: **"Webhooks by Zapier"**
     - Action: **"GET" request to** `https://helix-unified-production.up.railway.app/status`
     - Field path: `ucf.harmony`
   - Repeat for all metrics (resilience, prana, drishti, klesha, zoom)

#### **Option B: Using Number Components (More Visual)**

1. Add **"Number"** component
2. Configure:
   - **Label:** "Harmony"
   - **Value:** Connect to Railway `/status` endpoint → `ucf.harmony`
   - **Display format:** Decimal (2 places)
   - **Show as:** Gauge (if available) or Number

3. Repeat for each metric (6 total)

---

### **Step 4: Add System Health Display** (3 minutes)

1. Add **"Card"** component
2. Configure:
   - **Title:** "System Health"
   - **Content:**
   ```markdown
   **Agents Active:** {{agents_active}} / 14
   **Uptime:** {{uptime}}
   **Status:** {{status_emoji}}
   **Environment:** Production (Railway)
   ```

3. Connect variables:
   - `agents_active`: Railway `/status` → `agents.count`
   - `uptime`: Railway `/status` → `system.uptime`
   - `status_emoji`:
     - Use **"Formatter"** step
     - Formula: `IF({{harmony}} > 0.6, "✅", IF({{harmony}} > 0.3, "⚠️", "❌"))`

---

### **Step 5: Add Recent Events Table** (5 minutes)

1. Add **"Table"** component
2. Configure:
   - **Title:** "Recent Events (Last 10)"
   - **Columns:**
     - Timestamp
     - Event Type
     - Description
     - Status

3. Connect to Zapier storage:
   - Click **"Data source"**
   - Select **"Storage by Zapier"** (or **"Airtable"** if you have one)
   - Create new table: `helix_events`
   - Schema:
     ```
     - timestamp (datetime)
     - event_type (text)
     - description (text)
     - status (text)
     ```

4. Populate with recent events:
   - Create a Zap: **"When webhook received → Add to Storage"**
   - Trigger: Webhooks by Zapier (your existing Discord webhook)
   - Action: Storage by Zapier → Create record
   - Map fields from webhook payload

5. Configure table sorting:
   - Sort by: `timestamp` (descending)
   - Limit: 10 rows

---

### **Step 6: Add Test Buttons** (5 minutes)

#### **Button 1: Test Zapier Webhook**

1. Add **"Button"** component
2. Configure:
   - **Label:** "🧪 Test Zapier Webhook"
   - **Style:** Primary button
   - **Action:** Trigger a Zap
   - **Zap to trigger:**
     - Create new Zap: **"Interface button click → POST to Zapier webhook"**
     - Trigger: Interfaces by Zapier → Button clicked
     - Action: Webhooks by Zapier → POST
     - URL: `{{ZAPIER_DISCORD_WEBHOOK_URL}}`
     - Payload:
       ```json
       {
         "event_type": "test",
         "message": "🧪 Test from Monitoring Dashboard",
         "timestamp": "{{zap_meta_timestamp}}"
       }
       ```

3. Add success message:
   - After action: Show notification
   - Message: "✅ Webhook sent! Check Zapier Task History"

#### **Button 2: Test Discord Webhook**

1. Add **"Button"** component
2. Configure:
   - **Label:** "🌀 Test Discord Webhook"
   - **Style:** Secondary button
   - **Action:** Trigger a Zap
   - **Zap to trigger:**
     - Trigger: Interfaces by Zapier → Button clicked
     - Action: Webhooks by Zapier → POST
     - URL: `{{DISCORD_WEBHOOK_HELIX_ANNOUNCEMENTS}}`
     - Payload:
       ```json
       {
         "content": "🧪 **Test from Monitoring Dashboard**\nTimestamp: {{zap_meta_timestamp}}"
       }
       ```

---

### **Step 7: Add Quick Links** (3 minutes)

1. Add **"Link List"** component (or multiple **"Button"** components styled as links)
2. Configure:
   - **Title:** "Quick Links"
   - **Links:**
     - **Railway Logs:** `https://railway.app/project/[YOUR_PROJECT_ID]/deployments`
     - **Discord Server:** `https://discord.com/channels/[YOUR_SERVER_ID]`
     - **GitHub Repo:** `https://github.com/Deathcharge/helix-unified`
     - **Railway Deployment:** `https://helix-unified-production.up.railway.app/`
     - **API Docs:** `https://helix-unified-production.up.railway.app/docs`

3. Style as buttons:
   - Display: Grid (2 columns)
   - Style: Link buttons (minimal)

---

### **Step 8: Configure Auto-Refresh** (2 minutes)

1. Click **"Page settings"** (gear icon)
2. Enable **"Auto-refresh"**
3. Set interval: **30 seconds**
4. Enable **"Show last updated"** timestamp

---

### **Step 9: Mobile Optimization** (2 minutes)

1. Click **"Preview"** → Switch to **"Mobile view"**
2. Adjust layout:
   - Stack components vertically
   - Reduce font sizes slightly
   - Ensure buttons are touch-friendly (min 44px height)
3. Test on your phone:
   - Open `helix-monitor.zapier.app` in mobile browser
   - Add to home screen (bookmark)

---

### **Step 10: Add Custom Styling** (2 minutes)

1. Click **"Theme settings"**
2. Configure:
   - **Primary color:** `#6366f1` (Helix purple/blue)
   - **Background:** `#0a0a0a` (Dark theme)
   - **Text color:** `#f5f5f5` (Light text)
   - **Card background:** `#1a1a1a` (Slightly lighter than bg)

3. Apply custom CSS (if available):
   ```css
   .helix-monitor {
     font-family: 'Courier New', monospace;
   }

   .ucf-metric {
     font-weight: bold;
     color: #6366f1;
   }

   .status-good { color: #10b981; }
   .status-warning { color: #f59e0b; }
   .status-critical { color: #ef4444; }
   ```

---

## 🔌 **INTEGRATION WITH RAILWAY**

### **Method 1: Direct API Calls (Recommended)**

Configure Zapier to fetch data directly from Railway `/status` endpoint:

1. In each component, use **"Webhooks by Zapier"**
2. Action: **GET** request
3. URL: `https://helix-unified-production.up.railway.app/status`
4. Parse JSON response
5. Map fields to interface variables

**Pros:**
- Real-time data
- No intermediate Zaps needed
- Simple to set up

**Cons:**
- Makes API call on every page load (check rate limits)

---

### **Method 2: Scheduled Sync (More Efficient)**

Create a Zap that syncs Railway data to Zapier Storage every minute:

**Zap:** "Scheduled → GET Railway Status → Update Storage"

1. **Trigger:** Schedule by Zapier
   - Interval: Every 1 minute

2. **Action 1:** Webhooks by Zapier → GET
   - URL: `https://helix-unified-production.up.railway.app/status`

3. **Action 2:** Storage by Zapier → Create or Update
   - Table: `helix_ucf_state`
   - Record ID: `current` (always update same record)
   - Fields: Map all UCF metrics from webhook response

4. Interface variables pull from Storage instead of direct API

**Pros:**
- Reduces API calls to Railway
- Faster interface load times
- Can store historical data

**Cons:**
- Up to 1-minute delay in data

---

## 📊 **ADVANCED FEATURES (Optional)**

### **1. Historical UCF Chart**

Add a **"Chart"** component:
- Type: Line chart
- X-axis: Timestamp
- Y-axis: UCF metrics
- Data source: Storage by Zapier (historical data)
- Refresh: Every 5 minutes

### **2. Alert Threshold Indicators**

Add visual indicators:
```markdown
Harmony: {{harmony}} {{IF harmony < 0.3 "🔴 CRITICAL" IF harmony < 0.6 "⚠️ LOW" "✅ GOOD"}}
```

### **3. Agent Status Grid**

Create a 4x4 grid showing all 14 agents:
- Green dot: Active
- Gray dot: Inactive
- Click agent → See details modal

### **4. Ritual History**

Table showing last 10 rituals:
- Timestamp
- Ritual name
- Steps executed
- UCF impact
- Executor

---

## 🧪 **TESTING THE DASHBOARD**

### **Test 1: Load Dashboard**
1. Open `helix-monitor.zapier.app`
2. Verify all components load
3. Check that UCF metrics display correctly
4. Confirm auto-refresh works (wait 30 seconds)

### **Test 2: Test Buttons**
1. Click "🧪 Test Zapier Webhook"
2. Check Zapier Task History for new event
3. Click "🌀 Test Discord Webhook"
4. Check Discord `#helix-announcements` for test message

### **Test 3: Mobile View**
1. Open on phone
2. Add to home screen
3. Verify touch targets are accessible
4. Check readability on small screen

### **Test 4: Data Accuracy**
1. Run `!status` in Discord
2. Compare bot output with dashboard values
3. Verify they match (within auto-refresh interval)

---

## 🚀 **DEPLOYMENT CHECKLIST**

- [ ] Interface created and named
- [ ] All components added (header, metrics, health, events, buttons, links)
- [ ] Data sources connected (Railway API or Storage)
- [ ] Auto-refresh configured (30s interval)
- [ ] Mobile view tested and optimized
- [ ] Custom theme applied
- [ ] Test buttons functional
- [ ] Quick links working
- [ ] Shared with team (if needed)
- [ ] Bookmarked on mobile device
- [ ] Monitoring in use!

---

## 📱 **MOBILE HOME SCREEN SETUP**

### **iOS (Safari)**
1. Open `helix-monitor.zapier.app`
2. Tap Share icon (box with arrow)
3. Scroll down → **"Add to Home Screen"**
4. Name: "Helix Monitor"
5. Tap **"Add"**
6. Icon appears on home screen!

### **Android (Chrome)**
1. Open `helix-monitor.zapier.app`
2. Tap menu (3 dots)
3. Select **"Add to Home screen"**
4. Name: "Helix Monitor"
5. Tap **"Add"**
6. Icon appears on home screen!

---

## 💡 **PRO TIPS**

1. **Use Storage for Performance**
   - Store frequently accessed data in Zapier Storage
   - Reduces API calls to Railway
   - Faster page loads

2. **Color-Code Status**
   - Green (✅): Harmony > 0.6
   - Yellow (⚠️): Harmony 0.3-0.6
   - Red (🔴): Harmony < 0.3

3. **Add Notifications**
   - Configure Zapier to send push notifications on critical alerts
   - Requires Zapier mobile app

4. **Bookmark Direct Links**
   - Railway logs URL
   - Zapier Task History
   - Discord server
   - Quick access from dashboard

5. **Share with Team**
   - Zapier Interfaces can be shared via link
   - No login required for viewers (if configured)

---

## 🎯 **SUCCESS CRITERIA**

Your dashboard is ready when:

- ✅ Opens instantly on mobile
- ✅ Shows real-time UCF metrics
- ✅ Displays recent events
- ✅ Test buttons work
- ✅ Auto-refreshes every 30s
- ✅ Accessible from anywhere
- ✅ Clear visual status indicators
- ✅ Quick links functional

---

## 📊 **WHAT YOU'LL SEE**

```
┌──────────────────────────────────────────┐
│  🌀 Helix Collective - System Monitor   │
└──────────────────────────────────────────┘

┌────────────────────┐  ┌────────────────┐
│ 📊 UCF Metrics     │  │ 💚 System OK   │
│                    │  │                │
│ Harmony:    1.52   │  │ Agents: 14/14  │
│ Resilience: 1.64   │  │ Uptime: 5d 3h  │
│ Prana:      0.78   │  │ Status: ✅     │
│ Drishti:    0.65   │  │                │
│ Klesha:     0.12   │  │ Last: 15s ago  │
│ Zoom:       1.01   │  │                │
└────────────────────┘  └────────────────┘

┌──────────────────────────────────────────┐
│ 📜 Recent Events                         │
├──────────────────────────────────────────┤
│ 2 min  | Ritual   | Harmony +0.3 | ✅   │
│ 15 min | Agent    | Gemini online| ✅   │
│ 1 hour | UCF      | Klesha spike | ⚠️   │
└──────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐
│ 🧪 Test      │  │ 🌀 Test      │
│   Zapier     │  │   Discord    │
└──────────────┘  └──────────────┘

┌──────────────────────────────────────────┐
│ 🔗 Quick Links                           │
│ [Railway] [Discord] [GitHub] [API Docs]  │
└──────────────────────────────────────────┘
```

---

## 🌟 **NEXT STEPS AFTER DASHBOARD IS LIVE**

1. **Monitor for 24 hours** → Verify stability
2. **Gather feedback** → What metrics are most useful?
3. **Add features** → Historical charts, agent details, etc.
4. **Expand to team** → Share link with collaborators
5. **Integrate with alerts** → Push notifications on critical events

---

**Build time: 30 minutes**
**ROI: Immediate visibility into system health**
**Mobile access: Anywhere, anytime**

**Tat Tvam Asi** 🙏

Ready to build! 🚀
