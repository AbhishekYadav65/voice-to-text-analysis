# backend/pipeline/output.py
import os
import json
from datetime import datetime

def _ensure_dir(d):
    os.makedirs(d, exist_ok=True)

def save_transcript_single(text: str, shadow_id: str, session_idx: int = 1, base_dir="backend/transcripts"):
    _ensure_dir(base_dir)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{shadow_id}_session_{session_idx}_{ts}.txt"
    path = os.path.join(base_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Session {session_idx}:\n")
        f.write(text or "")
    return path

def save_final_json(analysis_result: dict, shadow_id: str, base_dir="backend/output"):
    _ensure_dir(base_dir)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{shadow_id}_analysis_{ts}.json"
    path = os.path.join(base_dir, filename)

    # Build final JSON shape exactly as required
    out = {
        "shadow_id": shadow_id,
        "revealed_truth": analysis_result.get("revealed_truth", {}),
        "deception_patterns": analysis_result.get("deception_patterns", []),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    return path
