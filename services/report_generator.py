"""
Report Generation Service.
Produces structured Markdown and plain text export reports for Resume Analyses,
ATS Comparisons, Improved Bullets, and CSV exports for Admin Application Logs.
"""

import csv
import io
from typing import Dict, Any, List

def generate_resume_analysis_report_markdown(analysis: Dict[str, Any], candidate_name: str = "Candidate") -> str:
    """Generates a professional Markdown audit report of a resume analysis."""
    score = analysis.get("overall_score", 0)
    rubric = analysis.get("rubric_breakdown", {})
    strengths = analysis.get("strengths", [])
    weaknesses = analysis.get("weaknesses", [])
    suggestions = analysis.get("suggestions", [])
    ats_checks = analysis.get("ats_checks", [])
    skills = analysis.get("skills", {})

    lines = [
        f"# Resume Audit & ATS Diagnostic Report: {candidate_name}",
        f"**Generated via**: AI-Powered Resume Analyzer & ATS",
        f"**Advisory Resume Score**: {score} / 100",
        "",
        "> *Notice: This score is an advisory diagnostic benchmark calculated using transparent rubric criteria. It is not an official score issued by any specific employer or ATS vendor.*",
        "",
        "## 1. Transparent Rubric Score Breakdown",
        f"- **Content Quality & Completeness**: {rubric.get('content_quality', 0)} / 25 pts",
        f"- **Skills Relevance & Breadth**: {rubric.get('skills_relevance', 0)} / 20 pts",
        f"- **Projects & Practical Experience**: {rubric.get('projects_experience', 0)} / 20 pts",
        f"- **Education & Certifications**: {rubric.get('education_certifications', 0)} / 10 pts",
        f"- **Quantified Impact & Metrics**: {rubric.get('achievements_impact', 0)} / 15 pts",
        f"- **Readability, Tone & Structure**: {rubric.get('readability_structure', 0)} / 10 pts",
        "",
        "## 2. Identified Competencies",
        f"**Technical Skills**: {', '.join(skills.get('technical_skills', [])) or 'None detected'}",
        f"**Soft Skills**: {', '.join(skills.get('soft_skills', [])) or 'None detected'}",
        "",
        "## 3. Notable Strengths",
    ]

    for s in strengths:
        lines.append(f"- **{s.get('title')}**: {s.get('detail')}")

    lines.append("")
    lines.append("## 4. Areas for Improvement (Weaknesses)")
    for w in weaknesses:
        lines.append(f"- **{w.get('title')}**: {w.get('detail')}")

    lines.append("")
    lines.append("## 5. ATS Formatting & Parsing Audit")
    for chk in ats_checks:
        status_sym = "[PASS]" if chk.get("passed") else "[FLAG]"
        lines.append(f"- **{status_sym} {chk.get('check')}**: {chk.get('recommendation')}")

    lines.append("")
    lines.append("## 6. Actionable Improvement Suggestions")
    for sug in suggestions:
        lines.append(f"### {sug.get('category')}")
        lines.append(f"**Recommendation**: {sug.get('action')}")
        lines.append(f"- *Before*: {sug.get('before')}")
        lines.append(f"- *After*: {sug.get('after')}")
        lines.append("")

    return "\n".join(lines)

def generate_ats_comparison_report_markdown(comparison: Dict[str, Any], job_title: str, company: str) -> str:
    """Generates a detailed Markdown report comparing a resume against a specific job description."""
    score = comparison.get("overall_match_score", 0)
    breakdown = comparison.get("score_breakdown", {})
    matched = comparison.get("matched_skills", [])
    related = comparison.get("related_skills", [])
    missing = comparison.get("missing_skills", [])
    recs = comparison.get("recommendations", [])

    lines = [
        f"# ATS Role Compatibility Report: {job_title} at {company}",
        f"**Estimated Compatibility Score**: {score} / 100",
        "",
        "> *Notice: Advisory estimate based on job description keyword analysis and skill heuristics. Proprietary ATS systems use varied internal ranking weights.*",
        "",
        "## 1. ATS Scoring Rubric Breakdown",
        f"- **Required Skill Coverage**: {breakdown.get('required_skills', 0)} / 40 pts",
        f"- **Experience & Project Evidence**: {breakdown.get('experience_evidence', 0)} / 25 pts",
        f"- **Education & Qualifications**: {breakdown.get('education_match', 0)} / 15 pts",
        f"- **Job Description Keywords**: {breakdown.get('keyword_coverage', 0)} / 15 pts",
        f"- **Certifications Alignment**: {breakdown.get('certifications_match', 0)} / 5 pts",
        "",
        "## 2. Skill Alignment Audit",
        f"### Matched Skills ({len(matched)})",
        f"{', '.join(matched) if matched else 'None directly matched'}",
        "",
        f"### Evidenced via Related Skills ({len(related)})",
        f"{', '.join(related) if related else 'None'}",
        "",
        f"### Missing Target Skills ({len(missing)})",
        f"{', '.join(missing) if missing else 'All key skills found'}",
        "",
        "## 3. Targeted Recommendations to Maximize Match",
    ]

    for r in recs:
        lines.append(f"- {r}")

    return "\n".join(lines)

def export_applications_to_csv(applications: List[Dict[str, Any]]) -> str:
    """Generates sanitized CSV export for administrator application audit."""
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Application ID", "Job ID", "Job Title", "Company",
        "Candidate Name", "Candidate Email", "Status",
        "ATS Match Score", "Date Applied"
    ])

    for app in applications:
        writer.writerow([
            app.get("id", ""),
            app.get("job_id", ""),
            app.get("job_title", ""),
            app.get("company", ""),
            app.get("candidate_name", ""),
            app.get("candidate_email", ""),
            app.get("status", ""),
            app.get("ats_match_score", ""),
            app.get("created_at", "")
        ])

    return output.getvalue()
