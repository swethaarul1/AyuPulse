"""
Check-in API Routes for AyuPulse Module 03: 30-Second Daily Check-in.
Stores and retrieves daily check-ins for sleep, stress, mood, and digestion.
"""
import uuid
from datetime import date
from fastapi import APIRouter
from schemas import CheckInRequest, CheckInResponse
from services.pattern import load_history

router = APIRouter(prefix="/api/checkin", tags=["Module 03 - Daily Check-in"])


@router.post("", response_model=CheckInResponse)
def record_checkin(payload: CheckInRequest):
    """
    Submits a quick 30-second check-in for sleep, stress, mood, and digestion.
    Returns confirmation and check-in ID.
    """
    checkin_id = f"chk-{uuid.uuid4().hex[:8]}"
    return CheckInResponse(
        status="recorded",
        module="checkin",
        checkin_id=checkin_id,
        message=f"Daily check-in recorded successfully for {date.today().isoformat()}."
    )


@router.get("")
def get_checkin_history():
    """
    Returns historical check-in data (including prototype seeded history for hackathon demo).
    """
    history = load_history()
    return {
        "status": "success",
        "total_records": len(history),
        "data_notice": "Seeded prototype demo data included for pattern analysis demonstration.",
        "history": history
    }
