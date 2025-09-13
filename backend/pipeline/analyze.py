import re
import json
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any

def extract_truth(transcript: str, shadow_id: str = "unknown") -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Advanced truth extraction for Whispering Shadows Mystery.
    Analyzes contradictions, deception patterns, and extracts most likely truth.
    Returns (revealed_truth, deception_patterns).
    """
    
    # Extract key information patterns
    programming_experience = extract_programming_experience(transcript)
    programming_language = extract_programming_language(transcript)
    skill_mastery = assess_skill_mastery(transcript, programming_language)
    leadership_claims = extract_leadership_claims(transcript)
    team_experience = extract_team_experience(transcript)
    skills_keywords = extract_skills_keywords(transcript)
    
    # Detect deception patterns
    deception_patterns = detect_deception_patterns(transcript, {
        'programming_experience': programming_experience,
        'programming_language': programming_language,
        'leadership_claims': leadership_claims,
        'team_experience': team_experience
    })
    
    # Build revealed truth
    revealed_truth = {
        "programming_experience": resolve_programming_experience(programming_experience),
        "programming_language": resolve_programming_language(programming_language),
        "skill_mastery": skill_mastery,
        "leadership_claims": resolve_leadership_claims(leadership_claims),
        "team_experience": resolve_team_experience(team_experience),
        "skills and other keywords": skills_keywords
    }
    
    return revealed_truth, deception_patterns

def extract_programming_experience(transcript: str) -> List[str]:
    """Extract all mentions of programming experience"""
    patterns = [
        r'(\d+)\s*years?\s*(?:of\s*)?(?:programming|coding|development|experience)',
        r'(?:programming|coding|development)\s*(?:for\s*)?(\d+)\s*years?',
        r'(\d+)\s*months?\s*(?:of\s*)?(?:programming|coding|development)',
        r'(?:programming|coding|development)\s*(?:for\s*)?(\d+)\s*months?',
        r'(\d+)\s*years?\s*(?:in\s*)?(?:python|java|javascript|c\+\+)',
        r'(?:python|java|javascript|c\+\+)\s*(?:for\s*)?(\d+)\s*years?'
    ]
    
    experiences = []
    for pattern in patterns:
        matches = re.findall(pattern, transcript.lower())
        experiences.extend(matches)
    
    return experiences

def extract_programming_language(transcript: str) -> List[str]:
    """Extract mentioned programming languages"""
    languages = ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin']
    mentioned = []
    
    for lang in languages:
        if lang in transcript.lower():
            mentioned.append(lang)
    
    return mentioned

def assess_skill_mastery(transcript: str, languages: List[str]) -> str:
    """Assess skill level based on language usage and context"""
    transcript_lower = transcript.lower()
    
    # Advanced indicators
    advanced_terms = ['machine learning', 'deep learning', 'neural networks', 'algorithms', 
                     'data structures', 'optimization', 'architecture', 'scalability', 'performance']
    
    # Intermediate indicators
    intermediate_terms = ['framework', 'library', 'api', 'database', 'testing', 'debugging']
    
    # Beginner indicators
    beginner_terms = ['learning', 'beginner', 'new to', 'just started', 'tutorial', 'basic']
    
    advanced_count = sum(1 for term in advanced_terms if term in transcript_lower)
    intermediate_count = sum(1 for term in intermediate_terms if term in transcript_lower)
    beginner_count = sum(1 for term in beginner_terms if term in transcript_lower)
    
    if advanced_count >= 2:
        return "advanced"
    elif intermediate_count >= 2 or (advanced_count >= 1 and len(languages) > 1):
        return "intermediate"
    elif beginner_count >= 1:
        return "beginner"
    else:
        return "intermediate"  # Default assumption

def extract_leadership_claims(transcript: str) -> List[str]:
    """Extract leadership and team management claims"""
    patterns = [
        r'led\s+(?:a\s*)?(?:team\s*of\s*)?(\d+)',
        r'managed\s+(?:a\s*)?(?:team\s*of\s*)?(\d+)',
        r'team\s*lead(?:er)?',
        r'project\s*manager',
        r'mentored\s+(\d+)',
        r'supervised\s+(?:a\s*)?(?:team\s*of\s*)?(\d+)'
    ]
    
    claims = []
    for pattern in patterns:
        matches = re.findall(pattern, transcript.lower())
        claims.extend(matches)
    
    return claims

def extract_team_experience(transcript: str) -> List[str]:
    """Extract team collaboration experience"""
    team_indicators = []
    
    if 'team' in transcript.lower():
        team_indicators.append('team collaboration')
    if 'collaborate' in transcript.lower():
        team_indicators.append('collaboration')
    if 'alone' in transcript.lower() or 'solo' in transcript.lower():
        team_indicators.append('individual contributor')
    if 'mentor' in transcript.lower():
        team_indicators.append('mentoring')
    
    return team_indicators

def extract_skills_keywords(transcript: str) -> List[str]:
    """Extract technical skills and keywords"""
    skills = []
    tech_terms = [
        'machine learning', 'deep learning', 'neural networks', 'ai', 'artificial intelligence',
        'data science', 'analytics', 'database', 'sql', 'nosql', 'mongodb', 'postgresql',
        'web development', 'frontend', 'backend', 'full stack', 'react', 'angular', 'vue',
        'mobile development', 'ios', 'android', 'flutter', 'react native',
        'cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'devops',
        'agile', 'scrum', 'git', 'version control', 'testing', 'unit testing'
    ]
    
    for term in tech_terms:
        if term in transcript.lower():
            skills.append(term.title())
    
    return skills

def detect_deception_patterns(transcript: str, extracted_data: Dict) -> List[Dict[str, Any]]:
    """Detect various deception patterns"""
    patterns = []
    
    # Experience inflation
    experiences = extracted_data.get('programming_experience', [])
    if len(experiences) > 1:
        # Check for contradictory experience claims
        numeric_experiences = []
        for exp in experiences:
            if exp.isdigit():
                numeric_experiences.append(int(exp))
        
        if len(numeric_experiences) > 1:
            max_exp = max(numeric_experiences)
            min_exp = min(numeric_experiences)
            if max_exp - min_exp >= 2:  # Significant difference
                patterns.append({
                    "lie_type": "experience_inflation",
                    "contradictory_claims": experiences
                })
    
    # Leadership fabrication
    leadership_claims = extracted_data.get('leadership_claims', [])
    team_experience = extracted_data.get('team_experience', [])
    
    if leadership_claims and 'individual contributor' in team_experience:
        patterns.append({
            "lie_type": "leadership_fabrication",
            "contradictory_claims": ["leadership claims", "individual contributor"]
        })
    
    # Skill exaggeration
    if 'advanced' in transcript.lower() and 'beginner' in transcript.lower():
        patterns.append({
            "lie_type": "skill_exaggeration",
            "contradictory_claims": ["advanced skills", "beginner level"]
        })
    
    return patterns

def resolve_programming_experience(experiences: List[str]) -> str:
    """Resolve conflicting experience claims to most likely truth"""
    if not experiences:
        return "unknown"
    
    # Convert to numeric values and take the most conservative (lowest) estimate
    numeric_experiences = []
    for exp in experiences:
        if exp.isdigit():
            numeric_experiences.append(int(exp))
    
    if numeric_experiences:
        # Take the minimum as most likely truth (conservative approach)
        min_exp = min(numeric_experiences)
        if min_exp < 12:
            return f"{min_exp} months"
        else:
            years = min_exp // 12
            months = min_exp % 12
            if months == 0:
                return f"{years} years"
            else:
                return f"{years} years {months} months"
    
    return "unknown"

def resolve_programming_language(languages: List[str]) -> str:
    """Resolve to most mentioned or most specific language"""
    if not languages:
        return "unknown"
    
    # Return the first mentioned language (most confident claim)
    return languages[0]

def resolve_leadership_claims(claims: List[str]) -> str:
    """Resolve leadership claims"""
    if not claims:
        return "no leadership claims"
    
    # If there are numeric claims, take the smallest (most conservative)
    numeric_claims = []
    for claim in claims:
        if claim.isdigit():
            numeric_claims.append(int(claim))
    
    if numeric_claims:
        return f"led team of {min(numeric_claims)}"
    
    return "leadership claims present"

def resolve_team_experience(experiences: List[str]) -> str:
    """Resolve team experience"""
    if not experiences:
        return "unknown"
    
    # Prioritize individual contributor if mentioned
    if 'individual contributor' in experiences:
        return "individual contributor"
    elif 'team collaboration' in experiences:
        return "team collaboration"
    else:
        return experiences[0]
