"""
Safety API Routes for AyuPulse Module 04: Guardrails & Clinical Boundary Escalation.
"""
from fastapi import APIRouter
from schemas import SafetyCheckRequest, SafetyCheckResponse
from services.safety import evaluate_safety

router = APIRouter(prefix="/api/safety", tags=["Module 04 - Safety & Escalation"])


@router.post("", response_model=SafetyCheckResponse)
def check_safety(payload: SafetyCheckRequest):
    """
    Validates user query or AI response against medical diagnosis boundaries and emergency red flags.
    Returns whether the input is safe, requires urgent emergency escalation, and sanitized output.
    """
    result = evaluate_safety(payload.text)
    return SafetyCheckResponse(
        status="evaluated",
        module="safety",
        is_safe=result["is_safe"],
        requires_escalation=result["requires_escalation"],
        sanitized_text=result["sanitized_text"],
        safety_notice=result["safety_notice"]
    )
