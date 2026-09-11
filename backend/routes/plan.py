"""
Plan API Routes for AyuPulse Module 02: AI Personalized Preventive Plan & Daily Tracker.
Generates tailored Dinacharya, Yoga, Pranayama, and Diet/Lifestyle recommendations
and an actionable daily tracker with persistent task completion states.
"""
import os
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from schemas import PlanRequest, PlanResponse
from services.claude_service import claude_service
import logging

router = APIRouter(prefix="/api/plan", tags=["Module 02 - Preventive Plan"])
logger = logging.getLogger("ayupulse.routes.plan")

TASKS_STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tasks_state.json")


def _load_tasks_state() -> Dict[str, Any]:
    if os.path.exists(TASKS_STATE_FILE):
        try:
            with open(TASKS_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_tasks_state(state: Dict[str, Any]):
    try:
        with open(TASKS_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to persist task state: {e}")


class TaskToggleRequest(BaseModel):
    completed: Optional[bool] = None
    session_id: Optional[str] = "demo-session"


@router.post("", response_model=PlanResponse, status_code=status.HTTP_200_OK)
def generate_preventive_plan(payload: PlanRequest):
    """
    Generates a personalized preventive daily plan and daily tracker.
    Considers dominant dosha, vata/pitta/kapha percentages, lifestyle, and goals.
    Produces 4 sections (Dinacharya, Yoga, Pranayama, Diet/Lifestyle)
    with What, Why, How, Safety and 4-6 actionable daily tracker tasks.
    Enriches tracker tasks with any previously persisted completion states.
    """
    try:
        plan_data = claude_service.generate_personalized_plan(
            dominant=payload.dominant,
            vata=payload.vata,
            pitta=payload.pitta,
            kapha=payload.kapha,
            lifestyle=payload.lifestyle,
            wellness_goals=payload.wellness_goals,
            preferences=payload.preferences
        )

        # Merge persisted task completion states if any
        persisted_states = _load_tasks_state()
        if "daily_tracker" in plan_data:
            for task in plan_data["daily_tracker"]:
                t_id = task["id"]
                if t_id in persisted_states:
                    task["completed"] = persisted_states[t_id].get("completed", False)

        return PlanResponse(**plan_data)
    except Exception as e:
        logger.error(f"Failed to generate preventive plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while personalizing your preventive plan."
        )


@router.get("/tasks/state")
def get_tasks_state():
    """Returns the persistent completion states for daily tracker tasks."""
    return {
        "status": "success",
        "tasks": _load_tasks_state()
    }


@router.post("/tasks/{task_id}/toggle")
def toggle_task_completion(task_id: str, payload: TaskToggleRequest = TaskToggleRequest()):
    """
    Persistently marks a daily tracker task as completed or incomplete.
    """
    state = _load_tasks_state()
    current_entry = state.get(task_id, {})
    current_completed = current_entry.get("completed", False)

    new_completed = payload.completed if payload.completed is not None else not current_completed

    state[task_id] = {
        "task_id": task_id,
        "completed": new_completed,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "session_id": payload.session_id
    }
    _save_tasks_state(state)

    return {
        "status": "updated",
        "task_id": task_id,
        "completed": new_completed,
        "message": f"Task '{task_id}' marked as {'completed' if new_completed else 'incomplete'}."
    }
