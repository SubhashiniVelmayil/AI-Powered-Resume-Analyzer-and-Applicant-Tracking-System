"""
Resume Analyzer Service.
Parses sections, detects technical and soft skills, performs ATS formatting audits,
and calculates a transparent 100-point rubric resume score with actionable feedback.
"""

import re
from typing import Dict, Any, List, Tuple
from config import RESUME_SCORING_WEIGHTS

# Common technical skills dictionary grouped by domain
COMMON_TECH_SKILLS = [
    "Python", "JavaScript", "TypeScript", "React", "Node.js", "Express", "Next.js",
    "HTML", "CSS", "Tailwind CSS", "Bootstrap", "SQL", "PostgreSQL", "MySQL", "MongoDB",
    "SQLite", "Redis", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "GitHub",
    "CI/CD", "Linux", "REST APIs", "GraphQL", "FastAPI", "Flask", "Django", "Java",
    "Spring Boot", "C++", "C#", ".NET", "PHP", "Go", "Rust", "Pandas", "NumPy",
    "Scikit-learn", "TensorFlow", "PyTorch", "Tableau", "Power BI", "Excel", "Figma"
]

COMMON_SOFT_SKILLS = [
    "Leadership", "Communication", "Problem Solving", "Teamwork", "Collaboration",
    "Time Management", "Critical Thinking", "Adaptability", "Agile", "Scrum",
    "Project Management", "Analytical Skills", "Mentorship", "Negotiation", "Creativity"
]

ACTION_VERBS = [
    "accelerated", "achieved", "architected", "automated", "built", "spearheaded",
    "designed", "developed", "deployed", "engineered", "enhanced", "established",
    "executed", "expanded", "generated", "implemented", "improved", "increased",
    "launched", "led", "mentored", "optimized", "orchestrated", "reduced", "scaled", "transformed"
]

def extract_contact_info(text: str) -> Dict[str, Any]:
    """Extracts candidate contact information including email, phone, and name."""
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    email = email_match.group(0) if email_match else None

    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', text)
    phone = phone_match.group(0).strip() if phone_match else None

    # Name extraction heuristic: First non-empty line with 2-4 capitalized words
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    candidate_name = None
    for line in lines[:5]:
        # Exclude header terms
        if re.search(r'(resume|curriculum|vitae|email|phone|contact|page)', line, re.IGNORECASE):
            continue
        words = line.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
            candidate_name = line
            break

    return {
        "candidate_name": candidate_name or "Candidate",
        "email": email,
        "phone": phone
    }

def extract_skills(text: str) -> Dict[str, List[str]]:
    """Identifies technical and soft skills present in the resume text."""
    lower_text = text.lower()
    found_tech = []
    for skill in COMMON_TECH_SKILLS:
        # Regex word boundary check
        pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill.lower()) + r'(?![a-zA-Z0-9])'
        if re.search(pattern, lower_text):
            found_tech.append(skill)

    found_soft = []
    for skill in COMMON_SOFT_SKILLS:
        pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill.lower()) + r'(?![a-zA-Z0-9])'
        if re.search(pattern, lower_text):
            found_soft.append(skill)

    return {
        "technical_skills": sorted(list(set(found_tech))),
        "soft_skills": sorted(list(set(found_soft)))
    }

def detect_sections(text: str) -> Dict[str, bool]:
    """Detects whether standard resume sections exist in the document."""
    lower = text.lower()
    return {
        "has_education": bool(re.search(r'\b(education|degree|university|college|bachelor|master|b\.s|m\.s|phd|gpa)\b', lower)),
        "has_experience": bool(re.search(r'\b(experience|employment|work history|professional history|internship)\b', lower)),
        "has_projects": bool(re.search(r'\b(projects|personal projects|portfolio|academic projects)\b', lower)),
        "has_skills": bool(re.search(r'\b(skills|technical skills|competencies|technologies)\b', lower)),
        "has_certifications": bool(re.search(r'\b(certifications?|licenses?|credentials?|accreditations?)\b', lower)),
        "has_achievements": bool(re.search(r'\b(achievements|awards|honors|publications|recognition)\b', lower))
    }

def detect_measurable_metrics(text: str) -> List[str]:
    """Finds quantifiable impact metrics (e.g. percentages, dollar amounts, numbers)."""
    # Matches patterns like 25%, $100k, 10x, 500+ users, reduced by 30%
    metric_patterns = re.findall(r'(\b\d+%\b|\$\d+[\d,]*|\b\d+x\b|\b\d+\+?\s*(?:users|clients|customers|requests|transactions|percent|ms|seconds|hours)\b)', text, re.IGNORECASE)
    return list(set(metric_patterns))

def audit_ats_formatting(text: str, contact_info: Dict[str, Any], sections: Dict[str, bool], metrics: List[str]) -> List[Dict[str, Any]]:
    """Performs deep ATS compatibility and formatting checks."""
    checks = []

    # 1. Contact info check
    if not contact_info.get("email") or not contact_info.get("phone"):
        checks.append({
            "check": "Contact Details",
            "passed": False,
            "severity": "High",
            "issue": "Missing contact information (email or phone).",
            "recommendation": "Add a prominent contact header containing your email, phone number, LinkedIn, and location."
        })
    else:
        checks.append({
            "check": "Contact Details",
            "passed": True,
            "severity": "None",
            "issue": None,
            "recommendation": "Contact details are complete and readable."
        })

    # 2. Dedicated Skills Section
    if not sections.get("has_skills"):
        checks.append({
            "check": "Skills Section",
            "passed": False,
            "severity": "High",
            "issue": "No dedicated Skills section header detected.",
            "recommendation": "Create a distinct 'Skills' section grouped into Technical, Frameworks, and Tools for ATS scanners."
        })
    else:
        checks.append({
            "check": "Skills Section",
            "passed": True,
            "severity": "None",
            "issue": None,
            "recommendation": "Dedicated skills section detected."
        })

    # 3. Education Details
    if not sections.get("has_education"):
        checks.append({
            "check": "Education Section",
            "passed": False,
            "severity": "Medium",
            "issue": "Missing or non-standard Education section.",
            "recommendation": "Add your degree, major, institution, and graduation year."
        })
    else:
        checks.append({
            "check": "Education Section",
            "passed": True,
            "severity": "None",
            "issue": None,
            "recommendation": "Education details present."
        })

    # 4. Measurable Achievements
    if len(metrics) < 2:
        checks.append({
            "check": "Measurable Impact & Metrics",
            "passed": False,
            "severity": "High",
            "issue": f"Only {len(metrics)} quantified metrics found in entire resume.",
            "recommendation": "Include quantifiable outcomes (e.g., 'Improved API response latency by 35%', 'Scaled application to 10,000+ users')."
        })
    else:
        checks.append({
            "check": "Measurable Impact & Metrics",
            "passed": True,
            "severity": "None",
            "issue": None,
            "recommendation": f"Good evidence of quantifiable impact ({len(metrics)} distinct metrics found)."
        })

    # 5. Strong Action Verbs
    lower_text = text.lower()
    used_verbs = [v for v in ACTION_VERBS if re.search(r'\b' + v + r'\b', lower_text)]
    if len(used_verbs) < 3:
        checks.append({
            "check": "Action Verbs",
            "passed": False,
            "severity": "Medium",
            "issue": "Few active accomplishment verbs detected.",
            "recommendation": "Begin bullet points with decisive action verbs like 'Architected', 'Spearheaded', 'Optimized', or 'Automated'."
        })
    else:
        checks.append({
            "check": "Action Verbs",
            "passed": True,
            "severity": "None",
            "issue": None,
            "recommendation": f"Strong active language used ({len(used_verbs)} power verbs identified)."
        })

    # 6. Formatting & Length
    word_count = len(text.split())
    if word_count < 150:
        checks.append({
            "check": "Resume Substance & Length",
            "passed": False,
            "severity": "High",
            "issue": f"Resume is brief ({word_count} words). May lack sufficient context for ATS keywords.",
            "recommendation": "Expand bullet points with technical scope, technologies leveraged, and results achieved."
        })
    elif word_count > 1200:
        checks.append({
            "check": "Resume Substance & Length",
            "passed": False,
            "severity": "Medium",
            "issue": f"Resume is very long ({word_count} words). Typical entry-to-mid resumes should be 1-2 pages (400-800 words).",
            "recommendation": "Condense older or less relevant roles to focus on high-impact projects."
        })
    else:
        checks.append({
            "check": "Resume Substance & Length",
            "passed": True,
            "severity": "None",
            "issue": None,
            "recommendation": f"Ideal resume length ({word_count} words)."
        })

    return checks

def calculate_resume_score(text: str, contact_info: Dict[str, Any], skills: Dict[str, List[str]], sections: Dict[str, bool], metrics: List[str]) -> Tuple[int, Dict[str, int], Dict[str, str]]:
    """
    Calculates a transparent 100-point rubric resume score.
    Returns overall score, rubric category scores, and category explanations.
    """
    weights = RESUME_SCORING_WEIGHTS
    word_count = len(text.split())
    tech_count = len(skills.get("technical_skills", []))
    soft_count = len(skills.get("soft_skills", []))
    metric_count = len(metrics)

    # 1. Content Quality (Max: 25)
    # Evaluates length, vocabulary variety, and presence of core sections
    cq_ratio = min(1.0, word_count / 450)
    has_contact = bool(contact_info.get("email") and contact_info.get("phone"))
    cq_score = int(weights["content_quality"] * (0.6 * cq_ratio + (0.4 if has_contact else 0.1)))
    cq_exp = f"Evaluated word count ({word_count} words) and contact clarity. Full contact info present." if has_contact else "Missing email or phone number in contact header."

    # 2. Skills Relevance and Evidence (Max: 20)
    # Checks breadth and explicit listing of technical and soft skills
    skills_ratio = min(1.0, (tech_count * 1.5 + soft_count) / 12)
    has_skills_sec = sections.get("has_skills", False)
    sk_score = int(weights["skills_relevance"] * (0.7 * skills_ratio + (0.3 if has_skills_sec else 0.0)))
    sk_exp = f"Found {tech_count} technical skills and {soft_count} soft skills." + (" Dedicated skills section present." if has_skills_sec else " Add a dedicated Skills section.")

    # 3. Projects and Experience (Max: 20)
    exp_present = sections.get("has_experience", False)
    proj_present = sections.get("has_projects", False)
    pe_ratio = 1.0 if (exp_present and proj_present) else (0.7 if (exp_present or proj_present) else 0.2)
    pe_score = int(weights["projects_experience"] * pe_ratio)
    pe_exp = "Both professional experience and project portfolio sections identified." if (exp_present and proj_present) else "Ensure both Hands-on Projects and Experience/Internships are featured."

    # 4. Education and Certifications (Max: 10)
    edu_present = sections.get("has_education", False)
    cert_present = sections.get("has_certifications", False)
    ec_ratio = 1.0 if (edu_present and cert_present) else (0.8 if edu_present else 0.2)
    ec_score = int(weights["education_certifications"] * ec_ratio)
    ec_exp = "Education and recognized certifications/credentials verified." if cert_present else "Education listed. Adding relevant industry certifications will boost this score."

    # 5. Achievements and Measurable Impact (Max: 15)
    if metric_count >= 4:
        am_ratio = 1.0
    elif metric_count >= 2:
        am_ratio = 0.75
    elif metric_count == 1:
        am_ratio = 0.45
    else:
        am_ratio = 0.15
    am_score = int(weights["achievements_impact"] * am_ratio)
    am_exp = f"Detected {metric_count} quantifiable metrics (percentages, numbers, cost savings). ATS and recruiters prioritize quantified impact."

    # 6. Readability and Structure (Max: 10)
    lower_text = text.lower()
    used_verbs = [v for v in ACTION_VERBS if re.search(r'\b' + v + r'\b', lower_text)]
    rs_ratio = min(1.0, (len(used_verbs) / 5) * 0.6 + (0.4 if 300 <= word_count <= 900 else 0.2))
    rs_score = int(weights["readability_structure"] * rs_ratio)
    rs_exp = f"Identified {len(used_verbs)} strong action verbs. Resume length falls within professional parameters."

    total_score = min(100, cq_score + sk_score + pe_score + ec_score + am_score + rs_score)

    breakdown = {
        "content_quality": cq_score,
        "skills_relevance": sk_score,
        "projects_experience": pe_score,
        "education_certifications": ec_score,
        "achievements_impact": am_score,
        "readability_structure": rs_score,
        "total_score": total_score
    }

    explanations = {
        "content_quality": cq_exp,
        "skills_relevance": sk_exp,
        "projects_experience": pe_exp,
        "education_certifications": ec_exp,
        "achievements_impact": am_exp,
        "readability_structure": rs_exp
    }

    return total_score, breakdown, explanations

def analyze_resume_text(text: str) -> Dict[str, Any]:
    """
    Comprehensive resume analysis engine.
    Executes section parsing, skills detection, ATS formatting checks,
    and returns a complete structured analysis payload.
    """
    contact_info = extract_contact_info(text)
    skills = extract_skills(text)
    sections = detect_sections(text)
    metrics = detect_measurable_metrics(text)
    ats_checks = audit_ats_formatting(text, contact_info, sections, metrics)
    total_score, breakdown, explanations = calculate_resume_score(text, contact_info, skills, sections, metrics)

    # Strengths formulation
    strengths = []
    if len(skills.get("technical_skills", [])) >= 5:
        strengths.append({
            "title": "Strong Technical Skill Coverage",
            "detail": f"Highlighted {len(skills['technical_skills'])} in-demand technical competencies including {', '.join(skills['technical_skills'][:4])}."
        })
    if len(metrics) >= 2:
        strengths.append({
            "title": "Quantified Achievements",
            "detail": f"Resume contains {len(metrics)} tangible performance metrics ({', '.join(metrics[:3])}), demonstrating business impact."
        })
    if sections.get("has_projects"):
        strengths.append({
            "title": "Project Portfolio Evidence",
            "detail": "Dedicated project section proves practical application of theoretical concepts."
        })
    if not strengths:
        strengths.append({
            "title": "Readable Foundational Structure",
            "detail": "Resume provides baseline background details suitable for further enhancement."
        })

    # Weaknesses formulation
    weaknesses = []
    if len(metrics) < 2:
        weaknesses.append({
            "title": "Sparse Measurable Metrics",
            "detail": "Bullet points primarily list tasks rather than quantified outcomes (e.g. latency reduced, user counts, % improvement)."
        })
    if not sections.get("has_certifications"):
        weaknesses.append({
            "title": "No Verified Certifications Listed",
            "detail": "Missing technical certifications (e.g., AWS, Azure, Google Cloud, Docker, or Coursera credentials)."
        })
    if not contact_info.get("phone") or not contact_info.get("email"):
        weaknesses.append({
            "title": "Incomplete Contact Header",
            "detail": "Critical contact details are absent or not automatically parseable by ATS scanners."
        })
    if len(skills.get("soft_skills", [])) < 2:
        weaknesses.append({
            "title": "Underrepresented Collaboration Skills",
            "detail": "Few leadership or cross-functional collaboration competencies noted."
        })

    # Actionable Improvement Suggestions
    suggestions = [
        {
            "category": "Quantifying Impact",
            "action": "Transform passive responsibility statements into Google XYZ formulas: 'Accomplished [X] as measured by [Y] by doing [Z]'.",
            "before": "Worked on backend API performance.",
            "after": "Refactored PostgreSQL queries and implemented Redis caching, reducing API latency by 42% across 15 endpoints [insert verified metric]."
        },
        {
            "category": "Keyword Optimization",
            "action": "Ensure technical tool names match exact industry terminology (e.g., 'TypeScript', 'REST APIs', 'Docker').",
            "before": "Experience with databases and cloud.",
            "after": "Architected cloud workloads on AWS (S3, Lambda, RDS) and managed relational databases using PostgreSQL."
        },
        {
            "category": "Project Impact",
            "action": "Include live demo links, GitHub repositories, and brief architecture notes for each project.",
            "before": "Created an e-commerce website.",
            "after": "Developed full-stack e-commerce SPA using React 19, Express, and SQLite with automated checkout and 99.8% test coverage."
        }
    ]

    return {
        "candidate_info": contact_info,
        "skills": skills,
        "sections": sections,
        "metrics": metrics,
        "overall_score": total_score,
        "rubric_breakdown": breakdown,
        "explanations": explanations,
        "ats_checks": ats_checks,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "disclaimer": (
            "Notice: This score is an advisory estimate calculated via transparent algorithmic heuristics "
            "and industry-standard rubric criteria. It is not an official score from any single employer or proprietary ATS vendor."
        )
    }
