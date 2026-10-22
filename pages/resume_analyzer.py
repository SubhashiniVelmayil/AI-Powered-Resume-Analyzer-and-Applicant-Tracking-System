"""
Resume Analyzer Page for Streamlit application.
Supports PDF uploading, parsed text preview, transparent 100-pt rubric scoring,
ATS formatting audit, AI bullet point improvement, and report downloads.
"""

import streamlit as st
import json
from database import get_connection
from services.pdf_parser import extract_text_from_pdf
from services.resume_analyzer import analyze_resume_text
from services.ai_service import enhance_resume_content
from services.report_generator import generate_resume_analysis_report_markdown
from styles import CUSTOM_CSS

def render_resume_analyzer(user: dict):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #38bdf8; margin-bottom: 4px;">AI Resume Analyzer & Diagnostic Engine</h1>
        <p style="color: #94a3b8;">Upload your resume to audit sections, calculate transparent rubric scores, and optimize for ATS scanners.</p>
    </div>
    """, unsafe_allow_html=True)

    # Privacy / AI Notice
    st.info(
        "🔒 Privacy & Processing Notice: Resumes are processed strictly for scoring and tracking within your account. "
        "By default, analysis uses our local heuristic rule-based engine. If GROQ_API_KEY is configured in your .env, "
        "sanitized text can optionally be processed via Groq Cloud LLM."
    )

    tab1, tab2 = st.tabs(["Upload & Analyze New Resume", "My Previous Resume Analyses"])

    with tab1:
        uploaded_file = st.file_uploader("Upload Resume in PDF Format (Max 5MB)", type=["pdf"], key="resume_uploader")

        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            filename = uploaded_file.name

            # Run extraction
            with st.spinner("Extracting and validating PDF contents..."):
                extraction_result = extract_text_from_pdf(file_bytes, filename)

            if not extraction_result["success"]:
                st.error(f"❌ Upload Failed: {extraction_result.get('error')}")
            else:
                raw_text = extraction_result["raw_text"]
                is_scanned = extraction_result.get("is_scanned", False)

                if is_scanned:
                    st.warning(extraction_result.get("warning"))
                    st.markdown("""
                    <div class="alert-box">
                        <strong>Why did this happen?</strong><br>
                        Your PDF contains embedded images without selectable text streams. Standard ATS systems require machine-readable text.
                        You can paste your resume text manually below or connect an OCR extension.
                    </div>
                    """, unsafe_allow_html=True)
                    raw_text = st.text_area("Or paste your resume text manually for instant analysis:", height=200)

                if raw_text and st.button("🚀 Analyze Resume Now", key="btn_run_analysis"):
                    with st.spinner("Executing rubric evaluation and ATS formatting audit..."):
                        analysis = analyze_resume_text(raw_text)

                        # Save to database
                        with get_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO resumes (user_id, filename, file_size_bytes, raw_text, is_scanned_notice)
                                VALUES (?, ?, ?, ?, ?);
                            """, (user["id"], filename, len(file_bytes), raw_text, 1 if is_scanned else 0))
                            resume_id = cursor.lastrowid

                            cursor.execute("""
                                INSERT INTO resume_analyses (
                                    resume_id, user_id, overall_score, rubric_breakdown_json,
                                    extracted_info_json, strengths_json, weaknesses_json,
                                    suggestions_json, ats_checks_json, ai_provider
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                            """, (
                                resume_id, user["id"], analysis["overall_score"],
                                json.dumps(analysis["rubric_breakdown"]),
                                json.dumps(analysis["candidate_info"]),
                                json.dumps(analysis["strengths"]),
                                json.dumps(analysis["weaknesses"]),
                                json.dumps(analysis["suggestions"]),
                                json.dumps(analysis["ats_checks"]),
                                "local_rubric_engine"
                            ))
                            conn.commit()

                    st.success("✅ Analysis Complete! Results saved to your profile.")

                    # Display Score & Rubric
                    score = analysis["overall_score"]
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <h2 style="color: #94a3b8; margin-bottom: 8px;">Advisory Resume Score</h2>
                        <div class="score-badge">{score}</div>
                        <p style="color: #cbd5e1; margin-top: 14px; max-width: 600px; margin-left: auto; margin-right: auto;">
                            {analysis['disclaimer']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Rubric breakdown cards
                    st.subheader("📊 Transparent Rubric Breakdown")
                    rb = analysis["rubric_breakdown"]
                    exp = analysis["explanations"]

                    r1, r2, r3 = st.columns(3)
                    with r1:
                        st.markdown(f"**Content Quality**: {rb['content_quality']} / 25 pts")
                        st.caption(exp["content_quality"])
                        st.markdown(f"**Skills Relevance**: {rb['skills_relevance']} / 20 pts")
                        st.caption(exp["skills_relevance"])
                    with r2:
                        st.markdown(f"**Projects & Experience**: {rb['projects_experience']} / 20 pts")
                        st.caption(exp["projects_experience"])
                        st.markdown(f"**Education & Certifications**: {rb['education_certifications']} / 10 pts")
                        st.caption(exp["education_certifications"])
                    with r3:
                        st.markdown(f"**Measurable Impact**: {rb['achievements_impact']} / 15 pts")
                        st.caption(exp["achievements_impact"])
                        st.markdown(f"**Readability & Tone**: {rb['readability_structure']} / 10 pts")
                        st.caption(exp["readability_structure"])

                    # Strengths and Weaknesses
                    st.markdown("<hr style='border-color: rgba(139,92,246,0.2);'>", unsafe_allow_html=True)
                    s_col, w_col = st.columns(2)

                    with s_col:
                        st.subheader("🌟 Core Strengths")
                        for s in analysis["strengths"]:
                            st.markdown(f"""
                            <div style="background: rgba(16,185,129,0.1); border-left: 3px solid #10b981; padding: 10px 14px; border-radius: 6px; margin-bottom: 10px;">
                                <strong style="color: #6ee7b7;">{s['title']}</strong><br>
                                <span style="font-size: 0.9rem; color: #e2e8f0;">{s['detail']}</span>
                            </div>
                            """, unsafe_allow_html=True)

                    with w_col:
                        st.subheader("⚠️ Areas for Improvement")
                        for w in analysis["weaknesses"]:
                            st.markdown(f"""
                            <div style="background: rgba(239,68,68,0.1); border-left: 3px solid #ef4444; padding: 10px 14px; border-radius: 6px; margin-bottom: 10px;">
                                <strong style="color: #fca5a5;">{w['title']}</strong><br>
                                <span style="font-size: 0.9rem; color: #e2e8f0;">{w['detail']}</span>
                            </div>
                            """, unsafe_allow_html=True)

                    # ATS Formatting Audit
                    st.subheader("📋 ATS Formatting & Parsing Checklist")
                    for chk in analysis["ats_checks"]:
                        icon = "✅" if chk["passed"] else "⚠️"
                        with st.expander(f"{icon} {chk['check']} - {'PASSED' if chk['passed'] else 'FLAGGED'}"):
                            if chk["issue"]:
                                st.write(f"**Issue Detected**: {chk['issue']}")
                            st.write(f"**Recommendation**: {chk['recommendation']}")

                    # Actionable Improvement Suggestions
                    st.subheader("💡 High-Impact Phrasing & Suggestions")
                    for sug in analysis["suggestions"]:
                        with st.expander(f"📌 {sug['category']}: {sug['action']}"):
                            st.markdown(f"**Original (Weak)**: `{sug['before']}`")
                            st.markdown(f"**Enhanced (Stronger)**: `{sug['after']}`")

                    # AI Bullet Point Rewriter Tool
                    st.markdown("<hr style='border-color: rgba(139,92,246,0.2);'>", unsafe_allow_html=True)
                    st.subheader("✨ AI-Powered Bullet Point Rewriter")
                    st.caption("Paste a weak resume bullet point to rewrite using the Google XYZ formula with verified metric placeholders.")
                    user_bullet = st.text_input("Enter a resume bullet point:", "Worked on database performance and backend endpoints.")
                    if st.button("Rewrite Bullet Point", key="btn_rewrite_single"):
                        rewritten_res = enhance_resume_content([user_bullet])
                        st.markdown(f"*Engine*: `{rewritten_res.get('provider')}`")
                        for item in rewritten_res.get("rewrites", []):
                            st.markdown(f"""
                            <div class="glass-card">
                                <div style="color: #94a3b8; font-size: 0.85rem;">ORIGINAL</div>
                                <div style="color: #f87171; text-decoration: line-through; margin-bottom: 8px;">{item['original']}</div>
                                <div style="color: #38bdf8; font-size: 0.85rem; font-weight: bold;">REWRITTEN (XYZ FORMULA)</div>
                                <div style="color: #4ade80; font-size: 1.05rem;">{item['improved']}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    # Download Markdown Report
                    cand_name = analysis["candidate_info"].get("candidate_name") or "Candidate"
                    report_md = generate_resume_analysis_report_markdown(analysis, cand_name)
                    st.download_button(
                        label="📥 Download Resume Diagnostic Report (.md)",
                        data=report_md,
                        file_name=f"{cand_name.replace(' ', '_')}_Resume_Diagnostic_Report.md",
                        mime="text/markdown"
                    )

    with tab2:
        st.subheader("Previous Resume Analyses")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.id as resume_id, r.filename, r.created_at, a.overall_score, a.rubric_breakdown_json
                FROM resumes r
                LEFT JOIN resume_analyses a ON r.id = a.resume_id
                WHERE r.user_id = ?
                ORDER BY r.id DESC;
            """, (user["id"],))
            past_resumes = cursor.fetchall()

        if not past_resumes:
            st.info("You haven't uploaded any resumes yet.")
        else:
            for r in past_resumes:
                col_info, col_del = st.columns([4, 1])
                with col_info:
                    st.markdown(f"""
                    **{r['filename']}** | Score: `{r['overall_score'] or 'N/A'} / 100` | Uploaded: *{r['created_at']}*
                    """)
                with col_del:
                    if st.button("Delete", key=f"del_res_{r['resume_id']}"):
                        with get_connection() as conn:
                            conn.execute("DELETE FROM resumes WHERE id = ? AND user_id = ?;", (r["resume_id"], user["id"]))
                            conn.commit()
                        st.success("Resume deleted.")
                        st.rerun()
                st.markdown("<hr style='margin: 8px 0; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
