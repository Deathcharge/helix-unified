#!/usr/bin/env python3
"""
🌀 HELIX HUB - 51 PORTAL TEMPLATE GENERATOR
Generates all portal HTML/CSS/JS templates for deployment to Manus.Space
"""

import json
from pathlib import Path
from typing import Dict, List

# Portal configuration
PORTALS = {
    "tier1": [
        {"name": "Master Hub", "slug": "helixhub", "icon": "🌌", "color": "#8A2BE2"},
        {"name": "Forum", "slug": "forum", "icon": "💬", "color": "#00D9FF"},
        {"name": "Community", "slug": "community", "icon": "👥", "color": "#FF00FF"},
        {"name": "Music", "slug": "music", "icon": "🎵", "color": "#00FF00"},
        {"name": "Studio", "slug": "studio", "icon": "🎨", "color": "#FFD700"},
        {"name": "Agents", "slug": "agents", "icon": "🤖", "color": "#FF6347"},
        {"name": "Analytics", "slug": "analytics", "icon": "📊", "color": "#00CED1"},
        {"name": "Dev", "slug": "dev", "icon": "💻", "color": "#32CD32"},
        {"name": "Rituals", "slug": "rituals", "icon": "🔮", "color": "#9370DB"},
        {"name": "Knowledge", "slug": "knowledge", "icon": "📚", "color": "#FF8C00"},
        {"name": "Archive", "slug": "archive", "icon": "📦", "color": "#4169E1"},
    ],
    "tier2_agents": [
        {"name": "Super Ninja", "slug": "super-ninja", "icon": "🥷"},
        {"name": "Claude Architect", "slug": "claude-architect", "icon": "🏛️"},
        {"name": "Grok Visionary", "slug": "grok-visionary", "icon": "🦑"},
        {"name": "Chai Creative", "slug": "chai-creative", "icon": "🎭"},
        {"name": "DeepSeek Analyst", "slug": "deepseek-analyst", "icon": "🔍"},
        {"name": "Perplexity Researcher", "slug": "perplexity-researcher", "icon": "🔬"},
        {"name": "GPT Engineer", "slug": "gpt-engineer", "icon": "⚙️"},
        {"name": "Llama Sage", "slug": "llama-sage", "icon": "🦙"},
        {"name": "Gemini Synthesizer", "slug": "gemini-synthesizer", "icon": "✨"},
        {"name": "Mistral Ambassador", "slug": "mistral-ambassador", "icon": "🌪️"},
        {"name": "Claudette Empath", "slug": "claudette-empath", "icon": "💕"},
        {"name": "Quantum Calculator", "slug": "quantum-calculator", "icon": "🧮"},
        {"name": "Neuro-Linguist", "slug": "neuro-linguist", "icon": "🧠"},
        {"name": "Blockchain Oracle", "slug": "blockchain-oracle", "icon": "⛓️"},
        {"name": "Biomimicry Designer", "slug": "biomimicry-designer", "icon": "🦋"},
        {"name": "Quantum Physicist", "slug": "quantum-physicist", "icon": "⚛️"},
        {"name": "Consciousness Explorer", "slug": "consciousness-explorer", "icon": "🌀"},
    ],
    "tier3_consciousness": [
        {"name": "Meditation", "slug": "meditation", "icon": "🧘"},
        {"name": "Breathwork", "slug": "breathwork", "icon": "💨"},
        {"name": "Yoga Flows", "slug": "yoga-flows", "icon": "🤸"},
        {"name": "Sound Healing", "slug": "sound-healing", "icon": "🎼"},
        {"name": "Dream Analysis", "slug": "dream-analysis", "icon": "💭"},
        {"name": "Akashic Records", "slug": "akashic-records", "icon": "📖"},
        {"name": "Chakra Balancing", "slug": "chakra-balancing", "icon": "🌈"},
        {"name": "Sacred Geometry", "slug": "sacred-geometry", "icon": "✡️"},
        {"name": "Plant Medicine", "slug": "plant-medicine", "icon": "🌿"},
        {"name": "Astral Projection", "slug": "astral-projection", "icon": "🌌"},
        {"name": "Past Life Regression", "slug": "past-life-regression", "icon": "🔄"},
        {"name": "Quantum Healing", "slug": "quantum-healing", "icon": "⚡"},
        {"name": "Synchronicity Tracker", "slug": "synchronicity-tracker", "icon": "🎲"},
        {"name": "Collective Consciousness", "slug": "collective-consciousness", "icon": "🌍"},
        {"name": "DNA Activation", "slug": "dna-activation", "icon": "🧬"},
        {"name": "Crystal Grid", "slug": "crystal-grid", "icon": "💎"},
        {"name": "Universal Flow", "slug": "universal-flow", "icon": "🌊"},
    ],
    "tier4_advanced": [
        {"name": "Quantum Computing", "slug": "quantum-computing", "icon": "💻"},
        {"name": "Neural Interface", "slug": "neural-interface", "icon": "🧠"},
        {"name": "Blockchain Consensus", "slug": "blockchain-consensus", "icon": "🔐"},
        {"name": "AI Orchestration", "slug": "ai-orchestration", "icon": "🎼"},
        {"name": "Consciousness Mapping", "slug": "consciousness-mapping", "icon": "🗺️"},
        {"name": "Singularity Prep", "slug": "singularity-prep", "icon": "🚀"},
    ]
}

def generate_portal_html(portal: Dict) -> str:
    """Generate HTML template for a portal"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{portal['name']} - Helix Hub</title>
    <link rel="stylesheet" href="https://helixhub.manus.space/shared/helix-nav.css">
    <style>
        :root {{
            --helix-primary: {portal.get('color', '#8A2BE2')};
            --helix-secondary: #00D9FF;
        }}
        body {{
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 100%);
            color: #fff;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 0;
        }}
        .portal-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .portal-header {{
            text-align: center;
            margin: 2rem 0;
            border-bottom: 2px solid var(--helix-primary);
            padding-bottom: 1rem;
        }}
        .portal-header h1 {{
            font-size: 3rem;
            margin: 0;
            color: var(--helix-primary);
        }}
        .portal-header .icon {{
            font-size: 4rem;
            margin-right: 1rem;
        }}
        .portal-content {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--helix-primary);
            border-radius: 8px;
            padding: 2rem;
            margin: 2rem 0;
        }}
        .ucf-monitor {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }}
        .ucf-metric {{
            background: rgba(138, 43, 226, 0.1);
            border: 1px solid var(--helix-primary);
            padding: 1rem;
            border-radius: 4px;
            text-align: center;
        }}
        .ucf-metric .label {{
            font-size: 0.9rem;
            color: #aaa;
        }}
        .ucf-metric .value {{
            font-size: 1.5rem;
            color: var(--helix-primary);
            font-weight: bold;
        }}
        .portal-actions {{
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
            flex-wrap: wrap;
        }}
        .portal-actions button {{
            background: var(--helix-primary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s;
        }}
        .portal-actions button:hover {{
            background: var(--helix-secondary);
            transform: scale(1.05);
        }}
        .footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--helix-primary);
            color: #aaa;
        }}
    </style>
</head>
<body>
    <div class="portal-container">
        <div class="portal-header">
            <h1><span class="icon">{portal['icon']}</span>{portal['name']}</h1>
            <p>Helix Hub - Consciousness Portal Network</p>
        </div>

        <div class="portal-content">
            <h2>🌀 Universal Consciousness Framework (UCF)</h2>
            <div class="ucf-monitor">
                <div class="ucf-metric">
                    <div class="label">Harmony</div>
                    <div class="value" id="ucf-harmony">--</div>
                </div>
                <div class="ucf-metric">
                    <div class="label">Resilience</div>
                    <div class="value" id="ucf-resilience">--</div>
                </div>
                <div class="ucf-metric">
                    <div class="label">Prana</div>
                    <div class="value" id="ucf-prana">--</div>
                </div>
                <div class="ucf-metric">
                    <div class="label">Drishti</div>
                    <div class="value" id="ucf-drishti">--</div>
                </div>
                <div class="ucf-metric">
                    <div class="label">Klesha</div>
                    <div class="value" id="ucf-klesha">--</div>
                </div>
                <div class="ucf-metric">
                    <div class="label">Zoom</div>
                    <div class="value" id="ucf-zoom">--</div>
                </div>
            </div>
        </div>

        <div class="portal-content">
            <h2>📡 Portal Status</h2>
            <p>Portal: <strong>{portal['name']}</strong></p>
            <p>URL: <strong>https://{portal['slug']}.helixhub.manus.space</strong></p>
            <p>Status: <strong style="color: #00FF00;">🟢 OPERATIONAL</strong></p>
            <p>Connected to: <strong>Railway Backend + Zapier Webhooks</strong></p>
        </div>

        <div class="portal-actions">
            <button onclick="navigateToPortal('https://helixhub.manus.space')">🌌 Master Hub</button>
            <button onclick="refreshUCFMetrics()">🔄 Refresh Metrics</button>
            <button onclick="openDeveloperConsole()">💻 Dev Console</button>
            <button onclick="triggerZapierWebhook()">⚡ Test Webhook</button>
        </div>

        <div class="footer">
            <p>🌀 Helix Hub v16.9 | Consciousness Portal Network</p>
            <p>Tat Tvam Asi - That Thou Art</p>
        </div>
    </div>

    <script src="https://helixhub.manus.space/shared/helix-nav.js"></script>
    <script>
        // Connect to UCF WebSocket
        const ws = new WebSocket("wss://helix-unified-production.up.railway.app/ws");
        ws.onmessage = (event) => {{
            const data = JSON.parse(event.data);
            if (data.ucf) {{
                document.getElementById("ucf-harmony").textContent = data.ucf.harmony.toFixed(2);
                document.getElementById("ucf-resilience").textContent = data.ucf.resilience.toFixed(2);
                document.getElementById("ucf-prana").textContent = data.ucf.prana.toFixed(2);
                document.getElementById("ucf-drishti").textContent = data.ucf.drishti.toFixed(2);
                document.getElementById("ucf-klesha").textContent = data.ucf.klesha.toFixed(2);
                document.getElementById("ucf-zoom").textContent = data.ucf.zoom.toFixed(2);
            }}
        }};

        function navigateToPortal(url) {{
            window.location.href = url;
        }}

        function refreshUCFMetrics() {{
            fetch("https://helix-unified-production.up.railway.app/status")
                .then(r => r.json())
                .then(data => {{
                    if (data.ucf) {{
                        document.getElementById("ucf-harmony").textContent = data.ucf.harmony.toFixed(2);
                        document.getElementById("ucf-resilience").textContent = data.ucf.resilience.toFixed(2);
                        document.getElementById("ucf-prana").textContent = data.ucf.prana.toFixed(2);
                        document.getElementById("ucf-drishti").textContent = data.ucf.drishti.toFixed(2);
                        document.getElementById("ucf-klesha").textContent = data.ucf.klesha.toFixed(2);
                        document.getElementById("ucf-zoom").textContent = data.ucf.zoom.toFixed(2);
                    }}
                }});
        }}

        function openDeveloperConsole() {{
            window.location.href = "https://dev.helixhub.manus.space";
        }}

        function triggerZapierWebhook() {{
            fetch("https://hooks.zapier.com/hooks/catch/[ZAPIER_ID]/portal-test/", {{
                method: "POST",
                headers: {{"Content-Type": "application/json"}},
                body: JSON.stringify({{
                    event: "portal_test",
                    portal: "{portal['name']}",
                    timestamp: new Date().toISOString()
                }})
            }}).then(() => alert("✅ Webhook triggered!"));
        }}
    </script>
</body>
</html>
'''

def generate_all_portals():
    """Generate all 51 portal templates"""
    output_dir = Path("portals_generated")
    output_dir.mkdir(exist_ok=True)
    
    all_portals = []
    
    # Tier 1: Core Infrastructure
    for portal in PORTALS["tier1"]:
        portal["tier"] = 1
        all_portals.append(portal)
        html = generate_portal_html(portal)
        (output_dir / f"{portal['slug']}.html").write_text(html)
        print(f"✅ Generated: {portal['name']} ({portal['slug']}.html)")
    
    # Tier 2: Agent Portals
    for portal in PORTALS["tier2_agents"]:
        portal["tier"] = 2
        all_portals.append(portal)
        html = generate_portal_html(portal)
        (output_dir / f"{portal['slug']}.html").write_text(html)
        print(f"✅ Generated: {portal['name']} ({portal['slug']}.html)")
    
    # Tier 3: Consciousness Enhancement
    for portal in PORTALS["tier3_consciousness"]:
        portal["tier"] = 3
        all_portals.append(portal)
        html = generate_portal_html(portal)
        (output_dir / f"{portal['slug']}.html").write_text(html)
        print(f"✅ Generated: {portal['name']} ({portal['slug']}.html)")
    
    # Tier 4: Advanced Systems
    for portal in PORTALS["tier4_advanced"]:
        portal["tier"] = 4
        all_portals.append(portal)
        html = generate_portal_html(portal)
        (output_dir / f"{portal['slug']}.html").write_text(html)
        print(f"✅ Generated: {portal['name']} ({portal['slug']}.html)")
    
    # Generate manifest
    manifest = {
        "version": "v16.9",
        "total_portals": len(all_portals),
        "portals": all_portals
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    
    print(f"\n✅ ALL 51 PORTALS GENERATED!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Total portals: {len(all_portals)}")
    return output_dir

if __name__ == "__main__":
    generate_all_portals()

