import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "saved_models"
DATA_DIR = BASE_DIR / "data"
AUDIO_DIR = DATA_DIR / "sample_audio"
TEXT_DIR = DATA_DIR / "parallel_texts"

# Create directories if they don't exist
for directory in [MODEL_DIR, AUDIO_DIR, TEXT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Model settings
INDICTRANS2_MODEL_NAME = "ai4bharat/indictrans2-indic-indic-1B"
INDICTRANS2_LOCAL_PATH = MODEL_DIR / "indictrans2"

# Supported languages
LANGUAGES = {
    "Hindi": "hin_Deva",
    "Sanskrit": "san_Deva"
}

# Audio settings
SAMPLE_RATE = 16000
MAX_AUDIO_DURATION = 30  # seconds