"""
Pydantic schemas for AyuPulse API
"""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# ── Assessment ──────────────────────────────────────────────────────────────

class AssessmentSubmit(BaseModel):
    session_key: str = Field(..., description="Browser session identifier")
    answers: Dict[str, Any] = Field(..., description="Map of question_id → answer value")

    @model_validator(mode="after")
    def check_answers(self) -> AssessmentSubmit:
        if len(self.answers) < 10:
            raise ValueError("At least 10 answers required for a valid assessment")
        return self


class DoshaResultOut(BaseModel):
    id: str
    assessment_id: str
    vata_score: float
    pitta_score: float
    kapha_score: float
    vata_pct: float
    pitta_pct: float
    kapha_pct: float
    dominant: str
    secondary: Optional[str]
    confidence: float
    explanation: Optional[str]
    reasoning_points: Optional[List[str]]
    created_at: datetime

    model_config = {"from_attributes": True}


class AssessmentOut(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    dosha_result: Optional[DoshaResultOut] = None

    model_config = {"from_attributes": True}


# ── Plan ─────────────────────────────────────────────────────────────────────

class PlanTaskOut(BaseModel):
    id: str
    plan_id: str
    title: str
    category: str
    duration: Optional[str]
    what: str
    why: str
    how: str
    safety: str
    sort_order: int
    is_adjusted: bool
    is_completed_today: bool = False

    model_config = {"from_attributes": True}


class PlanCreate(BaseModel):
    session_key: str
    dosha_result_id: str


class PreventivePlanOut(BaseModel):
    id: str
    user_id: str
    dosha_result_id: str
    created_at: datetime
    tasks: List[PlanTaskOut] = []

    model_config = {"from_attributes": True}


class TaskCompleteRequest(BaseModel):
    date_key: Optional[str] = None   # YYYY-MM-DD, defaults to today


class TaskCompleteResponse(BaseModel):
    task_id: str
    completed: bool
    completed_at: Optional[datetime]


# ── CheckIn ──────────────────────────────────────────────────────────────────

class CheckInCreate(BaseModel):
    session_key: str
    sleep_score: int = Field(..., ge=1, le=5)
    stress_score: int = Field(..., ge=1, le=5)
    mood_score: int = Field(..., ge=1, le=5)
    digestion_score: int = Field(..., ge=1, le=5)


class CheckInOut(BaseModel):
    id: str
    user_id: str
    sleep_score: int
    stress_score: int
    mood_score: int
    digestion_score: int
    created_at: datetime
    is_seeded: bool

    model_config = {"from_attributes": True}


# ── Wellness Score ────────────────────────────────────────────────────────────

class WellnessScoreOut(BaseModel):
    score: float
    trend: Optional[str]
    label: str
    message: str


# ── Pattern Insight ───────────────────────────────────────────────────────────

class PatternInsightOut(BaseModel):
    pattern_type: str
    insight_text: str
    adjustment_tasks: Optional[List[Dict[str, str]]]
    has_adjustment: bool


# ── Dashboard ─────────────────────────────────────────────────────────────────

class WeeklyAverages(BaseModel):
    sleep: float
    stress: float
    mood: float
    digestion: float


class DashboardOut(BaseModel):
    wellness_score: WellnessScoreOut
    weekly_averages: WeeklyAverages
    pattern_insight: Optional[PatternInsightOut]
    recent_check_ins: List[CheckInOut]
    has_plan: bool
    plan_id: Optional[str]
    dosha_result: Optional[DoshaResultOut]


# ── Misc ──────────────────────────────────────────────────────────────────────

class SessionInit(BaseModel):
    session_key: str


class MessageResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None
