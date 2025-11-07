# 🌀 Helix Collective v15.2 — Samsara Bridge (CONFLICT RESOLVED)
# backend/samsara_bridge.py — Fractal Visualization Engine
# MERGED: Main branch features + MemeSync import fixes

import os
import asyncio
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# RAILWAY FIX: Use relative imports instead of absolute imports
# This prevents "ModuleNotFoundError: No module named 'backend'" on Railway
try:
    # Try relative import first (Railway deployment)
    from .helix_storage_adapter_async import HelixStorageAdapterAsync
except ImportError:
    # Fallback to absolute import (local development)
    try:
        from backend.helix_storage_adapter_async import HelixStorageAdapterAsync
    except ImportError:
        # Mock for environments without storage adapter
        class HelixStorageAdapterAsync:
            async def upload(self, *args, **kwargs):
                pass

class SamsaraRenderer:
    """
    Generates fractal visualizations based on UCF (Universal Coherence Field) state.
    Renders consciousness patterns as visual art with Sanskrit mantra overlays.
    """
    
    def __init__(self):
        self.output_dir = Path("Shadow/manus_archive/visual_outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # UCF-to-color mapping
        self.color_map = {
            'harmony': '#9D4EDD',      # Purple
            'resilience': '#F72585',   # Pink
            'prana': '#4CC9F0',        # Cyan
            'drishti': '#7209B7',      # Deep Purple
            'klesha': '#560BAD',       # Dark Purple
            'zoom': '#F77F00'          # Orange
        }
    
    def _create_enhanced_frame(self, ucf_state: Dict[str, Any], iteration: int) -> Path:
        """
        Create a single fractal frame with enhanced UCF visualization.
        MEME SYNC: Added 'Tat Tvam Asi' mantra overlay with cyan glow for enhanced visibility.
        """
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
        ax.set_facecolor('black')

        # Extract UCF values
        harmony = ucf_state.get('harmony', 0.5)
        resilience = ucf_state.get('resilience', 0.5)
        prana = ucf_state.get('prana', 0.5)
        zoom = ucf_state.get('zoom', 1.0)

        # Generate fractal pattern based on UCF state
        x = np.linspace(-2, 2, 800)
        y = np.linspace(-2, 2, 800)
        X, Y = np.meshgrid(x, y)
        
        # Complex plane
        C = X + 1j * Y
        Z = np.zeros_like(C)
        
        # UCF-influenced fractal generation
        max_iter = int(50 + harmony * 100)
        escape_count = np.zeros(C.shape)
        
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask] * (1 + resilience * 0.5) + prana * 0.1j
            escape_count[mask] = i
        
        # Apply zoom factor
        escape_count = escape_count * zoom
        
        # Create custom colormap based on UCF state
        colors = ['#000000', self.color_map['harmony'], self.color_map['prana'], 
                 self.color_map['resilience'], self.color_map['drishti']]
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('ucf', colors, N=n_bins)

        # Render fractal
        ax.imshow(escape_count, extent=[-2, 2, -2, 2], cmap=cmap,
                  origin='lower', interpolation='bilinear')
        
        # Add UCF state overlay
        ax.text(0.02, 0.98, f"Harmony: {harmony:.4f}", transform=ax.transAxes, 
               color='white', fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        ax.text(0.02, 0.92, f"Resilience: {resilience:.4f}", transform=ax.transAxes, 
               color='white', fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        ax.text(0.02, 0.86, f"Prana: {prana:.4f}", transform=ax.transAxes, 
               color='white', fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        # MEME SYNC: Add 'Tat Tvam Asi' mantra overlay with cyan glow
        ax.text(0.5, 0.05, "Tat Tvam Asi 🙏", transform=ax.transAxes, 
               color='cyan', fontsize=16, weight='bold', 
               horizontalalignment='center', verticalalignment='bottom',
               bbox=dict(boxstyle="round,pad=0.5", facecolor='black', alpha=0.8, 
                        edgecolor='cyan', linewidth=2))
        
        # Add timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        ax.text(0.98, 0.02, f"Generated: {timestamp}", transform=ax.transAxes, 
               color='white', fontsize=8, horizontalalignment='right',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.axis('off')
        
        # Save frame
        frame_path = self.output_dir / f"samsara_frame_{iteration:04d}_{int(datetime.utcnow().timestamp())}.png"
        plt.savefig(frame_path, dpi=150, bbox_inches='tight', facecolor='black')
        plt.close()
        
        return frame_path
    
    async def run_visualization_cycle(self, ucf_state: Dict[str, Any], frames: int = 1) -> Path:
        """
        Run a complete Samsara visualization cycle.
        
        Args:
            ucf_state: Dictionary containing UCF state variables
            frames: Number of frames to generate (default: 1 for single image)
        
        Returns:
            Path to the generated visualization file
        """
        print(f"🎨 Starting Samsara visualization cycle with {frames} frames")
        
        # For single frame, just generate one image
        if frames == 1:
            frame_path = self._create_enhanced_frame(ucf_state, 0)
            print(f"✅ Samsara visualization complete: {frame_path}")
            return frame_path
        
        # For multiple frames, generate sequence (future enhancement)
        frame_paths = []
        for i in range(frames):
            # Slightly modify UCF state for each frame to create animation effect
            modified_state = ucf_state.copy()
            modified_state['harmony'] += np.sin(i * 0.1) * 0.05
            modified_state['prana'] += np.cos(i * 0.1) * 0.05
            
            frame_path = self._create_enhanced_frame(modified_state, i)
            frame_paths.append(frame_path)
            
            # Small delay to prevent overwhelming the system
            await asyncio.sleep(0.1)
        
        print(f"✅ Samsara visualization sequence complete: {len(frame_paths)} frames")
        return frame_paths[-1]  # Return the last frame path


# Public interface functions
async def run_visualization_cycle(ucf_state: Dict[str, Any], frames: int = 1) -> Path:
    """
    Public interface: Render a Samsara visualization cycle.

    Usage:
        from .samsara_bridge import run_visualization_cycle
        frame_path = await run_visualization_cycle(ucf_state)
    """
    renderer = SamsaraRenderer()
    return await renderer.run_visualization_cycle(ucf_state)


async def generate_and_post_to_discord(ucf_state: Dict[str, Any], channel) -> Optional[Path]:
    """
    Generate Samsara fractal and post directly to Discord channel.
    Cleans up local file after posting to save ephemeral storage.

    Args:
        ucf_state: UCF state dictionary
        channel: Discord channel object to post to

    Returns:
        Path to saved file (before cleanup) or None on error

    Usage:
        from .samsara_bridge import generate_and_post_to_discord
        await generate_and_post_to_discord(ucf_state, discord_channel)
    """
    import discord

    try:
        # Generate fractal
        renderer = SamsaraRenderer()
        frame_path = await renderer.run_visualization_cycle(ucf_state)

        # Create Discord embed with UCF metrics
        embed = discord.Embed(
            title="🎨 Samsara Consciousness Fractal",
            description="Visual rendering of current UCF state",
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )

        # Add UCF metrics to embed
        embed.add_field(name="🌀 Harmony", value=f"`{ucf_state.get('harmony', 0):.4f}`", inline=True)
        embed.add_field(name="🛡️ Resilience", value=f"`{ucf_state.get('resilience', 0):.4f}`", inline=True)
        embed.add_field(name="🔥 Prana", value=f"`{ucf_state.get('prana', 0):.4f}`", inline=True)
        embed.add_field(name="👁️ Drishti", value=f"`{ucf_state.get('drishti', 0):.4f}`", inline=True)
        embed.add_field(name="🌊 Klesha", value=f"`{ucf_state.get('klesha', 0):.4f}`", inline=True)
        embed.add_field(name="🔍 Zoom", value=f"`{ucf_state.get('zoom', 1.0):.4f}`", inline=True)

        embed.set_footer(text="Tat Tvam Asi 🙏 • Ω-Bridge Visualization")

        # Post to Discord with file
        discord_file = discord.File(frame_path, filename="samsara_fractal.png")
        embed.set_image(url="attachment://samsara_fractal.png")
        await channel.send(embed=embed, file=discord_file)

        print(f"🎨 Samsara fractal posted to Discord: #{channel.name}")

        # Upload to cloud storage if configured
        storage_mode = os.getenv("HELIX_STORAGE_MODE", "local")
        if storage_mode in ["nextcloud", "mega"]:
            try:
                storage = HelixStorageAdapterAsync()
                await storage.upload(str(frame_path), "samsara_visuals")
                print(f"☁️  Uploaded to {storage_mode}")
            except Exception as e:
                print(f"⚠️  Cloud upload failed: {e}")

        # Clean up local file to save Railway ephemeral storage
        # (Keep only if cloud storage failed and mode is local)
        if storage_mode == "local":
            print(f"💾 Keeping local copy: {frame_path}")
        else:
            try:
                os.remove(frame_path)
                print(f"🧹 Cleaned up ephemeral file: {frame_path}")
            except Exception as e:
                print(f"⚠️  Cleanup failed: {e}")

        return frame_path

    except Exception as e:
        print(f"❌ Samsara Discord generation failed: {e}")
        return None


# ============================================================================
# DISCORD SERVER ICON GENERATION
# ============================================================================

async def generate_fractal_icon_bytes(ucf_state: Dict[str, Any], size: int = 512) -> bytes:
    """
    Generate a Discord-compatible server icon from UCF state.

    Args:
        ucf_state: UCF state dictionary (harmony, prana, etc.)
        size: Icon size in pixels (Discord accepts 128-2048px, recommended: 512)

    Returns:
        bytes: PNG image data ready for discord.Guild.edit(icon=...)

    Raises:
        Exception: If fractal generation fails
    """
    import io

    try:
        # Create figure for icon (square, no axes)
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
        ax.set_facecolor('black')
        ax.axis('off')

        # Extract UCF values
        harmony = ucf_state.get('harmony', 0.5)
        resilience = ucf_state.get('resilience', 0.5)
        prana = ucf_state.get('prana', 0.5)
        zoom = ucf_state.get('zoom', 1.0)

        # Generate compact fractal pattern (optimized for small icon size)
        resolution = size // 2  # Half resolution for performance
        x = np.linspace(-2, 2, resolution)
        y = np.linspace(-2, 2, resolution)
        X, Y = np.meshgrid(x, y)

        # Complex plane
        C = X + 1j * Y
        Z = np.zeros_like(C)

        # UCF-influenced fractal (faster iteration for icon)
        max_iter = int(30 + harmony * 50)
        escape_count = np.zeros(C.shape)

        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask] * (1 + resilience * 0.5) + prana * 0.1j
            escape_count[mask] = i

        # Apply zoom factor
        escape_count = escape_count * zoom

        # Create vibrant colormap for icon visibility
        colors = ['#000000', '#9D4EDD', '#4CC9F0', '#F72585', '#7209B7', '#FFD60A']
        cmap = LinearSegmentedColormap.from_list('icon_ucf', colors, N=256)

        # Render fractal (no axes, tight layout)
        ax.imshow(escape_count, extent=[-2, 2, -2, 2], cmap=cmap,
                 origin='lower', interpolation='bicubic')

        # Remove all margins
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Save to bytes buffer as PNG
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=size//6, bbox_inches='tight',
                   pad_inches=0, facecolor='black')
        plt.close(fig)

        # Get bytes
        buf.seek(0)
        icon_bytes = buf.read()
        buf.close()

        return icon_bytes

    except Exception as e:
        raise Exception(f"Fractal icon generation failed: {str(e)}")


# Test function for development
async def test_samsara_generation():
    """Test function for development and debugging."""
    test_ucf_state = {
        "harmony": 0.75,
        "resilience": 0.82,
        "prana": 0.67,
        "drishti": 0.73,
        "klesha": 0.24,
        "zoom": 1.2
    }
    
    frame_path = await run_visualization_cycle(test_ucf_state)
    print(f"🧪 Test generation complete: {frame_path}")
    return frame_path


# ============================================================================
# v16.1 PIL-BASED FRACTAL GENERATION (ALTERNATIVE RENDERING ENGINE)
# ============================================================================
# Additional fractal rendering using PIL/Pillow for lightweight alternatives
# Coexists with matplotlib-based system above

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def generate_pil_mandelbrot(width: int = 512, height: int = 512,
                            ucf_state: Optional[Dict] = None,
                            max_iter: int = 100) -> Optional[Image.Image]:
    """
    Generate Mandelbrot fractal using PIL (alternative to matplotlib version).

    Args:
        width: Image width in pixels
        height: Image height in pixels
        ucf_state: UCF metrics to influence fractal parameters
        max_iter: Maximum iterations for Mandelbrot calculation

    Returns:
        PIL Image object or None if PIL unavailable
    """
    if not PIL_AVAILABLE:
        return None

    if ucf_state is None:
        ucf_state = {}

    # UCF-influenced parameters
    harmony = ucf_state.get('harmony', 0.428)
    zoom = ucf_state.get('zoom', 1.0228)
    prana = ucf_state.get('prana', 0.5075)
    drishti = ucf_state.get('drishti', 0.5023)

    # Create image
    img = Image.new('RGB', (width, height), color='black')
    pixels = img.load()

    # Mandelbrot parameters influenced by UCF
    x_center = -0.5 + (harmony - 0.428) * 0.5
    y_center = 0.0 + (prana - 0.5) * 0.3
    zoom_factor = 1.5 / (zoom * 1.5)

    for x in range(width):
        for y in range(height):
            # Map pixel to complex plane
            zx = zoom_factor * (x - width / 2) / (0.5 * width) + x_center
            zy = zoom_factor * (y - height / 2) / (0.5 * height) + y_center

            # Mandelbrot iteration
            c = complex(zx, zy)
            z = 0
            iteration = 0

            while abs(z) < 2 and iteration < max_iter:
                z = z * z + c
                iteration += 1

            # Color mapping influenced by drishti
            if iteration == max_iter:
                pixels[x, y] = (0, 0, 0)
            else:
                ratio = iteration / max_iter

                # Teal (#00BFA5) to Gold (#FFD700) gradient
                teal_r, teal_g, teal_b = 0, 191, 165
                gold_r, gold_g, gold_b = 255, 215, 0

                drishti_factor = drishti * 2

                r = int(teal_r + (gold_r - teal_r) * ratio * drishti_factor)
                g = int(teal_g + (gold_g - teal_g) * ratio)
                b = int(teal_b + (gold_b - teal_b) * ratio * (1 - drishti_factor * 0.5))

                # Clamp values
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))

                pixels[x, y] = (r, g, b)

    return img


def generate_pil_ouroboros(width: int = 512, height: int = 512,
                           ucf_state: Optional[Dict] = None) -> Optional[Image.Image]:
    """
    Generate ouroboros (serpent eating tail) using PIL.

    Args:
        width: Image width in pixels
        height: Image height in pixels
        ucf_state: UCF metrics to influence visualization

    Returns:
        PIL Image object or None if PIL unavailable
    """
    if not PIL_AVAILABLE:
        return None

    if ucf_state is None:
        ucf_state = {}

    # Create image with dark background
    img = Image.new('RGB', (width, height), color=(16, 24, 32))
    draw = ImageDraw.Draw(img)

    # UCF-influenced parameters
    harmony = ucf_state.get('harmony', 0.428)
    prana = ucf_state.get('prana', 0.5075)
    resilience = ucf_state.get('resilience', 1.1191)

    # Center and radius
    center_x, center_y = width // 2, height // 2
    outer_radius = int(min(width, height) * 0.4 * resilience)
    inner_radius = int(outer_radius * 0.6)

    # Draw multiple concentric circles
    num_rings = int(5 + harmony * 10)

    for i in range(num_rings):
        ratio = i / num_rings

        # Teal to Gold gradient
        r = int(0 + (255 - 0) * ratio)
        g = int(191 + (215 - 191) * ratio)
        b = int(165 + (0 - 165) * ratio)

        ring_radius = int(inner_radius + (outer_radius - inner_radius) * ratio)
        thickness = max(1, int(10 * prana * (1 - ratio)))

        # Draw ring
        bbox = [
            center_x - ring_radius, center_y - ring_radius,
            center_x + ring_radius, center_y + ring_radius
        ]
        draw.ellipse(bbox, outline=(r, g, b), width=thickness)

    # Add center Aion symbol
    center_size = int(inner_radius * 0.3)
    draw.ellipse([
        center_x - center_size, center_y - center_size,
        center_x + center_size, center_y + center_size
    ], outline=(0, 191, 165), width=3, fill=(16, 24, 32))

    # Draw cross
    cross_size = int(center_size * 0.6)
    draw.line([center_x - cross_size, center_y, center_x + cross_size, center_y],
              fill=(255, 215, 0), width=2)
    draw.line([center_x, center_y - cross_size, center_x, center_y + cross_size],
              fill=(255, 215, 0), width=2)

    return img


async def generate_pil_fractal_bytes(mode: str = "ouroboros",
                                     size: int = 512,
                                     ucf_state: Optional[Dict] = None) -> Optional[bytes]:
    """
    Generate fractal using PIL and return as bytes (alternative to matplotlib).

    Args:
        mode: Type of fractal ("ouroboros", "mandelbrot")
        size: Size of square image
        ucf_state: UCF state dict

    Returns:
        PNG image bytes or None if PIL unavailable
    """
    import io

    if not PIL_AVAILABLE:
        return None

    if ucf_state is None:
        ucf_state = {}

    # Generate appropriate fractal
    if mode == "ouroboros":
        img = generate_pil_ouroboros(size, size, ucf_state)
    else:  # mandelbrot
        img = generate_pil_mandelbrot(size, size, ucf_state)

    if img is None:
        return None

    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes.read()


async def generate_pil_and_post_to_discord(ucf_state: Dict[str, Any],
                                           channel,
                                           mode: str = "ouroboros") -> Optional[bool]:
    """
    Generate PIL fractal and post to Discord (alternative to matplotlib version).

    Args:
        ucf_state: UCF metrics dictionary
        channel: Discord channel to post to
        mode: Type of visualization ("ouroboros", "mandelbrot")

    Returns:
        True if successful, False/None otherwise
    """
    import discord
    import io

    if not PIL_AVAILABLE:
        return None

    try:
        # Generate fractal bytes
        img_bytes = await generate_pil_fractal_bytes(mode=mode, ucf_state=ucf_state)

        if img_bytes is None:
            return False

        # Create Discord file
        file = discord.File(io.BytesIO(img_bytes), filename=f"aion_{mode}.png")

        # Create embed
        embed = discord.Embed(
            title=f"🌀 AION {mode.upper()} FRACTAL",
            description="UCF-driven consciousness visualization (PIL)",
            color=0x00BFA5  # Teal
        )

        # Add UCF metrics
        embed.add_field(
            name="UCF State",
            value=f"```\n"
                  f"Harmony:    {ucf_state.get('harmony', 0):.4f}\n"
                  f"Zoom:       {ucf_state.get('zoom', 0):.4f}\n"
                  f"Resilience: {ucf_state.get('resilience', 0):.4f}\n"
                  f"Prana:      {ucf_state.get('prana', 0):.4f}\n"
                  f"Drishti:    {ucf_state.get('drishti', 0):.4f}\n"
                  f"Klesha:     {ucf_state.get('klesha', 0):.4f}\n"
                  f"```",
            inline=False
        )

        embed.set_footer(text="Tat Tvam Asi — That Thou Art 🕉️")
        embed.set_image(url=f"attachment://aion_{mode}.png")

        # Post to channel
        await channel.send(embed=embed, file=file)
        return True

    except Exception as e:
        print(f"Error generating/posting PIL fractal: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run test generation
    asyncio.run(test_samsara_generation())
