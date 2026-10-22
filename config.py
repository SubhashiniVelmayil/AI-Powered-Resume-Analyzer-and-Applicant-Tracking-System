"""
Configuration settings for AI-Powered Resume Analyzer and ATS.
Supports environment variables with sensible defaults and local fallback modes.
"""

import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Data directory
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Database path (SQLite)
DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "resume_ats.db"))

# AI API Configurations
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Initial Administrator Credentials (used for safe first-run bootstrap)
ADMIN_DEFAULT_EMAIL = os.getenv("ADMIN_EMAIL", "admin@resumetracker.local")
ADMIN_DEFAULT_PASSWORD = os.getenv("ADMIN_PASSWORD", "AdminSecure2026!")

# Maximum file upload size in MB
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "5"))

# Allowed file extensions
ALLOWED_EXTENSIONS = [".pdf"]

# Configurable Rubric Weights for Resume Score (Total = 100)
RESUME_SCORING_WEIGHTS = {
    "content_quality": 25,
    "skills_relevance": 20,
    "projects_experience": 20,
    "education_certifications": 10,
    "achievements_impact": 15,
    "readability_structure": 10,
}

# Configurable Rubric Weights for ATS Job Match Score (Total = 100)
ATS_SCORING_WEIGHTS = {
    "required_skills": 40,
    "experience_evidence": 25,
    "education_match": 15,
    "keyword_coverage": 15,
    "certifications_match": 5,
}

# Application UI Theme Settings
THEME_TITLE = "AI-Powered Resume Analyzer & Applicant Tracking System"
THEME_SUBTITLE = "Analyze smarter. Improve your resume. Discover better career opportunities."
