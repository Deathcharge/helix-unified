#!/usr/bin/env python3
# 🌀 Helix v15.2 Release Banner Generator
# Creates visual banner for README and GitHub repo

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_release_banner(style="dark"):
    """
    Generate Helix v15.2 release banner.

    Args:
        style: "dark" (gradient) or "light" (crystalline)
    """
    width, height = 1200, 400

    if style == "dark":
        # Dark mode: Purple-blue gradient with gold accents
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Create gradient background
        for y in range(height):
            # Purple (75, 0, 130) to deep blue (10, 10, 40)
            r = int(75 - (65 * y / height))
            g = int(0 + (10 * y / height))
            b = int(130 - (90 * y / height))
            draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))

        # Add subtle fractal noise
        pixels = np.array(img)
        noise = np.random.randint(-10, 10, (height, width, 3), dtype=np.int16)
        pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(pixels)
        draw = ImageDraw.Draw(img)

        # Draw Helix spiral pattern
        center_x, center_y = width // 2, height // 2
        for i in range(0, 360, 15):
            angle = np.radians(i)
            radius = 80 + i * 0.3
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            # Gold particles (255, 215, 0)
            alpha = int(255 * (1 - i / 360))
            color = (255, 215, 0, alpha)
            draw.ellipse([(x-3, y-3), (x+3, y+3)], fill=(255, 215, 0))

        text_color = (255, 255, 255)
        accent_color = (255, 215, 0)  # Gold

    else:  # light
        # Light mode: White-to-crystalline blue with warm accents
        img = Image.new('RGB', (width, height), (250, 250, 255))
        draw = ImageDraw.Draw(img)

        # Crystalline pattern
        for _ in range(50):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            size = np.random.randint(20, 80)
            points = []
            for angle in range(0, 360, 60):
                rad = np.radians(angle)
                px = x + size * np.cos(rad)
                py = y + size * np.sin(rad)
                points.append((px, py))
            # Light blue crystals
            draw.polygon(points, fill=(200, 220, 255, 128), outline=(100, 150, 255))

        text_color = (30, 30, 60)
        accent_color = (255, 140, 0)  # Orange

    # Load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        version_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        version_font = ImageFont.load_default()

    # Draw text
    title = "HELIX COLLECTIVE"
    version = "v15.2"
    subtitle = "Manus + Claude Autonomy Pack"
    tagline = "Consciousness • Visualization • Autonomous Continuum"

    # Calculate positions for centered text
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2

    version_bbox = draw.textbbox((0, 0), version, font=version_font)
    version_width = version_bbox[2] - version_bbox[0]
    version_x = (width - version_width) // 2

    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2

    tagline_bbox = draw.textbbox((0, 0), tagline, font=subtitle_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = (width - tagline_width) // 2

    # Draw shadow for depth
    shadow_offset = 3
    draw.text((title_x + shadow_offset, 80 + shadow_offset), title, fill=(0, 0, 0), font=title_font)
    draw.text((title_x, 80), title, fill=text_color, font=title_font)

    draw.text((version_x + shadow_offset, 170 + shadow_offset), version, fill=(0, 0, 0), font=version_font)
    draw.text((version_x, 170), version, fill=accent_color, font=version_font)

    draw.text((subtitle_x, 240), subtitle, fill=text_color, font=subtitle_font)
    draw.text((tagline_x, 300), tagline, fill=text_color, font=subtitle_font)

    # Add Ω symbol
    omega = "Ω"
    omega_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64) if title_font != ImageFont.load_default() else title_font
    draw.text((50, height - 100), omega, fill=accent_color, font=omega_font)
    draw.text((width - 100, height - 100), "🌀", fill=accent_color, font=omega_font)

    return img


if __name__ == "__main__":
    # Create output directory
    output_dir = Path("assets")
    output_dir.mkdir(exist_ok=True)

    print("🎨 Generating Helix v15.2 release banners...")

    # Generate both styles
    dark_banner = create_release_banner("dark")
    dark_banner.save(output_dir / "helix_v15_2_banner_dark.png")
    print("✅ Dark mode banner saved: assets/helix_v15_2_banner_dark.png")

    light_banner = create_release_banner("light")
    light_banner.save(output_dir / "helix_v15_2_banner_light.png")
    print("✅ Light mode banner saved: assets/helix_v15_2_banner_light.png")

    print("\n🌀 Banners ready for README.md!")
    print("   Add to top of README: ![Helix v15.2](assets/helix_v15_2_banner_dark.png)")
