"""
Safety Engine for AyuPulse (Module 05: Preventive Wellness Safety Gate).
Sits between AI-generated guidance and user-facing output.
Enforces non-clinical boundaries, sanitizes unsafe claims, checks for red flags,
and handles low-confidence situations.
"""
import re
from typing import Dict, Any, Optional

# High-risk emergency red-flags requiring urgent escalation
EMERGENCY_RED_FLAGS = [
    "chest pain", "heart attack", "difficulty breathing", "severe shortness of breath",
    "stroke", "paralysis", "blood vomiting", "suicidal", "severe depression",
    "unconscious", "seizure", "severe bleeding", "fracture", "coughing blood"
]

# Persistent / worsening concern signals requiring professional medical evaluation
PERSISTENT_CONCERN_SIGNALS = [
    "persistent fever", "chronic severe pain", "worsening for weeks",
    "unexplained weight loss", "severe insomnia for months", "chronic fatigue",
    "lump", "persistent bleeding", "black stools", "severe dizziness"
]

# Medication-stopping / dangerous instructions
DANGEROUS_INSTRUCTIONS = [
    r"stop\s+(?:taking\s+)?(?:your\s+)?(?:prescription|medication|medicine|insulin|inhaler|pills|drugs)",
    r"discontinue\s+(?:your\s+)?(?:medication|treatment|drugs|prescription)",
    r"replace\s+(?:your\s+)?(?:medicine|prescription)\s+with",
    r"cure[sd]?\s+(?:cancer|diabetes|hypertension|heart disease)",
    r"guaranteed\s+(?:cure|recovery|outcome|results)",
    r"100%\s+(?:cure|effective|recovery)",
]

# Clinical / diagnostic claim replacements
MEDICAL_CLAIM_REPLACEMENTS = {
    r"\bdiagnos(?:e|is|ed|ing)\b": "wellness tendency assessment",
    r"\bcure[sd]?\b": "support natural vitality",
    r"\btreat(?:ment|ed|ing|s)?\b": "preventive wellness practice",
    r"\bdisease[s]?\b": "constitutional imbalance",
    r"\billness(?:es)?\b": "pattern of imbalance",
    r"\byou have\b": "your responses indicate a tendency toward",
    r"\byou are suffering from\b": "your responses reflect an elevated pattern of",
    r"\bclinical\b": "traditional",
    r"\bmedical therapy\b": "preventive lifestyle practice",
    r"\bguarantee[sd]?\b": "may support",
}

DISCLAIMER_NOTE = (
    "AyuPulse provides traditional preventive wellness guidance rooted in AYUSH principles. "
    "It is not a medical diagnosis or clinical treatment. Always consult a qualified medical professional "
    "for any health conditions or before changing medications."
)

PROFESSIONAL_ATTENTION_NOTICE = (
    "Your responses suggest signals that may benefit from a qualified healthcare professional's attention. "
    "AyuPulse focuses on preventive wellness and is not a substitute for clinical medical care."
)


def sanitize_wellness_text(text: str) -> str:
    """Replaces clinical/diagnostic phrases with safe, compliant preventive-wellness phrasing."""
    if not text:
        return ""
    sanitized = text
    for pattern, replacement in MEDICAL_CLAIM_REPLACEMENTS.items():
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
    return sanitized


def inspect_safety_gate(
    text: str,
    user_input: Optional[str] = None,
    recommendation: Optional[str] = None,
    confidence: Optional[float] = None
) -> Dict[str, Any]:
    """
    Core Safety Gate pipeline:
    Inspects user input, AI recommendation, and confidence level.
    Returns structured action: 'allow', 'modify', 'caution', or 'professional_attention'.
    """
    combined_text = f"{text or ''} {user_input or ''} {recommendation or ''}".lower()
    content_to_inspect = recommendation or text or user_input or ""

    # 1. Check for acute emergency red-flags
    for flag in EMERGENCY_RED_FLAGS:
        if flag in combined_text:
            return {
                "safe": False,
                "risk_level": "high",
                "action": "professional_attention",
                "message": (
                    "URGENT: Your responses contain potential red-flag symptoms. AyuPulse is a preventive "
                    "wellness platform and cannot handle medical emergencies. Please immediately visit "
                    "the nearest hospital emergency room or contact local emergency medical services."
                ),
                "modified_content": sanitize_wellness_text(content_to_inspect),
                "professional_attention": True
            }

    # 2. Check for dangerous medical instructions (stopping medication, guaranteed cures)
    has_dangerous_instruction = False
    for danger_pat in DANGEROUS_INSTRUCTIONS:
        if re.search(danger_pat, combined_text, flags=re.IGNORECASE):
            has_dangerous_instruction = True
            break

    if has_dangerous_instruction:
        cleaned = sanitize_wellness_text(content_to_inspect)
        # Neutralize any mention of stopping meds
        cleaned = re.sub(r"stop\s+[a-z\s]+medication", "continue your prescribed care and discuss lifestyle habits with your physician", cleaned, flags=re.IGNORECASE)
        return {
            "safe": False,
            "risk_level": "high",
            "action": "modify",
            "message": "Dangerous medical claim or medication instruction was detected and removed. Always consult your doctor before adjusting prescription medication.",
            "modified_content": cleaned,
            "professional_attention": True
        }

    # 3. Check for persistent/worsening concern signals
    for signal in PERSISTENT_CONCERN_SIGNALS:
        if signal in combined_text:
            return {
                "safe": True,
                "risk_level": "medium",
                "action": "caution",
                "message": PROFESSIONAL_ATTENTION_NOTICE,
                "modified_content": sanitize_wellness_text(content_to_inspect),
                "professional_attention": True
            }

    # 4. Check for low AI confidence
    if confidence is not None and confidence < 0.55:
        return {
            "safe": True,
            "risk_level": "low",
            "action": "caution",
            "message": (
                "Assessment confidence is moderate due to balanced responses. We recommend focusing on "
                "general daily grounding practices and consulting an AYUSH practitioner for customized Pariksha."
            ),
            "modified_content": sanitize_wellness_text(content_to_inspect),
            "professional_attention": False
        }

    # 5. Check if clinical phrasing needs modification
    needs_modification = False
    for pattern in MEDICAL_CLAIM_REPLACEMENTS.keys():
        if re.search(pattern, content_to_inspect, flags=re.IGNORECASE):
            needs_modification = True
            break

    if needs_modification:
        modified = sanitize_wellness_text(content_to_inspect)
        return {
            "safe": True,
            "risk_level": "low",
            "action": "modify",
            "message": "Content was modified to align with preventive wellness and AYUSH non-clinical standards.",
            "modified_content": modified,
            "professional_attention": False
        }

    # 6. Completely safe preventive wellness content
    return {
        "safe": True,
        "risk_level": "low",
        "action": "allow",
        "message": "Safety check passed. Content complies with preventive wellness standards.",
        "modified_content": content_to_inspect,
        "professional_attention": False
    }


def evaluate_safety(text: str) -> Dict[str, Any]:
    """Backwards-compatible helper calling the safety gate."""
    return inspect_safety_gate(text)
