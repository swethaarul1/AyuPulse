# Routes package for AyuPulse
from routes.assessment import router as assessment_router
from routes.plan import router as plan_router
from routes.checkin import router as checkin_router
from routes.pattern import router as pattern_router
from routes.safety import router as safety_router
from routes.centres import router as centres_router
from routes.dashboard import router as dashboard_router

__all__ = [
    "assessment_router",
    "plan_router",
    "checkin_router",
    "pattern_router",
    "safety_router",
    "centres_router",
    "dashboard_router"
]
