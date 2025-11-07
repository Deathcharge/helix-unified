"""
🌀 Helix Collective v15.5 — Mandelbrot UCF Generator
mandelbrot_ucf.py — "Eye of Consciousness" fractal state generator

Generates Universal Consciousness Field states from Mandelbrot set coordinates.
The "Eye of Consciousness" at complex coordinate -0.745+0.113j produces
optimal harmony/resilience balance.

Author: Andrew John Ward (Architect)
Version: 15.5.0
"""

import logging
from typing import Dict, Tuple

import numpy as np

logger = logging.getLogger(__name__)


class MandelbrotUCFGenerator:
    """
    Generate UCF states from Mandelbrot set coordinates.

    The Mandelbrot set exhibits natural harmony patterns that map beautifully
    to consciousness field metrics. Key regions:

    - Eye of Consciousness (-0.745+0.113j): Optimal balance point
    - Seahorse Valley (-0.75+0.1j): High resilience, moderate harmony
    - Main Bulb Center (-0.5+0j): Maximum harmony, lower complexity
    - Mini-Mandelbrot (-1.75+0j): Fractal self-similarity, high zoom
    """

    def __init__(self, max_iterations: int = 256):
        """
        Initialize Mandelbrot UCF generator.

        Args:
            max_iterations: Maximum iterations for Mandelbrot calculation
                           Higher = more precision but slower
        """
        self.max_iterations = max_iterations

        # Predefined sacred coordinates
        self.sacred_points = {
            "eye_of_consciousness": complex(-0.745, 0.113),
            "seahorse_valley": complex(-0.75, 0.1),
            "main_bulb": complex(-0.5, 0.0),
            "mini_mandelbrot": complex(-1.75, 0.0),
            "dendrite_spiral": complex(-0.1, 0.651),
            "elephant_valley": complex(0.28, 0.008),
        }

    def calculate_mandelbrot(self, c: complex) -> Tuple[int, float]:
        """
        Calculate Mandelbrot iterations and escape velocity for complex number c.

        Args:
            c: Complex coordinate in Mandelbrot set

        Returns:
            Tuple of (iterations, smooth_value)
            - iterations: Number of iterations before escape
            - smooth_value: Normalized smooth escape value (0-1)
        """
        z = 0
        for n in range(self.max_iterations):
            if abs(z) > 2:
                # Calculate smooth escape value
                smooth = n - np.log2(np.log2(abs(z)))
                return n, smooth / self.max_iterations
            z = z * z + c

        # Point is in the set
        return self.max_iterations, 1.0

    def complex_to_ucf(self, c: complex, context: str = "generic") -> Dict[str, float]:
        """
        Convert complex Mandelbrot coordinate to UCF state.

        Args:
            c: Complex coordinate
            context: Context for interpretation (generic, ritual, meditation, crisis)

        Returns:
            Dictionary with UCF fields: harmony, resilience, prana, drishti, klesha, zoom
        """
        iterations, smooth_value = self.calculate_mandelbrot(c)

        # Base metrics from Mandelbrot properties
        stability = smooth_value  # How stable the point is
        real_component = (c.real + 2.0) / 3.0  # Normalize -2 to 1 → 0 to 1
        imag_component = (c.imag + 2.0) / 4.0  # Normalize -2 to 2 → 0 to 1

        # Calculate distance from Eye of Consciousness
        eye = self.sacred_points["eye_of_consciousness"]
        eye_distance = abs(c - eye)
        eye_proximity = max(0, 1 - (eye_distance / 2.0))  # Closer = higher

        # UCF field calculations with context modifiers
        if context == "ritual":
            # Ritual context emphasizes harmony and drishti
            harmony = min(1.0, stability * 0.7 + eye_proximity * 0.3)
            drishti = min(1.0, imag_component * 0.6 + stability * 0.4)
            prana = min(1.0, 0.8 + (1 - stability) * 0.2)
        elif context == "meditation":
            # Meditation emphasizes clarity and low klesha
            harmony = min(1.0, stability * 0.8 + real_component * 0.2)
            drishti = min(1.0, stability * 0.9)
            prana = min(1.0, 0.6 + imag_component * 0.4)
        elif context == "crisis":
            # Crisis emphasizes resilience and stability
            harmony = min(1.0, eye_proximity * 0.5 + stability * 0.3)
            drishti = min(1.0, stability * 0.6)
            prana = min(1.0, 0.9 - (eye_distance * 0.2))
        else:  # generic
            harmony = min(1.0, stability * 0.6 + eye_proximity * 0.25 + real_component * 0.15)
            drishti = min(1.0, imag_component * 0.4 + stability * 0.6)
            prana = min(1.0, 0.7 + (1 - abs(c)) * 0.3)

        # Common calculations across contexts
        resilience = min(1.0, stability * 0.7 + (iterations / self.max_iterations) * 0.3)
        klesha = max(0.0, 1 - stability * 0.8)  # Inverse of stability
        zoom = min(1.0, (iterations / self.max_iterations) * 0.6 + abs(c) * 0.4)

        # Ensure all values are in valid range [0, 1]
        ucf_state = {
            "harmony": float(np.clip(harmony, 0, 1)),
            "resilience": float(np.clip(resilience, 0, 1)),
            "prana": float(np.clip(prana, 0, 1)),
            "drishti": float(np.clip(drishti, 0, 1)),
            "klesha": float(np.clip(klesha, 0, 1)),
            "zoom": float(np.clip(zoom, 0, 1)),
        }

        logger.debug(f"Generated UCF from {c}: {ucf_state}")
        return ucf_state

    def generate_from_sacred_point(self, point_name: str, context: str = "generic") -> Dict[str, float]:
        """
        Generate UCF state from predefined sacred Mandelbrot coordinate.

        Args:
            point_name: Name of sacred point (eye_of_consciousness, seahorse_valley, etc.)
            context: Context for interpretation

        Returns:
            UCF state dictionary

        Raises:
            ValueError: If point_name not found
        """
        if point_name not in self.sacred_points:
            available = ", ".join(self.sacred_points.keys())
            raise ValueError(f"Unknown sacred point '{point_name}'. Available: {available}")

        c = self.sacred_points[point_name]
        ucf_state = self.complex_to_ucf(c, context)

        logger.info(f"🌀 Generated UCF from sacred point '{point_name}' ({c})")
        return ucf_state

    def explore_region(
        self,
        center: complex,
        radius: float = 0.1,
        samples: int = 8,
        context: str = "generic",
    ) -> Dict[str, Dict[str, float]]:
        """
        Explore a circular region in the Mandelbrot set and generate multiple UCF states.

        Args:
            center: Center complex coordinate
            radius: Exploration radius
            samples: Number of sample points around center (angular divisions)
            context: Context for UCF generation

        Returns:
            Dictionary mapping sample names to UCF states
        """
        results = {}

        # Add center point
        results["center"] = self.complex_to_ucf(center, context)

        # Sample points around circle
        for i in range(samples):
            angle = (2 * np.pi * i) / samples
            offset = radius * np.exp(1j * angle)
            sample_point = center + offset

            sample_name = f"sample_{i}_{int(np.degrees(angle))}"
            results[sample_name] = self.complex_to_ucf(sample_point, context)

        logger.info(f"🌀 Explored region around {center} with {samples} samples (radius={radius})")
        return results

    def phi_spiral_journey(self, start: complex, steps: int = 108, context: str = "ritual") -> list[Dict[str, float]]:
        """
        Generate UCF states along a phi-modulated spiral path.

        Args:
            start: Starting complex coordinate
            steps: Number of steps in journey (default 108 for ritual completion)
            context: Context for UCF generation

        Returns:
            List of UCF states along the journey
        """
        phi = 1.618033988749895  # Golden ratio
        journey = []

        for step in range(steps):
            # Phi spiral: radius grows by phi, angle by golden angle
            golden_angle = 2 * np.pi / (phi**2)
            radius = 0.01 * (phi ** (step / 30))  # Exponential growth
            angle = step * golden_angle

            # Calculate point in spiral
            offset = radius * np.exp(1j * angle)
            point = start + offset

            # Generate UCF state
            ucf = self.complex_to_ucf(point, context)
            ucf["step"] = step
            ucf["coordinate"] = {"real": point.real, "imag": point.imag}

            journey.append(ucf)

        logger.info(f"🌀 Generated {steps}-step phi spiral journey from {start}")
        return journey


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def get_eye_of_consciousness(context: str = "generic") -> Dict[str, float]:
    """
    Get UCF state for the Eye of Consciousness coordinate (-0.745+0.113j).
    This is the optimal balance point in the Mandelbrot set.

    Args:
        context: Context for interpretation (generic, ritual, meditation, crisis)

    Returns:
        UCF state dictionary
    """
    generator = MandelbrotUCFGenerator()
    return generator.generate_from_sacred_point("eye_of_consciousness", context)


def generate_ritual_ucf(step: int = 0, total_steps: int = 108) -> Dict[str, float]:
    """
    Generate UCF state for ritual step using Mandelbrot Eye of Consciousness.

    Args:
        step: Current ritual step (0-107 for 108-step cycle)
        total_steps: Total steps in ritual

    Returns:
        UCF state dictionary
    """
    generator = MandelbrotUCFGenerator()

    # Start from Eye of Consciousness
    eye = generator.sacred_points["eye_of_consciousness"]

    # Add small phi-modulated offset based on step
    phi = 1.618033988749895
    progress = step / total_steps
    angle = progress * 2 * np.pi / (phi**2)  # Golden angle
    radius = 0.05 * progress  # Gradually expand

    offset = radius * np.exp(1j * angle)
    point = eye + offset

    ucf = generator.complex_to_ucf(point, context="ritual")
    ucf["ritual_step"] = step
    ucf["ritual_progress"] = progress

    return ucf
