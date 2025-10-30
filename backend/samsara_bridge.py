# 🌀 Helix Collective v15.2 — Samsara Bridge (CONFLICT RESOLVED)
# backend/samsara_bridge.py — Fractal Visualization Engine
# MERGED: Main branch features + MemeSync import fixes

import os
import asyncio
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
        drishti = ucf_state.get('drishti', 0.5)
        klesha = ucf_state.get('klesha', 0.5)
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
        im = ax.imshow(escape_count, extent=[-2, 2, -2, 2], cmap=cmap, 
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


if __name__ == "__main__":
    # Run test generation
    asyncio.run(test_samsara_generation())
