"""
Safety Layer — AyuPulse
All outputs from the AI/business logic pass through this layer.
Never diagnose. Never claim medical certainty.
"""

FORBIDDEN_TERMS = [
    "diagnose", "diagnosis", "disease", "treatment", "cure", "cures",
    "medical condition", "disorder", "illness", "you have",
    "you are suffering", "risk factor", "cancer", "diabetes", "predict"
]

WELLNESS_DISCLAIMER = (
    "Traditional wellness tendency — not a medical diagnosis. "
    "For persistent or worsening concerns, please consult a qualified healthcare professional."
)

PLAN_DISCLAIMER = (
    "These are traditional wellness practices for general preventive wellbeing. "
    "They are not a substitute for medical advice. If you have any health condition, "
    "please consult a qualified practitioner before starting new practices."
)


def sanitize_text(text: str) -> str:
    """Remove or replace forbidden clinical language from generated text."""
    result = text
    replacements = {
        "diagnose": "assess tendency",
        "diagnosis": "wellness tendency",
        "disease": "imbalance",
        "treatment": "practice",
        "cure": "support",
        "disorder": "pattern",
        "illness": "imbalance",
    }
    for term, replacement in replacements.items():
        result = result.replace(term, replacement)
        result = result.replace(term.capitalize(), replacement.capitalize())
    return result


def validate_insight(text: str) -> str:
    """Ensure insight text is safe and sanitized."""
    return sanitize_text(text)


def validate_plan_task(task: dict) -> dict:
    """Ensure every plan task has a non-empty safety note."""
    if not task.get("safety"):
        task["safety"] = "If you experience discomfort, pause and rest. Consult a practitioner if needed."
    task["safety"] = sanitize_text(task["safety"])
    task["what"] = sanitize_text(task.get("what", ""))
    task["why"] = sanitize_text(task.get("why", ""))
    task["how"] = sanitize_text(task.get("how", ""))
    return task
