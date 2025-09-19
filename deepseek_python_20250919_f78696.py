from gtts import gTTS
import os
from config.settings import AUDIO_DIR

class TextToSpeechModel:
    def __init__(self):
        pass
    
    def text_to_speech(self, text, language):
        """Convert text to speech using gTTS"""
        try:
            # Map our language codes to gTTS language codes
            lang_map = {
                "hin_Deva": "hi",
                "san_Deva": "sa"  # Note: Sanskrit might not be fully supported
            }
            
            tts = gTTS(text=text, lang=lang_map.get(language, "hi"))
            
            # Save the audio file
            output_path = os.path.join(AUDIO_DIR, f"output_{hash(text)}.mp3")
            tts.save(output_path)
            
            return output_path
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            return None

# Create a global instance
tts_model = TextToSpeechModel()