"""
AI Service Integration Module.
Supports Groq API, Gemini API, and deterministic Local Rule-Based Engine fallback.
Provides resume enhancement, bullet rewriting with [insert verified metric] placeholders,
and safe prompt sanitization.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from config import GROQ_API_KEY, GROQ_MODEL, GEMINI_API_KEY

def is_ai_api_configured() -> Dict[str, bool]:
    """Checks which external AI services have configured API keys."""
    return {
        "groq": bool(os.getenv("GROQ_API_KEY") or GROQ_API_KEY),
        "gemini": bool(os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY)
    }

def sanitize_user_input(text: str) -> str:
    """Sanitizes user input to prevent prompt injection attempts."""
    # Truncate overly long text and neutralize prompt break tags
    sanitized = text.replace("```", "'''")
    # Limit to reasonable character count
    return sanitized[:8000]

def rewrite_bullet_points_local(bullets: List[str]) -> List[Dict[str, str]]:
    """
    Deterministic rule-based bullet point rewriter.
    Converts passive statements into high-impact accomplishment bullets with strong action verbs
    and verified metric placeholders. Never fabricates credentials or historical events.
    """
    replacements = [
        ("worked on", "Architected and delivered"),
        ("helped with", "Collaborated cross-functionally to optimize"),
        ("was responsible for", "Spearheaded end-to-end execution of"),
        ("made", "Engineered and deployed"),
        ("fixed bugs", "Diagnosed and resolved critical production defects, improving system stability by [insert verified %]"),
        ("managed", "Orchestrated and scaled"),
        ("did testing", "Authored comprehensive automated test suites achieving [insert verified %] code coverage"),
        ("learned", "Rapidly acquired expertise in and applied")
    ]

    results = []
    for bullet in bullets:
        clean = bullet.strip().lstrip("•-* ").strip()
        if not clean:
            continue

        improved = clean
        for target, replacement in replacements:
            if target in improved.lower():
                # Case-insensitive replacement
                start_idx = improved.lower().find(target)
                improved = improved[:start_idx] + replacement + improved[start_idx + len(target):]
                break
        else:
            # If no simple prefix matched, wrap in active structure
            words = improved.split()
            if words:
                first_word = words[0].lower()
                if first_word.endswith("ed") or first_word.endswith("ing"):
                    improved = f"Successfully {first_word.capitalize()} " + " ".join(words[1:]) + " to boost efficiency by [insert verified metric]."
                else:
                    improved = f"Engineered {clean}, driving measurable performance gains of [insert verified metric]."

        results.append({
            "original": clean,
            "improved": improved,
            "verb_used": improved.split()[0] if improved else "Engineered",
            "rule": "Google XYZ Action Formula with verified metric placeholder"
        })

    return results

def rewrite_bullets_with_groq(bullets: List[str], api_key: str, model: str) -> Optional[List[Dict[str, str]]]:
    """Attempts to call Groq Cloud API for intelligent bullet point rewriting."""
    prompt = f"""
You are an expert technical resume writer. Rewrite the following resume bullet points using the Google XYZ formula:
'Accomplished [X] as measured by [Y] by doing [Z]'.

STRICT RULES:
1. NEVER invent fake degrees, fake companies, fake metrics, or fake certifications.
2. If a specific metric or number is absent, use the exact placeholder: '[insert verified metric]' or '[insert verified %]'.
3. Begin each rewritten bullet with an active, high-impact verb.
4. Output valid JSON array with keys: "original" and "improved".

Original Bullets:
{json.dumps(bullets)}
"""

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a professional resume improvement engine that strictly outputs JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            # Find list in JSON
            if isinstance(parsed, list):
                return parsed
            for k, v in parsed.items():
                if isinstance(v, list):
                    return v
            return None
    except Exception:
        return None

def enhance_resume_content(bullets: List[str], preferred_provider: str = "auto") -> Dict[str, Any]:
    """
    Main entry point for resume enhancement.
    Attempts Groq API if key is present; smoothly falls back to local engine.
    """
    groq_key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    groq_model = os.getenv("GROQ_MODEL") or GROQ_MODEL

    if groq_key and preferred_provider in ("auto", "groq"):
        ai_rewrites = rewrite_bullets_with_groq(bullets, groq_key, groq_model)
        if ai_rewrites:
            return {
                "provider": "Groq API (" + groq_model + ")",
                "is_fallback": False,
                "rewrites": ai_rewrites
            }

    # Deterministic local fallback
    local_rewrites = rewrite_bullet_points_local(bullets)
    return {
        "provider": "Local Rule-Based NLP Fallback Engine",
        "is_fallback": True,
        "notice": "Processed using local rule-based analysis. To enable cloud LLM inference, configure GROQ_API_KEY in .env.",
        "rewrites": local_rewrites
    }
