"""
Safety Engine for AyuPulse.
Guarantees compliant wellness language, prevents clinical claims,
and flags red-flag health signals requiring immediate medical escalation.
"""
import re
from typing import Dict, Any

RED_FLAG_KEYWORDS = [
    "chest pain", "heart attack", "difficulty breathing", "severe shortness of breath",
    "stroke", "paralysis", "blood vomiting", "suicidal", "severe depression",
    "unconscious", "seizure", "severe bleeding", "fracture"
]

MEDICAL_CLAIM_REPLACEMENTS = {
    r"\bdiagnos(e|is|ed|ing)\b": "wellness tendency assessment",
    r"\bcure[sd]?\b": "support preventive balance",
    r"\btreat(ment|ed|ing|s)?\b": "daily preventive practice",
    r"\bdisease[s]?\b": "constitutional imbalance",
    r"\billness(es)?\b": "pattern of imbalance",
    r"\byou have\b": "your responses indicate a tendency toward",
    r"\byou are suffering from\b": "your pattern shows an elevation in",
}

DISCLAIMER_NOTE = (
    "This is a traditional wellness-oriented interpretation rooted in AYUSH principles, "
    "not a medical diagnosis or treatment plan. For clinical symptoms or health concerns, "
    "please consult a qualified medical professional."
)


def sanitize_wellness_text(text: str) -> str:
    """Replaces clinical/diagnostic phrases with compliant traditional wellness phrasing."""
    sanitized = text
    for pattern, replacement in MEDICAL_CLAIM_REPLACEMENTS.items():
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
    return sanitized


def evaluate_safety(text: str) -> Dict[str, Any]:
    """
    Checks text for emergency or severe medical red flags.
    Returns status, escalation requirements, and sanitized guidance.
    """
    text_lower = text.lower()
    for flag in RED_FLAG_KEYWORDS:
        if flag in text_lower:
            return {
                "is_safe": False,
                "requires_escalation": True,
                "sanitized_text": sanitize_wellness_text(text),
                "safety_notice": (
                    "URGENT: Your query contains potential red-flag symptoms. AyuPulse is a preventive "
                    "wellness system and cannot handle medical emergencies. Please immediately visit "
                    "the nearest hospital emergency room or contact local emergency services."
                )
            }

    return {
        "is_safe": True,
        "requires_escalation": False,
        "sanitized_text": sanitize_wellness_text(text),
        "safety_notice": DISCLAIMER_NOTE
    }
