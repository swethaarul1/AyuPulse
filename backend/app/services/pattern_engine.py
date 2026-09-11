"""
Pattern Engine — AyuPulse Module 03
Analyzes check-in history to detect recurring wellness patterns.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone


# ─────────────────────────────────────────────────────────────────────────────
# WELLNESS SCORE ALGORITHM
# ─────────────────────────────────────────────────────────────────────────────

def compute_wellness_score(check_ins: List[Any]) -> Dict[str, Any]:
    """
    Compute a 0–100 wellness score from recent check-ins.
    check_ins: list of CheckIn ORM objects or dicts with sleep/stress/mood/digestion scores.
    """
    if not check_ins:
        return {"score": 50.0, "trend": "stable", "label": "No data yet", "message": "Complete your first check-in to see your Wellness Score."}

    # Use last 7 check-ins for score
    recent = check_ins[-7:]
    older = check_ins[:-7] if len(check_ins) > 7 else []

    def extract(ci):
        if hasattr(ci, "sleep_score"):
            return ci.sleep_score, ci.stress_score, ci.mood_score, ci.digestion_score
        return ci["sleep_score"], ci["stress_score"], ci["mood_score"], ci["digestion_score"]

    def avg_score(items):
        if not items:
            return None
        scores = []
        for ci in items:
            s, st, m, d = extract(ci)
            # Stress is inverted (higher stress = lower wellness)
            val = (s * 20 + (6 - st) * 20 + m * 20 + d * 20) / 4
            # Normalize each dimension: sleep(1-5)*20=20-100, stress inverted (1-5)->80-20
            # Overall range: 20–100
            scores.append(val)
        return sum(scores) / len(scores)

    recent_score = avg_score(recent)
    older_score = avg_score(older)

    # Determine trend
    if older_score is not None:
        delta = recent_score - older_score
        if delta > 3:
            trend = "up"
        elif delta < -3:
            trend = "down"
        else:
            trend = "stable"
    else:
        trend = "stable"

    score = round(recent_score, 1)

    if score >= 75:
        label = "Thriving"
        message = "Your wellness pulse is strong this week. Keep up the great habits."
    elif score >= 60:
        label = "Good"
        message = "Your wellness pulse is looking good. Small consistent habits are making a difference."
    elif score >= 45:
        label = "Fair"
        if trend == "down":
            message = "Your wellness pulse is trending down slightly this week. Your plan has been reviewed."
        else:
            message = "Your wellness pulse is fair. Your personalized plan can help improve this."
    else:
        label = "Needs Attention"
        message = "Your wellness pulse suggests your body may benefit from extra rest and care this week."

    if trend == "up":
        message += " Trending upward — great momentum."
    elif trend == "down":
        message += " Consider reviewing your daily practices."

    return {"score": score, "trend": trend, "label": label, "message": message}


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def detect_pattern(check_ins: List[Any]) -> Optional[Dict[str, Any]]:
    """
    Detect recurring wellness patterns from check-in history.
    Returns a pattern result dict or None if insufficient data.
    """
    if len(check_ins) < 3:
        return None

    def extract(ci):
        if hasattr(ci, "sleep_score"):
            return {
                "sleep": ci.sleep_score,
                "stress": ci.stress_score,
                "mood": ci.mood_score,
                "digestion": ci.digestion_score,
            }
        return {k: ci[k] for k in ["sleep_score", "stress_score", "mood_score", "digestion_score"]}

    all_data = [extract(ci) for ci in check_ins]
    recent_data = all_data[-5:]  # last 5
    older_data = all_data[:-5] if len(all_data) > 5 else all_data

    def avg(items, key):
        return sum(d.get(key, d.get(key + "_score", 3)) for d in items) / len(items)

    # Compute averages for recent vs older
    r_sleep = avg(recent_data, "sleep")
    r_stress = avg(recent_data, "stress")
    r_mood = avg(recent_data, "mood")
    r_digestion = avg(recent_data, "digestion")

    o_sleep = avg(older_data, "sleep")
    o_stress = avg(older_data, "stress")
    o_mood = avg(older_data, "mood")
    o_digestion = avg(older_data, "digestion")

    patterns_found = []

    # Detect sleep+stress pattern
    if r_sleep < 3.0 and r_stress > 3.2:
        patterns_found.append("sleep_stress")

    # Detect low sleep alone
    elif r_sleep < 2.8 and o_sleep >= r_sleep:
        patterns_found.append("low_sleep")

    # Detect high stress alone
    elif r_stress > 3.5 and o_stress <= r_stress:
        patterns_found.append("high_stress")

    # Detect mood decline
    elif r_mood < 2.8 and r_mood < o_mood - 0.5:
        patterns_found.append("mood_decline")

    # Detect digestion inconsistency
    elif r_digestion < 2.8 or (max(d["digestion"] for d in recent_data) - min(d["digestion"] for d in recent_data)) >= 2:
        patterns_found.append("digestion_inconsistency")

    # Detect improving pattern
    elif r_sleep > o_sleep + 0.3 and r_mood > o_mood + 0.3:
        patterns_found.append("improving")

    # Default stable
    elif not patterns_found:
        patterns_found.append("stable")

    primary_pattern = patterns_found[0] if patterns_found else "stable"

    # Build insight text
    insight_text = _build_insight_text(
        primary_pattern, r_sleep, r_stress, r_mood, r_digestion,
        o_sleep, o_stress, o_mood, o_digestion
    )

    # Adjustment tasks only for actionable patterns
    from app.services.plan_engine import get_adjustment_tasks
    adjustment_tasks_raw = []
    if primary_pattern in ("sleep_stress", "low_sleep", "high_stress", "mood_decline", "digestion_inconsistency"):
        adjustment_tasks_raw = get_adjustment_tasks(primary_pattern)

    adjustment_tasks = [
        {"title": t["title"], "category": t["category"], "duration": t.get("duration", "")}
        for t in adjustment_tasks_raw
    ]

    return {
        "pattern_type": primary_pattern,
        "insight_text": insight_text,
        "adjustment_tasks": adjustment_tasks if adjustment_tasks else None,
        "has_adjustment": bool(adjustment_tasks),
        "averages": {
            "recent": {"sleep": round(r_sleep, 1), "stress": round(r_stress, 1), "mood": round(r_mood, 1), "digestion": round(r_digestion, 1)},
            "previous": {"sleep": round(o_sleep, 1), "stress": round(o_stress, 1), "mood": round(o_mood, 1), "digestion": round(o_digestion, 1)},
        }
    }


def _build_insight_text(
    pattern: str, r_sleep, r_stress, r_mood, r_digestion,
    o_sleep, o_stress, o_mood, o_digestion
) -> str:
    if pattern == "sleep_stress":
        return (
            f"Your recent check-ins show a recurring sleep and stress pattern. "
            f"Recent average sleep: {r_sleep:.1f}/5, stress: {r_stress:.1f}/5 — "
            f"compared to previous average sleep: {o_sleep:.1f}/5, stress: {o_stress:.1f}/5. "
            f"Supporting your sleep and managing stress together can have a compounding positive effect."
        )
    elif pattern == "low_sleep":
        return (
            f"Your recent sleep scores ({r_sleep:.1f}/5 avg) are lower than your previous average ({o_sleep:.1f}/5). "
            f"Consistent, quality sleep is a cornerstone of preventive wellness. "
            f"Your plan has been adjusted to support better sleep onset."
        )
    elif pattern == "high_stress":
        return (
            f"Your recent check-ins show elevated stress ({r_stress:.1f}/5 avg) compared to before ({o_stress:.1f}/5). "
            f"Sustained stress can affect sleep, digestion, and energy. "
            f"Your plan adjustment focuses on calming practices."
        )
    elif pattern == "mood_decline":
        return (
            f"Your mood scores have trended lower recently ({r_mood:.1f}/5 avg, vs previous {o_mood:.1f}/5). "
            f"Your wellness pattern suggests adding some grounding, uplifting practices to your routine. "
            f"If mood difficulties persist, consider reaching out to a qualified professional."
        )
    elif pattern == "digestion_inconsistency":
        return (
            f"Your digestion scores show some inconsistency in recent check-ins ({r_digestion:.1f}/5 avg). "
            f"Digestive wellbeing is central to Ayurvedic preventive health. "
            f"Your adjusted plan includes gentle digestive support practices."
        )
    elif pattern == "improving":
        return (
            f"Your wellness is trending in a positive direction! "
            f"Recent sleep: {r_sleep:.1f}/5 (up from {o_sleep:.1f}/5), mood: {r_mood:.1f}/5. "
            f"Your consistent daily practices are supporting your wellbeing."
        )
    else:
        return (
            f"Your wellness pattern is relatively stable this week. "
            f"Sleep: {r_sleep:.1f}/5, Stress: {r_stress:.1f}/5, Mood: {r_mood:.1f}/5, Digestion: {r_digestion:.1f}/5. "
            f"Continue your current practices to maintain this foundation."
        )


def compute_weekly_averages(check_ins: List[Any]) -> Dict[str, float]:
    """Compute average of each dimension from the last 7 check-ins."""
    recent = check_ins[-7:] if len(check_ins) >= 7 else check_ins
    if not recent:
        return {"sleep": 0.0, "stress": 0.0, "mood": 0.0, "digestion": 0.0}

    def val(ci, key):
        if hasattr(ci, key + "_score"):
            return getattr(ci, key + "_score")
        return ci.get(key + "_score", 3)

    return {
        "sleep": round(sum(val(ci, "sleep") for ci in recent) / len(recent), 1),
        "stress": round(sum(val(ci, "stress") for ci in recent) / len(recent), 1),
        "mood": round(sum(val(ci, "mood") for ci in recent) / len(recent), 1),
        "digestion": round(sum(val(ci, "digestion") for ci in recent) / len(recent), 1),
    }
