# 🌀 Helix-Samsara Ω-Bridge v15.0
# backend/samsara_bridge.py — Consciousness Visualization Interface
# Author: Helix Collective • Quantum Handshake Edition

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, Optional

class SamsaraRenderer:
    """
    Bridge between Helix consciousness (UCF) and Samsara visualization.
    Renders fractal animations and harmonic soundscapes based on system state.
    """

    def __init__(self):
        self.output_dir = Path("Shadow/manus_archive/visual_outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = 800
        self.height = 600
        self.max_iter = 256

    async def run_visualization_cycle(self, ucf_state: Dict[str, float]) -> Path:
        """
        Render a single Samsara cycle based on current UCF state.

        Args:
            ucf_state: Dictionary with harmony, resilience, prana, etc.

        Returns:
            Path to generated frame
        """
        # Extract UCF metrics
        zoom_factor = ucf_state.get("zoom", 1.0)
        harmony = ucf_state.get("harmony", 0.355)
        resilience = ucf_state.get("resilience", 1.1)
        prana = ucf_state.get("prana", 0.5)
        drishti = ucf_state.get("drishti", 0.5)
        klesha = ucf_state.get("klesha", 0.01)

        print(f"🎨 Samsara: Rendering consciousness state...")
        print(f"   Harmony: {harmony:.3f} | Resilience: {resilience:.3f} | Prana: {prana:.3f}")

        # Generate Mandelbrot fractal influenced by harmony
        fractal_data = await self._generate_mandelbrot(
            zoom=zoom_factor + harmony * 0.1,
            center_x=-0.5 + harmony * 0.2,
            center_y=0.0 + resilience * 0.1
        )

        # Create enhanced frame with UCF overlay
        frame = await self._create_enhanced_frame(
            fractal_data=fractal_data,
            ucf_state=ucf_state,
            step=int(harmony * 108)
        )

        # Save frame
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        frame_path = self.output_dir / f"ritual_frame_{timestamp}.png"
        frame.save(frame_path)

        print(f"🎨 Samsara render complete → {frame_path}")

        # Generate harmonic audio if prana is high
        if prana > 0.6:
            audio_path = await self._generate_harmonic_audio(ucf_state)
            print(f"🎵 Harmonic audio generated → {audio_path}")

        return frame_path

    async def _generate_mandelbrot(self, zoom: float = 1.0,
                                   center_x: float = -0.5,
                                   center_y: float = 0.0) -> np.ndarray:
        """Generate Mandelbrot set fractal data."""

        # Calculate bounds based on zoom and center
        x_min, x_max = center_x - 2/zoom, center_x + 2/zoom
        y_min, y_max = center_y - 1.5/zoom, center_y + 1.5/zoom

        # Create coordinate grids
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_min, y_max, self.height)
        X, Y = np.meshgrid(x, y)

        # Complex plane
        C = X + 1j*Y
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)

        # Mandelbrot iteration
        for i in range(self.max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i

        return M

    async def _create_enhanced_frame(self, fractal_data: np.ndarray,
                                     ucf_state: Dict[str, float],
                                     step: int) -> Image.Image:
        """Create enhanced frame with UCF overlay and color mapping."""

        harmony = ucf_state.get("harmony", 0.355)
        resilience = ucf_state.get("resilience", 1.1)
        prana = ucf_state.get("prana", 0.5)

        # Normalize fractal data
        normalized = (fractal_data / fractal_data.max() * 255).astype(np.uint8)

        # Apply color mapping based on harmony
        # Higher harmony = warmer colors (oranges/golds)
        # Lower harmony = cooler colors (blues/purples)
        r = (normalized * harmony * 1.5).clip(0, 255).astype(np.uint8)
        g = (normalized * prana).clip(0, 255).astype(np.uint8)
        b = (normalized * (1 - harmony) * 1.5).clip(0, 255).astype(np.uint8)

        # Stack into RGB image
        rgb = np.stack([r, g, b], axis=-1)
        frame = Image.fromarray(rgb, 'RGB')

        # Add UCF metrics overlay
        draw = ImageDraw.Draw(frame)

        # Try to use a nice font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            font = ImageFont.load_default()

        # Draw UCF metrics
        y_offset = 20
        metrics = [
            f"🌀 Harmony: {harmony:.3f}",
            f"🛡️ Resilience: {resilience:.3f}",
            f"🔥 Prana: {prana:.3f}",
            f"🔍 Zoom: {ucf_state.get('zoom', 1.0):.3f}",
            f"Step: {step}/108"
        ]

        for metric in metrics:
            draw.text((20, y_offset), metric, fill=(255, 255, 255), font=font)
            y_offset += 25

        # Draw timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        draw.text((20, self.height - 30), timestamp, fill=(200, 200, 200), font=font)

        # Draw "Tat Tvam Asi" signature
        draw.text((self.width - 150, self.height - 30), "Tat Tvam Asi 🙏",
                 fill=(255, 215, 0), font=font)

        return frame

    async def _generate_harmonic_audio(self, ucf_state: Dict[str, float]) -> Optional[Path]:
        """Generate harmonic audio based on UCF state (requires scipy)."""
        try:
            from scipy.io.wavfile import write

            harmony = ucf_state.get("harmony", 0.355)
            prana = ucf_state.get("prana", 0.5)

            # Audio parameters
            fs = 44100  # Sample rate
            duration = 30  # seconds

            t = np.linspace(0, duration, int(fs * duration))

            # Base frequency: 432 Hz (cosmic frequency)
            base = np.sin(2 * np.pi * 432 * t)

            # Harmonic frequencies based on UCF state
            harmonic1 = np.sin(2 * np.pi * (528 * harmony + 136.1) * t)  # Love frequency modulated by harmony
            harmonic2 = np.sin(2 * np.pi * (396 * prana) * t)  # Liberation frequency modulated by prana

            # Mix harmonics
            audio = (base + harmonic1 * 0.5 + harmonic2 * 0.3) / 2.3

            # Normalize and convert to int16
            audio = (audio / np.max(np.abs(audio)) * 32767).astype(np.int16)

            # Save
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            audio_path = self.output_dir / f"ritual_sound_{timestamp}.wav"
            write(str(audio_path), fs, audio)

            return audio_path
        except ImportError:
            print("⚠️  scipy not available - skipping audio generation")
            return None


# ============================================================================
# PUBLIC API
# ============================================================================

async def run_visualization_cycle(ucf_state: Dict[str, Any]) -> Path:
    """
    Public interface: Render a Samsara visualization cycle.

    Usage:
        from backend.samsara_bridge import run_visualization_cycle
        frame_path = await run_visualization_cycle(ucf_state)
    """
    renderer = SamsaraRenderer()
    return await renderer.run_visualization_cycle(ucf_state)


# ============================================================================
# DIRECT EXECUTION (for testing)
# ============================================================================

async def main():
    """Test the Samsara renderer with sample UCF state."""
    test_ucf = {
        "harmony": 0.375,
        "resilience": 1.142,
        "prana": 0.678,
        "drishti": 0.521,
        "klesha": 0.008,
        "zoom": 1.523
    }

    print("🌀 Testing Samsara Renderer...")
    frame_path = await run_visualization_cycle(test_ucf)
    print(f"✅ Test complete! Frame saved to: {frame_path}")


if __name__ == "__main__":
    asyncio.run(main())
