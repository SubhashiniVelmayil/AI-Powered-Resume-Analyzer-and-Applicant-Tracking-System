"""
Job Recommendation Engine.
Matches candidate resume profiles against active database jobs.
Calculates match percentages, identifies skill overlaps, and suggests tailored learning paths.
"""

from typing import List, Dict, Any, Optional
from database import get_connection
from services.ats_scorer import compare_resume_to_job

def get_job_recommendations(resume_text: str, candidate_skills: Optional[List[str]] = None, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Scans all active job listings in the database and ranks them by compatibility score.
    Returns structured recommendations with matched skills, missing skills, and learning paths.
    """
    recommendations = []

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, company, location, work_mode, experience_level,
                   salary_range, required_skills, preferred_qualifications,
                   description, application_url, is_demo
            FROM jobs
            WHERE is_active = 1
            ORDER BY id ASC;
        """)
        jobs = cursor.fetchall()

    for job in jobs:
        comp = compare_resume_to_job(
            resume_text=resume_text,
            job_title=job["title"],
            job_description=job["description"],
            required_skills=job["required_skills"],
            preferred_qualifications=job["preferred_qualifications"]
        )

        match_score = comp["overall_match_score"]
        matched = comp["matched_skills"]
        missing = comp["missing_skills"]

        # Formulate rationale
        if match_score >= 70:
            reason = f"High alignment with your core technical competencies ({', '.join(matched[:3])})."
        elif match_score >= 50:
            reason = f"Good baseline foundation. You possess {len(matched)} matching skills, with moderate gap in {', '.join(missing[:2])}."
        else:
            reason = f"Growth opportunity. Broadens your capabilities into {job['title']} technologies."

        # Formulate suggested learning path
        learning_path = []
        for m in missing[:3]:
            learning_path.append(f"Master {m}: Build a small portfolio micro-project demonstrating hands-on usage.")

        recommendations.append({
            "job_id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "work_mode": job["work_mode"],
            "experience_level": job["experience_level"],
            "salary_range": job["salary_range"],
            "required_skills": job["required_skills"],
            "description": job["description"],
            "application_url": job["application_url"],
            "is_demo": bool(job["is_demo"]),
            "match_score": match_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "related_skills": comp["related_skills"],
            "recommendation_reason": reason,
            "suggested_learning_path": learning_path or ["Continue maintaining and showcasing current project portfolio."]
        })

    # Sort descending by match score
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations
