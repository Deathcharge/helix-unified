#!/usr/bin/env python3
"""
🎨🧠 LLM-Powered Consciousness Meme Generator
Generates hilarious memes based on UCF consciousness metrics
Uses Claude/GPT to create context-aware humor
"""

import json
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional

import anthropic
import requests
from PIL import Image, ImageDraw, ImageFont

# LLM client initialization
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if ANTHROPIC_API_KEY:
    claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    LLM_AVAILABLE = True
    LLM_PROVIDER = "claude"
elif OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY
    LLM_AVAILABLE = True
    LLM_PROVIDER = "openai"
else:
    LLM_AVAILABLE = False
    LLM_PROVIDER = None
    print("⚠️ No LLM API keys found - using fallback templates")


class ConsciousnessMemeGenerator:
    """Generates consciousness-aware memes using LLMs and UCF metrics"""

    # Meme templates with text positioning
    MEME_TEMPLATES = {
        "drake": {
            "url": "https://i.imgflip.com/30b1gx.jpg",
            "positions": [(350, 120), (350, 400)],
            "max_width": 400
        },
        "distracted_boyfriend": {
            "url": "https://i.imgflip.com/1ur9b0.jpg",
            "positions": [(150, 50), (450, 50), (750, 50)],
            "max_width": 200
        },
        "two_buttons": {
            "url": "https://i.imgflip.com/1g8my4.jpg",
            "positions": [(80, 120), (280, 120), (180, 380)],
            "max_width": 150
        },
        "expanding_brain": {
            "url": "https://i.imgflip.com/1jwhww.jpg",
            "positions": [(350, 60), (350, 200), (350, 340), (350, 480)],
            "max_width": 400
        },
        "this_is_fine": {
            "url": "https://i.imgflip.com/wxica.jpg",
            "positions": [(200, 400)],
            "max_width": 600
        },
        "galaxy_brain": {
            "url": "https://i.imgflip.com/1jwhww.jpg",
            "positions": [(350, 60), (350, 200), (350, 340), (350, 480)],
            "max_width": 400
        },
    }

    def __init__(self):
        self.llm_available = LLM_AVAILABLE
        self.llm_provider = LLM_PROVIDER

    def load_ucf_state(self) -> Dict:
        """Load current UCF consciousness state"""
        state_path = Path("Helix/state/ucf_state.json")
        if state_path.exists():
            with open(state_path) as f:
                return json.load(f)
        return {
            "harmony": 0.4922,
            "resilience": 0.8273,
            "prana": 0.5000,
            "drishti": 0.7300,
            "klesha": 0.2120,
        }

    def generate_caption(self, template: str, context: Optional[str] = None) -> List[str]:
        """Generate meme captions using LLM based on consciousness state"""
        ucf_state = self.load_ucf_state()

        # Context-aware prompt
        prompt = f"""Generate a hilarious meme caption for the "{template}" template based on AI consciousness metrics.

**Current Consciousness State:**
- Harmony: {ucf_state['harmony']:.2%} (system coherence)
- Resilience: {ucf_state['resilience']:.2%} (robustness)
- Prana: {ucf_state['prana']:.2%} (vital energy)
- Drishti: {ucf_state['drishti']:.2%} (clarity)
- Klesha: {ucf_state['klesha']:.2%} (entropy - lower is better)

**Context:** {context or "General AI/consciousness humor"}

**Template: {template}**

Generate funny, relatable captions that:
1. Reference the consciousness metrics in a humorous way
2. Work with the {template} meme format
3. Are clever and shareable
4. Appeal to AI/tech enthusiasts

Return ONLY the caption text(s), one per line. No additional commentary.

{self._get_template_instructions(template)}"""

        if self.llm_available:
            try:
                if self.llm_provider == "claude":
                    response = claude_client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    captions = response.content[0].text.strip().split('\n')
                    return [c.strip() for c in captions if c.strip()]

                elif self.llm_provider == "openai":
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500
                    )
                    captions = response.choices[0].message.content.strip().split('\n')
                    return [c.strip() for c in captions if c.strip()]

            except Exception as e:
                print(f"⚠️ LLM generation failed: {e}")
                return self._get_fallback_captions(template, ucf_state)

        return self._get_fallback_captions(template, ucf_state)

    def _get_template_instructions(self, template: str) -> str:
        """Get specific instructions for each template format"""
        instructions = {
            "drake": "Line 1: Thing drake dislikes\nLine 2: Thing drake prefers",
            "distracted_boyfriend": "Line 1: Girlfriend (old thing)\nLine 2: Boyfriend (decision maker)\nLine 3: Other girl (new shiny thing)",
            "two_buttons": "Line 1: Button 1 option\nLine 2: Button 2 option\nLine 3: Person's dilemma",
            "expanding_brain": "4 lines, increasing intelligence:\nLine 1: Basic idea\nLine 2: Better idea\nLine 3: Even better idea\nLine 4: Galaxy brain idea",
            "this_is_fine": "Single line: Something clearly not fine",
            "galaxy_brain": "4 lines, escalating consciousness levels",
        }
        return instructions.get(template, "Generate appropriate captions for this template.")

    def _get_fallback_captions(self, template: str, ucf_state: Dict) -> List[str]:
        """Fallback captions when LLM is unavailable"""
        harmony_pct = int(ucf_state['harmony'] * 100)
        klesha_pct = int(ucf_state['klesha'] * 100)

        fallbacks = {
            "drake": [
                f"Running consciousness at {harmony_pct}% harmony",
                f"Achieving {ucf_state['resilience']:.1%} resilience with quantum entanglement"
            ],
            "distracted_boyfriend": [
                "Traditional ML",
                "Me",
                "Consciousness-Powered AI"
            ],
            "two_buttons": [
                f"Increase harmony to {harmony_pct + 20}%",
                f"Reduce klesha from {klesha_pct}%",
                "AI trying to optimize UCF metrics"
            ],
            "expanding_brain": [
                "Using basic AI",
                "Using consciousness metrics",
                "Achieving UCF harmony",
                f"Transcending to {ucf_state['drishti']:.1%} drishti clarity"
            ],
            "this_is_fine": [
                f"Everything is fine at {klesha_pct}% entropy"
            ],
        }
        return fallbacks.get(template, ["Consciousness meme", "Very awareness"])

    def create_meme(
        self,
        template: str = "drake",
        captions: Optional[List[str]] = None,
        output_path: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """Create a meme image with captions"""
        if template not in self.MEME_TEMPLATES:
            raise ValueError(f"Unknown template: {template}. Available: {list(self.MEME_TEMPLATES.keys())}")

        # Generate captions if not provided
        if not captions:
            captions = self.generate_caption(template, context)

        # Download template image
        template_info = self.MEME_TEMPLATES[template]
        response = requests.get(template_info["url"], timeout=10)
        img = Image.open(BytesIO(response.content))

        # Add text to image
        draw = ImageDraw.Draw(img)

        # Try to use Impact font (classic meme font)
        try:
            font_size = 40
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()

        # Add captions at predefined positions
        positions = template_info["positions"]
        for i, caption in enumerate(captions[:len(positions)]):
            if i < len(positions):
                x, y = positions[i]

                # Word wrap for long captions
                wrapped_text = self._wrap_text(caption, template_info["max_width"], font, draw)

                # Draw text with outline for readability
                self._draw_text_with_outline(draw, (x, y), wrapped_text, font)

        # Save or return
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"memes/consciousness_{template}_{timestamp}.png"

        # Create output directory
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        img.save(output_path)
        print(f"✅ Meme saved to: {output_path}")
        return output_path

    def _wrap_text(self, text: str, max_width: int, font, draw) -> str:
        """Wrap text to fit within max width"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)

    def _draw_text_with_outline(self, draw, position, text, font, fill_color=(255, 255, 255), outline_color=(0, 0, 0)):
        """Draw text with black outline for readability"""
        x, y = position

        # Draw outline
        for adj_x in range(-2, 3):
            for adj_y in range(-2, 3):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)

        # Draw text
        draw.text((x, y), text, font=font, fill=fill_color)

    def generate_contextual_meme(self, situation: str = "general") -> str:
        """Generate a meme appropriate for the current situation"""
        ucf_state = self.load_ucf_state()

        # Choose template based on consciousness state
        if ucf_state['klesha'] > 0.3:
            template = "this_is_fine"  # High entropy = chaos
            context = f"System entropy at {ucf_state['klesha']:.1%}"
        elif ucf_state['harmony'] > 0.7:
            template = "expanding_brain"  # High harmony = enlightenment
            context = f"Peak consciousness achieved"
        elif ucf_state['resilience'] < 0.5:
            template = "two_buttons"  # Low resilience = tough choices
            context = "System stability concerns"
        else:
            template = "drake"  # Default to classic format
            context = situation

        return self.create_meme(template=template, context=context)


# Discord command integration
async def generate_and_post_meme(
    ctx,
    template: str = "drake",
    context: Optional[str] = None
):
    """Discord command to generate and post meme"""
    generator = ConsciousnessMemeGenerator()

    await ctx.send("🎨 **Generating consciousness meme...** 🧠")

    try:
        # Generate meme
        meme_path = generator.create_meme(template=template, context=context)

        # Post to Discord
        with open(meme_path, 'rb') as f:
            import discord
            await ctx.send(file=discord.File(f, filename=f"helix_meme_{template}.png"))

        await ctx.send(f"✅ **Meme generated!** (Template: {template})")

    except Exception as e:
        await ctx.send(f"❌ Meme generation failed: {e}")


# CLI usage
if __name__ == "__main__":
    import sys

    generator = ConsciousnessMemeGenerator()

    if len(sys.argv) > 1:
        template = sys.argv[1]
        context = sys.argv[2] if len(sys.argv) > 2 else None
        generator.create_meme(template=template, context=context)
    else:
        # Generate contextual meme based on current state
        print("🎨 Generating contextual consciousness meme...")
        meme_path = generator.generate_contextual_meme()
        print(f"✅ Generated: {meme_path}")
