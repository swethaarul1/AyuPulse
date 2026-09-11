"""
Pattern Insight and Wellness Pulse Engine for AyuPulse Module 03.
Reads history data, computes 0-100 Wellness Score, detects recurring patterns,
and suggests plan adjustments.
"""
import json
import os
from typing import Dict, Any, List

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")


def load_history() -> List[Dict[str, Any]]:
    """Loads check-in history from data/history.json."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def compute_wellness_pulse(checkins: List[Dict[str, Any]]) -> int:
    """
    Computes a 0-100 wellness score based on the last 7 check-ins.
    Higher sleep, mood, and digestion improve the score; higher stress reduces it.
    """
    if not checkins:
        return 75

    recent = checkins[-7:]
    scores = []
    for c in recent:
        s = c.get("sleep_score", 3)
        st = c.get("stress_score", 3)
        m = c.get("mood_score", 3)
        d = c.get("digestion_score", 3)
        # Each dimension is 1-5. Invert stress: 1 (low stress) -> 5, 5 (high stress) -> 1
        inverted_stress = 6 - st
        daily_avg = (s + inverted_stress + m + d) / 4.0  # Range: 1.0 to 5.0
        daily_score = daily_avg * 20.0  # Range: 20 to 100
        scores.append(daily_score)

    return int(round(sum(scores) / len(scores)))


def analyze_history_patterns(checkins: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Analyzes check-in history to identify patterns, generate human insights,
    and trigger plan adjustments.
    """
    if checkins is None:
        checkins = load_history()

    if not checkins or len(checkins) < 3:
        return {
            "wellness_pulse": 75,
            "detected_pattern": "baseline_establishing",
            "insight": "Initial check-in baseline established. Continue daily check-ins to track trends.",
            "plan_adjusted": False,
            "adjustment_tasks": []
        }

    pulse = compute_wellness_pulse(checkins)

    # Compare last 5 days with previous days
    recent = checkins[-5:]
    prior = checkins[:-5] if len(checkins) > 5 else checkins

    avg_recent_sleep = sum(c.get("sleep_score", 3) for c in recent) / len(recent)
    avg_recent_stress = sum(c.get("stress_score", 3) for c in recent) / len(recent)
    avg_prior_sleep = sum(c.get("sleep_score", 3) for c in prior) / len(prior)
    avg_prior_stress = sum(c.get("stress_score", 3) for c in prior) / len(prior)

    avg_recent_digestion = sum(c.get("digestion_score", 3) for c in recent) / len(recent)

    # Pattern evaluation
    if avg_recent_sleep <= 2.8 and avg_recent_stress >= 3.6:
        pattern = "sleep_stress"
        insight = (
            f"Your recent check-ins show a recurring sleep and stress pattern. "
            f"Recent average sleep is {avg_recent_sleep:.1f}/5 with elevated stress at {avg_recent_stress:.1f}/5. "
            "A structured evening wind-down routine can help calm the nervous system."
        )
        plan_adjusted = True
        adjustment_tasks = [
            "Consistent evening wind-down (dim lights, no screens 30 min before bed)",
            "Gentle Nadi Shodhana (5-8 min alternate nostril breathing before sleep)",
            "Warm chamomile or nutmeg milk before sleep"
        ]
    elif avg_recent_sleep <= 2.6:
        pattern = "low_sleep"
        insight = (
            f"Your recent sleep quality ({avg_recent_sleep:.1f}/5) is below your typical baseline ({avg_prior_sleep:.1f}/5). "
            "Supporting your sleep onset routine is our current priority."
        )
        plan_adjusted = True
        adjustment_tasks = [
            "Consistent sleep anchor (fixed wake-up time every morning)",
            "Foot massage (Padabhyanga) with warm sesame oil before bed"
        ]
    elif avg_recent_stress >= 3.8:
        pattern = "elevated_stress"
        insight = (
            f"Your recent check-ins indicate elevated stress ({avg_recent_stress:.1f}/5). "
            "Micro-breaks and grounding breathwork are recommended."
        )
        plan_adjusted = True
        adjustment_tasks = [
            "Mid-day 5-minute mindfulness breathing pause",
            "Evening cooling walk in nature or open green space"
        ]
    elif avg_recent_digestion <= 2.6:
        pattern = "digestion_inconsistency"
        insight = (
            f"Recent check-ins highlight digestive irregularity ({avg_recent_digestion:.1f}/5). "
            "Kindling your digestive fire (Agni) through warm fluids is recommended."
        )
        plan_adjusted = True
        adjustment_tasks = [
            "Warm ginger water 15 minutes before main meals",
            "Avoid cold or raw foods during evening meals"
        ]
    else:
        pattern = "balanced_improving"
        insight = (
            f"Your wellness pulse is steady at {pulse}/100. Sleep and stress markers are well balanced."
        )
        plan_adjusted = False
        adjustment_tasks = []

    return {
        "wellness_pulse": pulse,
        "detected_pattern": pattern,
        "insight": insight,
        "plan_adjusted": plan_adjusted,
        "adjustment_tasks": adjustment_tasks
    }
