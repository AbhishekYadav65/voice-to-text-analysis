# backend/pipeline/analyze.py
import re
import uuid
from statistics import median

def _extract_years(text):
    years = []
    for m in re.finditer(r"(\d+)\s*(?:years|yrs|year)", text, flags=re.I):
        years.append(int(m.group(1)))
    mapping = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "nine": 9, "ten": 10
    }
    for word, val in mapping.items():
        if re.search(rf"\b{word}\s+(?:years|yrs|year)\b", text, flags=re.I):
            years.append(val)
    return years

def _extract_skills(text):
    kws = ["python", "machine learning", "deep learning", "sql",
           "docker", "kubernetes", "flask", "django", "react"]
    found = []
    for k in kws:
        if re.search(rf"\b{k}\b", text, flags=re.I):
            found.append(k.lower())
    return sorted(set(found))

def merge_sessions(sessions):
    all_text = " ".join(s["text"] for s in sessions if s.get("text"))
    per_session_years = {}
    years = []

    for s in sessions:
        y = _extract_years(s.get("text", ""))
        if y:
            per_session_years[s["session"]] = y
            years.extend(y)

    # programming experience
    if years:
        likely = int(median(years))
        exp = f"{max(0, likely-1)}-{likely+1} years" if likely > 1 else f"{likely} years"
    else:
        exp = "unknown"

    # programming language & skills
    skills = _extract_skills(all_text)
    language = "python" if "python" in skills else "unknown"

    # leadership claims
    leadership_mentions = [s for s in sessions if re.search(r"\bled\b", s.get("text",""), flags=re.I)]
    solo_mentions = [s for s in sessions if re.search(r"\b(work alone|solo|by myself)\b", s.get("text",""), flags=re.I)]

    if leadership_mentions and solo_mentions:
        leadership_claims = "fabricated"
    elif leadership_mentions:
        leadership_claims = "genuine"
    elif solo_mentions:
        leadership_claims = "fabricated"
    else:
        leadership_claims = "unclear"

    team_experience = "individual contributor" if solo_mentions else "team_or_unknown"

    # deception patterns
    deception_patterns = []
    if years and len(set(years)) > 1:
        uniq = sorted({f"{y} years" for y in years})
        deception_patterns.append({
            "lie_type": "experience_inflation",
            "contradictory_claims": uniq
        })
    if leadership_mentions and solo_mentions:
        deception_patterns.append({
            "lie_type": "leadership_contradiction",
            "contradictory_claims": ["led a team", "worked alone"]
        })

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
