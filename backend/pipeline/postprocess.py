# backend/pipeline/postprocess.py
import re

def clean_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    text = raw_text.strip()
    text = re.sub(r"\s+", " ", text)
    # remove unprintable characters
    text = re.sub(r"[\x00-\x1f]+", " ", text)
    return text.strip()
