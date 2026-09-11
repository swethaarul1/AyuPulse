"""
Deterministic Scoring Engine for AyuPulse Module 01.
Applies weighted rules to questionnaire inputs, computes raw Vata/Pitta/Kapha scores,
normalizes them to percentages that total 100, and determines the dominant tendency.
"""
from typing import Dict, Any, Tuple
from schemas import AssessmentRequest


# Weights mapping for questionnaire domain values: (Vata, Pitta, Kapha)
ANSWER_WEIGHTS: Dict[str, Dict[str, Tuple[int, int, int]]] = {
    "sleep": {
        "light_restless": (3, 0, 0),
        "light": (3, 0, 0),
        "racing_mind": (3, 1, 0),
        "irregular": (3, 0, 0),
        "moderate_sound": (0, 3, 0),
        "hot_restless": (0, 3, 0),
        "moderate": (0, 2, 1),
        "deep_heavy": (0, 0, 3),
        "oversleeping": (0, 0, 3),
        "deep": (0, 0, 3),
        "balanced": (1, 1, 1),
    },
    "digestion": {
        "irregular_variable": (3, 0, 0),
        "irregular": (3, 0, 0),
        "bloating": (3, 0, 0),
        "variable_appetite": (3, 0, 0),
        "sharp_fast": (0, 3, 0),
        "acidic": (0, 3, 0),
        "strong_hunger": (0, 3, 0),
        "heartburn": (0, 3, 0),
        "slow_steady": (0, 0, 3),
        "sluggish": (0, 0, 3),
        "heavy_after_meals": (0, 0, 3),
        "balanced": (1, 1, 1),
    },
    "stress_response": {
        "anxious_worry": (3, 0, 0),
        "anxiety": (3, 0, 0),
        "overthinking": (3, 0, 0),
        "scattered": (3, 0, 0),
        "irritable_intense": (0, 3, 0),
        "irritability": (0, 3, 0),
        "anger": (0, 3, 0),
        "frustration": (0, 3, 0),
        "withdrawn_slow": (0, 0, 3),
        "withdrawn": (0, 0, 3),
        "stubborn": (0, 0, 3),
        "lethargy": (0, 0, 3),
        "calm": (1, 1, 1),
    },
    "energy": {
        "variable_bursts": (3, 0, 0),
        "erratic": (3, 0, 0),
        "quick_exhaustion": (3, 0, 0),
        "afternoon_crash": (2, 1, 0),
        "high_sustained": (0, 3, 0),
        "driven": (0, 3, 0),
        "push_through": (0, 3, 0),
        "steady_calm": (0, 0, 3),
        "slow_starter": (0, 0, 3),
        "consistent_low": (0, 0, 3),
        "balanced": (1, 1, 1),
    },
    "body_tendencies": {
        "dry_cold_slender": (3, 0, 0),
        "cold_hands": (3, 0, 0),
        "dry_skin": (3, 0, 0),
        "slender_lean": (3, 0, 0),
        "warm_medium_athletic": (0, 3, 0),
        "warm": (0, 3, 0),
        "sensitive_skin": (0, 3, 0),
        "athletic_medium": (0, 3, 0),
        "cool_solid_heavy": (0, 0, 3),
        "solid_frame": (0, 0, 3),
        "smooth_oily_skin": (0, 0, 3),
        "heavier_build": (0, 0, 3),
        "balanced": (1, 1, 1),
    },
    "lifestyle": {
        "irregular_active": (3, 0, 0),
        "frequent_travel": (3, 0, 0),
        "sporadic": (3, 0, 0),
        "competitive_demanding": (0, 3, 0),
        "intense_workout": (0, 3, 0),
        "goal_driven": (0, 3, 0),
        "routine_sedentary": (0, 0, 3),
        "slow_relaxed": (0, 0, 3),
        "calm_routine": (0, 0, 3),
        "balanced": (1, 1, 1),
    }
}


def calculate_dosha_scores(request: AssessmentRequest) -> Dict[str, Any]:
    """
    Computes deterministic Vata, Pitta, and Kapha percentages.
    Normalizes so that vata + pitta + kapha == 100.
    Identifies the dominant dosha.
    """
    v_raw, p_raw, k_raw = 0, 0, 0

    # 1. Process explicit domain fields
    domain_fields = {
        "sleep": request.sleep,
        "digestion": request.digestion,
        "stress_response": request.stress_response,
        "energy": request.energy,
        "body_tendencies": request.body_tendencies,
        "lifestyle": request.lifestyle,
    }

    for domain, val in domain_fields.items():
        if val:
            val_clean = str(val).lower().strip().replace(" ", "_")
            weights_map = ANSWER_WEIGHTS.get(domain, {})
            # Look up directly or check partial match
            if val_clean in weights_map:
                w_v, w_p, w_k = weights_map[val_clean]
            else:
                w_v, w_p, w_k = _find_best_match(val_clean, weights_map)
            v_raw += w_v
            p_raw += w_p
            k_raw += w_k

    # 2. Process flexible answers dictionary if provided
    if request.answers:
        for q_key, q_val in request.answers.items():
            val_clean = str(q_val).lower().strip().replace(" ", "_")
            # If answer is integer choice or text
            found = False
            for weights_map in ANSWER_WEIGHTS.values():
                if val_clean in weights_map:
                    w_v, w_p, w_k = weights_map[val_clean]
                    v_raw += w_v
                    p_raw += w_p
                    k_raw += w_k
                    found = True
                    break
            if not found:
                # Text keywords
                if any(w in val_clean for w in ["vata", "wind", "light", "dry", "cold", "irregular", "worry"]):
                    v_raw += 2
                elif any(w in val_clean for w in ["pitta", "fire", "heat", "warm", "sharp", "anger", "intense"]):
                    p_raw += 2
                elif any(w in val_clean for w in ["kapha", "earth", "water", "heavy", "slow", "sluggish", "steady"]):
                    k_raw += 2

    # 3. Consider wellness goals as subtle weights
    if request.wellness_goals:
        for goal in request.wellness_goals:
            g_lower = goal.lower()
            if any(w in g_lower for w in ["sleep", "anxiety", "grounding", "wind-down"]):
                v_raw += 1
            if any(w in g_lower for w in ["stress", "anger", "cooling", "burnout"]):
                p_raw += 1
            if any(w in g_lower for w in ["energy", "weight", "metabolism", "sluggish"]):
                k_raw += 1

    # Ensure non-zero
    total = v_raw + p_raw + k_raw
    if total == 0:
        # Default baseline if empty
        v_raw, p_raw, k_raw = 4, 3, 3
        total = 10

    # 4. Normalize to integer percentages summing to 100
    v_pct = round((v_raw / total) * 100)
    p_pct = round((p_raw / total) * 100)
    k_pct = 100 - (v_pct + p_pct)  # Guarantees exact 100 total

    # Safety clamp
    if k_pct < 0:
        k_pct = 0
        diff = 100 - (v_pct + p_pct)
        if v_pct > p_pct:
            v_pct += diff
        else:
            p_pct += diff

    # 5. Determine dominant tendency
    scores = {"Vata": v_pct, "Pitta": p_pct, "Kapha": k_pct}
    dominant = max(scores, key=scores.get)

    return {
        "vata": int(v_pct),
        "pitta": int(p_pct),
        "kapha": int(k_pct),
        "dominant": dominant
    }


def _find_best_match(val: str, weights_map: Dict[str, Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """Finds closest match by keyword or returns default balanced score."""
    for key, weights in weights_map.items():
        if key in val or val in key:
            return weights
    if "vata" in val or "light" in val or "dry" in val or "restless" in val or "anxious" in val:
        return (3, 0, 0)
    if "pitta" in val or "warm" in val or "hot" in val or "sharp" in val or "irritable" in val:
        return (0, 3, 0)
    if "kapha" in val or "heavy" in val or "slow" in val or "deep" in val or "sluggish" in val:
        return (0, 0, 3)
    return (1, 1, 1)
