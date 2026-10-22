"""
Job-Specific ATS Score Checker Page for Streamlit application.
Compares candidate resume against existing or custom job descriptions,
evaluates 100-point compatibility rubric, and provides keyword gap analysis.
"""

import streamlit as st
from database import get_connection
from services.ats_scorer import compare_resume_to_job
from services.report_generator import generate_ats_comparison_report_markdown
from styles import CUSTOM_CSS

def render_ats_checker(user: dict):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #38bdf8; margin-bottom: 4px;">Job-Specific ATS Compatibility Checker</h1>
        <p style="color: #94a3b8;">Benchmark your resume against specific job requirements using our 100-point transparent compatibility rubric.</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Select or paste resume
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, raw_text FROM resumes WHERE user_id = ? ORDER BY id DESC;", (user["id"],))
        user_resumes = cursor.fetchall()

    if not user_resumes:
        st.warning("You have not uploaded a resume yet. Please upload one in the Resume Analyzer or paste your text below.")
        resume_text = st.text_area("Paste your Resume Text:", height=150)
    else:
        resume_options = {f"{r['filename']} (ID: {r['id']})": r["raw_text"] for r in user_resumes}
        resume_options["Paste custom text directly"] = ""
        chosen_resume = st.selectbox("Select Resume to Evaluate:", list(resume_options.keys()))
        if chosen_resume == "Paste custom text directly":
            resume_text = st.text_area("Paste Resume Text:", height=150)
        else:
            resume_text = resume_options[chosen_resume]

    # 2. Select or paste target job description
    st.markdown("<hr style='border-color: rgba(139,92,246,0.2);'>", unsafe_allow_html=True)
    st.subheader("Target Job Posting")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, company, required_skills, preferred_qualifications, description FROM jobs WHERE is_active = 1;")
        active_jobs = cursor.fetchall()

    job_choice_mode = st.radio("Choose Target Job Source:", ["Select from Curated Active Listings", "Paste Custom Job Description Manually"], horizontal=True)

    target_title = ""
    target_company = ""
    target_req_skills = ""
    target_pref_quals = ""
    target_desc = ""

    if job_choice_mode == "Select from Curated Active Listings" and active_jobs:
        job_map = {f"{j['title']} @ {j['company']}": j for j in active_jobs}
        selected_job_key = st.selectbox("Choose Job:", list(job_map.keys()))
        sel_job = job_map[selected_job_key]
        target_title = sel_job["title"]
        target_company = sel_job["company"]
        target_req_skills = sel_job["required_skills"]
        target_pref_quals = sel_job["preferred_qualifications"]
        target_desc = sel_job["description"]

        st.caption(f"Required Skills: **{target_req_skills}**")
    else:
        target_title = st.text_input("Job Title:", "Senior Full Stack Engineer")
        target_company = st.text_input("Company Name:", "TechCorp Global")
        target_req_skills = st.text_input("Required Skills (comma separated):", "React, TypeScript, Python, SQL, Docker, AWS")
        target_desc = st.text_area("Full Job Description:", height=150, value="We are looking for an experienced software engineer to build scalable web applications with React, TypeScript, Python microservices, and PostgreSQL.")

    if st.button("🔍 Check ATS Compatibility Score", key="btn_check_ats"):
        if not resume_text:
            st.error("Please supply resume text.")
            return

        with st.spinner("Calculating ATS compatibility rubric & semantic alignment..."):
            comparison = compare_resume_to_job(
                resume_text=resume_text,
                job_title=target_title,
                job_description=target_desc,
                required_skills=target_req_skills,
                preferred_qualifications=target_pref_quals
            )

        match_score = comparison["overall_match_score"]

        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h2 style="color: #94a3b8; margin-bottom: 8px;">Role ATS Compatibility Estimate</h2>
            <div class="score-badge" style="border-color: #a855f7; box-shadow: 0 0 24px rgba(168,85,247,0.4);">{match_score}%</div>
            <p style="color: #cbd5e1; margin-top: 14px; max-width: 600px; margin-left: auto; margin-right: auto;">
                {comparison['disclaimer']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Rubric breakdown
        st.subheader("🎯 ATS Rubric Breakdown (Max: 100 Points)")
        bd = comparison["score_breakdown"]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Required Skill Coverage", f"{bd['required_skills']} / 40 pts")
            st.metric("Experience Evidence", f"{bd['experience_evidence']} / 25 pts")
        with c2:
            st.metric("Education & Qualifications", f"{bd['education_match']} / 15 pts")
            st.metric("Keyword Coverage", f"{bd['keyword_coverage']} / 15 pts")
        with c3:
            st.metric("Certifications Alignment", f"{bd['certifications_match']} / 5 pts")

        # Skills breakdown: Matched, Related, Missing
        st.markdown("<hr style='border-color: rgba(139,92,246,0.2);'>", unsafe_allow_html=True)
        col_m, col_r, col_gap = st.columns(3)

        with col_m:
            st.markdown(f"### ✅ Exact Matches ({len(comparison['matched_skills'])})")
            for m in comparison["matched_skills"]:
                st.markdown(f"<span style='color: #4ade80;'>• {m}</span>", unsafe_allow_html=True)
            if not comparison["matched_skills"]:
                st.caption("No exact keyword matches found.")

        with col_r:
            st.markdown(f"### 🔄 Related Skills ({len(comparison['related_skills'])})")
            for r in comparison["related_skills"]:
                st.markdown(f"<span style='color: #38bdf8;'>• {r}</span>", unsafe_allow_html=True)
            if not comparison["related_skills"]:
                st.caption("No related skills detected.")

        with col_gap:
            st.markdown(f"### ⚠️ Missing Skills ({len(comparison['missing_skills'])})")
            for gap in comparison["missing_skills"]:
                st.markdown(f"<span style='color: #f87171;'>• {gap}</span>", unsafe_allow_html=True)
            if not comparison["missing_skills"]:
                st.caption("No skill gaps detected!")

        # Recommendations
        st.subheader("💡 Strategic Recommendations to Maximize Match")
        for rec in comparison["recommendations"]:
            st.markdown(f"""
            <div class="alert-box">
                {rec}
            </div>
            """, unsafe_allow_html=True)

        # Download comparison report
        report_md = generate_ats_comparison_report_markdown(comparison, target_title, target_company)
        st.download_button(
            label="📥 Download ATS Compatibility Report (.md)",
            data=report_md,
            file_name=f"{target_title.replace(' ', '_')}_ATS_Report.md",
            mime="text/markdown"
        )
