def clean_text(transcript: str) -> str:
    """
    Basic cleanup: trim and normalize whitespace.
    """
    if not isinstance(transcript, str):
        return ""
    return " ".join(transcript.strip().split())
