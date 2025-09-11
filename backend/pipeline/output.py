def generate_json(transcript: str, facts: list, contradictions: list) -> dict:
    """
    Formats final transcript and analysis into JSON.
    """
    return {
        "transcript": transcript,
        "facts": facts,
        "contradictions": contradictions
    }
