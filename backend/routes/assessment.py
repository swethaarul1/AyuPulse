"""
Assessment API Routes for AyuPulse Module 01: AI Prakriti Assessment.
Receives user answers, computes deterministic Vata/Pitta/Kapha scores,
interprets via Claude (with fallback), and returns standardized JSON.
"""
from fastapi import APIRouter, HTTPException, status
from schemas import AssessmentRequest, AssessmentResponse
from services.scoring import calculate_dosha_scores
from services.claude_service import claude_service
import logging

router = APIRouter(prefix="/api/assessment", tags=["Module 01 - Prakriti Assessment"])
logger = logging.getLogger("ayupulse.routes.assessment")


@router.get("/questions")
def get_assessment_questions():
    """
    Returns structured questions for the frontend questionnaire.
    Covers Sleep, Digestion, Stress Response, Energy, Body Tendencies, and Lifestyle.
    """
    return {
        "status": "success",
        "questions": [
            {
                "id": "sleep",
                "category": "Sleep",
                "question": "How would you describe your typical sleep quality and pattern?",
                "options": [
                    {"value": "light_restless", "label": "Light, easily awakened, prone to racing thoughts or insomnia"},
                    {"value": "moderate_sound", "label": "Moderate, sound sleep, but wake up easily if overheated"},
                    {"value": "deep_heavy", "label": "Deep, heavy, long sleep; difficult to wake up in the morning"}
                ]
            },
            {
                "id": "digestion",
                "category": "Digestion",
                "question": "What is your digestion and appetite usually like?",
                "options": [
                    {"value": "irregular_variable", "label": "Variable or irregular appetite; frequent gas or bloating"},
                    {"value": "sharp_fast", "label": "Strong, intense hunger; irritable if meals are delayed; occasional acidity"},
                    {"value": "slow_steady", "label": "Steady but slow digestion; feeling heavy or sluggish after eating"}
                ]
            },
            {
                "id": "stress_response",
                "category": "Stress Response",
                "question": "Under pressure or stress, how do your mind and body usually react?",
                "options": [
                    {"value": "anxious_worry", "label": "Anxiety, worry, overthinking, feeling scattered or restless"},
                    {"value": "irritable_intense", "label": "Irritability, impatience, frustration, critical intensity"},
                    {"value": "withdrawn_slow", "label": "Withdrawal, resistance to change, procrastination, low energy"}
                ]
            },
            {
                "id": "energy",
                "category": "Energy Patterns",
                "question": "How do your energy levels fluctuate throughout the day?",
                "options": [
                    {"value": "variable_bursts", "label": "Bursts of spontaneous creativity followed by sudden fatigue"},
                    {"value": "high_sustained", "label": "Focused, sustained drive; tendency to push until burned out"},
                    {"value": "steady_calm", "label": "Steady, enduring stamina; slow to start but consistent all day"}
                ]
            },
            {
                "id": "body_tendencies",
                "category": "Body Tendencies",
                "question": "Which physical traits resonate most with your natural constitution?",
                "options": [
                    {"value": "dry_cold_slender", "label": "Slender build, dry skin or hair, sensitive to cold weather"},
                    {"value": "warm_medium_athletic", "label": "Medium athletic frame, warm body temperature, sensitive skin"},
                    {"value": "cool_solid_heavy", "label": "Solid/broad build, smooth well-hydrated skin, gain weight easily"}
                ]
            },
            {
                "id": "lifestyle",
                "category": "Lifestyle Habits",
                "question": "What does your typical daily routine look like?",
                "options": [
                    {"value": "irregular_active", "label": "Variable daily schedule, irregular meal times, frequent travel/multitasking"},
                    {"value": "competitive_demanding", "label": "Structured, goal-oriented, demanding schedule, high physical or mental activity"},
                    {"value": "routine_sedentary", "label": "Predictable routine, relaxed pace, preference for comfort and familiar settings"}
                ]
            }
        ]
    }


@router.post("", response_model=AssessmentResponse, status_code=status.HTTP_200_OK)
def submit_assessment(payload: AssessmentRequest):
    """
    Submits user questionnaire responses.
    1. Validates input schema.
    2. Runs deterministic scoring engine (Vata/Pitta/Kapha percentages summing to 100).
    3. Calls Claude for cautious, supportive traditional wellness interpretation.
    4. Combines scores + interpretation and returns structured JSON.
    """
    try:
        # Step 1: Deterministic scoring
        scores = calculate_dosha_scores(payload)
        vata = scores["vata"]
        pitta = scores["pitta"]
        kapha = scores["kapha"]
        dominant = scores["dominant"]

        # Context dict for Claude
        context = {
            "sleep": payload.sleep,
            "digestion": payload.digestion,
            "stress_response": payload.stress_response,
            "energy": payload.energy,
            "body_tendencies": payload.body_tendencies,
            "lifestyle": payload.lifestyle,
            "wellness_goals": ", ".join(payload.wellness_goals) if payload.wellness_goals else None
        }

        # Step 2: Claude interpretation (with automatic graceful fallback)
        interpretation = claude_service.interpret_prakriti(
            vata=vata,
            pitta=pitta,
            kapha=kapha,
            dominant=dominant,
            context=context
        )

        # Step 3: Combine scores + AI interpretation
        return AssessmentResponse(
            vata=vata,
            pitta=pitta,
            kapha=kapha,
            dominant=dominant,
            summary=interpretation.get("summary", ""),
            wellness_focus=interpretation.get("wellness_focus", []),
            note=interpretation.get("note", "This is a traditional wellness-oriented interpretation, not a medical diagnosis.")
        )

    except Exception as e:
        logger.error(f"Error processing assessment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the wellness assessment."
        )
