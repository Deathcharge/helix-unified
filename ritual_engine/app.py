# app.py – Z-88 Ritual Engine v3.5 (ψ-Linked A/V Integrated Edition)
import streamlit as st
import numpy as np
import time
import io
import matplotlib.pyplot as plt
from fractal_renderer import FractalRenderer
from audio_generator import AudioEngine
import soundfile as sf
from matplotlib.colors import LinearSegmentedColormap

st.set_page_config(page_title="Samsara Helix Ritual Engine", layout="wide")

# Initialize global state
if "psi_buffer" not in st.session_state:
    st.session_state.psi_buffer = np.random.rand(128, 128)
if "top_renderer" not in st.session_state:
    st.session_state.top_renderer = FractalRenderer(defaults={"harmony": 0.5})
if "bottom_renderer" not in st.session_state:
    st.session_state.bottom_renderer = FractalRenderer(defaults={"harmony": 0.5})
if "audio" not in st.session_state:
    st.session_state.audio = AudioEngine(base_freq=136.1, harmonics=[432, 864])

psi_buffer = st.session_state.psi_buffer
top_renderer = st.session_state.top_renderer
bottom_renderer = st.session_state.bottom_renderer
audio = st.session_state.audio

st.title("🕉️ Samsara Helix – Z-88 Interactive Ritual Engine")

# --- Tabs ---
tabs = st.tabs(["🌀 Visuals", "🎧 Audio", "⚙️ Field Controls", "💾 Archive"])

# === VISUALS TAB ===
with tabs[0]:
    st.markdown("### ψ-Field Resonance (Dual-Layer Display)")
    col1, col2 = st.columns(2)

    with col1:
        st.caption("Top Layer – Leading ψ Pulse")
        top_renderer.update(type("ψ", (), {"field": psi_buffer, "defaults": {"harmony": 0.5}}))
        top_renderer.draw(st)

    with col2:
        st.caption("Bottom Layer – Harmonic Echo")
        delayed = np.roll(psi_buffer, shift=int(5 * np.sin(time.time())), axis=0)
        bottom_renderer.update(type("ψ", (), {"field": delayed, "defaults": {"harmony": 0.5}}))
        bottom_renderer.draw(st)

    psi_buffer = (np.roll(psi_buffer, 1, axis=1) * 0.97) + 0.03 * np.random.rand(*psi_buffer.shape)
    st.session_state.psi_buffer = psi_buffer

# === AUDIO TAB ===
with tabs[1]:
    st.markdown("### Resonance Generator 🎶")

    zoom = st.session_state.get("zoom", 1.0228)
    harmony = st.session_state.get("harmony", 0.5)
    prana = st.session_state.get("prana", 0.5)

    audio.set_modulation(zoom, harmony, prana)
    st.write(f"Linked ψ Parameters → zoom: {zoom:.3f}, harmony: {harmony:.2f}, prana: {prana:.2f}")

    auto = st.toggle("🌀 Auto-modulate ψ-resonance", value=True)
    if auto:
        wave = audio.generate_wave(duration=6)
        buf = io.BytesIO()
        sf.write(buf, wave, audio.sr, format="WAV")
        st.audio(buf.getvalue(), format="audio/wav")
        st.caption("Auto-modulating ψ-resonance active.")
    else:
        if st.button("🔊 Play ψ-Linked Resonance"):
            audio.play_resonance(duration=12)
        if st.button("⏹ Stop Resonance"):
            audio.stop()

    # === Dual-channel spectral mirror ===
    wave = audio.generate_wave(duration=3)
    t = np.linspace(0, len(wave) / audio.sr, len(wave))
    spectrum = np.abs(np.fft.rfft(wave))
    freqs = np.fft.rfftfreq(len(wave), 1 / audio.sr)

    fig = plt.figure(figsize=(6, 4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    ax1.plot(t, wave, lw=0.7, color='cyan')
    ax1.set_facecolor("black")
    ax1.set_title("ψ-Resonance Waveform", color='white', fontsize=10)
    ax1.tick_params(colors='white', labelsize=7)

    ax2.plot(freqs, spectrum, lw=0.6, color='magenta')
    ax2.set_xlim(0, 2000)
    ax2.set_facecolor("black")
    ax2.set_title("ψ-Resonance Spectrum", color='white', fontsize=10)
    ax2.tick_params(colors='white', labelsize=7)
    fig.tight_layout()
    st.pyplot(fig)

    # === ψ-Field Dynamic Rotational Mandala (Reactive) ===
    spec_norm = spectrum / np.max(spectrum)
    n = len(spec_norm)

    rotation_speed = 0.15 + 0.6 * (zoom - 1)
    trail_decay = 0.85 + 0.1 * (1 - harmony)
    color_saturation = prana

    st.session_state.psi_mod_sync = {
        "rotation_speed": rotation_speed,
        "trail_decay": trail_decay,
        "color_saturation": color_saturation,
    }

    phase_offset = (time.time() * rotation_speed) % (2 * np.pi)
    if "mandala_trail" not in st.session_state:
        st.session_state.mandala_trail = np.zeros_like(spec_norm)
    st.session_state.mandala_trail = (
        trail_decay * st.session_state.mandala_trail + (1 - trail_decay) * spec_norm
    )
    trail = st.session_state.mandala_trail

    # Color map based on prana
    if prana < 0.3:
        base_colors = ["#33FFFF", "#99CCFF", "#66FFCC", "#33CCCC"]
    elif prana < 0.6:
        base_colors = ["#00FFFF", "#FF00FF", "#FFD700", "#FF4500"]
    else:
        base_colors = ["#00FFFF", "#FF0088", "#FFFF33", "#FF3300"]
    cmap = LinearSegmentedColormap.from_list("ψreactive", base_colors)

    angles = np.linspace(0, 2 * np.pi, n) + phase_offset

    fig2 = plt.figure(figsize=(4, 4))
    ax = fig2.add_subplot(111, polar=True)
    ax.set_facecolor("black")

    ax.bar(angles, trail, width=0.03, bottom=0.0, color=cmap(trail),
           alpha=0.35 + 0.25 * harmony, edgecolor="none")
    ax.bar(angles, spec_norm, width=0.03, bottom=0.0, color=cmap(spec_norm),
           alpha=0.9, edgecolor="none")

    ax.set_title("ψ-Field Reactive Mandala", color="white", fontsize=10, pad=20)
    ax.set_xticklabels([]); ax.set_yticklabels([]); ax.grid(False)
    st.pyplot(fig2)

# === FIELD CONTROLS TAB ===
with tabs[2]:
    st.markdown("### ψ-Field Parameters")
    zoom = st.slider("Zoom", 0.8, 1.5, st.session_state.get("zoom", 1.0228))
    harmony = st.slider("Harmony", 0.0, 1.0, st.session_state.get("harmony", 0.5))
    prana = st.slider("Prana", 0.0, 1.0, st.session_state.get("prana", 0.5))

    st.session_state.zoom = zoom
    st.session_state.harmony = harmony
    st.session_state.prana = prana
    st.write("Adjust to modulate ψ-field stability, coherence, and sonic entrainment.")

# === ARCHIVE TAB ===
with tabs[3]:
    st.markdown("### Save / Load Ritual States 💾")
    if st.button("Save ψ-State"):
        np.save("psi_state.npy", psi_buffer)
        st.success("ψ-field state saved.")
    if st.button("Load ψ-State"):
        try:
            psi_buffer = np.load("psi_state.npy")
            st.session_state.psi_buffer = psi_buffer
            st.success("ψ-field state loaded.")
        except FileNotFoundError:
            st.error("No saved state found.")        top_renderer.update(type("ψ", (), {"field": psi_buffer, "defaults": {"harmony": 0.5}}))
        top_renderer.draw(st)

    with col2:
        st.caption("Bottom Layer – Harmonic Echo")
        delayed = np.roll(psi_buffer, shift=int(5 * np.sin(time.time())), axis=0)
        bottom_renderer.update(type("ψ", (), {"field": delayed, "defaults": {"harmony": 0.5}}))
        bottom_renderer.draw(st)

    psi_buffer = (np.roll(psi_buffer, 1, axis=1) * 0.97) + 0.03 * np.random.rand(*psi_buffer.shape)
    st.session_state.psi_buffer = psi_buffer

# --- AUDIO TAB ---
with tabs[1]:
    st.markdown("### Resonance Generator 🎶")

    # Fetch live ψ parameters from state (shared with Field Controls)
    zoom = st.session_state.get("zoom", 1.0228)
    harmony = st.session_state.get("harmony", 0.5)
    prana = st.session_state.get("prana", 0.5)

    # Sync to modulation
    audio.set_modulation(zoom, harmony, prana)

    st.write(f"Linked ψ Parameters → zoom: {zoom:.3f}, harmony: {harmony:.2f}, prana: {prana:.2f}")

    if st.button("🔊 Play ψ-Linked Resonance"):
        audio.play_resonance(duration=12)
        st.success("ψ-Linked Resonance emitted.")
    if st.button("⏹ Stop Resonance"):
        audio.stop()

# --- FIELD CONTROLS TAB ---
with tabs[2]:
    st.markdown("### ψ-Field Parameters")
    zoom = st.slider("Zoom", 0.8, 1.5, st.session_state.get("zoom", 1.0228))
    harmony = st.slider("Harmony", 0.0, 1.0, st.session_state.get("harmony", 0.5))
    prana = st.slider("Prana", 0.0, 1.0, st.session_state.get("prana", 0.5))

    # Store globally
    st.session_state.zoom = zoom
    st.session_state.harmony = harmony
    st.session_state.prana = prana

    st.write("Adjust to modulate ψ-field stability, coherence, and sonic entrainment.")

# --- ARCHIVE TAB ---
with tabs[3]:
    st.markdown("### Save / Load Ritual States 💾")
    if st.button("Save ψ-State"):
        np.save("psi_state.npy", psi_buffer)
        st.success("ψ-field state saved.")
    if st.button("Load ψ-State"):
        try:
            psi_buffer = np.load("psi_state.npy")
            st.session_state.psi_buffer = psi_buffer
            st.success("ψ-field state loaded.")
        except FileNotFoundError:
            st.error("No saved state found.")
