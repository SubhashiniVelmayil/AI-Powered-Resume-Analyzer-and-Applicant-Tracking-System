"""
My Applications Page for Streamlit application.
Allows job seekers to monitor their application statuses, view submission dates,
and filter applications by status. Strictly excludes private admin notes.
"""

import streamlit as st
from database import get_connection
from styles import CUSTOM_CSS
from utils.helpers import get_status_badge_color

def render_applications(user: dict):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #38bdf8; margin-bottom: 4px;">My Tracked Applications</h1>
        <p style="color: #94a3b8;">Monitor application stages, estimated match scores, and interview milestones.</p>
    </div>
    """, unsafe_allow_html=True)

    # Filter selector
    status_filter = st.selectbox(
        "Filter by Status:",
        ["All Statuses", "Applied", "Under Review", "Shortlisted", "Interview", "Selected", "Rejected"]
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT a.id as app_id, a.status, a.ats_match_score, a.created_at, a.cover_note,
                   j.title, j.company, j.location, j.work_mode, j.salary_range, j.is_demo
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.user_id = ?
        """
        params = [user["id"]]

        if status_filter != "All Statuses":
            query += " AND a.status = ?"
            params.append(status_filter)

        query += " ORDER BY a.id DESC;"
        cursor.execute(query, params)
        apps = cursor.fetchall()

    if not apps:
        st.info("No applications found matching the selected filter. Browse Job Recommendations to submit your first application!")
        return

    st.caption(f"Displaying **{len(apps)}** application(s):")

    for app in apps:
        color = get_status_badge_color(app["status"])
        demo_str = " (DEMO)" if app["is_demo"] else ""

        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <h3 style="color: #f8fafc; margin: 0;">{app['title']} {demo_str}</h3>
                    <div style="color: #38bdf8; font-size: 0.95rem;">{app['company']} • {app['location']} ({app['work_mode']})</div>
                </div>
                <div style="text-align: right;">
                    <span style="background-color: {color}; color: #ffffff; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;">
                        {app['status']}
                    </span>
                </div>
            </div>
            <div style="display: flex; gap: 24px; font-size: 0.85rem; color: #94a3b8; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px;">
                <div><strong>Applied on:</strong> {app['created_at']}</div>
                <div><strong>ATS Match Score:</strong> {app['ats_match_score'] or 'N/A'}%</div>
                <div><strong>Compensation:</strong> {app['salary_range']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
