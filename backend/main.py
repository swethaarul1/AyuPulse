"""
AyuPulse Backend Application
Preventive wellness, rooted in AYUSH. Personalized by AI.
"""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from routes import (
    assessment_router,
    plan_router,
    checkin_router,
    pattern_router,
    safety_router,
    centres_router,
    dashboard_router,
)

app = FastAPI(
    title="AyuPulse API",
    description="Preventive wellness, rooted in AYUSH. Personalized by AI.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS CONFIGURATION ────────────────────────────────────────────────────────
cors_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173")
origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ROUTER REGISTRATION ───────────────────────────────────────────────────────
app.include_router(assessment_router)
app.include_router(plan_router)
app.include_router(checkin_router)
app.include_router(pattern_router)
app.include_router(safety_router)
app.include_router(centres_router)
app.include_router(dashboard_router)


# ── HEALTH & ROOT ENDPOINTS ───────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Returns application health status."""
    return {
        "status": "ok",
        "service": "AyuPulse backend"
    }


@app.get("/", tags=["Root"])
def root():
    """Returns platform meta and documentation link."""
    return {
        "name": "AyuPulse API",
        "tagline": "Preventive wellness, rooted in AYUSH. Personalized by AI.",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "health": "GET /health",
            "assessment": "POST /api/assessment",
            "plan": "POST /api/plan",
            "checkin": "POST /api/checkin",
            "pattern": "POST /api/pattern",
            "safety": "POST /api/safety",
            "centres": "GET /api/centres",
            "match": "POST /api/centres/match",
            "consultation": "POST /api/consultation",
            "dashboard": "GET /api/dashboard"
        }
    }


# ── ERROR HANDLING ────────────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred. Please verify your request payload.",
        }
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)
