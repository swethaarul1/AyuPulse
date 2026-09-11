"""
Safety API Routes for AyuPulse Module 05: Preventive Wellness Safety Gate.
Guarantees AI-generated output adheres to AYUSH wellness standards, modifies unsafe claims,
and flags red-flag health emergencies.
"""
from fastapi import APIRouter, status
from schemas import SafetyCheckRequest, SafetyCheckResponse
from services.safety import inspect_safety_gate

router = APIRouter(prefix="/api/safety", tags=["Module 05 - Preventive Wellness Safety Gate"])


@router.post("", response_model=SafetyCheckResponse, status_code=status.HTTP_200_OK)
def run_safety_gate(payload: SafetyCheckRequest):
    """
    Evaluates input or AI-generated recommendation through the Safety Gate.
    Returns:
    - safe: boolean
    - risk_level: 'low', 'medium', 'high'
    - action: 'allow', 'modify', 'caution', 'professional_attention'
    - message: user-facing explanation
    - modified_content: safe, sanitized wellness content
    - professional_attention: whether medical attention is advised
    """
    result = inspect_safety_gate(
        text=payload.text or "",
        user_input=payload.user_input,
        recommendation=payload.recommendation,
        confidence=payload.confidence
    )
    return SafetyCheckResponse(
        safe=result["safe"],
        risk_level=result["risk_level"],
        action=result["action"],
        message=result["message"],
        modified_content=result["modified_content"],
        professional_attention=result["professional_attention"]
    )
