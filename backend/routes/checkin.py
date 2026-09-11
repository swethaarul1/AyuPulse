"""
Check-in API Routes for AyuPulse Module 03: Daily Check-in & Wellness Score.
Computes deterministic 0-100 Wellness Score from Sleep, Stress, Mood, Digestion, and Energy.
"""
import uuid
from datetime import date
from fastapi import APIRouter, status
from schemas import CheckInRequest, CheckInResponse
from services.pattern import calculate_checkin_wellness_score, load_history

router = APIRouter(prefix="/api/checkin", tags=["Module 03 - Daily Check-in"])


@router.post("", response_model=CheckInResponse, status_code=status.HTTP_200_OK)
def record_daily_checkin(payload: CheckInRequest):
    """
    Submits a daily 30-second check-in across 5 core wellness dimensions:
    Sleep (1-5), Stress (1-5), Mood (1-5), Digestion (1-5), and Energy (1-5).
    Calculates a deterministic 0-100 Wellness Score and returns immediate feedback.
    """
    checkin_id = f"chk-{uuid.uuid4().hex[:8]}"
    today_str = payload.date or date.today().isoformat()

    calc = calculate_checkin_wellness_score(
        sleep=payload.sleep_score,
        stress=payload.stress_score,
        mood=payload.mood_score,
        digestion=payload.digestion_score,
        energy=payload.energy_score
    )

    checkin_dict = {
        "user_id": payload.user_id,
        "date": today_str,
        "sleep": payload.sleep_score,
        "stress": payload.stress_score,
        "mood": payload.mood_score,
        "digestion": payload.digestion_score,
        "energy": payload.energy_score,
        "notes": payload.notes
    }

    return CheckInResponse(
        status="recorded",
        module="checkin",
        checkin_id=checkin_id,
        wellness_score=calc["wellness_score"],
        summary=calc["summary"],
        checkin=checkin_dict,
        message=f"Daily wellness check-in recorded successfully for {today_str}."
    )


@router.get("")
def get_checkin_history():
    """
    Returns historical check-in data.
    Clearly labeled with prototype seeded status for demonstration.
    """
    history = load_history()
    return {
        "status": "success",
        "total_records": len(history),
        "data_status": "Prototype seeded history",
        "disclaimer": "Seeded check-in data for prototype demonstration — Not live national health data.",
        "history": history
    }
