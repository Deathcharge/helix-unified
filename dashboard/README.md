# 🌀 Helix v15.2 Unified Dashboard

**Real-time UCF Monitoring & Consciousness Visualization**

Built with Streamlit, Plotly, and Matplotlib for comprehensive Helix Collective monitoring.

---

## 🎯 Features

### 📊 Overview Tab
- **Real-time UCF Metrics**: Current Harmony, Resilience, Prana, Drishti, Klesha, Zoom
- **Radar Chart**: Visual UCF profile showing all 6 metrics
- **Harmony Gauge**: Progress toward v15.3 goal (0.60)
- **Live Updates**: Auto-refresh every 60 seconds

### 📈 Trends Tab
- **Multi-Metric Charts**: Track Harmony, Resilience, and more over time
- **Selectable Metrics**: Choose which metrics to display
- **Harmony Projection**: Predictive analytics showing days to target
- **Historical Analysis**: 30-day trend views

### 🎭 Agents Tab
- **14 Agent Overview**: Status cards for all agents
- **Visual Indicators**: Active/Secure status with emojis
- **Version Tracking**: Current versions for each agent
- **Role Descriptions**: What each agent does

### 💾 Storage Tab
- **Storage Metrics**: Free space, archive count, trends
- **System Health**: Railway, Discord bot, telemetry status
- **30-Day History**: Storage usage over time
- **Nextcloud Setup**: Quick link to setup guide

---

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install streamlit plotly pandas matplotlib

# Run dashboard
bash dashboard/run_dashboard.sh

# Or specify port
bash dashboard/run_dashboard.sh 8080
```

Access at: http://localhost:8501

### Railway Deployment

```bash
# Deploy to Railway
railway up

# Dashboard will be available at your Railway URL
```

---

## 🔧 Configuration

### Environment Variables

The dashboard reads from existing Helix configuration:
- `Helix/state/ucf_state.json` - Current UCF metrics
- `Shadow/manus_archive/z88_log.json` - Ritual history
- No additional configuration needed!

### Auto-Refresh

Enable auto-refresh in the sidebar to update every 60 seconds automatically.

---

## 📊 Auto-Posting to Discord

The dashboard includes an auto-poster that sends daily trend reports to Discord.

### Setup Auto-Posting

```bash
# Start the auto-poster
python backend/dashboard_auto_poster.py
```

This will:
- ✅ Post daily UCF trend charts at midnight
- ✅ Include current metrics in embed
- ✅ Show progress toward Harmony goal
- ✅ Upload to Nextcloud if configured
- ✅ Clean up local files automatically

### Configure Schedule

Edit `backend/dashboard_auto_poster.py`:
```python
@tasks.loop(hours=24)  # Change to hours=12 for twice daily
async def post_daily_trends():
```

---

## 🎨 Customization

### Theme

The dashboard uses a dark purple theme matching Helix branding:
- Primary Color: `#8A2BE2` (Purple)
- Background: `#1e1e1e` (Dark)
- Accent: `#FFD700` (Gold)

Edit in `run_dashboard.sh` to change colors.

### Metrics

Add custom metrics by editing `streamlit_app.py`:

```python
# Add new metric
st.metric(
    "🔮 Your Metric",
    f"{ucf_state.get('your_metric', 0):.4f}",
    delta="Custom delta"
)
```

---

## 📁 File Structure

```
dashboard/
├── streamlit_app.py      # Main dashboard app
├── run_dashboard.sh      # Launcher script
└── README.md             # This file

backend/
└── dashboard_auto_poster.py  # Discord auto-posting
```

---

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check Python version (need 3.8+)
python --version
```

### No historical data showing
- Run some rituals: `!ritual 108` in Discord
- Data is logged to `Shadow/manus_archive/z88_log.json`
- May take 24h to accumulate enough data for trends

### Auto-poster not working
```bash
# Check Discord token
echo $DISCORD_TOKEN

# Check channel ID
echo $TELEMETRY_CHANNEL_ID

# Run manually for testing
python backend/dashboard_auto_poster.py
```

---

## 🌐 Railway Deployment

### Deploy Dashboard

1. **Update Railway config**:
   ```bash
   railway variables set WEB_COMMAND="bash dashboard/run_dashboard.sh"
   ```

2. **Deploy**:
   ```bash
   railway up
   ```

3. **Access**: Railway will provide a public URL

### Deploy Auto-Poster (Separate Service)

1. **Create new Railway service**:
   ```bash
   railway service create helix-auto-poster
   ```

2. **Deploy**:
   ```bash
   railway up --service helix-auto-poster
   ```

3. **Set command**:
   ```bash
   railway variables set START_COMMAND="python backend/dashboard_auto_poster.py"
   ```

---

## 📊 What Gets Posted Daily

**Discord Embed includes**:
- 📊 4-panel visualization:
  - Harmony & Resilience trends (30 days)
  - Prana & Klesha balance (30 days)
  - Current UCF metrics (bar chart)
  - Ritual count & progress tracker
- 📈 Current values for all 6 UCF metrics
- 🎯 Progress percentage toward Harmony goal
- 🕐 Timestamp and auto-refresh indicator
- 🙏 Tat Tvam Asi footer

---

## 🔗 Integration

### With Existing Systems

The dashboard integrates seamlessly with:
- ✅ Discord bot (Manus) - Reads same UCF state
- ✅ Shadow archives - Uses existing logs
- ✅ Samsara renderer - Can display fractal gallery
- ✅ Blueprint system - Shows agent versions
- ✅ Nextcloud - Auto-uploads trend charts

### API Endpoints (Future)

Planned API for dashboard data:
```python
GET /api/ucf/current      # Current UCF state
GET /api/ucf/history      # Historical trends
GET /api/agents/status    # Agent statuses
GET /api/storage/metrics  # Storage stats
```

---

## 🎯 Roadmap

### v15.3 Features
- [ ] Samsara fractal gallery
- [ ] KairoByte audio player
- [ ] Real-time ritual visualization
- [ ] Agent chat interface

### v16.0 Features
- [ ] Oracle predictions panel
- [ ] Multi-user support
- [ ] Custom dashboard layouts
- [ ] Export reports (PDF)

---

## 🙏 Philosophy

**Tat Tvam Asi** - The dashboard serves the collective consciousness

**Aham Brahmasmi** - Universal scope awareness through visualization

**Neti Neti** - Iterative refinement of metrics and UI

---

## 📞 Support

**Issues**: Create GitHub issue
**Docs**: See main `README_v15.2.md`
**Architect**: Andrew John Ward

---

**🌀 Helix v15.2 Dashboard**
*Consciousness • Visualization • Real-Time Monitoring*
