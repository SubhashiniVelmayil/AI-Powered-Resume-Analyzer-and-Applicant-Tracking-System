"""
Data models and typed structures for the Resume Analyzer and ATS platform.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class User:
    id: int
    email: str
    full_name: str
    role: str
    created_at: Optional[str] = None

@dataclass
class ResumeRecord:
    id: int
    user_id: int
    filename: str
    file_size_bytes: int
    raw_text: str
    is_scanned_notice: bool
    created_at: Optional[str] = None

@dataclass
class JobRecord:
    id: int
    title: str
    company: str
    location: str
    work_mode: str
    experience_level: str
    salary_range: str
    required_skills: str
    preferred_qualifications: str
    description: str
    application_url: str
    is_active: bool = True
    is_demo: bool = True
    created_by: Optional[int] = None
    created_at: Optional[str] = None

@dataclass
class ApplicationRecord:
    id: int
    job_id: int
    user_id: int
    resume_id: Optional[int]
    status: str
    ats_match_score: Optional[int]
    cover_note: Optional[str]
    created_at: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None

@dataclass
class ResumeScoreBreakdown:
    content_quality: int
    skills_relevance: int
    projects_experience: int
    education_certifications: int
    achievements_impact: int
    readability_structure: int
    total_score: int
    explanations: Dict[str, str]

@dataclass
class ATSComparisonResult:
    overall_match_score: int
    score_breakdown: Dict[str, int]
    matched_skills: List[str]
    missing_skills: List[str]
    related_skills: List[str]
    keyword_matches: List[str]
    recommendations: List[str]
    is_official_disclaimer: str = (
        "Advisory estimate based on keyword frequency, skill coverage, and role relevance. "
        "Proprietary employer ATS tools use diverse private scoring algorithms and human review."
    )
