"""
Pattern Engine API Routes for AyuPulse Module 03: Pattern Insight & Wellness Score.
Analyzes recent check-ins against historical baseline, computes Wellness Score,
and outputs pattern insights with plan adjustments.
"""
from fastapi import APIRouter
from schemas import PatternRequest, PatternResponse
from services.pattern import analyze_history_patterns

router = APIRouter(prefix="/api/pattern", tags=["Module 03 - Pattern Insight & Wellness Pulse"])


@router.post("", response_model=PatternResponse)
def analyze_pattern(payload: PatternRequest = PatternRequest()):
    """
    Analyzes historical check-ins to compute Wellness Pulse (0-100),
    detect recurring patterns (e.g. sleep + stress), and trigger plan adjustments.
    """
    result = analyze_history_patterns()
    return PatternResponse(
        status="success",
        module="pattern",
        wellness_pulse=result["wellness_pulse"],
        detected_pattern=result["detected_pattern"],
        insight=result["insight"],
        plan_adjusted=result["plan_adjusted"],
        adjustment_tasks=result["adjustment_tasks"]
    )


@router.get("", response_model=PatternResponse)
def get_current_pattern():
    """GET shortcut to view current pattern insight and wellness score."""
    result = analyze_history_patterns()
    return PatternResponse(
        status="success",
        module="pattern",
        wellness_pulse=result["wellness_pulse"],
        detected_pattern=result["detected_pattern"],
        insight=result["insight"],
        plan_adjusted=result["plan_adjusted"],
        adjustment_tasks=result["adjustment_tasks"]
    )
