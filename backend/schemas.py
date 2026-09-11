"""
AyuPulse Pydantic Schemas
Defines request and response contracts for all API endpoints across Modules 01–06.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator


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
# MODULE 02 — PERSONALIZED PREVENTIVE PLAN & DAILY TRACKER SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class PlanRecommendation(BaseModel):
    title: str = Field(..., description="Title of the preventive practice")
    what: str = Field(..., description="Exact description of the practice")
    why: str = Field(..., description="Why this fits user tendency and goal")
    how: str = Field(..., description="Step-by-step practical method with duration/timing")
    safety: str = Field(..., description="Safety considerations and clinical boundaries")


class DailyTrackerTask(BaseModel):
    id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Actionable task title")
    description: str = Field(..., description="Brief practical task cue")
    category: Optional[str] = Field(None, description="Category: Dinacharya, Yoga, Pranayama, Diet, Lifestyle")
    duration: Optional[str] = Field(None, description="Recommended duration (e.g., '5 min')")
    completed: bool = Field(False, description="Checkbox completion status")


class PlanTaskItem(BaseModel):
    """Backwards-compatible task item representation."""
    id: str
    title: str
    category: str
    duration: Optional[str] = None
    what: str
    why: str
    how: str
    safety: str
    is_completed: bool = False
    is_adjusted: bool = False


class PlanSections(BaseModel):
    dinacharya: List[PlanRecommendation] = Field(default_factory=list, description="Daily routine practices")
    yoga: List[PlanRecommendation] = Field(default_factory=list, description="Yoga and movement practices")
    pranayama: List[PlanRecommendation] = Field(default_factory=list, description="Breathwork practices")
    diet_lifestyle: List[PlanRecommendation] = Field(default_factory=list, description="Dietary and lifestyle guidance")


class PlanRequest(BaseModel):
    dominant: str = Field(..., description="Dominant dosha: 'Vata', 'Pitta', or 'Kapha'")
    vata: Optional[int] = Field(None, ge=0, le=100, description="Vata percentage")
    pitta: Optional[int] = Field(None, ge=0, le=100, description="Pitta percentage")
    kapha: Optional[int] = Field(None, ge=0, le=100, description="Kapha percentage")
    lifestyle: Optional[str] = Field(None, description="User lifestyle context")
    wellness_goals: Optional[List[str]] = Field(default_factory=list, description="Target wellness goals")
    preferences: Optional[Dict[str, Any]] = Field(default=None, description="Additional user preferences")

    model_config = {
        "json_schema_extra": {
            "example": {
                "dominant": "Vata",
                "vata": 52,
                "pitta": 31,
                "kapha": 17,
                "lifestyle": "irregular schedule, late nights",
                "wellness_goals": ["sleep consistency", "stress management"]
            }
        }
    }


class PlanResponse(BaseModel):
    status: str = "success"
    module: str = "plan"
    dominant: str
    sections: PlanSections
    daily_tracker: List[DailyTrackerTask]
    tasks: List[PlanTaskItem] = []  # Backwards compatibility
    message: str
    note: str = Field(
        default="AyuPulse provides preventive wellness guidance, not medical diagnosis or treatment.",
        description="Preventive wellness disclaimer"
    )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 03 — CHECK-IN, PATTERN INSIGHT & WELLNESS SCORE SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class CheckInRequest(BaseModel):
    """
    Accepts 1-5 scale ratings for Sleep, Stress, Mood, Digestion, and Energy.
    Supports either 'sleep_score' or 'sleep' naming conventions.
    """
    sleep_score: Optional[int] = Field(None, ge=1, le=5)
    stress_score: Optional[int] = Field(None, ge=1, le=5)
    mood_score: Optional[int] = Field(None, ge=1, le=5)
    digestion_score: Optional[int] = Field(None, ge=1, le=5)
    energy_score: Optional[int] = Field(None, ge=1, le=5)

    sleep: Optional[int] = Field(None, ge=1, le=5)
    stress: Optional[int] = Field(None, ge=1, le=5)
    mood: Optional[int] = Field(None, ge=1, le=5)
    digestion: Optional[int] = Field(None, ge=1, le=5)
    energy: Optional[int] = Field(None, ge=1, le=5)

    user_id: Optional[str] = "demo-user"
    date: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def unify_fields(self) -> "CheckInRequest":
        # Consolidate aliases
        if self.sleep_score is None:
            self.sleep_score = self.sleep or 3
        if self.stress_score is None:
            self.stress_score = self.stress or 3
        if self.mood_score is None:
            self.mood_score = self.mood or 3
        if self.digestion_score is None:
            self.digestion_score = self.digestion or 3
        if self.energy_score is None:
            self.energy_score = self.energy or 3
        return self


class CheckInResponse(BaseModel):
    status: str = "recorded"
    module: str = "checkin"
    checkin_id: str
    wellness_score: int = Field(..., ge=0, le=100, description="Deterministic 0-100 wellness score")
    summary: str = Field(..., description="Short explanation of today's check-in pulse")
    checkin: Dict[str, Any] = Field(..., description="Consolidated check-in values")
    message: str


class PatternItem(BaseModel):
    type: str = Field(..., description="Pattern identifier, e.g. 'sleep_stress'")
    title: str = Field(..., description="Human-readable title")
    description: str = Field(..., description="Analysis of recurring trend")
    strength: str = Field("moderate", description="Strength: 'mild', 'moderate', 'strong'")


class PatternRequest(BaseModel):
    days: Optional[int] = 7
    checkins: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Optional list of check-in entries to evaluate directly"
    )


class PatternResponse(BaseModel):
    status: str = "success"
    module: str = "pattern"
    patterns: List[PatternItem] = []
    next_step: str = Field(..., description="Simple preventive wellness action")
    wellness_pulse: int = Field(..., ge=0, le=100)
    detected_pattern: str
    insight: str
    plan_adjusted: bool = False
    adjustment_tasks: List[str] = []
    data_status: str = "Prototype seeded history"


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 04 — AYUSH ACCESS BRIDGE & CENTRES SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

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
    data_status: str = "Prototype AYUSH centre data"


class CentresResponse(BaseModel):
    status: str = "success"
    total: int
    data_status: str = "Prototype AYUSH centre data"
    disclaimer: str = "Seeded centre data for demonstration — Not a live nationwide directory."
    centres: List[CentreItem]


class CentreMatchRequest(BaseModel):
    wellness_goal: Optional[str] = Field(None, description="e.g. 'stress relief', 'sleep quality'")
    wellness_focus: Optional[str] = Field(None, description="e.g. 'stress', 'movement', 'digestion'")
    preferred_system: Optional[str] = Field(None, description="e.g. 'Ayurveda', 'Yoga', 'Naturopathy'")
    location: Optional[str] = Field(None, description="City or state filter")


class CentreMatchResponse(BaseModel):
    status: str = "matched"
    wellness_focus: str
    recommended_service: str
    data_status: str = "Prototype AYUSH centre data"
    matched_centres: List[CentreItem]
    professional_notice: Optional[str] = None


class ConsultationRequest(BaseModel):
    centre_id: str
    preferred_date: str
    preferred_system: Optional[str] = "Ayurveda"
    patient_notes: Optional[str] = None


class ConsultationResponse(BaseModel):
    status: str = "requested"
    module: str = "consultation"
    booking_id: str
    centre_id: str
    message: str
    next_step: str = "A qualified provider would contact the user in a production system."
    notice: str = "Prototype demonstration only. Not a live appointment."


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 05 — SAFETY GATE SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class SafetyCheckRequest(BaseModel):
    text: Optional[str] = Field(None, description="Text to validate for medical claims or red flags")
    user_input: Optional[str] = Field(None, description="Original user prompt or query")
    recommendation: Optional[str] = Field(None, description="AI or system recommendation to inspect")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="AI confidence score if available")

    @model_validator(mode="after")
    def populate_text(self) -> "SafetyCheckRequest":
        if not self.text:
            self.text = self.recommendation or self.user_input or ""
        return self


class SafetyCheckResponse(BaseModel):
    safe: bool = Field(..., description="Whether content is safe for user presentation")
    risk_level: str = Field(..., description="'low', 'medium', or 'high'")
    action: str = Field(..., description="'allow', 'modify', 'caution', or 'professional_attention'")
    message: str = Field(..., description="User-facing status message")
    modified_content: str = Field(..., description="Sanitized, compliant preventive wellness content")
    professional_attention: bool = Field(False, description="True if medical escalation is advised")

    # Backwards-compatible aliases
    is_safe: bool = True
    requires_escalation: bool = False
    sanitized_text: str = ""
    safety_notice: str = ""

    @model_validator(mode="after")
    def sync_aliases(self) -> "SafetyCheckResponse":
        self.is_safe = self.safe
        self.requires_escalation = self.professional_attention
        self.sanitized_text = self.modified_content
        self.safety_notice = self.message
        return self


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 06 — COMMUNITY WELLNESS DASHBOARD SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class CommunityDashboardResponse(BaseModel):
    prototype: bool = True
    disclaimer: str = "Prototype simulation — Not live national data."
    metrics: Dict[str, Any] = Field(
        default_factory=lambda: {
            "total_assessments": 12480,
            "task_start_rate": 68,
            "active_checkins_this_week": 8420,
            "common_pattern": "Sleep + stress",
            "ayush_matches_count": 4
        }
    )
    common_patterns: List[Dict[str, Any]] = Field(default_factory=list)
    ayush_matches: List[Dict[str, Any]] = Field(default_factory=list)
    trends: List[Dict[str, Any]] = Field(default_factory=list)
