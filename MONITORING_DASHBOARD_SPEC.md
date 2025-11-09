# 📊 Helix Collective - Lightweight Monitoring Dashboard

**Purpose:** Real-time system health monitoring accessible from any device (especially mobile)

---

## Option A: Zapier Interface (Fastest - 30 minutes)

**Advantages:**
- No deployment needed
- Mobile-optimized by default
- Built-in form handling
- Free on your existing Zapier plan

**What it displays:**
- Latest UCF metrics (pulled from Railway `/status` endpoint)
- Last 10 events from webhook history
- Quick links to Railway logs, Discord server
- "Panic button" to trigger diagnostic ritual

**Implementation:**
1. Create Zapier Interface at `helix-monitor.zapier.app`
2. Add widgets:
   - **Text Widget** - UCF Harmony meter
   - **Table Widget** - Recent events
   - **Button Widget** - Trigger test webhook
   - **Link Widgets** - Quick navigation
3. Connect to Railway API using Webhooks by Zapier
4. Refresh interval: 30 seconds

**Build Time:** ~30 minutes
**Mobile-Friendly:** ✅ Yes
**Cost:** $0 (included in Zapier plan)

---

## Option B: Streamlit App (1-2 hours)

**Advantages:**
- Full Python control
- Rich visualizations (Plotly charts)
- Can run diagnostic queries
- Customizable layout

**What it displays:**
- Real-time UCF metrics with historical charts
- Agent status grid (14 agents)
- Recent ritual completions
- System logs tail
- Environment variable status
- Test buttons for each integration

**Tech Stack:**
- Streamlit (already in your stack)
- Plotly for charts
- Requests for API calls
- Deploy to Streamlit Community Cloud

**Implementation:**
```python
# dashboard.py
import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Helix Monitor", layout="wide")

# Fetch UCF state
ucf = requests.get("https://helix-unified-production.up.railway.app/status").json()

# Display harmony meter
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = ucf['harmony'],
    title = {'text': "Harmony"},
    gauge = {'axis': {'range': [None, 2.0]}}
))
st.plotly_chart(fig)

# Agent status
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Agents Active", ucf['agents_active'])
with col2:
    st.metric("Resilience", ucf['resilience'])
with col3:
    st.metric("Prana", ucf['prana'])

# Test buttons
if st.button("🧪 Test Zapier Webhook"):
    response = requests.post(
        st.secrets["ZAPIER_WEBHOOK_URL"],
        json={"event_type": "test", "message": "Dashboard test"}
    )
    st.success(f"Webhook sent! Status: {response.status_code}")
```

**Build Time:** 1-2 hours
**Mobile-Friendly:** ✅ Yes (Streamlit is responsive)
**Cost:** $0 (Streamlit Community Cloud is free)

---

## Recommended: **Option A (Zapier Interface)**

**Why:**
- You can have it running in 30 minutes
- Perfect for mobile monitoring
- No deployment/hosting needed
- Integrates seamlessly with your existing Zapier workflows

We can always build Option B later for more advanced analytics.

---

## 2. 📱 Mobile Access

Both options provide **native mobile access**:
- Zapier Interface: Optimized for mobile browsers
- Streamlit: Responsive design, works on any device

**Bookmark the URL on your phone's home screen** for instant access!

---

## Next Steps

1. Choose Option A or B
2. I'll build the prototype (30 min - 2 hours)
3. Test on your phone
4. Iterate based on your feedback
5. Add more widgets/features as needed

Which option do you prefer? 🎯
