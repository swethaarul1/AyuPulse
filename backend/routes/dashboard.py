"""
Community Wellness Dashboard Route for AyuPulse Module 06.
Provides prototype community-level metrics on wellness engagement, patterns, and AYUSH utilization.
"""
from fastapi import APIRouter
from schemas import CommunityDashboardResponse

router = APIRouter(prefix="/api/dashboard", tags=["Module 06 - Community Wellness Dashboard"])


@router.get("", response_model=CommunityDashboardResponse)
def get_community_dashboard():
    """
    Returns prototype community wellness engagement and trend metrics.
    All data is clearly labeled as prototype simulation for demonstration.
    """
    return CommunityDashboardResponse(
        prototype=True,
        disclaimer="Prototype simulation — Not live national data.",
        metrics={
            "total_assessments": 12480,
            "task_start_rate": 68,
            "active_checkins_this_week": 8420,
            "common_pattern": "Sleep + stress",
            "ayush_matches_count": 4,
            "average_community_pulse": 71
        },
        common_patterns=[
            {"pattern": "Sleep + Stress Correlation", "frequency_percentage": 44, "dominant_dosha": "Vata"},
            {"pattern": "Low Energy & Sleep Disruption", "frequency_percentage": 26, "dominant_dosha": "Vata/Kapha"},
            {"pattern": "Digestive Irregularity & Acidity", "frequency_percentage": 18, "dominant_dosha": "Pitta"},
            {"pattern": "Balanced Seasonal Vitality", "frequency_percentage": 12, "dominant_dosha": "Balanced"}
        ],
        ayush_matches=[
            {"system": "Yoga & Pranayama", "share_percentage": 38, "top_service": "Nadi Shodhana & Restorative Asana"},
            {"system": "Ayurveda Dinacharya", "share_percentage": 34, "top_service": "Abhyanga & Agni Counseling"},
            {"system": "Naturopathy", "share_percentage": 18, "top_service": "Hydrotherapy & Nutritional Balancing"},
            {"system": "Siddha & Unani", "share_percentage": 10, "top_service": "Varma Therapy & Regimenal Care"}
        ],
        trends=[
            {"day": "Mon", "avg_wellness_pulse": 68, "checkin_count": 1180},
            {"day": "Tue", "avg_wellness_pulse": 70, "checkin_count": 1240},
            {"day": "Wed", "avg_wellness_pulse": 69, "checkin_count": 1210},
            {"day": "Thu", "avg_wellness_pulse": 72, "checkin_count": 1300},
            {"day": "Fri", "avg_wellness_pulse": 71, "checkin_count": 1280},
            {"day": "Sat", "avg_wellness_pulse": 74, "checkin_count": 1110},
            {"day": "Sun", "avg_wellness_pulse": 76, "checkin_count": 1100}
        ]
    )
