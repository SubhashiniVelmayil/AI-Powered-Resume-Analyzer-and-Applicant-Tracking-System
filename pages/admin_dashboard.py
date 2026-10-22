"""
Administrator Dashboard Page for Streamlit application.
Provides system metrics, candidate application review, status pipeline updates,
confidential internal recruiter notes, job creation/management, and CSV audits.
Strictly enforced on backend.
"""

import streamlit as st
import json
from database import get_connection
from utils.validators import validate_job_payload, VALID_APPLICATION_STATUSES
from services.report_generator import export_applications_to_csv
from styles import CUSTOM_CSS, render_metric_card

def render_admin_dashboard(user: dict):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Server-side backend authorization check
    if user.get("role") != "admin":
        st.error("🚫 Access Denied: You do not possess administrator credentials.")
        st.stop()

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #38bdf8; margin-bottom: 4px;">Recruiter & ATS Administrator Console</h1>
        <p style="color: #94a3b8;">Manage job listings, evaluate candidate pipelines, update statuses, and log confidential notes.</p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch Platform Statistics
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM resumes;")
        total_resumes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM resume_analyses;")
        total_analyses = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs;")
        total_jobs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications;")
        total_apps = cursor.fetchone()[0]

        # Status count breakdown
        cursor.execute("SELECT status, COUNT(*) as cnt FROM applications GROUP BY status;")
        status_counts = {r["status"]: r["cnt"] for r in cursor.fetchall()}

    # KPI Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(render_metric_card("Registered Users", str(total_users)), unsafe_allow_html=True)
    with c2:
        st.markdown(render_metric_card("Uploaded Resumes", str(total_resumes)), unsafe_allow_html=True)
    with c3:
        st.markdown(render_metric_card("Completed Analyses", str(total_analyses)), unsafe_allow_html=True)
    with c4:
        st.markdown(render_metric_card("Job Listings", str(total_jobs)), unsafe_allow_html=True)
    with c5:
        st.markdown(render_metric_card("Total Applications", str(total_apps)), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_apps, tab_jobs, tab_users = st.tabs(["Candidate Application Pipeline", "Job Management", "Platform Users"])

    with tab_apps:
        st.subheader("Candidate Application Pipeline & Status Management")

        # Filters
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            filter_status = st.selectbox("Filter Status:", ["All"] + VALID_APPLICATION_STATUSES)
        with f_col2:
            search_query = st.text_input("Search Candidate Name or Job Title:")

        # Query applications
        with get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT a.id as app_id, a.job_id, a.user_id, a.resume_id, a.status, a.ats_match_score,
                       a.cover_note, a.created_at,
                       u.full_name as candidate_name, u.email as candidate_email,
                       j.title as job_title, j.company
                FROM applications a
                JOIN users u ON a.user_id = u.id
                JOIN jobs j ON a.job_id = j.id
                WHERE 1=1
            """
            params = []
            if filter_status != "All":
                query += " AND a.status = ?"
                params.append(filter_status)
            if search_query:
                query += " AND (u.full_name LIKE ? OR j.title LIKE ? OR u.email LIKE ?)"
                wildcard = f"%{search_query}%"
                params.extend([wildcard, wildcard, wildcard])

            query += " ORDER BY a.id DESC;"
            cursor.execute(query, params)
            applications_list = [dict(r) for r in cursor.fetchall()]

        # CSV Export button
        if applications_list:
            csv_data = export_applications_to_csv(applications_list)
            st.download_button(
                label="📥 Export Filtered Applications (CSV)",
                data=csv_data,
                file_name="applicant_tracking_pipeline_export.csv",
                mime="text/csv"
            )

        st.caption(f"Showing **{len(applications_list)}** application record(s):")

        for app in applications_list:
            app_id = app["app_id"]
            with st.expander(f"Candidate: {app['candidate_name']} ({app['candidate_email']}) -> {app['job_title']} [{app['status']}]"):
                col_info, col_action = st.columns([3, 2])

                with col_info:
                    st.markdown(f"**Applied On:** {app['created_at']}")
                    st.markdown(f"**ATS Compatibility Estimate:** `{app['ats_match_score'] or 'N/A'}%`")
                    st.markdown(f"**Company:** {app['company']}")

                    # Resume content preview if available
                    if app["resume_id"]:
                        with get_connection() as conn:
                            cur2 = conn.cursor()
                            cur2.execute("SELECT raw_text, filename FROM resumes WHERE id = ?;", (app["resume_id"],))
                            res_row = cur2.fetchone()
                        if res_row:
                            st.caption(f"Attached Resume: {res_row['filename']}")
                            with st.expander("View Candidate Resume Text"):
                                st.text(res_row["raw_text"][:1200] + ("..." if len(res_row["raw_text"]) > 1200 else ""))

                with col_action:
                    st.markdown("#### Update Lifecycle Status")
                    curr_idx = VALID_APPLICATION_STATUSES.index(app["status"]) if app["status"] in VALID_APPLICATION_STATUSES else 0
                    new_status = st.selectbox(
                        "Change Status:",
                        VALID_APPLICATION_STATUSES,
                        index=curr_idx,
                        key=f"status_select_{app_id}"
                    )
                    if st.button("Save New Status", key=f"btn_save_status_{app_id}"):
                        with get_connection() as conn:
                            conn.execute("UPDATE applications SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?;", (new_status, app_id))
                            conn.commit()
                        st.success(f"Updated status to {new_status}!")
                        st.rerun()

                # Confidential internal notes
                st.markdown("<hr style='border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
                st.markdown("#### 🔒 Confidential Internal Recruiter Notes *(Strictly hidden from candidate)*")

                with get_connection() as conn:
                    cur_notes = conn.cursor()
                    cur_notes.execute("""
                        SELECT n.id, n.note, n.created_at, u.full_name as author_name
                        FROM application_notes n
                        JOIN users u ON n.author_id = u.id
                        WHERE n.application_id = ?
                        ORDER BY n.id ASC;
                    """, (app_id,))
                    notes = cur_notes.fetchall()

                for n in notes:
                    st.markdown(f"""
                    <div style="background: rgba(30, 41, 59, 0.7); border-left: 3px solid #38bdf8; padding: 8px 12px; border-radius: 6px; margin-bottom: 6px; font-size: 0.85rem;">
                        <strong>{n['author_name']}</strong> <span style="color: #94a3b8; font-size: 0.75rem;">({n['created_at']})</span><br>
                        {n['note']}
                    </div>
                    """, unsafe_allow_html=True)

                new_note = st.text_input("Add internal observation / interview feedback:", key=f"input_note_{app_id}")
                if st.button("Add Confidential Note", key=f"btn_note_{app_id}"):
                    if new_note.strip():
                        with get_connection() as conn:
                            conn.execute("""
                                INSERT INTO application_notes (application_id, author_id, note)
                                VALUES (?, ?, ?);
                            """, (app_id, user["id"], new_note.strip()))
                            conn.commit()
                        st.success("Internal note recorded.")
                        st.rerun()

    with tab_jobs:
        st.subheader("Manage Job Listings")

        with st.expander("➕ Create New Job Listing"):
            new_title = st.text_input("Job Title*", "DevOps Engineer")
            new_company = st.text_input("Company Name*", "CloudWave Infrastructure (DEMO DATA)")
            new_location = st.text_input("Location*", "Austin, TX")
            new_mode = st.selectbox("Work Mode*", ["Remote", "Hybrid", "On-site"])
            new_level = st.selectbox("Experience Level*", ["Entry Level (0-2 years)", "Mid Level (2-5 years)", "Senior (5+ years)"])
            new_salary = st.text_input("Salary Range*", "$90,000 - $115,000/yr")
            new_skills = st.text_input("Required Skills (comma separated)*", "Docker, Kubernetes, AWS, Python, CI/CD")
            new_prefs = st.text_input("Preferred Qualifications", "Terraform, Linux, Prometheus")
            new_desc = st.text_area("Job Description*", height=100, value="Seeking a DevOps engineer to automate deployment pipelines, maintain Kubernetes infrastructure, and build cloud-native monitoring solutions. [DEMO DATA]")
            new_url = st.text_input("Application URL*", "https://example.com/careers/demo-job")
            is_demo = st.checkbox("Mark as DEMO DATA", value=True)

            if st.button("Publish Job Listing", key="btn_publish_job"):
                payload = {
                    "title": new_title,
                    "company": new_company,
                    "location": new_location,
                    "work_mode": new_mode,
                    "description": new_desc,
                    "required_skills": new_skills
                }
                valid, msg = validate_job_payload(payload)
                if not valid:
                    st.error(msg)
                else:
                    with get_connection() as conn:
                        conn.execute("""
                            INSERT INTO jobs (
                                title, company, location, work_mode, experience_level,
                                salary_range, required_skills, preferred_qualifications,
                                description, application_url, is_active, is_demo, created_by
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?);
                        """, (
                            new_title, new_company, new_location, new_mode, new_level,
                            new_salary, new_skills, new_prefs, new_desc, new_url,
                            1 if is_demo else 0, user["id"]
                        ))
                        conn.commit()
                    st.success(f"Job '{new_title}' successfully published!")
                    st.rerun()

        # List existing jobs
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs ORDER BY id DESC;")
            all_jobs = cursor.fetchall()

        st.caption(f"Total jobs in database: **{len(all_jobs)}**")
        for job in all_jobs:
            status_text = "Active" if job["is_active"] else "Inactive"
            badge = "🟢" if job["is_active"] else "🔴"
            demo_flag = " (DEMO DATA)" if job["is_demo"] else ""

            col_j, col_tog = st.columns([4, 1])
            with col_j:
                st.markdown(f"**{badge} {job['title']}** @ {job['company']}{demo_flag} | {job['location']} ({job['work_mode']}) | *{status_text}*")
            with col_tog:
                action_label = "Deactivate" if job["is_active"] else "Activate"
                if st.button(action_label, key=f"tog_job_{job['id']}"):
                    new_val = 0 if job["is_active"] else 1
                    with get_connection() as conn:
                        conn.execute("UPDATE jobs SET is_active = ? WHERE id = ?;", (new_val, job["id"]))
                        conn.commit()
                    st.rerun()

    with tab_users:
        st.subheader("Platform User Accounts")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, full_name, role, created_at FROM users ORDER BY id ASC;")
            users_list = cursor.fetchall()

        for u in users_list:
            role_badge = "👑 Admin" if u["role"] == "admin" else "👤 Job Seeker"
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.4); padding: 8px 14px; border-radius: 8px; margin-bottom: 6px; display: flex; justify-content: space-between;">
                <div><strong>{u['full_name']}</strong> ({u['email']})</div>
                <div><span style="color: #38bdf8;">{role_badge}</span> &nbsp; <span style="color: #94a3b8; font-size: 0.8rem;">Joined: {u['created_at']}</span></div>
            </div>
            """, unsafe_allow_html=True)
