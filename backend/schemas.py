"""
AyuPulse Pydantic Schemas
Defines request and response contracts for all API endpoints.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 01 — AI PRAKRITI ASSESSMENT SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class AssessmentRequest(BaseModel):
    """
    Questionnaire answers submitted by the user.
    Accepts specific wellness domain values or a flexible answers dict.
    """
    sleep: Optional[str] = Field(
        None,
        description="Sleep tendency: 'light_restless', 'moderate_sound', 'deep_heavy', or general description"
    )
    digestion: Optional[str] = Field(
        None,
        description="Digestion tendency: 'irregular_variable', 'sharp_fast', 'slow_steady'"
    )
    stress_response: Optional[str] = Field(
        None,
        description="Stress response: 'anxious_worry', 'irritable_intense', 'withdrawn_slow'"
    )
    energy: Optional[str] = Field(
        None,
        description="Energy pattern: 'variable_bursts', 'high_sustained', 'steady_calm'"
    )
    body_tendencies: Optional[str] = Field(
        None,
        description="Body tendency: 'dry_cold_slender', 'warm_medium_athletic', 'cool_solid_heavy'"
    )
    lifestyle: Optional[str] = Field(
        None,
        description="Activity and lifestyle habits"
    )
    wellness_goals: Optional[List[str]] = Field(
        default_factory=list,
        description="User wellness goals, e.g., ['sleep consistency', 'stress management']"
    )
    answers: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional key-value map of question IDs to selected choices"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "sleep": "light_restless",
                "digestion": "irregular_variable",
                "stress_response": "anxious_worry",
                "energy": "variable_bursts",
                "body_tendencies": "dry_cold_slender",
                "lifestyle": "irregular_active",
                "wellness_goals": ["sleep consistency", "stress relief"]
            }
        }
    }


class AssessmentResponse(BaseModel):
    """
    Standardized response returned by POST /api/assessment.
    Percentages come from deterministic scoring; interpretation from Claude/AI.
    """
    vata: int = Field(..., description="Vata constitution percentage (0-100)")
    pitta: int = Field(..., description="Pitta constitution percentage (0-100)")
    kapha: int = Field(..., description="Kapha constitution percentage (0-100)")
    dominant: str = Field(..., description="Dominant dosha tendency: 'Vata', 'Pitta', or 'Kapha'")
    summary: str = Field(..., description="Supportive explanation of this traditional wellness tendency")
    wellness_focus: List[str] = Field(..., description="Key daily wellness focus areas")
    note: str = Field(
        default="This is a traditional wellness-oriented interpretation, not a medical diagnosis.",
        description="Mandatory wellness disclaimer"
    )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 02 — PERSONALIZED PLAN SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class PlanTaskItem(BaseModel):
    id: str
    title: str
    category: str  # Dinacharya, Yoga, Pranayama, Diet, Lifestyle
    duration: Optional[str] = None
    what: str
    why: str
    how: str
    safety: str
    is_completed: bool = False
    is_adjusted: bool = False


class PlanRequest(BaseModel):
    dominant: str
    vata: Optional[int] = None
    pitta: Optional[int] = None
    kapha: Optional[int] = None
    wellness_goals: Optional[List[str]] = None


class PlanResponse(BaseModel):
    status: str
    module: str = "plan"
    dominant: Optional[str] = None
    tasks: List[PlanTaskItem] = []
    message: str


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 03 — CHECK-IN & PATTERN SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class CheckInRequest(BaseModel):
    sleep_score: int = Field(..., ge=1, le=5, description="Sleep quality rating (1-5)")
    stress_score: int = Field(..., ge=1, le=5, description="Stress level rating (1-5)")
    mood_score: int = Field(..., ge=1, le=5, description="General mood rating (1-5)")
    digestion_score: int = Field(..., ge=1, le=5, description="Digestion comfort rating (1-5)")
    notes: Optional[str] = None


class CheckInResponse(BaseModel):
    status: str
    module: str = "checkin"
    checkin_id: Optional[str] = None
    message: str


class PatternRequest(BaseModel):
    days: Optional[int] = 7


class PatternResponse(BaseModel):
    status: str
    module: str = "pattern"
    wellness_pulse: Optional[int] = None
    detected_pattern: Optional[str] = None
    insight: Optional[str] = None
    plan_adjusted: bool = False
    adjustment_tasks: List[str] = []


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 04 & 05 — SAFETY & CENTRES SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class SafetyCheckRequest(BaseModel):
    text: str = Field(..., description="Text or symptom query to validate for medical claims or red flags")


class SafetyCheckResponse(BaseModel):
    status: str
    module: str = "safety"
    is_safe: bool
    requires_escalation: bool
    sanitized_text: str
    safety_notice: str


class CentreItem(BaseModel):
    id: str
    name: str
    system: str
    city: str
    state: str
    pincode: str
    address: str
    phone: str
    services: List[str]
    rating: float


class CentresResponse(BaseModel):
    status: str
    total: int
    centres: List[CentreItem]


class ConsultationRequest(BaseModel):
    centre_id: str
    preferred_date: str
    preferred_system: Optional[str] = "Ayurveda"
    patient_notes: Optional[str] = None


class ConsultationResponse(BaseModel):
    status: str
    module: str = "consultation"
    booking_id: Optional[str] = None
    message: str
