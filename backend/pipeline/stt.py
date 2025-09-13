import whisper
import torch
import os

def transcribe_audio(file_path: str) -> str:
    """
    Uses OpenAI Whisper to convert audio to text.
    Handles poor quality audio with static, whispers, and background noise.
    Returns transcript as string.
    """
    try:
        # Load Whisper model (base model for good balance of speed/accuracy)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("base", device=device)
        
        # Transcribe with enhanced settings for poor quality audio
        result = model.transcribe(
            file_path,
            language="en",  # English
            fp16=False,     # Better for poor quality audio
            verbose=False,
            word_timestamps=True,  # Useful for session analysis
            condition_on_previous_text=False,  # Better for independent sessions
            temperature=0.0,  # More deterministic
            compression_ratio_threshold=2.4,  # Handle repetitive speech
            logprob_threshold=-1.0,  # Lower threshold for poor audio
            no_speech_threshold=0.6  # Handle silence better
        )
        
        return result["text"].strip()
        
    except Exception as e:
        print(f"Error in transcription: {e}")
        return f"Transcription failed: {str(e)}"
