import os
from pydub import AudioSegment
from config.settings import SAMPLE_RATE, MAX_AUDIO_DURATION, AUDIO_DIR

def convert_audio_to_wav(audio_path, output_dir=AUDIO_DIR):
    """Convert any audio format to WAV with proper sample rate"""
    try:
        # Load audio file
        audio = AudioSegment.from_file(audio_path)
        
        # Limit duration if needed
        if len(audio) > MAX_AUDIO_DURATION * 1000:  # pydub uses milliseconds
            audio = audio[:MAX_AUDIO_DURATION * 1000]
        
        # Set channels and sample rate
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(SAMPLE_RATE)
        
        # Create output path
        filename = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(output_dir, f"{filename}.wav")
        
        # Export as WAV
        audio.export(output_path, format="wav")
        
        return output_path
    except Exception as e:
        print(f"Error converting audio: {e}")
        return None

def save_uploaded_audio(uploaded_file, output_dir=AUDIO_DIR):
    """Save uploaded audio file and return path"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(output_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    except Exception as e:
        print(f"Error saving uploaded audio: {e}")
        return None
