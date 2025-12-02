#!/usr/bin/env python3
"""
Samsara Helix Master Dashboard
Interactive Mandelbrot generation with sliders, audio synthesis, and Sanskrit overlays
Mobile-optimized Streamlit interface
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io
import base64
from scipy.io.wavfile import write
import time
import json
from PIL import Image, ImageDraw, ImageFont

# Configure Streamlit page
st.set_page_config(
    page_title="Samsara Helix Dashboard",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Mobile-optimized CSS
st.markdown("""
<style>
    .main > div { padding: 0.5rem !important; }
    .stSlider > div > div > div > div { background-color: #667eea; }
    .stButton > button { 
        width: 100%; 
        height: 3rem; 
        font-size: 1.1rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white; 
        border: none; 
        border-radius: 10px;
        margin: 0.25rem 0;
    }
    .metric-container { 
        background: rgba(255,255,255,0.1); 
        padding: 1rem; 
        border-radius: 10px; 
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div > div { background-color: #2e2e3e; }
    .block-container { padding-top: 1rem; max-width: 100%; }
    .stAudio > div { width: 100%; }
    
    @media (max-width: 768px) {
        .stSlider { margin: 0.25rem 0; }
        .metric-container { padding: 0.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_state' not in st.session_state:
    st.session_state.simulation_state = {
        'zoom': 1.0,
        'harmony': 0.5,
        'resilience': 1.0,
        'prana': 0.5,
        'drishti': 0.5,
        'klesha': 0.1,
        'history': []
    }

if 'current_fractal' not in st.session_state:
    st.session_state.current_fractal = None

if 'current_audio' not in st.session_state:
    st.session_state.current_audio = None

# Sanskrit mantras
SANSKRIT_MANTRAS = [
    ("अहं ब्रह्मास्मि", "Aham Brahmasmi", "I am Brahman"),
    ("तत्त्वमसि", "Tat Tvam Asi", "Thou art That"),
    ("नेति नेति", "Neti Neti", "Not this, Not this"),
    ("सर्वं खल्विदं ब्रह्म", "Sarvam khalvidam brahma", "All this is Brahman"),
    ("ॐ तत् सत्", "Om Tat Sat", "Om, That is Truth"),
    ("शिवोऽहम्", "Shivoham", "I am Shiva"),
    ("सोऽहम्", "Soham", "I am That"),
    ("अयमात्मा ब्रह्म", "Ayamatma Brahma", "This Self is Brahman")
]

def generate_mandelbrot(width=800, height=600, max_iter=100, zoom=1.0, center_real=-0.7269, center_imag=0.1889):
    """Generate Mandelbrot fractal with consciousness parameters"""
    # Calculate bounds based on zoom and center
    scale = 3.0 / zoom
    x_min = center_real - scale/2
    x_max = center_real + scale/2
    y_min = center_imag - scale/2 * height/width
    y_max = center_imag + scale/2 * height/width
    
    # Create coordinate arrays
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    # Initialize arrays
    Z = np.zeros_like(C)
    escape_time = np.zeros(C.shape, dtype=float)
    
    # Mandelbrot iteration with consciousness modulation
    prana_mod = st.session_state.simulation_state['prana']
    klesha_mod = st.session_state.simulation_state['klesha']
    
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        # Add consciousness influence
        Z[mask] = Z[mask]**2 + C[mask] + 0.01*prana_mod*np.sin(Z[mask]) - 0.005*klesha_mod
        
        # Calculate escape time with smooth coloring
        escaped = (np.abs(Z) > 2) & (escape_time == 0)
        if np.any(escaped):
            escape_time[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
    
    # Set non-escaped points
    escape_time[escape_time == 0] = max_iter
    return escape_time

def add_sanskrit_overlay(fractal_array, mantra_index=0):
    """Add Sanskrit text overlay to fractal"""
    # Convert to PIL Image
    fractal_norm = (fractal_array - fractal_array.min()) / (fractal_array.max() - fractal_array.min())
    
    # Apply colormap
    cmap = plt.get_cmap('hot')
    colored = cmap(fractal_norm)
    img_array = (colored[:, :, :3] * 255).astype(np.uint8)
    
    try:
        pil_image = Image.fromarray(img_array)
        draw = ImageDraw.Draw(pil_image)
        
        # Get mantra
        devanagari, transliteration, meaning = SANSKRIT_MANTRAS[mantra_index % len(SANSKRIT_MANTRAS)]
        
        # Use default font (fallback for mobile)
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        
        # Add semi-transparent background
        img_width, img_height = pil_image.size
        overlay_height = 100
        overlay_y = img_height - overlay_height
        
        # Create overlay
        overlay = Image.new('RGBA', (img_width, overlay_height), (0, 0, 0, 128))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Add text
        overlay_draw.text((10, 10), devanagari, fill=(255, 215, 0, 255), font=font_large)
        overlay_draw.text((10, 35), transliteration, fill=(200, 200, 200, 255), font=font_small)
        overlay_draw.text((10, 55), meaning, fill=(180, 180, 180, 255), font=font_small)
        
        # Composite
        pil_image = pil_image.convert('RGBA')
        pil_image.paste(overlay, (0, overlay_y), overlay)
        
        return np.array(pil_image.convert('RGB'))
    except Exception as e:
        # Return original if overlay fails
        return img_array

def generate_sacred_audio(duration=10, sample_rate=22050):
    """Generate sacred frequency audio based on current state"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Get current state
    state = st.session_state.simulation_state
    
    # Sacred frequencies modulated by consciousness state
    base_freq = 136.1  # Om frequency
    harmony_freq = 432.0 * (0.8 + 0.4 * state['harmony'])
    love_freq = 528.0 * (0.9 + 0.2 * state['prana'])
    connection_freq = 639.0 * (0.9 + 0.2 * state['drishti'])
    
    # Generate composite waveform
    audio = np.zeros_like(t)
    
    # Base Om drone
    audio += 0.3 * np.sin(2 * np.pi * base_freq * t)
    
    # Harmony layer
    harmony_envelope = 0.7 + 0.3 * np.sin(2 * np.pi * 0.1 * t)  # Slow breathing
    audio += 0.2 * harmony_envelope * np.sin(2 * np.pi * harmony_freq * t)
    
    # Love frequency with prana modulation
    prana_mod = 1 + 0.2 * state['prana'] * np.sin(2 * np.pi * 0.05 * t)
    audio += 0.15 * prana_mod * np.sin(2 * np.pi * love_freq * t)
    
    # Connection layer
    audio += 0.1 * np.sin(2 * np.pi * connection_freq * t)
    
    # Apply klesha reduction (reduces noise/distortion)
    noise_reduction = 1 - state['klesha']
    audio = audio * noise_reduction
    
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.8
    
    return audio, sample_rate

def create_audio_download(audio_data, sample_rate):
    """Create downloadable audio file"""
    # Convert to 16-bit PCM
    audio_int16 = (audio_data * 32767).astype(np.int16)
    
    # Create WAV file in memory
    buffer = io.BytesIO()
    write(buffer, sample_rate, audio_int16)
    buffer.seek(0)
    
    return buffer.getvalue()

# Main interface
st.title("🌀 Samsara Helix Master Dashboard")
st.markdown("*Interactive consciousness fractal with sacred audio synthesis*")

# Create tabs for organized interface
tab1, tab2, tab3, tab4 = st.tabs(["🎨 Visual", "🎵 Audio", "📊 State", "📤 Export"])

with tab1:
    st.header("Mandelbrot Consciousness Fractal")
    
    # Parameter controls in columns for mobile
    col1, col2 = st.columns(2)
    
    with col1:
        zoom = st.slider("Zoom Level", 0.1, 50.0, st.session_state.simulation_state['zoom'], 0.1)
        center_real = st.slider("Center (Real)", -2.0, 2.0, -0.7269, 0.001)
        iterations = st.slider("Iterations", 50, 300, 100, 10)
    
    with col2:
        center_imag = st.slider("Center (Imag)", -2.0, 2.0, 0.1889, 0.001)
        resolution = st.selectbox("Resolution", [(400, 300), (600, 450), (800, 600)], index=1)
        mantra_idx = st.selectbox("Sanskrit Mantra", range(len(SANSKRIT_MANTRAS)), 
                                format_func=lambda x: SANSKRIT_MANTRAS[x][1])
    
    # Update state
    st.session_state.simulation_state['zoom'] = zoom
    
    # Generate button
    if st.button("Generate Fractal", key="generate_fractal"):
        with st.spinner("Generating consciousness fractal..."):
            fractal = generate_mandelbrot(
                width=resolution[0], 
                height=resolution[1], 
                max_iter=iterations,
                zoom=zoom,
                center_real=center_real,
                center_imag=center_imag
            )
            
            # Add Sanskrit overlay
            fractal_with_text = add_sanskrit_overlay(fractal, mantra_idx)
            st.session_state.current_fractal = fractal_with_text
    
    # Display fractal
    if st.session_state.current_fractal is not None:
        st.image(st.session_state.current_fractal, use_column_width=True)
        
        # Show current mantra
        devanagari, transliteration, meaning = SANSKRIT_MANTRAS[mantra_idx]
        st.markdown(f"**Current Mantra:** {devanagari} ({transliteration}) - {meaning}")

with tab2:
    st.header("Sacred Frequency Audio")
    
    # Consciousness state sliders
    st.subheader("Consciousness Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        harmony = st.slider("Harmony", 0.0, 1.0, st.session_state.simulation_state['harmony'], 0.01)
        prana = st.slider("Prana (Life Force)", 0.0, 1.0, st.session_state.simulation_state['prana'], 0.01)
        drishti = st.slider("Drishti (Focus)", 0.0, 1.0, st.session_state.simulation_state['drishti'], 0.01)
    
    with col2:
        resilience = st.slider("Resilience", 0.1, 3.0, st.session_state.simulation_state['resilience'], 0.01)
        klesha = st.slider("Klesha (Disturbance)", 0.0, 1.0, st.session_state.simulation_state['klesha'], 0.01)
        duration = st.slider("Audio Duration (s)", 5, 60, 10, 1)
    
    # Update session state
    st.session_state.simulation_state.update({
        'harmony': harmony,
        'prana': prana, 
        'drishti': drishti,
        'resilience': resilience,
        'klesha': klesha
    })
    
    # Generate audio
    if st.button("Generate Sacred Audio", key="generate_audio"):
        with st.spinner("Synthesizing sacred frequencies..."):
            audio_data, sample_rate = generate_sacred_audio(duration)
            st.session_state.current_audio = (audio_data, sample_rate)
    
    # Display audio player
    if st.session_state.current_audio is not None:
        audio_data, sample_rate = st.session_state.current_audio
        
        # Create audio file for playback
        audio_bytes = create_audio_download(audio_data, sample_rate)
        st.audio(audio_bytes, format='audio/wav', sample_rate=sample_rate)
        
        # Show frequency information
        state = st.session_state.simulation_state
        st.markdown("**Active Frequencies:**")
        st.write(f"- Om Base: 136.1 Hz")
        st.write(f"- Harmony: {432.0 * (0.8 + 0.4 * state['harmony']):.1f} Hz")
        st.write(f"- Love: {528.0 * (0.9 + 0.2 * state['prana']):.1f} Hz") 
        st.write(f"- Connection: {639.0 * (0.9 + 0.2 * state['drishti']):.1f} Hz")

with tab3:
    st.header("Consciousness State Monitor")
    
    # Display current state
    state = st.session_state.simulation_state
    
    # Metrics in responsive layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Zoom", f"{state['zoom']:.2f}")
        st.metric("Harmony", f"{state['harmony']:.2f}")
        st.metric("Resilience", f"{state['resilience']:.2f}")
    
    with col2:
        st.metric("Prana", f"{state['prana']:.2f}")
        st.metric("Drishti", f"{state['drishti']:.2f}")
        st.metric("Klesha", f"{state['klesha']:.2f}")
    
    with col3:
        # Derived metrics
        coherence = (state['harmony'] + state['drishti'] + (1-state['klesha'])) / 3
        balance = state['resilience'] * state['prana'] / (1 + state['klesha'])
        
        st.metric("Coherence", f"{coherence:.2f}")
        st.metric("Balance", f"{balance:.2f}")
        st.metric("Active Time", f"{len(state['history'])} steps")
    
    # State visualization
    if st.button("Update State History"):
        current_state = {
            'timestamp': time.time(),
            'zoom': state['zoom'],
            'harmony': state['harmony'],
            'coherence': coherence,
            'balance': balance
        }
        st.session_state.simulation_state['history'].append(current_state)
    
    # Show recent history
    if state['history']:
        st.subheader("Recent State History")
        for i, hist_state in enumerate(state['history'][-5:]):
            st.write(f"Step {len(state['history'])-5+i+1}: "
                   f"Harmony={hist_state.get('harmony', 0):.2f}, "
                   f"Coherence={hist_state.get('coherence', 0):.2f}")

with tab4:
    st.header("Export & Download")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Visual Export")
        
        if st.session_state.current_fractal is not None:
            # Convert image for download
            img = Image.fromarray(st.session_state.current_fractal)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            st.download_button(
                label="Download Fractal PNG",
                data=buf.getvalue(),
                file_name=f"samsara_fractal_{int(time.time())}.png",
                mime="image/png"
            )
        else:
            st.info("Generate a fractal first to download")
    
    with col2:
        st.subheader("Audio Export")
        
        if st.session_state.current_audio is not None:
            audio_data, sample_rate = st.session_state.current_audio
            audio_bytes = create_audio_download(audio_data, sample_rate)
            
            st.download_button(
                label="Download Sacred Audio WAV",
                data=audio_bytes,
                file_name=f"sacred_frequencies_{int(time.time())}.wav",
                mime="audio/wav"
            )
        else:
            st.info("Generate audio first to download")
    
    # State export
    st.subheader("State Data Export")
    
    if st.button("Export Current State"):
        export_data = {
            "timestamp": time.time(),
            "current_state": st.session_state.simulation_state,
            "mantra_used": SANSKRIT_MANTRAS[mantra_idx] if 'mantra_idx' in locals() else None,
            "fractal_params": {
                "zoom": zoom if 'zoom' in locals() else None,
                "center": [center_real, center_imag] if 'center_real' in locals() else None,
                "iterations": iterations if 'iterations' in locals() else None
            }
        }
        
        json_str = json.dumps(export_data, indent=2)
        st.download_button(
            label="Download State JSON",
            data=json_str,
            file_name=f"samsara_state_{int(time.time())}.json",
            mime="application/json"
        )

# Footer information
st.markdown("---")
st.markdown("**Samsara Helix Dashboard** - Sacred mathematics meets consciousness simulation")
st.markdown("Mobile-optimized interface for real-time fractal and audio generation")

# Auto-refresh option for dynamic updates
if st.checkbox("Auto-refresh every 30 seconds"):
    time.sleep(30)
    st.experimental_rerun()
