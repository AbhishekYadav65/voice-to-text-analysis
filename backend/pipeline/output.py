import json
import os
from datetime import datetime
from typing import Dict, List, Any

def generate_json(transcript: str, revealed_truth: Dict[str, Any], deception_patterns: List[Dict[str, Any]], shadow_id: str = "unknown") -> Dict[str, Any]:
    """
    Generates the exact JSON format required for Whispering Shadows Mystery submission.
    """
    return {
        "shadow_id": shadow_id,
        "revealed_truth": revealed_truth,
        "deception_patterns": deception_patterns
    }

def save_transcript(transcript: str, shadow_id: str = "unknown", session_number: int = 1) -> str:
    """
    Saves transcript to a .txt file as required for submission.
    """
    # Create transcripts directory if it doesn't exist
    os.makedirs("transcripts", exist_ok=True)
    
    filename = f"transcripts/{shadow_id}_session_{session_number}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Shadow ID: {shadow_id}\n")
        f.write(f"Session: {session_number}\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(transcript)
    
    return filename

def save_final_json(revealed_truth: Dict[str, Any], deception_patterns: List[Dict[str, Any]], shadow_id: str = "unknown") -> str:
    """
    Saves the final analysis JSON as required for submission.
    """
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    filename = f"output/{shadow_id}_analysis.json"
    
    final_json = generate_json("", revealed_truth, deception_patterns, shadow_id)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
    
    return filename

def process_multiple_sessions(sessions_data: List[Dict[str, Any]], shadow_id: str) -> Dict[str, Any]:
    """
    Process multiple sessions for a single shadow and combine the analysis.
    This handles the 5-session structure described in the project.
    """
    all_transcripts = []
    all_revealed_truths = []
    all_deception_patterns = []
    
    # Process each session
    for i, session in enumerate(sessions_data, 1):
        transcript = session.get('transcript', '')
        revealed_truth = session.get('revealed_truth', {})
        deception_patterns = session.get('deception_patterns', [])
        
        # Save individual session transcript
        save_transcript(transcript, shadow_id, i)
        
        all_transcripts.append(transcript)
        all_revealed_truths.append(revealed_truth)
        all_deception_patterns.extend(deception_patterns)
    
    # Combine all transcripts
    combined_transcript = "\n\n--- SESSION SEPARATOR ---\n\n".join(all_transcripts)
    
    # Save combined transcript
    save_transcript(combined_transcript, f"{shadow_id}_combined", 0)
    
    # Merge revealed truths (take most conservative estimates)
    merged_truth = merge_revealed_truths(all_revealed_truths)
    
    # Combine deception patterns
    merged_patterns = merge_deception_patterns(all_deception_patterns)
    
    # Save final analysis
    final_json_path = save_final_json(merged_truth, merged_patterns, shadow_id)
    
    return {
        "shadow_id": shadow_id,
        "revealed_truth": merged_truth,
        "deception_patterns": merged_patterns,
        "transcript_file": f"transcripts/{shadow_id}_combined_session_0.txt",
        "json_file": final_json_path
    }

def merge_revealed_truths(truths: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple revealed truths, taking the most conservative estimates.
    """
    if not truths:
        return {}
    
    merged = {}
    
    # Get all unique keys
    all_keys = set()
    for truth in truths:
        all_keys.update(truth.keys())
    
    for key in all_keys:
        values = [truth.get(key) for truth in truths if key in truth]
        
        if key == "programming_experience":
            # Take the minimum experience
            merged[key] = min_experience(values)
        elif key == "skill_mastery":
            # Take the lowest skill level
            merged[key] = min_skill_level(values)
        elif key == "leadership_claims":
            # Take the most conservative leadership claim
            merged[key] = min_leadership_claims(values)
        elif key == "skills and other keywords":
            # Combine all unique skills
            all_skills = []
            for skill_list in values:
                if isinstance(skill_list, list):
                    all_skills.extend(skill_list)
            merged[key] = list(set(all_skills))  # Remove duplicates
        else:
            # For other fields, take the first non-empty value
            merged[key] = next((v for v in values if v and v != "unknown"), "unknown")
    
    return merged

def merge_deception_patterns(patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge deception patterns, removing duplicates and combining similar patterns.
    """
    if not patterns:
        return []
    
    # Group by lie_type
    grouped = {}
    for pattern in patterns:
        lie_type = pattern.get("lie_type", "unknown")
        if lie_type not in grouped:
            grouped[lie_type] = []
        grouped[lie_type].append(pattern)
    
    # Merge patterns of the same type
    merged = []
    for lie_type, pattern_list in grouped.items():
        if len(pattern_list) == 1:
            merged.append(pattern_list[0])
        else:
            # Combine contradictory claims
            all_claims = []
            for pattern in pattern_list:
                claims = pattern.get("contradictory_claims", [])
                all_claims.extend(claims)
            
            merged.append({
                "lie_type": lie_type,
                "contradictory_claims": list(set(all_claims))  # Remove duplicates
            })
    
    return merged

def min_experience(experiences: List[str]) -> str:
    """Find the minimum experience claim"""
    if not experiences:
        return "unknown"
    
    # Convert to months for comparison
    min_months = float('inf')
    min_exp = "unknown"
    
    for exp in experiences:
        months = experience_to_months(exp)
        if months < min_months:
            min_months = months
            min_exp = exp
    
    return min_exp

def experience_to_months(exp: str) -> int:
    """Convert experience string to months"""
    if not exp or exp == "unknown":
        return float('inf')
    
    exp_lower = exp.lower()
    if 'year' in exp_lower:
        years = int(''.join(filter(str.isdigit, exp)))
        return years * 12
    elif 'month' in exp_lower:
        return int(''.join(filter(str.isdigit, exp)))
    else:
        return float('inf')

def min_skill_level(levels: List[str]) -> str:
    """Find the minimum skill level"""
    if not levels:
        return "unknown"
    
    skill_hierarchy = {"beginner": 1, "intermediate": 2, "advanced": 3}
    
    min_level = min(levels, key=lambda x: skill_hierarchy.get(x.lower(), 2))
    return min_level

def min_leadership_claims(claims: List[str]) -> str:
    """Find the most conservative leadership claim"""
    if not claims:
        return "no leadership claims"
    
    # If any claim is "no leadership claims", return that
    if "no leadership claims" in claims:
        return "no leadership claims"
    
    # Otherwise return the first claim
    return claims[0]
