"""
Plan API Router — Module 02
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.schemas import PlanCreate, PreventivePlanOut, PlanTaskOut, TaskCompleteRequest, TaskCompleteResponse
from app.models import DemoUser, DoshaResult, PreventivePlan, PlanTask, TaskCompletion
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api/plan", tags=["Plan"])


def _today_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _enrich_tasks(tasks: list, db: Session) -> list[PlanTaskOut]:
    today = _today_key()
    result = []
    for task in tasks:
        completion = db.query(TaskCompletion).filter(
            TaskCompletion.task_id == task.id,
            TaskCompletion.date_key == today,
        ).first()
        out = PlanTaskOut.model_validate(task)
        out.is_completed_today = completion is not None
        result.append(out)
    return result


@router.post("", response_model=PreventivePlanOut)
def create_plan(payload: PlanCreate, db: Session = Depends(get_db)):
    """Generate a personalized preventive plan from a Dosha result."""
    # Validate dosha result exists
    dosha_result = db.query(DoshaResult).filter(DoshaResult.id == payload.dosha_result_id).first()
    if not dosha_result:
        raise HTTPException(status_code=404, detail="Dosha result not found")

    # Get or create user
    user = db.query(DemoUser).filter(DemoUser.session_key == payload.session_key).first()
    if not user:
        raise HTTPException(status_code=404, detail="User session not found")

    # Check for existing plan for this dosha result
    existing = db.query(PreventivePlan).filter(
        PreventivePlan.dosha_result_id == payload.dosha_result_id
    ).first()
    if existing:
        tasks_out = _enrich_tasks(existing.tasks, db)
        plan_out = PreventivePlanOut.model_validate(existing)
        plan_out.tasks = tasks_out
        return plan_out

    # Generate practices
    dosha_dict = {
        "dominant": dosha_result.dominant,
        "secondary": dosha_result.secondary,
        "vata_pct": dosha_result.vata_pct,
        "pitta_pct": dosha_result.pitta_pct,
        "kapha_pct": dosha_result.kapha_pct,
    }
    practices = ai_service.generate_preventive_plan(dosha_dict)

    # Persist plan
    plan = PreventivePlan(
        user_id=user.id,
        dosha_result_id=dosha_result.id,
    )
    db.add(plan)
    db.flush()

    for practice in practices:
        task = PlanTask(
            plan_id=plan.id,
            title=practice["title"],
            category=practice["category"],
            duration=practice.get("duration"),
            what=practice["what"],
            why=practice["why"],
            how=practice["how"],
            safety=practice["safety"],
            sort_order=practice.get("sort_order", 0),
            is_adjusted=practice.get("is_adjusted", False),
        )
        db.add(task)

    db.commit()
    db.refresh(plan)

    tasks_out = _enrich_tasks(plan.tasks, db)
    plan_out = PreventivePlanOut.model_validate(plan)
    plan_out.tasks = tasks_out
    return plan_out


@router.get("/{plan_id}", response_model=PreventivePlanOut)
def get_plan(plan_id: str, db: Session = Depends(get_db)):
    """Retrieve a plan by ID."""
    plan = db.query(PreventivePlan).filter(PreventivePlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    tasks_out = _enrich_tasks(plan.tasks, db)
    plan_out = PreventivePlanOut.model_validate(plan)
    plan_out.tasks = tasks_out
    return plan_out


@router.get("/{plan_id}/tasks", response_model=list[PlanTaskOut])
def get_tasks(plan_id: str, db: Session = Depends(get_db)):
    """Get tasks for a plan."""
    plan = db.query(PreventivePlan).filter(PreventivePlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _enrich_tasks(plan.tasks, db)


@router.post("/tasks/{task_id}/complete", response_model=TaskCompleteResponse)
def complete_task(task_id: str, payload: TaskCompleteRequest = None, db: Session = Depends(get_db)):
    """Mark a task as complete (or toggle off) for today."""
    task = db.query(PlanTask).filter(PlanTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    date_key = (payload.date_key if payload and payload.date_key else None) or _today_key()

    existing = db.query(TaskCompletion).filter(
        TaskCompletion.task_id == task_id,
        TaskCompletion.date_key == date_key,
    ).first()

    if existing:
        # Toggle off
        db.delete(existing)
        db.commit()
        return TaskCompleteResponse(task_id=task_id, completed=False, completed_at=None)

    # Mark complete
    completion = TaskCompletion(task_id=task_id, date_key=date_key)
    db.add(completion)
    db.commit()
    db.refresh(completion)
    return TaskCompleteResponse(task_id=task_id, completed=True, completed_at=completion.completed_at)


@router.get("/by-session/{session_key}", response_model=PreventivePlanOut)
def get_plan_by_session(session_key: str, db: Session = Depends(get_db)):
    """Get the latest plan for a session."""
    user = db.query(DemoUser).filter(DemoUser.session_key == session_key).first()
    if not user:
        raise HTTPException(status_code=404, detail="Session not found")

    plan = (
        db.query(PreventivePlan)
        .filter(PreventivePlan.user_id == user.id)
        .order_by(PreventivePlan.created_at.desc())
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="No plan found for this session")

    tasks_out = _enrich_tasks(plan.tasks, db)
    plan_out = PreventivePlanOut.model_validate(plan)
    plan_out.tasks = tasks_out
    return plan_out
