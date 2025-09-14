# backend/pipeline/stt.py
import whisper
import os

# Load model once at import time
# Options: tiny, base, small, medium, large
model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio file using local Whisper model.
    Returns: transcript text (string).
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    result = model.transcribe(audio_path, fp16=False)  # fp16=False ensures CPU works too
    text = result.get("text", "").strip()
    return text
