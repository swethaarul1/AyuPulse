"""
Pattern Insight and Wellness Score Engine for AyuPulse Module 03.
Computes deterministic 0-100 Wellness Scores from daily check-ins,
analyzes multi-day history to detect recurring patterns, and recommends next steps.
"""
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")


SESSION_CHECKINS: List[Dict[str, Any]] = []


def record_session_checkin(entry: Dict[str, Any]):
    """Records a new live user check-in in memory for immediate history and pattern reflection."""
    SESSION_CHECKINS.append(entry)


def load_history() -> List[Dict[str, Any]]:
    """Loads check-in history from data/history.json merged with any live session check-ins."""
    base = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                base = json.load(f)
        except Exception:
            base = []
    return base + SESSION_CHECKINS


def calculate_checkin_wellness_score(
    sleep: int,
    stress: int,
    mood: int,
    digestion: int,
    energy: int = 3
) -> Dict[str, Any]:
    """
    Computes a deterministic 0-100 Wellness Score for a single check-in across 5 dimensions.
    Sleep (1-5), Stress (1-5, inverted), Mood (1-5), Digestion (1-5), Energy (1-5).
    """
    # Invert stress so 1 (minimal stress) -> 5 points, 5 (extreme stress) -> 1 point
    inverted_stress = 6 - stress

    # Dimensions weighted equally (each 1-5 scale)
    total_pts = sleep + inverted_stress + mood + digestion + energy  # 5 to 25
    wellness_score = int(round(((total_pts - 5) / 20.0) * 100))  # Normalize 5-25 -> 0-100
    wellness_score = max(0, min(100, wellness_score))

    if wellness_score >= 75:
        summary = "Your daily wellness pulse is strong and revitalized today. Key markers reflect balanced vitality."
    elif wellness_score >= 55:
        summary = "Your daily wellness pulse is moderate today. Mindful hydration and consistent evening rest will support you."
    else:
        summary = "Your daily wellness pulse indicates heightened fatigue or stress today. Gentle restorative practices are advised."

    return {
        "wellness_score": wellness_score,
        "summary": summary
    }


def compute_wellness_pulse(checkins: List[Dict[str, Any]]) -> int:
    """Computes aggregate 0-100 wellness pulse from the last 7 check-ins."""
    if not checkins:
        return 72

    recent = checkins[-7:]
    scores = []
    for c in recent:
        s = c.get("sleep_score") or c.get("sleep") or 3
        st = c.get("stress_score") or c.get("stress") or 3
        m = c.get("mood_score") or c.get("mood") or 3
        d = c.get("digestion_score") or c.get("digestion") or 3
        e = c.get("energy_score") or c.get("energy") or 3
        calc = calculate_checkin_wellness_score(s, st, m, d, e)
        scores.append(calc["wellness_score"])

    return int(round(sum(scores) / len(scores)))


def analyze_history_patterns(checkins: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Analyzes check-in history to detect recurring self-reported patterns,
    computes current wellness pulse, and provides actionable preventive next steps.
    """
    if checkins is None or len(checkins) == 0:
        checkins = load_history()

    pulse = compute_wellness_pulse(checkins)

    if not checkins or len(checkins) < 3:
        return {
            "wellness_pulse": pulse,
            "detected_pattern": "baseline_establishing",
            "insight": "Initial check-in baseline established. Continue daily check-ins to track trends.",
            "patterns": [
                {
                    "type": "baseline_establishing",
                    "title": "Establishing Personal Baseline",
                    "description": "Continue logging 30-second check-ins to build your wellness trend graph.",
                    "strength": "mild"
                }
            ],
            "next_step": "Complete 3 consecutive daily check-ins to unlock multi-day pattern detection.",
            "plan_adjusted": False,
            "adjustment_tasks": [],
            "data_status": "Prototype seeded history"
        }

    recent = checkins[-5:]
    prior = checkins[:-5] if len(checkins) > 5 else checkins

    def get_avg(lst, keys):
        vals = []
        for item in lst:
            for k in keys:
                if k in item and item[k] is not None:
                    vals.append(item[k])
                    break
            else:
                vals.append(3)
        return sum(vals) / len(vals)

    recent_sleep = get_avg(recent, ["sleep_score", "sleep"])
    recent_stress = get_avg(recent, ["stress_score", "stress"])
    recent_mood = get_avg(recent, ["mood_score", "mood"])
    recent_digestion = get_avg(recent, ["digestion_score", "digestion"])
    recent_energy = get_avg(recent, ["energy_score", "energy"])

    prior_sleep = get_avg(prior, ["sleep_score", "sleep"])
    prior_stress = get_avg(prior, ["stress_score", "stress"])

    patterns: List[Dict[str, Any]] = []
    plan_adjusted = False
    adjustment_tasks: List[str] = []
    detected_pattern = "balanced_steady"
    insight = "Your recent check-ins show balanced sleep, energy, and stress rhythms."
    next_step = "Continue your regular Dinacharya and hydration habits."

    # 1. Pattern: Poor sleep + high stress
    if recent_sleep <= 2.8 and recent_stress >= 3.6:
        detected_pattern = "sleep_stress"
        insight = (
            f"Your recent check-ins show a recurring sleep and stress pattern. "
            f"Recent average sleep is {recent_sleep:.1f}/5 with elevated stress at {recent_stress:.1f}/5. "
            "A structured evening wind-down routine can help calm the nervous system."
        )
        patterns.append({
            "type": "sleep_stress",
            "title": "Sleep and Stress Correlation",
            "description": f"Lower sleep quality ({recent_sleep:.1f}/5) frequently pairs with elevated daytime stress ({recent_stress:.1f}/5).",
            "strength": "strong"
        })
        next_step = "Begin a 20-minute screen-free evening wind-down with 5 minutes of gentle alternate nostril breathing."
        plan_adjusted = True
        adjustment_tasks = [
            "Consistent evening wind-down (dim lights, no screens 30 min before bed)",
            "Gentle Nadi Shodhana (5-8 min alternate nostril breathing before sleep)",
            "Warm chamomile or nutmeg milk before sleep"
        ]

    # 2. Pattern: Low energy + poor sleep
    elif recent_energy <= 2.5 and recent_sleep <= 2.8:
        detected_pattern = "low_energy_sleep"
        insight = (
            f"Recent check-ins show low daily energy ({recent_energy:.1f}/5) linked to disrupted sleep ({recent_sleep:.1f}/5). "
            "Prioritizing restorative sleep onset will naturally elevate daytime stamina."
        )
        patterns.append({
            "type": "low_energy_sleep",
            "title": "Sleep-Dependent Energy Dip",
            "description": "Daytime vitality is dipping following restless or shortened sleep windows.",
            "strength": "moderate"
        })
        next_step = "Establish a fixed morning wake-up anchor and avoid heavy evening meals."
        plan_adjusted = True
        adjustment_tasks = [
            "Fixed morning wake-up time (Brahma Muhurta or before 7 AM)",
            "Warm ginger tea at midday to sustain natural digestive fire"
        ]

    # 3. Pattern: Repeated low mood
    elif recent_mood <= 2.5:
        detected_pattern = "repeated_low_mood"
        insight = (
            f"Recent mood ratings have averaged {recent_mood:.1f}/5. "
            "Gentle morning sunlight, nature walks, and uplifting breathwork can gently support emotional buoyancy."
        )
        patterns.append({
            "type": "repeated_low_mood",
            "title": "Sustained Mood Dip",
            "description": "Emotional buoyancy has dipped below baseline across multiple consecutive check-ins.",
            "strength": "moderate"
        })
        next_step = "Spend 15 minutes outdoors in morning daylight and practice mindful gratitude journaling."
        plan_adjusted = True
        adjustment_tasks = [
            "15-minute morning outdoor walk in natural sunlight",
            "Bhramari pranayama (humming bee breath) for emotional balance"
        ]

    # 4. Pattern: Digestion discomfort
    elif recent_digestion <= 2.6:
        detected_pattern = "digestion_discomfort"
        insight = (
            f"Digestion regularity has averaged {recent_digestion:.1f}/5 recently. "
            "Kindling digestive fire (Agni) with warm fluids and timely meals is recommended."
        )
        patterns.append({
            "type": "digestion_discomfort",
            "title": "Digestive Irregularity Pattern",
            "description": "Self-reported digestion shows recurring sluggishness or post-meal heaviness.",
            "strength": "moderate"
        })
        next_step = "Sip warm ginger-cumin water 15 minutes before lunch and dinner."
        plan_adjusted = True
        adjustment_tasks = [
            "Warm ginger-cumin infusion before main meals",
            "Avoid chilled beverages and raw salads at dinner"
        ]

    # 5. Pattern: Improving or declining wellness trend
    else:
        recent_calc = calculate_checkin_wellness_score(int(recent_sleep), int(recent_stress), int(recent_mood), int(recent_digestion), int(recent_energy))
        prior_calc = calculate_checkin_wellness_score(int(prior_sleep), int(prior_stress), 3, 3, 3)
        diff = recent_calc["wellness_score"] - prior_calc["wellness_score"]

        if diff >= 8:
            detected_pattern = "improving_wellness"
            insight = (
                f"Your wellness pulse is trending upward (+{diff} points). "
                "Your consistent preventive routines are supporting stability and vitality."
            )
            patterns.append({
                "type": "improving_wellness",
                "title": "Upward Wellness Trajectory",
                "description": "Consistent self-care habits are producing measurable improvements in energy and sleep.",
                "strength": "moderate"
            })
            next_step = "Maintain your current daily routine to sustain this positive momentum."
        elif diff <= -8:
            detected_pattern = "declining_wellness"
            insight = (
                f"Your wellness pulse has softened by {abs(diff)} points across recent check-ins. "
                "Consider reviewing your daily rest rhythm and scaling back overexertion."
            )
            patterns.append({
                "type": "declining_wellness",
                "title": "Mild Downward Trend",
                "description": "Accumulating fatigue or stress has temporarily reduced overall wellness vitality.",
                "strength": "mild"
            })
            next_step = "Dedicate tonight to an early bedtime and restorative warm foot massage."
            plan_adjusted = True
            adjustment_tasks = [
                "Early bedtime (lights out by 10:15 PM)",
                "Gentle restorative yoga before sleep"
            ]
        else:
            detected_pattern = "balanced_steady"
            insight = f"Your wellness pulse is steady at {pulse}/100 with consistent baseline markers."
            patterns.append({
                "type": "balanced_steady",
                "title": "Steady Baseline Balance",
                "description": "All self-reported markers remain stable and in equilibrium.",
                "strength": "moderate"
            })
            next_step = "Keep up with your regular daily hydration and morning movement."

    return {
        "wellness_pulse": pulse,
        "detected_pattern": detected_pattern,
        "insight": insight,
        "patterns": patterns,
        "next_step": next_step,
        "plan_adjusted": plan_adjusted,
        "adjustment_tasks": adjustment_tasks,
        "data_status": "Prototype seeded history"
    }
