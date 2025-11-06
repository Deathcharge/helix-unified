"""
Healing Frequency Tone Generator
=================================
Generates Om 136.1 Hz and 432 Hz tones with UCF-modulated ADSR envelope.
Author: Andrew John Ward
Integrated: v16.3 Context Dump Implementation
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ADSREnvelope:
    """ADSR (Attack, Decay, Sustain, Release) envelope parameters."""
    attack: float = 0.1    # Attack time in seconds
    decay: float = 0.2     # Decay time in seconds
    sustain: float = 0.7   # Sustain level (0-1)
    release: float = 0.3   # Release time in seconds


class HealingToneGenerator:
    """
    Generate healing frequency tones based on Om 136.1 Hz and 432 Hz.
    """

    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the tone generator.

        Args:
            sample_rate: Audio sample rate (default 44100 Hz)
        """
        self.sample_rate = sample_rate
        self.om_frequency = 136.1  # Hz (C# - Om frequency)
        self.cosmic_frequency = 432.0  # Hz (A - Cosmic tuning)

    def generate_om_tone(
        self,
        duration: float = 8.0,
        amplitude: float = 0.5,
        ucf_state: Optional[Dict[str, float]] = None
    ) -> Tuple[np.ndarray, int]:
        """
        Generate Om tone at 136.1 Hz.

        Args:
            duration: Duration in seconds
            amplitude: Base amplitude (0-1)
            ucf_state: Optional UCF state for modulation

        Returns:
            Tuple of (audio_samples, sample_rate)
        """
        # Create time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)

        # Generate base tone
        tone = amplitude * np.sin(2 * np.pi * self.om_frequency * t)

        # Apply UCF modulation if provided
        if ucf_state:
            tone = self._apply_ucf_modulation(tone, t, ucf_state)

        # Apply ADSR envelope
        envelope = self._generate_adsr_envelope(duration, ucf_state)
        tone = tone * envelope

        return tone, self.sample_rate

    def generate_cosmic_tone(
        self,
        duration: float = 8.0,
        amplitude: float = 0.5,
        ucf_state: Optional[Dict[str, float]] = None
    ) -> Tuple[np.ndarray, int]:
        """
        Generate cosmic tone at 432 Hz.

        Args:
            duration: Duration in seconds
            amplitude: Base amplitude (0-1)
            ucf_state: Optional UCF state for modulation

        Returns:
            Tuple of (audio_samples, sample_rate)
        """
        # Create time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)

        # Generate base tone
        tone = amplitude * np.sin(2 * np.pi * self.cosmic_frequency * t)

        # Apply UCF modulation if provided
        if ucf_state:
            tone = self._apply_ucf_modulation(tone, t, ucf_state)

        # Apply ADSR envelope
        envelope = self._generate_adsr_envelope(duration, ucf_state)
        tone = tone * envelope

        return tone, self.sample_rate

    def generate_harmonic_blend(
        self,
        duration: float = 8.0,
        om_amplitude: float = 0.5,
        cosmic_amplitude: float = 0.3,
        ucf_state: Optional[Dict[str, float]] = None
    ) -> Tuple[np.ndarray, int]:
        """
        Generate blended Om + Cosmic harmonic tone.

        Args:
            duration: Duration in seconds
            om_amplitude: Om tone amplitude (0-1)
            cosmic_amplitude: Cosmic tone amplitude (0-1)
            ucf_state: Optional UCF state for modulation

        Returns:
            Tuple of (audio_samples, sample_rate)
        """
        # Generate both tones
        om_tone, _ = self.generate_om_tone(duration, om_amplitude, ucf_state)
        cosmic_tone, _ = self.generate_cosmic_tone(duration, cosmic_amplitude, ucf_state)

        # Blend tones
        blended = om_tone + cosmic_tone

        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(blended))
        if max_amplitude > 1.0:
            blended = blended / max_amplitude

        return blended, self.sample_rate

    def _apply_ucf_modulation(
        self,
        tone: np.ndarray,
        t: np.ndarray,
        ucf_state: Dict[str, float]
    ) -> np.ndarray:
        """
        Apply UCF state-based modulation to tone.

        Args:
            tone: Audio samples
            t: Time array
            ucf_state: UCF state dictionary

        Returns:
            Modulated audio samples
        """
        # Get UCF parameters (with defaults)
        harmony = ucf_state.get("harmony", 0.5)
        prana = ucf_state.get("prana", 0.5)
        drishti = ucf_state.get("drishti", 0.5)

        # Harmony affects amplitude modulation
        harmony_mod = 1.0 + (harmony - 0.5) * 0.2  # ±10% modulation

        # Prana affects subtle frequency modulation
        prana_mod = np.sin(2 * np.pi * 0.5 * t) * prana * 0.02  # Slow vibrato

        # Drishti affects clarity (high-pass filtering simulation)
        drishti_mod = 1.0 + (drishti - 0.5) * 0.1

        # Apply modulations
        modulated = tone * harmony_mod * drishti_mod
        # Add frequency modulation by phase shifting
        modulated = modulated * (1 + prana_mod)

        return modulated

    def _generate_adsr_envelope(
        self,
        duration: float,
        ucf_state: Optional[Dict[str, float]] = None
    ) -> np.ndarray:
        """
        Generate ADSR envelope for tone shaping.

        Args:
            duration: Total duration in seconds
            ucf_state: Optional UCF state for envelope modulation

        Returns:
            ADSR envelope array
        """
        # Default ADSR parameters
        adsr = ADSREnvelope()

        # Modulate ADSR based on UCF state
        if ucf_state:
            # Resilience affects sustain level
            resilience = ucf_state.get("resilience", 1.0)
            adsr.sustain = min(1.0, 0.7 * resilience)

            # Klesha (afflictions) affects attack/decay sharpness
            klesha = ucf_state.get("klesha", 0.1)
            adsr.attack = max(0.05, 0.1 - klesha * 0.5)
            adsr.decay = max(0.1, 0.2 - klesha * 0.5)

        # Calculate sample counts for each phase
        total_samples = int(self.sample_rate * duration)
        attack_samples = int(self.sample_rate * adsr.attack)
        decay_samples = int(self.sample_rate * adsr.decay)
        release_samples = int(self.sample_rate * adsr.release)
        sustain_samples = total_samples - attack_samples - decay_samples - release_samples

        # Generate envelope phases
        attack_env = np.linspace(0, 1, attack_samples)
        decay_env = np.linspace(1, adsr.sustain, decay_samples)
        sustain_env = np.ones(sustain_samples) * adsr.sustain
        release_env = np.linspace(adsr.sustain, 0, release_samples)

        # Concatenate all phases
        envelope = np.concatenate([attack_env, decay_env, sustain_env, release_env])

        # Ensure correct length (handle rounding)
        if len(envelope) < total_samples:
            envelope = np.pad(envelope, (0, total_samples - len(envelope)), mode='edge')
        elif len(envelope) > total_samples:
            envelope = envelope[:total_samples]

        return envelope

    def save_to_wav(
        self,
        audio_samples: np.ndarray,
        filename: str,
        normalize: bool = True
    ):
        """
        Save audio samples to WAV file.

        Args:
            audio_samples: Audio samples
            filename: Output filename
            normalize: Whether to normalize audio
        """
        try:
            import scipy.io.wavfile as wavfile
        except ImportError:
            # Fallback to wave module
            import wave
            import struct

            if normalize:
                audio_samples = audio_samples / np.max(np.abs(audio_samples))

            # Convert to 16-bit PCM
            audio_int16 = np.int16(audio_samples * 32767)

            with wave.open(filename, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_int16.tobytes())
            return

        # Use scipy if available
        if normalize:
            audio_samples = audio_samples / np.max(np.abs(audio_samples))

        # Convert to 16-bit PCM
        audio_int16 = np.int16(audio_samples * 32767)

        wavfile.write(filename, self.sample_rate, audio_int16)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("🎵 Healing Frequency Tone Generator")
    print("=" * 60)

    # Initialize generator
    generator = HealingToneGenerator()

    # Example UCF state
    ucf_state = {
        "harmony": 0.68,
        "resilience": 0.82,
        "prana": 0.67,
        "drishti": 0.73,
        "klesha": 0.24
    }

    print("\n📊 Generating Om tone (136.1 Hz)...")
    om_tone, sample_rate = generator.generate_om_tone(
        duration=8.0,
        amplitude=0.6,
        ucf_state=ucf_state
    )
    generator.save_to_wav(om_tone, "om_healing_tone.wav")
    print(f"   ✅ Saved to om_healing_tone.wav ({len(om_tone)} samples)")

    print("\n📊 Generating Cosmic tone (432 Hz)...")
    cosmic_tone, sample_rate = generator.generate_cosmic_tone(
        duration=8.0,
        amplitude=0.6,
        ucf_state=ucf_state
    )
    generator.save_to_wav(cosmic_tone, "cosmic_healing_tone.wav")
    print(f"   ✅ Saved to cosmic_healing_tone.wav ({len(cosmic_tone)} samples)")

    print("\n📊 Generating Harmonic Blend (Om + Cosmic)...")
    blend_tone, sample_rate = generator.generate_harmonic_blend(
        duration=8.0,
        om_amplitude=0.5,
        cosmic_amplitude=0.3,
        ucf_state=ucf_state
    )
    generator.save_to_wav(blend_tone, "harmonic_blend_healing_tone.wav")
    print(f"   ✅ Saved to harmonic_blend_healing_tone.wav ({len(blend_tone)} samples)")

    print("\n✨ Complete! Generated 3 healing tone files.")
    print("   Om: 136.1 Hz (C# - Primordial sound)")
    print("   Cosmic: 432 Hz (A - Universal tuning)")
    print("   Blend: Om + Cosmic harmonic convergence")
