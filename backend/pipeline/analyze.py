# backend/pipeline/analyze.py
import re
from statistics import median
from collections import defaultdict
import uuid

def _extract_years(text):
    years = []
    for m in re.finditer(r"(\d+)\s*(?:years|yrs|year)", text, flags=re.I):
        try:
            years.append(int(m.group(1)))
        except:
            pass
    mapping = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}
    for word, val in mapping.items():
        if re.search(rf"\b{word}\s+(?:years|yrs|year)\b", text, flags=re.I):
            years.append(val)
    return years

def _extract_skills(text):
    kws = ["python","machine learning","ml","docker","kubernetes","react","flask","django","sql"]
    found = []
    for k in kws:
        if re.search(rf"\b{k}\b", text, flags=re.I):
            found.append(k.lower())
    return sorted(set(found))

def merge_sessions(sessions):
    """
    Input: sessions = [{'session': int, 'text': str}, ...]
    Returns dict with revealed_truth and deception_patterns
    """
    all_text = " ".join(s.get("text","") for s in sessions)
    per_session_years = {}
    years = []
    for s in sessions:
        y = _extract_years(s.get("text",""))
        if y:
            per_session_years[s["session"]] = y
            years.extend(y)

    if years:
        likely = int(median(years))
        if likely <= 1:
            exp = f"{likely} years"
        else:
            exp = f"{max(0, likely-1)}-{likely+1} years"
    else:
        exp = "unknown"

    skills = _extract_skills(all_text)
    language = "python" if "python" in skills else ("unknown" if not skills else skills[0])

    # leadership detection heuristics
    lead_count = sum(1 for s in sessions if re.search(r"\bled\b", s.get("text",""), flags=re.I))
    solo_count = sum(1 for s in sessions if re.search(r"\balone\b|\bsolo\b|\bby myself\b", s.get("text",""), flags=re.I))
    if lead_count and solo_count:
        leadership_claims = "possibly fabricated"
    elif lead_count:
        leadership_claims = "likely genuine"
    else:
        leadership_claims = "unclear"

    team_experience = "individual contributor" if solo_count else "team_or_unknown"

    deception_patterns = []
    if years and len(set(years)) > 1:
        uniq = sorted({f"{y} years" for y in years})
        deception_patterns.append({"lie_type": "experience_inflation_or_inconsistency", "contradictory_claims": uniq})

    revealed_truth = {
        "programming_experience": exp,
        "programming_language": language,
        "skill_mastery": "intermediate" if ("python" in skills or "machine learning" in skills) else "unknown",
        "leadership_claims": leadership_claims,
        "team_experience": team_experience,
        "skills and other keywords": skills
    }

    return {"revealed_truth": revealed_truth, "deception_patterns": deception_patterns}

def extract_truth_for_sessions(sessions, shadow_id=None):
    if not shadow_id:
        shadow_id = f"shadow_{uuid.uuid4().hex[:8]}"
    merged = merge_sessions(sessions)
    return {
        "shadow_id": shadow_id,
        "revealed_truth": merged["revealed_truth"],
        "deception_patterns": merged["deception_patterns"],
        "sessions": sessions
    }
