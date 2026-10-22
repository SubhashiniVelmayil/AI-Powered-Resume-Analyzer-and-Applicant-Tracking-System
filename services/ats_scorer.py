"""
ATS Compatibility Scorer Service.
Performs semantic & keyword matching against specific job requirements.
Calculates 100-point transparent rubric score distinguishing exact matches from related skills.
"""

import re
from typing import Dict, Any, List, Set, Tuple
from config import ATS_SCORING_WEIGHTS

# Skill relationship / ontology graph (bidirectional relationships)
RELATED_SKILLS_MAP = {
    "python": ["django", "flask", "fastapi", "pandas", "numpy", "pytorch"],
    "javascript": ["typescript", "react", "node.js", "vue", "angular", "next.js"],
    "typescript": ["javascript", "react", "node.js", "angular"],
    "react": ["next.js", "javascript", "typescript", "redux", "vue"],
    "sql": ["postgresql", "mysql", "sqlite", "oracle", "database"],
    "postgresql": ["sql", "mysql", "sqlite", "relational database"],
    "docker": ["kubernetes", "containers", "ci/cd", "devops"],
    "kubernetes": ["docker", "containers", "helm", "devops"],
    "terraform": ["cloudformation", "ansible", "iac"],
    "aws": ["cloud", "azure", "gcp", "lambda", "s3", "ec2"],
    "machine learning": ["deep learning", "pytorch", "tensorflow", "scikit-learn", "nlp", "llm"],
    "git": ["github", "gitlab", "version control"],
    "rest apis": ["graphql", "api", "microservices", "fastapi", "express"]
}

STOP_WORDS = {
    "and", "the", "with", "for", "our", "you", "will", "are", "have", "been", "from",
    "that", "this", "must", "years", "role", "team", "work", "looking", "candidate",
    "experience", "preferred", "required", "qualifications", "responsibilities"
}

def extract_job_keywords(job_description: str, required_skills_str: str = "") -> Dict[str, Any]:
    """Extracts explicit skills, qualifications, and important domain keywords from job posting."""
    # Combine skills string and description
    combined = f"{required_skills_str} {job_description}".lower()

    # Extract distinct skill terms
    explicit_skills = [s.strip().lower() for s in re.split(r'[,|/;\n]+', required_skills_str) if s.strip()]

    # Extract significant alphanumeric keywords
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9_\-\.]{2,}\b', combined)
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    unique_keywords = sorted(list(set(keywords)))

    return {
        "explicit_skills": list(set(explicit_skills)),
        "all_keywords": unique_keywords
    }

def compare_resume_to_job(resume_text: str, job_title: str, job_description: str, required_skills: str, preferred_qualifications: str = "") -> Dict[str, Any]:
    """
    Compares resume text against job requirements.
    Distinguishes exact matches, related skills, and missing requirements.
    Calculates 100-point ATS compatibility score.
    """
    weights = ATS_SCORING_WEIGHTS
    resume_lower = resume_text.lower()

    # Parse required skills
    raw_req_skills = [s.strip() for s in re.split(r'[,|/;\n]+', required_skills) if s.strip()]
    if not raw_req_skills:
        raw_req_skills = ["Communication", "Problem Solving", "Relevant Technical Skills"]

    matched_skills = []
    related_skills = []
    missing_skills = []

    for skill in raw_req_skills:
        skill_clean = skill.lower()
        # Word boundary search for exact match
        pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_clean) + r'(?![a-zA-Z0-9])'
        if re.search(pattern, resume_lower):
            matched_skills.append(skill)
        else:
            # Check related skills
            relatives = RELATED_SKILLS_MAP.get(skill_clean, [])
            found_rel = False
            for rel in relatives:
                if re.search(r'(?<![a-zA-Z0-9])' + re.escape(rel) + r'(?![a-zA-Z0-9])', resume_lower):
                    related_skills.append(f"{skill} (Evidenced via related skill: {rel.title()})")
                    found_rel = True
                    break
            if not found_rel:
                missing_skills.append(skill)

    # 1. Required Skill Coverage Score (Max: 40)
    total_req = len(raw_req_skills)
    skill_coverage_ratio = (len(matched_skills) * 1.0 + len(related_skills) * 0.5) / max(1, total_req)
    skill_score = int(weights["required_skills"] * min(1.0, skill_coverage_ratio))

    # 2. Experience & Project Evidence (Max: 25)
    # Check if job title keywords or project words appear in context with actions
    title_words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', job_title) if w.lower() not in STOP_WORDS]
    title_matches = [w for w in title_words if w in resume_lower]
    has_proj_evidence = bool(re.search(r'\b(project|portfolio|built|developed|architected)\b', resume_lower))
    exp_ratio = (len(title_matches) / max(1, len(title_words))) * 0.5 + (0.5 if has_proj_evidence else 0.2)
    exp_score = int(weights["experience_evidence"] * min(1.0, exp_ratio))

    # 3. Education & Qualification Match (Max: 15)
    has_degree = bool(re.search(r'\b(bachelor|master|b\.s|m\.s|degree|computer science|engineering|diploma)\b', resume_lower))
    pref_words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', preferred_qualifications) if w.lower() not in STOP_WORDS]
    pref_matches = [w for w in pref_words if w in resume_lower]
    edu_ratio = (0.7 if has_degree else 0.3) + (0.3 * (len(pref_matches) / max(1, len(pref_words))) if pref_words else 0.3)
    edu_score = int(weights["education_match"] * min(1.0, edu_ratio))

    # 4. Job Description Keyword Coverage (Max: 15)
    desc_words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', job_description) if w.lower() not in STOP_WORDS]
    unique_desc_words = list(set(desc_words))[:25]
    kw_matches = [w for w in unique_desc_words if w in resume_lower]
    kw_ratio = len(kw_matches) / max(1, len(unique_desc_words))
    kw_score = int(weights["keyword_coverage"] * min(1.0, kw_ratio * 1.3))

    # 5. Relevant Certifications (Max: 5)
    has_cert = bool(re.search(r'\b(certified|certification|aws|azure|gcp|comptia|cissp|scrum master|cka)\b', resume_lower))
    cert_score = weights["certifications_match"] if has_cert else 1

    total_match_score = min(100, skill_score + exp_score + edu_score + kw_score + cert_score)

    breakdown = {
        "required_skills": skill_score,
        "experience_evidence": exp_score,
        "education_match": edu_score,
        "keyword_coverage": kw_score,
        "certifications_match": cert_score,
        "total_match_score": total_match_score
    }

    # Actionable Recommendations
    recommendations = []
    if missing_skills:
        recommendations.append(
            f"Bridge the skills gap: Incorporate missing required skills ({', '.join(missing_skills[:3])}) "
            "into your project descriptions or highlight them in your skills list if you possess experience with them."
        )
    if related_skills:
        recommendations.append(
            "Replace generic terms with exact target keywords: For example, if you list JavaScript and the job specifically requests TypeScript, explicitly mention TypeScript projects."
        )
    if kw_score < (weights["keyword_coverage"] * 0.6):
        recommendations.append(
            "Tailor your project bullet points to mirror key phrases found in the job description to improve semantic relevance."
        )
    if cert_score <= 1:
        recommendations.append(
            "Consider earning and listing a recognized foundational certification (e.g. AWS Certified Cloud Practitioner or Docker Certified Associate)."
        )

    return {
        "overall_match_score": total_match_score,
        "score_breakdown": breakdown,
        "matched_skills": matched_skills,
        "related_skills": related_skills,
        "missing_skills": missing_skills,
        "keyword_matches_sample": kw_matches[:10],
        "recommendations": recommendations,
        "disclaimer": (
            "Advisory Compatibility Estimate: This assessment is an analytical heuristic based on requirements "
            "and keyword coverage. Real-world ATS systems and hiring managers use diverse proprietary screening algorithms."
        )
    }
