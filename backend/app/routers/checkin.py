"""
Check-in API Router — Module 03
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas import (
    CheckInCreate, CheckInOut, WellnessScoreOut,
    PatternInsightOut, DashboardOut, WeeklyAverages
)
from app.models import DemoUser, CheckIn, PreventivePlan, DoshaResult
from app.services.ai_service import ai_service
from app.services.pattern_engine import compute_weekly_averages
from app.seed import DEMO_SESSION_KEY

router = APIRouter(prefix="/api", tags=["CheckIn"])


def get_or_create_user(session_key: str, db: Session) -> DemoUser:
    user = db.query(DemoUser).filter(DemoUser.session_key == session_key).first()
    if not user:
        user = DemoUser(session_key=session_key)
        db.add(user)
        db.flush()
        db.commit()
        db.refresh(user)
    return user


@router.post("/checkins", response_model=CheckInOut)
def submit_checkin(payload: CheckInCreate, db: Session = Depends(get_db)):
    """Submit a daily check-in."""
    user = get_or_create_user(payload.session_key, db)

    checkin = CheckIn(
        user_id=user.id,
        sleep_score=payload.sleep_score,
        stress_score=payload.stress_score,
        mood_score=payload.mood_score,
        digestion_score=payload.digestion_score,
        is_seeded=False,
    )
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return CheckInOut.model_validate(checkin)


@router.get("/checkins", response_model=list[CheckInOut])
def get_checkins(
    session_key: str = Query(...),
    limit: int = Query(30, le=100),
    db: Session = Depends(get_db)
):
    """Get check-in history for a session."""
    user = db.query(DemoUser).filter(DemoUser.session_key == session_key).first()
    if not user:
        return []
    checkins = (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user.id)
        .order_by(CheckIn.created_at.asc())
        .limit(limit)
        .all()
    )
    return [CheckInOut.model_validate(c) for c in checkins]


@router.get("/wellness-score", response_model=WellnessScoreOut)
def get_wellness_score(
    session_key: str = Query(...),
    db: Session = Depends(get_db)
):
    """Compute and return the wellness score."""
    user = db.query(DemoUser).filter(DemoUser.session_key == session_key).first()
    if not user:
        return WellnessScoreOut(score=50.0, trend="stable", label="No data", message="Complete your first check-in.")

    checkins = (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user.id)
        .order_by(CheckIn.created_at.asc())
        .all()
    )
    result = ai_service.compute_wellness_score(checkins)
    return WellnessScoreOut(**result)


@router.get("/pattern-insight", response_model=Optional[PatternInsightOut])
def get_pattern_insight(
    session_key: str = Query(...),
    db: Session = Depends(get_db)
):
    """Analyze check-in history and return pattern insight."""
    user = db.query(DemoUser).filter(DemoUser.session_key == session_key).first()
    if not user:
        return None

    checkins = (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user.id)
        .order_by(CheckIn.created_at.asc())
        .all()
    )
    result = ai_service.analyze_check_in_pattern(checkins)
    if not result:
        return None

    return PatternInsightOut(
        pattern_type=result["pattern_type"],
        insight_text=result["insight_text"],
        adjustment_tasks=result.get("adjustment_tasks"),
        has_adjustment=result.get("has_adjustment", False),
    )


@router.get("/dashboard", response_model=DashboardOut)
def get_dashboard(
    session_key: str = Query(...),
    db: Session = Depends(get_db)
):
    """Aggregate dashboard data for Module 03."""
    user = db.query(DemoUser).filter(DemoUser.session_key == session_key).first()
    if not user:
        # Return empty dashboard
        return DashboardOut(
            wellness_score=WellnessScoreOut(score=50.0, trend="stable", label="No data", message="Complete your first check-in."),
            weekly_averages=WeeklyAverages(sleep=0, stress=0, mood=0, digestion=0),
            pattern_insight=None,
            recent_check_ins=[],
            has_plan=False,
            plan_id=None,
            dosha_result=None,
        )

    checkins = (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user.id)
        .order_by(CheckIn.created_at.asc())
        .all()
    )

    wellness = ai_service.compute_wellness_score(checkins)
    pattern = ai_service.analyze_check_in_pattern(checkins)
    weekly_avgs = compute_weekly_averages(checkins)

    recent_checkins_out = [CheckInOut.model_validate(c) for c in checkins[-14:]]

    # Latest plan
    plan = (
        db.query(PreventivePlan)
        .filter(PreventivePlan.user_id == user.id)
        .order_by(PreventivePlan.created_at.desc())
        .first()
    )

    # Latest dosha result
    from app.schemas import DoshaResultOut
    dosha_out = None
    if plan:
        dr = db.query(DoshaResult).filter(DoshaResult.id == plan.dosha_result_id).first()
        if dr:
            dosha_out = DoshaResultOut.model_validate(dr)

    pattern_out = None
    if pattern:
        pattern_out = PatternInsightOut(
            pattern_type=pattern["pattern_type"],
            insight_text=pattern["insight_text"],
            adjustment_tasks=pattern.get("adjustment_tasks"),
            has_adjustment=pattern.get("has_adjustment", False),
        )

    return DashboardOut(
        wellness_score=WellnessScoreOut(**wellness),
        weekly_averages=WeeklyAverages(**weekly_avgs),
        pattern_insight=pattern_out,
        recent_check_ins=recent_checkins_out,
        has_plan=plan is not None,
        plan_id=plan.id if plan else None,
        dosha_result=dosha_out,
    )
