import speech_recognition as sr
from utils.audio_utils import convert_audio_to_wav

class SpeechToTextModel:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe_audio(self, audio_path):
        """Convert speech to text using Google Speech Recognition"""
        try:
            # Convert audio to WAV format if needed
            wav_path = convert_audio_to_wav(audio_path)
            
            # Use the audio file as the audio source
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language="hi-IN")
                return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error with speech recognition service: {e}"
        except Exception as e:
            return f"Error transcribing audio: {e}"

# Create a global instance
stt_model = SpeechToTextModel()