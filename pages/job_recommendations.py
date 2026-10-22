"""
Job Recommendations Page for Streamlit application.
Ranks database job opportunities by resume compatibility, explains match rationale,
and provides tailored learning paths with in-app 1-click apply.
"""

import streamlit as st
from database import get_connection
from services.job_matcher import get_job_recommendations
from styles import CUSTOM_CSS

def render_job_recommendations(user: dict):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #38bdf8; margin-bottom: 4px;">Smart Job Recommendations</h1>
        <p style="color: #94a3b8;">Career opportunities ranked dynamically by compatibility with your resume profile.</p>
    </div>
    """, unsafe_allow_html=True)

    # Get user's latest resume
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, raw_text FROM resumes WHERE user_id = ? ORDER BY id DESC LIMIT 1;", (user["id"],))
        latest_res = cursor.fetchone()

    if not latest_res:
        st.warning("⚠️ No uploaded resume found. Upload a resume first to unlock personalized role matching.")
        resume_text = st.text_area("Or paste skills/resume text here to test recommendations immediately:", height=100)
        resume_id = None
    else:
        st.success(f"Matching based on: **{latest_res['filename']}**")
        resume_text = latest_res["raw_text"]
        resume_id = latest_res["id"]

    if not resume_text:
        return

    # Check already submitted applications to prevent duplicates
    applied_job_ids = set()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT job_id FROM applications WHERE user_id = ?;", (user["id"],))
        rows = cursor.fetchall()
        applied_job_ids = {r["job_id"] for r in rows}

    recs = get_job_recommendations(resume_text)

    # Filter controls
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        work_mode_filter = st.multiselect("Filter by Work Mode:", ["Remote", "Hybrid", "On-site"], default=["Remote", "Hybrid", "On-site"])
    with col_f2:
        min_score = st.slider("Minimum Match Percentage:", 0, 100, 30)

    filtered_recs = [r for r in recs if r["work_mode"] in work_mode_filter and r["match_score"] >= min_score]

    st.caption(f"Showing **{len(filtered_recs)}** matched roles:")

    for r in filtered_recs:
        job_id = r["job_id"]
        is_already_applied = job_id in applied_job_ids

        demo_badge = '<span style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; margin-left: 8px;">DEMO DATA</span>' if r["is_demo"] else ''

        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h2 style="color: #f8fafc; margin-bottom: 2px;">{r['title']} {demo_badge}</h2>
                    <h4 style="color: #38bdf8; margin-top: 0;">{r['company']} • <span style="color: #94a3b8; font-size: 0.95rem;">{r['location']} ({r['work_mode']})</span></h4>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 1.8rem; font-weight: 800; color: #4ade80;">{r['match_score']}%</span><br>
                    <span style="font-size: 0.8rem; color: #94a3b8;">Compatibility</span>
                </div>
            </div>
            <div style="margin: 12px 0; color: #cbd5e1; font-size: 0.9rem;">
                <strong>Compensation:</strong> {r['salary_range']} &nbsp;|&nbsp; <strong>Experience Level:</strong> {r['experience_level']}
            </div>
            <div style="color: #e2e8f0; font-size: 0.95rem; margin-bottom: 12px;">
                {r['description']}
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                <div style="font-size: 0.85rem; color: #38bdf8; font-weight: bold;">WHY RECOMMENDED:</div>
                <div style="font-size: 0.9rem; color: #f1f5f9;">{r['recommendation_reason']}</div>
                <div style="margin-top: 8px; font-size: 0.85rem; color: #c084fc; font-weight: bold;">SUGGESTED LEARNING PATH:</div>
                <div style="font-size: 0.85rem; color: #cbd5e1;">{" • ".join(r['suggested_learning_path'])}</div>
            </div>
            <div style="margin-bottom: 12px;">
                <span style="color: #4ade80; font-size: 0.85rem; font-weight: bold;">Matched Skills:</span> <span style="color: #cbd5e1; font-size: 0.85rem;">{', '.join(r['matched_skills']) or 'None'}</span><br>
                <span style="color: #f87171; font-size: 0.85rem; font-weight: bold;">Missing Skills:</span> <span style="color: #cbd5e1; font-size: 0.85rem;">{', '.join(r['missing_skills']) or 'None'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_app1, col_app2 = st.columns([2, 5])
        with col_app1:
            if is_already_applied:
                st.button("Applied Already", key=f"btn_applied_{job_id}", disabled=True)
            else:
                if st.button("Submit Application (ATS)", key=f"btn_apply_{job_id}"):
                    with get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO applications (job_id, user_id, resume_id, status, ats_match_score)
                            VALUES (?, ?, ?, 'Applied', ?);
                        """, (job_id, user["id"], resume_id, r["match_score"]))
                        conn.commit()
                    st.success(f"Application submitted for {r['title']}!")
                    st.rerun()
        with col_app2:
            st.markdown(f"[External Posting Link]({r['application_url']}) *(Example DEMO application URL)*")

        st.markdown("<br>", unsafe_allow_html=True)
