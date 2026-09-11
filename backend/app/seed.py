"""
Seed demo data for AyuPulse hackathon demonstration.
Creates a demo session with realistic check-in history.
"""
from datetime import datetime, timezone, timedelta
import random
from sqlalchemy.orm import Session
from app.models import DemoUser, CheckIn

DEMO_SESSION_KEY = "demo-session-ayupulse-2024"

# Realistic seeded check-in data — shows a sleep+stress pattern in recent entries
# Clearly labeled as prototype demo data
SEED_CHECKINS = [
    # 14 days ago — good state
    {"sleep": 4, "stress": 2, "mood": 4, "digestion": 4, "days_ago": 14},
    {"sleep": 4, "stress": 2, "mood": 4, "digestion": 3, "days_ago": 13},
    {"sleep": 3, "stress": 3, "mood": 4, "digestion": 4, "days_ago": 12},
    {"sleep": 4, "stress": 2, "mood": 5, "digestion": 4, "days_ago": 11},
    {"sleep": 4, "stress": 2, "mood": 4, "digestion": 4, "days_ago": 10},
    {"sleep": 3, "stress": 3, "mood": 3, "digestion": 3, "days_ago": 9},
    {"sleep": 4, "stress": 2, "mood": 4, "digestion": 4, "days_ago": 8},
    # Recent — sleep declining, stress rising (pattern to detect)
    {"sleep": 3, "stress": 3, "mood": 3, "digestion": 3, "days_ago": 7},
    {"sleep": 2, "stress": 4, "mood": 3, "digestion": 3, "days_ago": 6},
    {"sleep": 2, "stress": 4, "mood": 2, "digestion": 2, "days_ago": 5},
    {"sleep": 2, "stress": 4, "mood": 3, "digestion": 3, "days_ago": 4},
    {"sleep": 2, "stress": 4, "mood": 2, "digestion": 2, "days_ago": 3},
    {"sleep": 3, "stress": 4, "mood": 2, "digestion": 3, "days_ago": 2},
    {"sleep": 2, "stress": 4, "mood": 3, "digestion": 2, "days_ago": 1},
]


def seed_demo_data(db: Session) -> DemoUser:
    """
    Create (or retrieve) the demo user and seed check-in history.
    Safe to call multiple times — will not duplicate.
    """
    now = datetime.now(timezone.utc)

    # Get or create demo user
    demo_user = db.query(DemoUser).filter(DemoUser.session_key == DEMO_SESSION_KEY).first()
    if not demo_user:
        demo_user = DemoUser(session_key=DEMO_SESSION_KEY)
        db.add(demo_user)
        db.flush()

    # Only seed if no check-ins yet
    existing = db.query(CheckIn).filter(
        CheckIn.user_id == demo_user.id,
        CheckIn.is_seeded == True
    ).count()

    if existing == 0:
        for entry in SEED_CHECKINS:
            dt = now - timedelta(days=entry["days_ago"])
            ci = CheckIn(
                user_id=demo_user.id,
                sleep_score=entry["sleep"],
                stress_score=entry["stress"],
                mood_score=entry["mood"],
                digestion_score=entry["digestion"],
                created_at=dt,
                is_seeded=True,
            )
            db.add(ci)

    db.commit()
    return demo_user
