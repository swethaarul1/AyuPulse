"""
AYUSH Access Bridge & Centres Routes for AyuPulse Module 04.
Connects user wellness focus with suitable AYUSH services, matches prototype centres,
and simulates prototype consultation requests.
"""
import os
import json
import uuid
from typing import Optional
from fastapi import APIRouter, Query, HTTPException, status
from schemas import (
    CentresResponse, CentreItem,
    CentreMatchRequest, CentreMatchResponse,
    ConsultationRequest, ConsultationResponse
)
from services.safety import evaluate_safety

router = APIRouter(prefix="/api", tags=["Module 04 - AYUSH Access Bridge"])
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
def list_ayush_centres(
    focus: Optional[str] = Query(None, description="Filter by wellness focus: stress, sleep, movement, digestion"),
    system: Optional[str] = Query(None, description="Filter by AYUSH system: Ayurveda, Yoga, Naturopathy, Unani, Siddha, Homeopathy"),
    location: Optional[str] = Query(None, description="Filter by city or state")
):
    """
    Returns prototype AYUSH centres with optional filters for focus, system, and location.
    Explicitly labeled as prototype demonstration data.
    """
    raw_data = load_centres()
    filtered = []

    for c in raw_data:
        # Filter by AYUSH system
        if system and system.lower() not in c.get("system", "").lower():
            continue

        # Filter by location (city or state)
        if location:
            loc_lower = location.lower()
            if loc_lower not in c.get("city", "").lower() and loc_lower not in c.get("state", "").lower():
                continue

        # Filter by wellness focus keyword
        if focus:
            f_lower = focus.lower()
            services_str = " ".join(c.get("services", [])).lower()
            system_str = c.get("system", "").lower()

            if f_lower in ["stress", "sleep", "relaxation"]:
                if not any(k in services_str or k in system_str for k in ["stress", "yoga", "prakriti", "panchakarma"]):
                    continue
            elif f_lower in ["movement", "mobility", "joints"]:
                if not any(k in services_str or k in system_str for k in ["yoga", "naturopathy", "hydrotherapy", "varma"]):
                    continue
            elif f_lower in ["digestion", "metabolism", "gut"]:
                if not any(k in services_str or k in system_str for k in ["diet", "panchakarma", "ayurveda", "naturopathy"]):
                    continue

        filtered.append(CentreItem(
            id=c["id"],
            name=c["name"],
            system=c["system"],
            city=c["city"],
            state=c["state"],
            pincode=c["pincode"],
            address=c["address"],
            phone=c["phone"],
            services=c["services"],
            rating=c["rating"],
            data_status="Prototype AYUSH centre data"
        ))

    return CentresResponse(
        status="success",
        total=len(filtered),
        data_status="Prototype AYUSH centre data",
        disclaimer="Seeded centre data for demonstration — Not a live nationwide directory.",
        centres=filtered
    )


@router.post("/centres/match", response_model=CentreMatchResponse)
def match_ayush_centre(payload: CentreMatchRequest):
    """
    Matches user wellness focus/goals with appropriate AYUSH service categories
    and suitable prototype wellness institutes.
    """
    focus = (payload.wellness_focus or payload.wellness_goal or "general wellness").lower()
    system_pref = payload.preferred_system.lower() if payload.preferred_system else None

    # Safety check: if input indicates persistent or worsening symptoms, add professional notice
    safety_eval = evaluate_safety(f"{payload.wellness_goal or ''} {payload.wellness_focus or ''}")
    professional_notice = None
    if safety_eval.get("requires_escalation") or safety_eval.get("risk_level") in ["medium", "high"]:
        professional_notice = (
            "Your indicated wellness concern suggests symptoms that may benefit from in-person clinical "
            "evaluation by a qualified medical specialist alongside supportive AYUSH care."
        )

    # Determine recommended AYUSH service category
    if any(w in focus for w in ["stress", "sleep", "burnout", "anxiety", "calm"]):
        recommended_service = "Yoga Therapy & Ayurvedic Stress Care (Shirodhara / Pranayama)"
        target_keywords = ["yoga", "stress", "ayurveda", "prakriti"]
    elif any(w in focus for w in ["movement", "mobility", "joints", "flexibility", "stiffness"]):
        recommended_service = "Yoga Therapy, Naturopathic Hydrotherapy & Siddha Varma Care"
        target_keywords = ["yoga", "naturopathy", "varma", "hydrotherapy"]
    elif any(w in focus for w in ["digestion", "gut", "metabolism", "weight", "acidity"]):
        recommended_service = "Ayurvedic Agni Counseling & Naturopathic Dietary Guidance"
        target_keywords = ["diet", "panchakarma", "ayurveda", "naturopathy"]
    else:
        recommended_service = "Comprehensive AYUSH Dinacharya & Prakriti Pariksha Consultation"
        target_keywords = ["prakriti", "wellness", "ayurveda", "consultation"]

    raw_data = load_centres()
    matched = []

    for c in raw_data:
        # Match system if preferred
        if system_pref and system_pref not in c.get("system", "").lower():
            continue
        # Check service or system keyword matches
        services_str = " ".join(c.get("services", [])).lower()
        if any(k in services_str or k in c.get("system", "").lower() for k in target_keywords):
            matched.append(CentreItem(
                id=c["id"],
                name=c["name"],
                system=c["system"],
                city=c["city"],
                state=c["state"],
                pincode=c["pincode"],
                address=c["address"],
                phone=c["phone"],
                services=c["services"],
                rating=c["rating"],
                data_status="Prototype AYUSH centre data"
            ))

    # Fallback to all if none matched
    if not matched:
        matched = [CentreItem(**c, data_status="Prototype AYUSH centre data") for c in raw_data[:3]]

    return CentreMatchResponse(
        status="matched",
        wellness_focus=payload.wellness_focus or payload.wellness_goal or "General Preventive Wellness",
        recommended_service=recommended_service,
        data_status="Prototype AYUSH centre data",
        matched_centres=matched,
        professional_notice=professional_notice
    )


@router.post("/consultation", response_model=ConsultationResponse, status_code=status.HTTP_200_OK)
def request_consultation_simulation(payload: ConsultationRequest):
    """
    Simulates a consultation booking request with an AYUSH centre.
    Returns simulated prototype confirmation without pretending a live appointment was scheduled.
    """
    # Verify centre exists in database
    raw_data = load_centres()
    centre = next((c for c in raw_data if c["id"] == payload.centre_id), None)
    if not centre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centre with ID '{payload.centre_id}' was not found."
        )

    booking_id = f"ayush-sim-{uuid.uuid4().hex[:6]}"
    return ConsultationResponse(
        status="requested",
        module="consultation",
        booking_id=booking_id,
        centre_id=payload.centre_id,
        message=f"Consultation request recorded for prototype demonstration at {centre['name']}.",
        next_step="In a production deployment, an AYUSH healthcare coordinator would contact you within 24 hours.",
        notice="Prototype demonstration only. Not a live appointment."
    )
