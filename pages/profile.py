"""
Profile & Settings Page for Streamlit application.
Displays user account information, role permissions, active session details,
API key configuration instructions, and security guidelines.
"""

import streamlit as st
import os
from styles import CUSTOM_CSS

def render_profile(user: dict):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #38bdf8; margin-bottom: 4px;">Profile & System Settings</h1>
        <p style="color: #94a3b8;">Manage your account credentials, security preferences, and AI API integrations.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: #38bdf8; margin-top: 0;">Account Profile</h3>
            <p><strong>Full Name:</strong> {user.get('full_name')}</p>
            <p><strong>Email Address:</strong> {user.get('email')}</p>
            <p><strong>Account Role:</strong> <span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 2px 8px; border-radius: 4px; font-weight: bold;">{user.get('role')}</span></p>
            <p><strong>User ID:</strong> #{user.get('id')}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Log Out of Session", key="btn_logout"):
            st.session_state["user"] = None
            st.session_state["nav_selection"] = "Home Dashboard"
            st.success("You have been safely logged out.")
            st.rerun()

    with c2:
        groq_configured = bool(os.getenv("GROQ_API_KEY"))
        groq_badge = "🟢 Configured" if groq_configured else "⚪ Local Fallback Active"

        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: #c084fc; margin-top: 0;">AI Service Integration Status</h3>
            <p><strong>Groq Cloud API:</strong> {groq_badge}</p>
            <p><strong>Active Model:</strong> <code>{os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")}</code></p>
            <p><strong>Local Heuristic Engine:</strong> 🟢 Ready & Fully Operational</p>
            <hr style="border-color: rgba(255,255,255,0.08);">
            <div style="font-size: 0.85rem; color: #cbd5e1;">
                <strong>How to configure Groq API Key:</strong><br>
                1. Obtain a free API key at <a href="https://console.groq.com" target="_blank" style="color: #38bdf8;">console.groq.com</a><br>
                2. Open your <code>.env</code> file in the project root<br>
                3. Set: <code>GROQ_API_KEY="your_api_key_here"</code><br>
                4. Restart the Streamlit application
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(139,92,246,0.2);'>", unsafe_allow_html=True)
    st.subheader("🛡️ Security & Privacy Notice")
    st.markdown("""
    - **Password Security:** Passwords are never stored in plaintext. They are hashed using standard PBKDF2-HMAC-SHA256 with unique 16-byte cryptographically secure random salts and 100,000 computation rounds.
    - **Data Isolation:** Job seekers can only view and manage their own uploaded resumes and submitted applications.
    - **Confidential Notes:** Recruiter internal notes on applications are strictly restricted to administrators and are never sent to candidate clients.
    - **Advisory Scoring:** All resume and ATS compatibility scores are advisory heuristics designed to assist candidate preparation and ATS formatting compliance.
    """)
