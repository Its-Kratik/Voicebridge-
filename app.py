import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import time
from datetime import datetime
import wave
import tempfile
import os

# Configure page
st.set_page_config(
    page_title="VoiceBridge",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .language-toggle {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 2rem 0;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    
    .processing-animation {
        text-align: center;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .audio-controls {
        display: flex;
        gap: 10px;
        margin: 1rem 0;
    }
    
    .footer-info {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 3rem;
        font-size: 0.9rem;
        color: #555;
    }
    
    .text-display {
        background: #fff;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        min-height: 60px;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 0.75rem;
        margin: 1rem 0;
        color: #155724;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 0.75rem;
        margin: 1rem 0;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'current_audio_input' not in st.session_state:
    st.session_state.current_audio_input = None
if 'current_transcription' not in st.session_state:
    st.session_state.current_transcription = ""
if 'current_translation' not in st.session_state:
    st.session_state.current_translation = ""
if 'current_audio_output' not in st.session_state:
    st.session_state.current_audio_output = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Helper functions
def generate_waveform(audio_data, title="Audio Waveform"):
    """Generate a waveform visualization"""
    fig, ax = plt.subplots(figsize=(10, 2))
    if audio_data is not None:
        # Simulate audio waveform (replace with actual audio processing)
        time_axis = np.linspace(0, len(audio_data) / 16000, len(audio_data))
        ax.plot(time_axis, audio_data, color='#3498db', linewidth=0.8)
    else:
        # Generate sample waveform for demo
        t = np.linspace(0, 2, 32000)
        waveform = np.sin(2 * np.pi * 440 * t) * np.exp(-t/2)
        ax.plot(t, waveform, color='#3498db', linewidth=0.8)
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def mock_speech_to_text(audio_data, language):
    """Mock STT function - replace with actual Whisper implementation"""
    time.sleep(2)  # Simulate processing time
    
    if language == "Sanskrit":
        return "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।"
    else:
        return "भगवद्गीता का यह श्लोक बहुत प्रसिद्ध है।"

def mock_translate(text, source_lang, target_lang):
    """Mock translation function - replace with actual IndicTrans2 implementation"""
    time.sleep(1.5)  # Simulate processing time
    
    if source_lang == "Sanskrit" and target_lang == "Hindi":
        return "धर्म के क्षेत्र में, कुरुक्षेत्र में, युद्ध की इच्छा से एकत्रित हुए।"
    else:
        return "dharma-kṣetre kuru-kṣetre samavetā yuyutsavaḥ।"

def mock_text_to_speech(text, voice_type="female"):
    """Mock TTS function - replace with actual IndicParler implementation"""
    time.sleep(1)  # Simulate processing time
    
    # Generate dummy audio data for demo
    sample_rate = 16000
    duration = 3
    t = np.linspace(0, duration, sample_rate * duration)
    frequency = 220 if voice_type == "male" else 440
    audio_data = 0.3 * np.sin(2 * np.pi * frequency * t) * np.exp(-t/4)
    return audio_data

def save_to_history(source_lang, target_lang, transcription, translation):
    """Save translation to session history"""
    entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'source_lang': source_lang,
        'target_lang': target_lang,
        'transcription': transcription,
        'translation': translation
    }
    st.session_state.translation_history.append(entry)

# Main application
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🌉 VoiceBridge</div>
        <div class="subtitle">Voice of the Ancients in a Modern Tongue</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Language Direction Toggle
    st.markdown('<div class="section-header">🔄 Translation Direction</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        direction = st.radio(
            "Select translation direction:",
            ("Sanskrit to Hindi", "Hindi to Sanskrit"),
            horizontal=True,
            key="direction"
        )
    
    source_lang = "Sanskrit" if direction == "Sanskrit to Hindi" else "Hindi"
    target_lang = "Hindi" if direction == "Sanskrit to Hindi" else "Sanskrit"
    
    # Input Section
    st.markdown('<div class="section-header">🎤 Input Section</div>', unsafe_allow_html=True)
    
    # Audio input options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📹 Record Audio")
        if st.button("🎙️ Press to Record", key="record_btn", type="primary"):
            with st.spinner("Recording... (This is a demo - actual recording would happen here)"):
                time.sleep(3)
                # Simulate recorded audio
                st.session_state.current_audio_input = np.random.normal(0, 0.1, 16000 * 3)
                st.success("Recording completed!")
    
    with col2:
        st.markdown("### 📁 Upload Audio File")
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=['wav', 'mp3', 'ogg', 'm4a'],
            key="audio_upload"
        )
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            # Here you would process the uploaded file
            st.session_state.current_audio_input = np.random.normal(0, 0.1, 16000 * 5)
    
    # Display input waveform if audio is available
    if st.session_state.current_audio_input is not None:
        st.markdown("### 📊 Input Audio Visualization")
        input_fig = generate_waveform(st.session_state.current_audio_input, f"Input Audio ({source_lang})")
        st.pyplot(input_fig)
        plt.close()
        
        # Process the audio
        if st.button("🚀 Process Audio", type="primary", key="process_btn"):
            st.session_state.processing = True
            
            # Step 1: Speech to Text
            with st.spinner(f"🎯 Transcribing {source_lang} audio..."):
                transcription = mock_speech_to_text(st.session_state.current_audio_input, source_lang)
                st.session_state.current_transcription = transcription
            
            # Step 2: Translation
            with st.spinner(f"🔄 Translating to {target_lang}..."):
                translation = mock_translate(transcription, source_lang, target_lang)
                st.session_state.current_translation = translation
            
            # Step 3: Text to Speech
            with st.spinner(f"🗣️ Generating {target_lang} audio..."):
                voice_type = st.session_state.get('voice_selection', 'female')
                audio_output = mock_text_to_speech(translation, voice_type)
                st.session_state.current_audio_output = audio_output
            
            st.session_state.processing = False
            save_to_history(source_lang, target_lang, transcription, translation)
            st.success("✅ Translation completed successfully!")
    
    # Display transcription
    if st.session_state.current_transcription:
        st.markdown(f"### 📝 Original Text ({source_lang}):")
        st.markdown(f'<div class="text-display">{st.session_state.current_transcription}</div>', 
                   unsafe_allow_html=True)
    
    # Processing animation
    if st.session_state.processing:
        st.markdown("""
        <div class="processing-animation">
            <h3>🌉 Building the Bridge...</h3>
            <p>Connecting ancient wisdom with modern understanding</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Output Section
    if st.session_state.current_translation:
        st.markdown('<div class="section-header">🎯 Output Section</div>', unsafe_allow_html=True)
        
        st.markdown(f"### 📖 Translated Text ({target_lang}):")
        st.markdown(f'<div class="text-display">{st.session_state.current_translation}</div>', 
                   unsafe_allow_html=True)
        
        # Voice selection
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            voice_selection = st.radio(
                "🎵 Select Voice:",
                ("Female Voice", "Male Voice"),
                horizontal=True,
                key="voice_selection"
            )
        
        # Audio controls
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("▶️ Play Translated Audio", key="play_btn"):
                st.success("🎵 Playing audio... (Audio would play here in actual implementation)")
        
        with col2:
            if st.button("💾 Download Audio", key="download_btn"):
                # In actual implementation, you would generate a downloadable file
                st.success("📁 Audio download prepared!")
        
        with col3:
            if st.button("🔄 Regenerate with Different Voice", key="regenerate_btn"):
                with st.spinner("🎭 Regenerating audio..."):
                    voice_type = "male" if "Male" in voice_selection else "female"
                    st.session_state.current_audio_output = mock_text_to_speech(
                        st.session_state.current_translation, voice_type
                    )
                st.success("✅ Audio regenerated!")
        
        # Output waveform
        if st.session_state.current_audio_output is not None:
            st.markdown("### 📊 Output Audio Visualization")
            output_fig = generate_waveform(st.session_state.current_audio_output, f"Output Audio ({target_lang})")
            st.pyplot(output_fig)
            plt.close()
    
    # Translation History Sidebar
    with st.sidebar:
        st.markdown("## 📚 Translation History")
        
        if st.session_state.translation_history:
            for i, entry in enumerate(reversed(st.session_state.translation_history[-5:])):
                with st.expander(f"Translation {len(st.session_state.translation_history) - i}"):
                    st.write(f"**Time:** {entry['timestamp']}")
                    st.write(f"**Direction:** {entry['source_lang']} → {entry['target_lang']}")
                    st.write(f"**Original:** {entry['transcription'][:50]}...")
                    st.write(f"**Translation:** {entry['translation'][:50]}...")
        else:
            st.info("No translations yet. Start by recording or uploading audio!")
        
        if st.button("🗑️ Clear History"):
            st.session_state.translation_history = []
            st.success("History cleared!")
    
    # Educational Information
    with st.expander("📖 About VoiceBridge"):
        st.markdown("""
        **VoiceBridge** is an innovative speech-to-speech translation system designed to bridge 
        the gap between ancient Sanskrit and modern Hindi languages.
        
        **How it works:**
        1. **Speech Recognition** - Converts your audio to text using Whisper ASR
        2. **Neural Translation** - Translates text using IndicTrans2 models
        3. **Speech Synthesis** - Generates natural-sounding audio using IndicParler TTS
        
        **Best Practices:**
        - Speak clearly and at a moderate pace
        - Use simple sentences for better accuracy
        - Record in a quiet environment
        - Sanskrit pronunciation affects transcription quality
        """)
    
    # Settings
    with st.expander("⚙️ Settings"):
        st.markdown("### Model Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            stt_model = st.selectbox("STT Model", ["Whisper-large", "Whisper-medium", "Whisper-small"])
            mt_model = st.selectbox("Translation Model", ["IndicTrans2-large", "IndicTrans2-base"])
        
        with col2:
            tts_model = st.selectbox("TTS Model", ["IndicParler-v1", "IndicParler-v2"])
            audio_quality = st.selectbox("Audio Quality", ["High (48kHz)", "Standard (16kHz)", "Low (8kHz)"])
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")
    
    # Footer with Important Information
    st.markdown("""
    <div class="footer-info">
        <h4>⚠️ Important Notes</h4>
        <ul>
            <li><strong>Accuracy:</strong> Translation quality is highest for clear audio and simple sentences</li>
            <li><strong>Sanskrit TTS:</strong> Generated Sanskrit audio may sound synthetic due to limited training data</li>
            <li><strong>Cultural Context:</strong> Some Sanskrit concepts may not have direct Hindi equivalents</li>
            <li><strong>Privacy:</strong> Your audio data is processed locally and not stored permanently</li>
        </ul>
        
        <p><strong>Feedback:</strong> Help us improve VoiceBridge by reporting issues or suggesting improvements!</p>
        
        <div style="text-align: center; margin-top: 1rem;">
            <small>VoiceBridge v1.0 | Preserving Ancient Wisdom for Modern Times</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feedback Section
    with st.expander("💬 Provide Feedback"):
        feedback_type = st.selectbox(
            "Feedback Type", 
            ["General Feedback", "Bug Report", "Feature Request", "Translation Quality", "Audio Quality"]
        )
        
        feedback_text = st.text_area("Your feedback:", height=100)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Submit Feedback"):
                if feedback_text:
                    st.success("Thank you for your feedback! It helps us improve VoiceBridge.")
                else:
                    st.warning("Please enter your feedback before submitting.")

if __name__ == "__main__":
    main()
