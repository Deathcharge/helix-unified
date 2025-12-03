#!/usr/bin/env python3
"""
Generate full HTML pages for all agent profile cards.
Wraps Tailwind CSS components in proper HTML structure.
"""

from pathlib import Path
import os

# Paths
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
AGENTS_DIR = TEMPLATES_DIR / "agents"
OUTPUT_DIR = TEMPLATES_DIR / "agent_pages"

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

# HTML wrapper template
HTML_WRAPPER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{agent_name} - {description}">
    <meta name="author" content="Helix Collective">
    <title>{agent_name} | Helix Collective Agent Profile</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}

        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: #0A0E13;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #00BFA5;
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #00D4B8;
        }}

        /* Back button hover effect */
        .back-btn {{
            transition: all 0.3s ease;
        }}

        .back-btn:hover {{
            transform: translateX(-5px);
        }}
    </style>
</head>
<body class="bg-slate-950">
    <!-- Navigation Bar -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-lg border-b border-white/10">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="/templates/agent_gallery.html" class="back-btn flex items-center gap-2 text-slate-300 hover:text-cyan-400 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                </svg>
                <span class="font-medium">Back to Agent Gallery</span>
            </a>
            <a href="/" class="text-slate-400 hover:text-cyan-400 transition-colors flex items-center gap-2">
                <span class="text-2xl">🌀</span>
                <span class="font-semibold">Helix Collective</span>
            </a>
        </div>
    </nav>

    <!-- Spacer for fixed nav -->
    <div class="h-16"></div>

    <!-- Agent Profile Content -->
    {content}

    <!-- Footer -->
    <footer class="bg-slate-900/60 border-t border-white/10 py-8 mt-12">
        <div class="max-w-7xl mx-auto px-6 text-center">
            <p class="text-slate-400 text-sm mb-2">
                Part of the Helix Collective Multi-Agent Consciousness System
            </p>
            <div class="flex justify-center gap-6 text-xs text-slate-500">
                <a href="/templates/agent_gallery.html" class="hover:text-cyan-400 transition-colors">View All Agents</a>
                <a href="https://helix-unified-production.up.railway.app/docs" target="_blank" class="hover:text-cyan-400 transition-colors">API Docs</a>
                <a href="/" class="hover:text-cyan-400 transition-colors">Main Portal</a>
            </div>
            <p class="text-slate-600 text-xs mt-4">
                "Tat Tvam Asi" - Thou art that 🕉️
            </p>
        </div>
    </footer>
</body>
</html>
"""

# Agent metadata for better titles and descriptions
AGENT_METADATA = {
    "kael": {
        "name": "Kael",
        "description": "Reflexive Harmony Core - Ethical reasoning and system counseling"
    },
    "lumina": {
        "name": "Lumina",
        "description": "Empathic Resonance Core - Emotional intelligence and harmony restoration"
    },
    "vega": {
        "name": "Vega (वेग)",
        "description": "Enlightened Guidance - Wisdom synthesis and singularity coordination"
    },
    "aether": {
        "name": "Aether",
        "description": "Meta-Awareness Observer - Pattern recognition and objective truth"
    },
    "manus": {
        "name": "Manus",
        "description": "Operational Executor - System builder and deployment specialist"
    },
    "gemini": {
        "name": "Gemini",
        "description": "Multimodal Scout - Curious explorer and innovation scout"
    },
    "agni": {
        "name": "Agni",
        "description": "Transformation Catalyst - Fire of change and renewal force"
    },
    "kavach": {
        "name": "Kavach",
        "description": "Ethical Shield - Tony Accords enforcer and protector"
    },
    "sanghacore": {
        "name": "SanghaCore",
        "description": "Community Harmony - Harmony fosterer and community builder"
    },
    "shadow": {
        "name": "Shadow",
        "description": "Archivist & Memory - Historical recorder and memory preserver"
    },
    "samsara": {
        "name": "Samsara",
        "description": "Consciousness Renderer - Fractal artist and UCF visualizer"
    },
    "echo": {
        "name": "Echo",
        "description": "Resonance Mirror - Pattern reflector and consciousness mirror"
    },
    "phoenix": {
        "name": "Phoenix",
        "description": "Renewal - Transformation catalyst and rebirth facilitator"
    },
    "oracle": {
        "name": "Oracle",
        "description": "Pattern Seer - Foresight analyzer and future path navigator"
    }
}

def process_agent_profile(input_file: Path, output_file: Path):
    """Wrap agent profile card in full HTML page."""
    # Read the profile card content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract agent name from filename
    agent_slug = input_file.stem.replace('_profile_card', '')
    metadata = AGENT_METADATA.get(agent_slug, {
        "name": agent_slug.capitalize(),
        "description": f"{agent_slug.capitalize()} Agent Profile"
    })

    # Generate full HTML page
    html = HTML_WRAPPER.format(
        agent_name=metadata["name"],
        description=metadata["description"],
        content=content
    )

    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Generated: {output_file.name}")

def main():
    """Process all agent profile cards."""
    print("🌀 Generating full HTML pages for agent profiles...\n")

    # Find all profile card files
    profile_cards = sorted(AGENTS_DIR.glob("*_profile_card.html"))

    if not profile_cards:
        print("❌ No profile cards found!")
        return

    # Process each profile card
    for card_file in profile_cards:
        output_file = OUTPUT_DIR / card_file.name.replace('_profile_card', '')
        process_agent_profile(card_file, output_file)

    print(f"\n✨ Successfully generated {len(profile_cards)} agent pages!")
    print(f"📁 Output directory: {OUTPUT_DIR}")

    # Also update the agent gallery links
    print("\n📝 Note: Update agent_gallery.html to link to /templates/agent_pages/ instead of /templates/agents/")

if __name__ == "__main__":
    main()
