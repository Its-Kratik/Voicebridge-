import streamlit as st
import os
from config.settings import LANGUAGES
from models.translation_model import translation_model
from models.stt_model import stt_model
from models.tts_model import tts_model
from utils.audio_utils import save_uploaded_audio, convert_audio_to_wav

# Set page config
st.set_page_config(
    page_title="VoiceBridge",
    page_icon="🎤",
    layout="wide"
)

# App title and description
st.title("🎤 VoiceBridge - Sanskrit-Hindi Translation")
st.markdown("""
A real-time voice translation app that converts between Sanskrit and Hindi speech.
""")

# Initialize session state
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'source_audio_path' not in st.session_state:
    st.session_state.source_audio_path = None
if 'target_audio_path' not in st.session_state:
    st.session_state.target_audio_path = None

# Create two columns for the interface
col1, col2 = st.columns(2)

with col1:
    st.header("Source Language")
    
    # Language selection
    source_lang = st.selectbox(
        "Select source language",
        options=list(LANGUAGES.keys()),
        key="source_lang"
    )
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["Text Input", "Voice Recording", "Audio Upload"]
    )
    
    source_text = ""
    
    if input_method == "Text Input":
        source_text = st.text_area(
            "Enter text to translate:",
            height=150,
            placeholder=f"Type {source_lang} text here..."
        )
    
    elif input_method == "Voice Recording":
        audio_bytes = st.audio_input(f"Record {source_lang} audio:")
        
        if audio_bytes:
            # Save the audio
            with open("temp_audio.webm", "wb") as f:
                f.write(audio_bytes)
            
            # Convert to WAV and transcribe
            wav_path = convert_audio_to_wav("temp_audio.webm")
            if wav_path:
                source_text = stt_model.transcribe_audio(wav_path)
                st.session_state.source_audio_path = wav_path
                st.text_area("Transcribed text:", value=source_text, height=100)
    
    elif input_method == "Audio Upload":
        uploaded_file = st.file_uploader(
            "Upload an audio file", 
            type=['wav', 'mp3', 'ogg', 'm4a']
        )
        
        if uploaded_file:
            # Save the uploaded file
            audio_path = save_uploaded_audio(uploaded_file)
            if audio_path:
                # Convert to WAV and transcribe
                wav_path = convert_audio_to_wav(audio_path)
                if wav_path:
                    source_text = stt_model.transcribe_audio(wav_path)
                    st.session_state.source_audio_path = wav_path
                    st.text_area("Transcribed text:", value=source_text, height=100)

with col2:
    st.header("Target Language")
    
    # Target language selection (auto-set to the other language)
    target_options = [lang for lang in LANGUAGES.keys() if lang != source_lang]
    target_lang = st.selectbox(
        "Select target language",
        options=target_options,
        key="target_lang"
    )
    
    # Translate button
    if st.button("Translate", type="primary"):
        if source_text:
            with st.spinner("Translating..."):
                # Translate the text
                translated = translation_model.translate(
                    [source_text], 
                    LANGUAGES[source_lang], 
                    LANGUAGES[target_lang]
                )
                
                if translated and translated[0] != "Translation failed":
                    st.session_state.translated_text = translated[0]
                else:
                    st.error("Translation failed. Please try again.")
        else:
            st.warning("Please enter some text to translate.")
    
    # Display translated text
    st.text_area(
        "Translated text:",
        value=st.session_state.translated_text,
        height=150,
        key="translated_output"
    )
    
    # Generate speech from translated text
    if st.session_state.translated_text and st.button("Convert to Speech"):
        with st.spinner("Generating audio..."):
            audio_path = tts_model.text_to_speech(
                st.session_state.translated_text, 
                LANGUAGES[target_lang]
            )
            
            if audio_path:
                st.session_state.target_audio_path = audio_path
                st.audio(audio_path)
            else:
                st.error("Failed to generate audio.")

# Add some sample texts for testing
st.divider()
st.subheader("Sample Texts")

sample_col1, sample_col2 = st.columns(2)

with sample_col1:
    st.write("**Hindi Samples:**")
    hindi_samples = [
        "वह बाजार जाता है।",
        "हमें सत्य बोलना चाहिए।",
        "गंगा एक पवित्र नदी है।"
    ]
    
    for sample in hindi_samples:
        if st.button(sample, key=f"hin_{sample}"):
            st.session_state.translated_text = translation_model.translate(
                [sample], "hin_Deva", "san_Deva"
            )[0]

with sample_col2:
    st.write("**Sanskrit Samples:**")
    sanskrit_samples = [
        "अहं भोजनं खादामि।",
        "सः विपणिं गच्छति।",
        "गङ्गा पवित्रनदी अस्ति।"
    ]
    
    for sample in sanskrit_samples:
        if st.button(sample, key=f"san_{sample}"):
            st.session_state.translated_text = translation_model.translate(
                [sample], "san_Deva", "hin_Deva"
            )[0]

# Footer
st.divider()
st.markdown("---")
st.markdown(
    "### VoiceBridge 🎤 | Sanskrit-Hindi Voice Translation | "
    "[Learn More](https://github.com/yourusername/voicebridge)"
)