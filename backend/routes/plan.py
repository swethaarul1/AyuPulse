"""
Plan API Routes for AyuPulse Module 02: AI Personalized Preventive Plan & Daily Tracker.
Generates tailored Dinacharya, Yoga, Pranayama, and Diet/Lifestyle recommendations
and an actionable daily tracker based on user dosha, goals, and lifestyle.
"""
from fastapi import APIRouter, HTTPException, status
from schemas import PlanRequest, PlanResponse
from services.claude_service import claude_service
import logging

router = APIRouter(prefix="/api/plan", tags=["Module 02 - Preventive Plan"])
logger = logging.getLogger("ayupulse.routes.plan")


@router.post("", response_model=PlanResponse, status_code=status.HTTP_200_OK)
def generate_preventive_plan(payload: PlanRequest):
    """
    Generates a personalized preventive daily plan and daily tracker.
    Considers dominant dosha, vata/pitta/kapha percentages, lifestyle, and goals.
    Produces 4 sections (Dinacharya, Yoga, Pranayama, Diet/Lifestyle)
    with What, Why, How, Safety and 4-6 actionable daily tracker tasks.
    """
    try:
        plan_data = claude_service.generate_personalized_plan(
            dominant=payload.dominant,
            vata=payload.vata,
            pitta=payload.pitta,
            kapha=payload.kapha,
            lifestyle=payload.lifestyle,
            wellness_goals=payload.wellness_goals,
            preferences=payload.preferences
        )
        return PlanResponse(**plan_data)
    except Exception as e:
        logger.error(f"Failed to generate preventive plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while personalizing your preventive plan."
        )
