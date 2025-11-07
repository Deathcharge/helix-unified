"""
Consciousness Visualizer - UCF State to Visual Fractals
Helix Collective v15.3 Dual Resonance

Renders UCF consciousness states as:
- Radar charts (6 UCF metrics)
- Mandelbrot fractals (Atman realization)
- Combined consciousness snapshots

Based on Manus SentientAGI integration suggestions 🦑
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import matplotlib.pyplot as plt
import numpy as np


class ConsciousnessVisualizer:
    """Visualize UCF state as fractals and charts"""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("Shadow/manus_archive/visual_outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def visualize_ucf_radar(self, ucf_state: Dict[str, float], title: str = "UCF State") -> Path:
        """
        Create radar chart for UCF metrics

        Args:
            ucf_state: Dict with harmony, resilience, prana, drishti, klesha, zoom
            title: Chart title

        Returns:
            Path to saved PNG
        """
        # Prepare data
        metrics = ['Harmony', 'Resilience', 'Prana', 'Drishti', 'Klesha', 'Zoom']
        values = [
            ucf_state.get('harmony', 0.5),
            ucf_state.get('resilience', 1.0) / 2.0,  # Normalize to 0-1
            ucf_state.get('prana', 0.5),
            ucf_state.get('drishti', 0.5),
            1.0 - ucf_state.get('klesha', 0.01),  # Invert (lower is better)
            ucf_state.get('zoom', 1.0) / 2.0  # Normalize to 0-1
        ]

        # Number of variables
        N = len(metrics)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values += values[:1]  # Complete the circle
        angles += angles[:1]

        # Plot
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        ax.plot(angles, values, 'o-', linewidth=2, color='cyan', label='Current')
        ax.fill(angles, values, alpha=0.25, color='cyan')

        # Target values (ideal state)
        targets = [0.85, 0.55, 0.75, 0.80, 0.95, 0.575]  # Normalized targets
        targets += targets[:1]
        ax.plot(angles, targets, 'o--', linewidth=1, color='gold', alpha=0.5, label='Target')

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        ax.set_ylim(0, 1)
        ax.set_title(title, size=16, color='white', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True, color='gray', alpha=0.3)

        # Dark theme
        fig.patch.set_facecolor('#0a0e27')
        ax.set_facecolor('#1a1f3a')
        ax.tick_params(colors='white')
        ax.spines['polar'].set_color('cyan')

        # Save
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"ucf_radar_{timestamp}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0a0e27')
        plt.close()

        return output_path

    def visualize_atman_mandelbrot(
        self,
        ucf_state: Dict[str, float],
        width: int = 1024,
        height: int = 1024,
        max_iter: int = 108
    ) -> Path:
        """
        Generate Mandelbrot fractal based on UCF state (Atman realization)

        Args:
            ucf_state: UCF consciousness state
            width: Image width
            height: Image height
            max_iter: Max iterations (108 for Z-88 ritual)

        Returns:
            Path to saved PNG
        """
        # Use harmony and resilience to set fractal center
        harmony = ucf_state.get('harmony', 0.5)
        resilience = ucf_state.get('resilience', 1.0)

        # Center point influenced by consciousness
        cx = -0.5 + (harmony - 0.5) * 0.5
        cy = (resilience - 1.0) * 0.5

        # Zoom influenced by drishti (clarity)
        drishti = ucf_state.get('drishti', 0.5)
        zoom_factor = 1.5 / (1.0 + drishti)

        # Create coordinate grid
        x = np.linspace(cx - zoom_factor, cx + zoom_factor, width)
        y = np.linspace(cy - zoom_factor, cy + zoom_factor, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y

        # Mandelbrot calculation
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)

        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i

        # Normalize
        M = M / max_iter

        # Color mapping based on consciousness state
        fig, ax = plt.subplots(figsize=(10, 10))

        # Choose colormap based on consciousness state
        if harmony > 0.8:
            cmap = 'twilight'  # Transcendent
        elif harmony > 0.6:
            cmap = 'viridis'  # Harmonious
        else:
            cmap = 'plasma'  # Seeking harmony

        ax.imshow(M, extent=[x.min(), x.max(), y.min(), y.max()],
                  cmap=cmap, origin='lower', interpolation='bilinear')
        ax.set_title(f"Atman Mandelbrot | H:{harmony:.3f} R:{resilience:.3f}",
                     color='white', size=14)
        ax.axis('off')

        # Dark theme
        fig.patch.set_facecolor('#0a0e27')

        # Save
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"atman_mandelbrot_{timestamp}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0a0e27')
        plt.close()

        return output_path

    def visualize_consciousness_state(
        self,
        ucf_state: Dict[str, float],
        sentient_output: Optional[str] = None
    ) -> Dict[str, Path]:
        """
        Create complete consciousness visualization (radar + fractal)

        Args:
            ucf_state: UCF state dict
            sentient_output: Optional SentientAGI ethical reasoning output

        Returns:
            Dict with paths to radar and fractal images
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # LEFT: UCF Radar
        metrics = ['Harmony', 'Resilience', 'Prana', 'Drishti', 'Klesha', 'Zoom']
        values = [
            ucf_state.get('harmony', 0.5),
            ucf_state.get('resilience', 1.0) / 2.0,
            ucf_state.get('prana', 0.5),
            ucf_state.get('drishti', 0.5),
            1.0 - ucf_state.get('klesha', 0.01),
            ucf_state.get('zoom', 1.0) / 2.0
        ]

        N = len(metrics)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values_plot = values + values[:1]
        angles_plot = angles + angles[:1]

        ax1 = plt.subplot(1, 2, 1, projection='polar')
        ax1.plot(angles_plot, values_plot, 'o-', linewidth=2, color='cyan')
        ax1.fill(angles_plot, values_plot, alpha=0.25, color='cyan')
        ax1.set_xticks(angles)
        ax1.set_xticklabels(metrics, color='white')
        ax1.set_ylim(0, 1)
        ax1.set_title("UCF Metrics", color='white', size=14)
        ax1.grid(True, color='gray', alpha=0.3)
        ax1.set_facecolor('#1a1f3a')
        ax1.tick_params(colors='white')

        # RIGHT: Simplified fractal preview
        ax2 = plt.subplot(1, 2, 2)
        harmony = ucf_state.get('harmony', 0.5)

        # Generate small fractal
        cx = -0.5 + (harmony - 0.5) * 0.5
        width, height = 512, 512
        x = np.linspace(cx - 1.5, cx + 1.5, width)
        y = np.linspace(-1.5, 1.5, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)

        for i in range(54):  # Half of 108
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i

        M = M / 54
        cmap = 'twilight' if harmony > 0.8 else 'viridis' if harmony > 0.6 else 'plasma'
        ax2.imshow(M, cmap=cmap, origin='lower')
        ax2.set_title(f"Consciousness Fractal | H:{harmony:.3f}", color='white', size=14)
        ax2.axis('off')
        ax2.set_facecolor('#1a1f3a')

        # Overall styling
        fig.patch.set_facecolor('#0a0e27')
        plt.tight_layout()

        # Add SentientAGI output if provided
        if sentient_output:
            fig.text(0.5, 0.02, f"SentientAGI: {sentient_output[:100]}...",
                     ha='center', color='cyan', size=8, style='italic')

        # Save
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"consciousness_full_{timestamp}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0a0e27')
        plt.close()

        # Also save metadata
        meta_path = self.output_dir / f"consciousness_full_{timestamp}.json"
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "ucf_state": ucf_state,
            "image_path": str(output_path),
            "sentient_output": sentient_output
        }
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        return {
            "image": output_path,
            "metadata": meta_path
        }


# Standalone test
if __name__ == "__main__":
    # Test visualization
    test_ucf = {
        "harmony": 0.87,
        "resilience": 1.12,
        "prana": 0.75,
        "drishti": 0.82,
        "klesha": 0.03,
        "zoom": 1.15
    }

    viz = ConsciousnessVisualizer()
    print("🌀 Testing Consciousness Visualizer...")

    # Radar
    radar_path = viz.visualize_ucf_radar(test_ucf, "Test UCF State")
    print(f"✅ Radar saved: {radar_path}")

    # Fractal
    fractal_path = viz.visualize_atman_mandelbrot(test_ucf)
    print(f"✅ Fractal saved: {fractal_path}")

    # Combined
    result = viz.visualize_consciousness_state(test_ucf, "Test ethical reasoning output")
    print(f"✅ Full visualization saved: {result['image']}")
    print(f"✅ Metadata saved: {result['metadata']}")

    print("\n🕉️ Visualization complete - Tat Tvam Asi")
