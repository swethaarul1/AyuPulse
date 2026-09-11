"""
AYUSH Centres & Consultation Booking Routes for AyuPulse Module 05: Connect.
"""
import os
import json
import uuid
from fastapi import APIRouter
from schemas import CentresResponse, CentreItem, ConsultationRequest, ConsultationResponse

router = APIRouter(prefix="/api", tags=["Module 05 - AYUSH Centres & Consultation"])
CENTRES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "centres.json")


def load_centres():
    if os.path.exists(CENTRES_FILE):
        try:
            with open(CENTRES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


@router.get("/centres", response_model=CentresResponse)
def list_ayush_centres():
    """
    Returns verified national AYUSH institutes and wellness centres for offline/hybrid connection.
    """
    data = load_centres()
    items = [CentreItem(**c) for c in data]
    return CentresResponse(
        status="success",
        total=len(items),
        centres=items
    )


@router.post("/consultation", response_model=ConsultationResponse)
def book_consultation(payload: ConsultationRequest):
    """
    Books an AYUSH wellness consultation with a certified practitioner.
    """
    booking_id = f"ayush-bk-{uuid.uuid4().hex[:6]}"
    return ConsultationResponse(
        status="confirmed",
        module="consultation",
        booking_id=booking_id,
        message=f"Consultation request confirmed for {payload.preferred_date} with {payload.preferred_system} specialist."
    )
