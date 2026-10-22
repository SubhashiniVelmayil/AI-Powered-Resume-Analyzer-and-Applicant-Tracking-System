"""
Home Dashboard Page for Streamlit application.
Displays overview KPI metrics, quick actions, recent activity, and system diagnostics.
"""

import streamlit as st
from database import get_connection
from styles import CUSTOM_CSS, render_metric_card

def render_home_dashboard(user: dict):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        <h1 style="color: #38bdf8; margin-bottom: 4px;">Welcome back, {user.get('full_name', 'User')}</h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">AI-Powered Resume Analyzer & Applicant Tracking Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch user counts
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM resumes WHERE user_id = ?;", (user["id"],))
        resumes_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE user_id = ?;", (user["id"],))
        apps_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1;")
        active_jobs_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT overall_score FROM resume_analyses
            WHERE user_id = ? ORDER BY id DESC LIMIT 1;
        """, (user["id"],))
        latest_analysis = cursor.fetchone()
        latest_score = f"{latest_analysis['overall_score']} / 100" if latest_analysis else "No upload yet"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_metric_card("Analyzed Resumes", str(resumes_count), "Uploaded & parsed"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("Latest Resume Score", latest_score, "Transparent 100-pt rubric"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("Active Job Listings", str(active_jobs_count), "Curated DEMO & live roles"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_card("My Applications", str(apps_count), "Active ATS tracking"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Access Workflow Cards
    st.subheader("Quick Navigation & Actions")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #38bdf8; margin-top:0;">📄 Resume Analyzer</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">
                Upload your PDF resume to extract contact details, technical skills, identify strengths & gaps,
                and receive an advisory 100-point rubric score.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Resume Analyzer", key="btn_dash_resume"):
            st.session_state["nav_selection"] = "Resume Analyzer"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #c084fc; margin-top:0;">🎯 ATS Score Checker</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">
                Paste a target job description to measure skill overlap, uncover missing keywords,
                and review action-oriented phrasing suggestions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open ATS Checker", key="btn_dash_ats"):
            st.session_state["nav_selection"] = "ATS Score Checker"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #34d399; margin-top:0;">💼 Job Recommendations</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">
                Explore automated job matches ranked by compatibility with your resume skills,
                complete with custom learning paths.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Jobs", key="btn_dash_jobs"):
            st.session_state["nav_selection"] = "Job Recommendations"
            st.rerun()
