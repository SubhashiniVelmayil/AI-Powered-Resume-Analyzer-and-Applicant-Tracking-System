"""
Validation utilities for inputs, statuses, and role-based permissions.
"""

from typing import Tuple, Dict, Any, List

VALID_APPLICATION_STATUSES = [
    "Applied",
    "Under Review",
    "Shortlisted",
    "Interview",
    "Selected",
    "Rejected"
]

VALID_WORK_MODES = ["Remote", "Hybrid", "On-site"]

VALID_ROLES = ["job_seeker", "admin"]

def validate_job_payload(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates required fields when creating or updating a job posting."""
    title = str(data.get("title", "")).strip()
    company = str(data.get("company", "")).strip()
    location = str(data.get("location", "")).strip()
    work_mode = str(data.get("work_mode", "")).strip()
    description = str(data.get("description", "")).strip()
    required_skills = str(data.get("required_skills", "")).strip()

    if not title:
        return False, "Job title cannot be empty."
    if not company:
        return False, "Company name cannot be empty."
    if not location:
        return False, "Location cannot be empty."
    if work_mode not in VALID_WORK_MODES:
        return False, f"Work mode must be one of: {', '.join(VALID_WORK_MODES)}."
    if not description or len(description) < 20:
        return False, "Job description must be at least 20 characters."
    if not required_skills:
        return False, "Please provide at least one required skill."

    return True, "Valid job payload."

def validate_application_status(status: str) -> bool:
    """Verifies that an application status is one of the permitted lifecycle states."""
    return status in VALID_APPLICATION_STATUSES
