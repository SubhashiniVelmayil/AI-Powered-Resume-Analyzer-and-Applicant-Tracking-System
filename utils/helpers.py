"""
Helper functions for formatting, scores, badges, and safe serialization.
"""

import json
from typing import Any, Dict

def get_score_color(score: int) -> str:
    """Returns CSS hex color code corresponding to a numerical score."""
    if score >= 80:
        return "#10B981"  # Emerald / Green
    elif score >= 65:
        return "#06B6D4"  # Cyan / Blue
    elif score >= 50:
        return "#F59E0B"  # Amber / Yellow
    return "#EF4444"      # Rose / Red

def get_status_badge_color(status: str) -> str:
    """Returns status badge styling color."""
    mapping = {
        "Applied": "#60A5FA",       # Blue
        "Under Review": "#F59E0B",  # Amber
        "Shortlisted": "#A855F7",   # Purple
        "Interview": "#06B6D4",     # Cyan
        "Selected": "#10B981",      # Emerald
        "Rejected": "#F43F5E"       # Rose
    }
    return mapping.get(status, "#94A3B8")

def safe_json_loads(val: Any, default: Any = None) -> Any:
    """Safely parses JSON string or returns default value on failure."""
    if val is None:
        return default if default is not None else {}
    if isinstance(val, (dict, list)):
        return val
    try:
        return json.loads(val)
    except Exception:
        return default if default is not None else {}
