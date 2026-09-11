"""
AyuPulse FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.models import *  # noqa: ensure all models are registered
from app.routers import assessment, plan, checkin
from app.seed import seed_demo_data
from app.database import SessionLocal

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AyuPulse API",
    description="Preventive wellness, rooted in AYUSH. Personalized by AI.",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(assessment.router)
app.include_router(plan.router)
app.include_router(checkin.router)


@app.on_event("startup")
async def startup_event():
    """Seed demo data on startup."""
    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "app": "AyuPulse API",
        "version": "1.0.0",
        "tagline": "Preventive wellness, rooted in AYUSH. Personalized by AI.",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
