"""
AyuPulse SQLAlchemy Models
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, Boolean,
    DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


def gen_id():
    return str(uuid.uuid4())


class DemoUser(Base):
    __tablename__ = "demo_users"

    id = Column(String, primary_key=True, default=gen_id)
    session_key = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)

    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    preventive_plans = relationship("PreventivePlan", back_populates="user", cascade="all, delete-orphan")
    check_ins = relationship("CheckIn", back_populates="user", cascade="all, delete-orphan")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("demo_users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    answers = Column(JSON, nullable=False)  # {question_id: answer_value}

    user = relationship("DemoUser", back_populates="assessments")
    dosha_result = relationship("DoshaResult", back_populates="assessment", uselist=False, cascade="all, delete-orphan")


class DoshaResult(Base):
    __tablename__ = "dosha_results"

    id = Column(String, primary_key=True, default=gen_id)
    assessment_id = Column(String, ForeignKey("assessments.id"), nullable=False)
    vata_score = Column(Float, nullable=False)
    pitta_score = Column(Float, nullable=False)
    kapha_score = Column(Float, nullable=False)
    vata_pct = Column(Float, nullable=False)
    pitta_pct = Column(Float, nullable=False)
    kapha_pct = Column(Float, nullable=False)
    dominant = Column(String, nullable=False)
    secondary = Column(String, nullable=True)
    confidence = Column(Float, nullable=False)
    explanation = Column(Text, nullable=True)
    reasoning_points = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)

    assessment = relationship("Assessment", back_populates="dosha_result")
    preventive_plan = relationship("PreventivePlan", back_populates="dosha_result", uselist=False)


class PreventivePlan(Base):
    __tablename__ = "preventive_plans"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("demo_users.id"), nullable=False)
    dosha_result_id = Column(String, ForeignKey("dosha_results.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user = relationship("DemoUser", back_populates="preventive_plans")
    dosha_result = relationship("DoshaResult", back_populates="preventive_plan")
    tasks = relationship("PlanTask", back_populates="plan", cascade="all, delete-orphan")


class PlanTask(Base):
    __tablename__ = "plan_tasks"

    id = Column(String, primary_key=True, default=gen_id)
    plan_id = Column(String, ForeignKey("preventive_plans.id"), nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)          # Dinacharya, Yoga, Pranayama, Diet, Lifestyle
    duration = Column(String, nullable=True)
    what = Column(Text, nullable=False)
    why = Column(Text, nullable=False)
    how = Column(Text, nullable=False)
    safety = Column(Text, nullable=False)
    sort_order = Column(Integer, default=0)
    is_adjusted = Column(Boolean, default=False)       # True when added by pattern engine

    plan = relationship("PreventivePlan", back_populates="tasks")
    completions = relationship("TaskCompletion", back_populates="task", cascade="all, delete-orphan")


class TaskCompletion(Base):
    __tablename__ = "task_completions"

    id = Column(String, primary_key=True, default=gen_id)
    task_id = Column(String, ForeignKey("plan_tasks.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), default=utcnow)
    date_key = Column(String, nullable=False)          # YYYY-MM-DD for idempotency

    task = relationship("PlanTask", back_populates="completions")


class CheckIn(Base):
    __tablename__ = "check_ins"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("demo_users.id"), nullable=False)
    sleep_score = Column(Integer, nullable=False)      # 1-5
    stress_score = Column(Integer, nullable=False)     # 1-5
    mood_score = Column(Integer, nullable=False)       # 1-5
    digestion_score = Column(Integer, nullable=False)  # 1-5
    created_at = Column(DateTime(timezone=True), default=utcnow)
    is_seeded = Column(Boolean, default=False)         # True for demo seed data

    user = relationship("DemoUser", back_populates="check_ins")


class WellnessScore(Base):
    __tablename__ = "wellness_scores"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("demo_users.id"), nullable=False)
    score = Column(Float, nullable=False)
    trend = Column(String, nullable=True)              # up, down, stable
    computed_at = Column(DateTime(timezone=True), default=utcnow)


class PatternInsight(Base):
    __tablename__ = "pattern_insights"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("demo_users.id"), nullable=False)
    pattern_type = Column(String, nullable=False)      # e.g. sleep_stress, improving, stable
    insight_text = Column(Text, nullable=False)
    adjustment_tasks = Column(JSON, nullable=True)     # list of task titles to surface
    created_at = Column(DateTime(timezone=True), default=utcnow)
