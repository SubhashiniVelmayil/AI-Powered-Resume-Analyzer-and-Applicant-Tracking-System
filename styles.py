"""
Custom CSS styling and design system for Streamlit interface.
Implements dark navy and purple gradient background with cyan accents,
glassmorphism cards, modern metric cards, and responsive layouts.
"""

CUSTOM_CSS = """
<style>
/* Main Background and Typography */
.stApp {
    background: radial-gradient(circle at 10% 20%, #0d1117 0%, #161b22 40%, #1a103c 100%) !important;
    color: #e2e8f0 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Glassmorphism Card Container */
.glass-card {
    background: rgba(22, 27, 34, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(6, 182, 212, 0.5);
    box-shadow: 0 12px 40px 0 rgba(6, 182, 212, 0.15);
}

/* Metric KPI Card */
.metric-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(49, 46, 129, 0.5));
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 14px;
    padding: 18px 22px;
    text-align: left;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

.metric-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #38bdf8;
    line-height: 1.1;
}

.metric-sub {
    font-size: 0.8rem;
    color: #cbd5e1;
    margin-top: 6px;
}

/* Circular-style Score Badge */
.score-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.9) 100%);
    border: 4px solid #06b6d4;
    box-shadow: 0 0 24px rgba(6, 182, 212, 0.4);
    font-size: 2.2rem;
    font-weight: 800;
    color: #f8fafc;
}

/* Status Badges */
.badge-applied { background-color: #1e3a8a; color: #93c5fd; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; }
.badge-review { background-color: #78350f; color: #fde68a; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; }
.badge-shortlisted { background-color: #581c87; color: #e9d5ff; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; }
.badge-interview { background-color: #164e63; color: #a5f3fc; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; }
.badge-selected { background-color: #064e3b; color: #a7f3d0; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; }
.badge-rejected { background-color: #881337; color: #fecdd3; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; }

/* Custom Buttons */
.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(6, 182, 212, 0.35) !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0b0f19 !important;
    border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
}

/* Callout & Notice Alert Boxes */
.alert-box {
    background: rgba(15, 23, 42, 0.6);
    border-left: 4px solid #06b6d4;
    border-radius: 8px;
    padding: 12px 18px;
    margin: 12px 0;
    font-size: 0.9rem;
    color: #e2e8f0;
}
</style>
"""

def render_metric_card(title: str, value: str, subtitle: str = "") -> str:
    """Renders HTML for a glassmorphism KPI metric box."""
    return f"""
    <div class="metric-box">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{subtitle}</div>
    </div>
    """
