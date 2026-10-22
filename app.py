"""
Main Streamlit Application Entrypoint.
Coordinates database initialization, authentication, session state,
and multi-page dashboard navigation.
"""

import streamlit as st
import os
from database import init_db
from auth import register_user, authenticate_user, bootstrap_admin
from styles import CUSTOM_CSS
from config import THEME_TITLE, THEME_SUBTITLE

# Import multi-page view renderers
from pages.dashboard import render_home_dashboard
from pages.resume_analyzer import render_resume_analyzer
from pages.ats_checker import render_ats_checker
from pages.job_recommendations import render_job_recommendations
from pages.applications import render_applications
from pages.admin_dashboard import render_admin_dashboard
from pages.profile import render_profile

# Configure Streamlit page layout
st.set_page_config(
    page_title="AI Resume Analyzer & ATS",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 1. Initialize Database & Safe Admin Bootstrap
if "db_initialized" not in st.session_state:
    init_db()
    bootstrap_admin()
    st.session_state["db_initialized"] = True

# 2. Session state management
if "user" not in st.session_state:
    st.session_state["user"] = None

if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "Home Dashboard"

def render_login_and_landing():
    """Renders the landing and authentication interface for unauthenticated guests."""
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 20px 20px;">
        <h1 style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px;">
            {THEME_TITLE}
        </h1>
        <p style="font-size: 1.25rem; color: #94a3b8; max-width: 700px; margin: 0 auto 30px;">
            {THEME_SUBTITLE}
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_left, c_right = st.columns([1, 1], gap="large")

    with c_left:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #38bdf8; margin-top: 0;">Why Use AI Resume Analyzer?</h3>
            <ul style="color: #cbd5e1; line-height: 1.8; font-size: 0.95rem;">
                <li><strong>Transparent 100-Point Scoring:</strong> Clear rubric for content quality, skills relevance, projects, impact metrics, and readability.</li>
                <li><strong>Job-Specific ATS Compatibility:</strong> Semantic alignment distinguishing exact keywords from related technologies.</li>
                <li><strong>Smart Job Matching:</strong> Discover verified roles and tailored learning paths based on your real resume evidence.</li>
                <li><strong>Full Applicant Tracking System:</strong> Apply directly, monitor review stages, and manage candidate workflows.</li>
                <li><strong>Privacy First:</strong> Secure PBKDF2 password hashing, isolated user data, and zero plaintext exposure.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.info("💡 **Quick Demo Credentials**:\n- **Admin**: `admin@resumetracker.local` / `AdminSecure2026!`\n- Or register your own instant job seeker account on the right.")

    with c_right:
        auth_mode = st.radio("Choose Action:", ["Login to Existing Account", "Register New Account"], horizontal=True)

        if auth_mode == "Login to Existing Account":
            with st.form("login_form"):
                st.subheader("Account Sign In")
                email = st.text_input("Email Address", placeholder="name@example.com")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign In")

                if submitted:
                    ok, msg, user = authenticate_user(email, password)
                    if ok:
                        st.session_state["user"] = user
                        st.session_state["nav_selection"] = "Home Dashboard"
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
        else:
            with st.form("register_form"):
                st.subheader("Create Free Account")
                full_name = st.text_input("Full Name", placeholder="Alex Morgan")
                reg_email = st.text_input("Email Address", placeholder="alex.morgan@example.com")
                reg_password = st.text_input("Password (min 8 characters, uppercase, lowercase, digit)", type="password")
                role_choice = st.selectbox("I am joining as a:", ["job_seeker", "admin"], format_func=lambda x: "Job Seeker / Candidate" if x == "job_seeker" else "Recruiter / Administrator")
                reg_submitted = st.form_submit_button("Create Account")

                if reg_submitted:
                    ok, msg, new_user = register_user(reg_email, reg_password, full_name, role_choice)
                    if ok:
                        st.session_state["user"] = new_user
                        st.session_state["nav_selection"] = "Home Dashboard"
                        st.success("Registration successful! Logging you in...")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

def render_authenticated_app():
    """Renders the main navigation sidebar and views for signed-in users."""
    user = st.session_state["user"]
    is_admin = user.get("role") == "admin"

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="padding: 10px 0 16px;">
            <h2 style="color: #38bdf8; font-size: 1.3rem; margin: 0;">⚡ Resume & ATS</h2>
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 2px 0 0;">Intelligent Career Portal</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 10px; border-radius: 8px; margin-bottom: 20px;">
            <div style="font-weight: 600; color: #f8fafc; font-size: 0.9rem;">{user['full_name']}</div>
            <div style="font-size: 0.8rem; color: #38bdf8;">{'👑 Administrator' if is_admin else '👤 Job Seeker'}</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation options
        nav_options = [
            "Home Dashboard",
            "Resume Analyzer",
            "ATS Score Checker",
            "Job Recommendations",
            "My Applications"
        ]

        # Admin only options
        if is_admin:
            nav_options.append("Admin Dashboard")

        nav_options.append("Profile and Settings")

        # Selectbox navigation
        curr_nav = st.session_state.get("nav_selection", "Home Dashboard")
        curr_index = nav_options.index(curr_nav) if curr_nav in nav_options else 0

        selection = st.radio("Navigation Menu", nav_options, index=curr_index)
        st.session_state["nav_selection"] = selection

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Log Out", key="sidebar_logout_btn"):
            st.session_state["user"] = None
            st.session_state["nav_selection"] = "Home Dashboard"
            st.rerun()

    # View Routing
    active_page = st.session_state["nav_selection"]

    if active_page == "Home Dashboard":
        render_home_dashboard(user)
    elif active_page == "Resume Analyzer":
        render_resume_analyzer(user)
    elif active_page == "ATS Score Checker":
        render_ats_checker(user)
    elif active_page == "Job Recommendations":
        render_job_matcher = render_job_recommendations(user)
    elif active_page == "My Applications":
        render_applications(user)
    elif active_page == "Admin Dashboard":
        if is_admin:
            render_admin_dashboard(user)
        else:
            st.error("Access denied.")
    elif active_page == "Profile and Settings":
        render_profile(user)

def main():
    if st.session_state["user"] is None:
        render_login_and_landing()
    else:
        render_authenticated_app()

if __name__ == "__main__":
    main()
