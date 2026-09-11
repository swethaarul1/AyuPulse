"""
Pattern Engine API Routes for AyuPulse Module 03: Pattern Insight & Wellness Pulse.
Analyzes recent check-in patterns against baseline, detects recurring relationships
(e.g., poor sleep + high stress), and recommends actionable next steps.
"""
from fastapi import APIRouter, status
from schemas import PatternRequest, PatternResponse, PatternItem
from services.pattern import analyze_history_patterns

router = APIRouter(prefix="/api/pattern", tags=["Module 03 - Pattern Insight & Wellness Pulse"])


@router.post("", response_model=PatternResponse, status_code=status.HTTP_200_OK)
def analyze_pattern(payload: PatternRequest = PatternRequest()):
    """
    Analyzes check-in history to detect recurring self-reported patterns,
    evaluates Wellness Pulse (0-100), and outputs personalized preventive adjustments.
    """
    result = analyze_history_patterns(payload.checkins)
    return PatternResponse(
        status="success",
        module="pattern",
        patterns=[PatternItem(**p) for p in result["patterns"]],
        next_step=result["next_step"],
        wellness_pulse=result["wellness_pulse"],
        detected_pattern=result["detected_pattern"],
        insight=result["insight"],
        plan_adjusted=result["plan_adjusted"],
        adjustment_tasks=result["adjustment_tasks"],
        data_status=result.get("data_status", "Prototype seeded history")
    )


@router.get("", response_model=PatternResponse)
def get_current_pattern():
    """GET shortcut to retrieve current pattern insight from seeded history."""
    result = analyze_history_patterns()
    return PatternResponse(
        status="success",
        module="pattern",
        patterns=[PatternItem(**p) for p in result["patterns"]],
        next_step=result["next_step"],
        wellness_pulse=result["wellness_pulse"],
        detected_pattern=result["detected_pattern"],
        insight=result["insight"],
        plan_adjusted=result["plan_adjusted"],
        adjustment_tasks=result["adjustment_tasks"],
        data_status=result.get("data_status", "Prototype seeded history")
    )
