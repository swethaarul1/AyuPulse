"""
Assessment API Router — Module 01
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AssessmentSubmit, AssessmentOut, DoshaResultOut, MessageResponse
from app.models import DemoUser, Assessment, DoshaResult
from app.services.ai_service import ai_service
from app.services.assessment_engine import get_questions

router = APIRouter(prefix="/api/assessment", tags=["Assessment"])


def get_or_create_user(session_key: str, db: Session) -> DemoUser:
    user = db.query(DemoUser).filter(DemoUser.session_key == session_key).first()
    if not user:
        user = DemoUser(session_key=session_key)
        db.add(user)
        db.flush()
    return user


@router.get("/questions")
def list_questions():
    """Return the assessment questionnaire."""
    return {"questions": get_questions()}


@router.post("", response_model=AssessmentOut)
def submit_assessment(payload: AssessmentSubmit, db: Session = Depends(get_db)):
    """Submit assessment answers and compute Dosha result."""
    user = get_or_create_user(payload.session_key, db)

    # Score the assessment
    result = ai_service.interpret_assessment(payload.answers)

    # Persist Assessment
    assessment = Assessment(
        user_id=user.id,
        answers=payload.answers,
    )
    db.add(assessment)
    db.flush()

    # Persist DoshaResult
    dosha_result = DoshaResult(
        assessment_id=assessment.id,
        vata_score=result["vata_score"],
        pitta_score=result["pitta_score"],
        kapha_score=result["kapha_score"],
        vata_pct=result["vata_pct"],
        pitta_pct=result["pitta_pct"],
        kapha_pct=result["kapha_pct"],
        dominant=result["dominant"],
        secondary=result.get("secondary"),
        confidence=result["confidence"],
        explanation=result.get("explanation"),
        reasoning_points=result.get("reasoning_points"),
    )
    db.add(dosha_result)
    db.commit()
    db.refresh(assessment)
    db.refresh(dosha_result)

    return AssessmentOut(
        id=assessment.id,
        user_id=user.id,
        created_at=assessment.created_at,
        dosha_result=DoshaResultOut.model_validate(dosha_result),
    )


@router.get("/{assessment_id}", response_model=AssessmentOut)
def get_assessment(assessment_id: str, db: Session = Depends(get_db)):
    """Retrieve an assessment by ID."""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return AssessmentOut(
        id=assessment.id,
        user_id=assessment.user_id,
        created_at=assessment.created_at,
        dosha_result=DoshaResultOut.model_validate(assessment.dosha_result) if assessment.dosha_result else None,
    )


@router.get("/result/{dosha_result_id}", response_model=DoshaResultOut)
def get_dosha_result(dosha_result_id: str, db: Session = Depends(get_db)):
    """Retrieve a Dosha result directly by ID."""
    result = db.query(DoshaResult).filter(DoshaResult.id == dosha_result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Dosha result not found")
    return DoshaResultOut.model_validate(result)
