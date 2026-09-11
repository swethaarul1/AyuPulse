"""
Assessment Engine — AyuPulse Module 01
Deterministic scoring model for Vata / Pitta / Kapha tendencies.
"""
from typing import Dict, Any, Tuple, List
from app.services.safety_engine import sanitize_text

# ─────────────────────────────────────────────────────────────────────────────
# QUESTION BANK
# Each question has answer options with (vata, pitta, kapha) weight tuples.
# Weights are relative: higher = stronger tendency toward that dosha.
# ─────────────────────────────────────────────────────────────────────────────

QUESTIONS = [
    # SLEEP
    {
        "id": "sleep_quality",
        "category": "Sleep",
        "text": "How would you describe your sleep quality overall?",
        "options": [
            {"label": "Light, easily disturbed — I wake up often", "weights": (3, 0, 0)},
            {"label": "Moderate — I sleep okay but feel hot or restless", "weights": (0, 2, 1)},
            {"label": "Deep, long — I could sleep all day", "weights": (0, 0, 3)},
            {"label": "Generally restful, 6–8 hours", "weights": (1, 1, 1)},
        ],
    },
    {
        "id": "sleep_timing",
        "category": "Sleep",
        "text": "What best describes your sleep schedule?",
        "options": [
            {"label": "Irregular — I go to bed at different times each night", "weights": (3, 0, 0)},
            {"label": "Late-night owl — I stay up late but sleep soundly", "weights": (0, 2, 1)},
            {"label": "Early to bed, early to rise — very consistent", "weights": (0, 1, 2)},
            {"label": "I try to be consistent but often stay up slightly late", "weights": (1, 2, 0)},
        ],
    },
    {
        "id": "sleep_restlessness",
        "category": "Sleep",
        "text": "Do you experience restlessness at night?",
        "options": [
            {"label": "Yes, racing thoughts keep me awake", "weights": (3, 1, 0)},
            {"label": "Occasionally, usually when I'm stressed or overheated", "weights": (0, 3, 0)},
            {"label": "Rarely — once I'm asleep I'm out", "weights": (0, 0, 3)},
            {"label": "Sometimes mild restlessness", "weights": (1, 1, 1)},
        ],
    },
    # DIGESTION
    {
        "id": "digestion_regularity",
        "category": "Digestion",
        "text": "How regular is your digestion?",
        "options": [
            {"label": "Irregular — sometimes constipated, sometimes fine", "weights": (3, 0, 0)},
            {"label": "Strong and regular, sometimes too fast or loose", "weights": (0, 3, 0)},
            {"label": "Slow and steady — I rarely feel discomfort", "weights": (0, 0, 3)},
            {"label": "Generally regular with occasional variation", "weights": (1, 1, 1)},
        ],
    },
    {
        "id": "digestion_appetite",
        "category": "Digestion",
        "text": "How would you describe your appetite?",
        "options": [
            {"label": "Variable — sometimes very hungry, sometimes not at all", "weights": (3, 0, 0)},
            {"label": "Strong and consistent — I get irritable if I miss meals", "weights": (0, 3, 0)},
            {"label": "Moderate — I can skip meals without much discomfort", "weights": (0, 0, 3)},
            {"label": "Steady, I enjoy meals but adapt easily", "weights": (1, 1, 1)},
        ],
    },
    {
        "id": "digestion_heaviness",
        "category": "Digestion",
        "text": "How do you feel after a heavy meal?",
        "options": [
            {"label": "Bloated, gassy, uneasy", "weights": (3, 0, 0)},
            {"label": "Fine usually, but heartburn if food is too rich or spicy", "weights": (0, 3, 0)},
            {"label": "Sluggish or sleepy", "weights": (0, 0, 3)},
            {"label": "Comfortably full but manageable", "weights": (1, 1, 1)},
        ],
    },
    # STRESS RESPONSE
    {
        "id": "stress_response",
        "category": "Stress",
        "text": "When you feel stressed or overwhelmed, you tend to:",
        "options": [
            {"label": "Worry, overthink, and feel anxious or scattered", "weights": (3, 0, 0)},
            {"label": "Get irritable, intense, or driven to solve problems immediately", "weights": (0, 3, 0)},
            {"label": "Withdraw, slow down, or want to sleep it off", "weights": (0, 0, 3)},
            {"label": "Feel a mix — sometimes anxious, sometimes irritable", "weights": (2, 2, 0)},
        ],
    },
    {
        "id": "stress_physical",
        "category": "Stress",
        "text": "How does your body physically respond to stress?",
        "options": [
            {"label": "Dry mouth, cold hands, difficulty focusing", "weights": (3, 0, 0)},
            {"label": "Sweating, flushing, tension headaches", "weights": (0, 3, 0)},
            {"label": "Weight gain, fatigue, heavy feeling", "weights": (0, 0, 3)},
            {"label": "Mild symptoms — I recover reasonably well", "weights": (1, 1, 1)},
        ],
    },
    # ENERGY PATTERNS
    {
        "id": "energy_pattern",
        "category": "Energy",
        "text": "How would you describe your daily energy?",
        "options": [
            {"label": "Bursts of energy followed by sudden exhaustion", "weights": (3, 0, 0)},
            {"label": "High and sustained — I push until I crash", "weights": (0, 3, 0)},
            {"label": "Steady but low — I prefer a slow, consistent pace", "weights": (0, 0, 3)},
            {"label": "Good in the morning, moderate by evening", "weights": (1, 2, 1)},
        ],
    },
    {
        "id": "energy_afternoon",
        "category": "Energy",
        "text": "Do you experience an afternoon energy dip?",
        "options": [
            {"label": "Yes, major crash — I need a nap or caffeine", "weights": (2, 0, 1)},
            {"label": "Mild dip but I push through with willpower", "weights": (0, 3, 0)},
            {"label": "I feel most sluggish after lunch, heavy and slow", "weights": (0, 0, 3)},
            {"label": "Rarely — my energy is fairly even", "weights": (1, 1, 1)},
        ],
    },
    # BODY TENDENCIES
    {
        "id": "body_warmth",
        "category": "Body",
        "text": "How do you relate to warmth and cold?",
        "options": [
            {"label": "I feel cold easily, prefer warmth", "weights": (3, 0, 0)},
            {"label": "I run warm — I prefer cool environments", "weights": (0, 3, 0)},
            {"label": "I adapt well but tend to feel neutral or slightly cool", "weights": (0, 0, 2)},
            {"label": "I'm comfortable in most temperatures", "weights": (1, 1, 1)},
        ],
    },
    {
        "id": "body_build",
        "category": "Body",
        "text": "Which describes your body tendencies best?",
        "options": [
            {"label": "Naturally lean, difficulty gaining weight", "weights": (3, 0, 0)},
            {"label": "Medium build, moderate weight, athletic", "weights": (0, 3, 0)},
            {"label": "Tendency to gain weight, more solid or rounded build", "weights": (0, 0, 3)},
            {"label": "Variable — depends on my lifestyle", "weights": (1, 1, 1)},
        ],
    },
    {
        "id": "body_skin",
        "category": "Body",
        "text": "How would you describe your skin?",
        "options": [
            {"label": "Dry, rough, or flaky", "weights": (3, 0, 0)},
            {"label": "Sensitive, oily in spots, prone to redness or rashes", "weights": (0, 3, 0)},
            {"label": "Moist, smooth, thick — slow to develop issues", "weights": (0, 0, 3)},
            {"label": "Normal — occasionally dry or oily", "weights": (1, 1, 1)},
        ],
    },
    # LIFESTYLE & GOALS
    {
        "id": "lifestyle_activity",
        "category": "Lifestyle",
        "text": "What best describes your current activity level?",
        "options": [
            {"label": "Sporadic — I go all-in then rest for days", "weights": (3, 0, 0)},
            {"label": "High — I exercise intensely and regularly", "weights": (0, 3, 0)},
            {"label": "Low — I prefer gentle movement and rest", "weights": (0, 0, 3)},
            {"label": "Moderate — I try to stay consistent", "weights": (1, 2, 0)},
        ],
    },
    {
        "id": "lifestyle_food",
        "category": "Lifestyle",
        "text": "What describes your food preferences?",
        "options": [
            {"label": "Warm, moist, grounding foods — soups, stews, root vegetables", "weights": (3, 0, 0)},
            {"label": "Cool, refreshing foods — salads, raw vegetables, cold drinks", "weights": (0, 3, 0)},
            {"label": "Heavy, rich, satisfying meals — I love variety and comfort food", "weights": (0, 0, 3)},
            {"label": "I eat what's convenient or whatever I'm in the mood for", "weights": (1, 1, 1)},
        ],
    },
    {
        "id": "lifestyle_goal",
        "category": "Lifestyle",
        "text": "What is your primary wellness goal right now?",
        "options": [
            {"label": "Better sleep and less anxiety", "weights": (3, 0, 0)},
            {"label": "Manage stress and stay focused", "weights": (0, 3, 0)},
            {"label": "More energy and motivation", "weights": (0, 0, 3)},
            {"label": "Overall balance and prevention", "weights": (1, 1, 1)},
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SCORING ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def score_assessment(answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic Vata/Pitta/Kapha scoring.
    answers: {question_id: option_index (0-based)}
    Returns complete scoring result dict.
    """
    vata, pitta, kapha = 0.0, 0.0, 0.0
    category_contributions: Dict[str, List[str]] = {}

    question_map = {q["id"]: q for q in QUESTIONS}

    for q_id, answer_idx in answers.items():
        question = question_map.get(q_id)
        if not question:
            continue
        try:
            idx = int(answer_idx)
            if idx < 0 or idx >= len(question["options"]):
                continue
            option = question["options"][idx]
            w_v, w_p, w_k = option["weights"]
            vata += w_v
            pitta += w_p
            kapha += w_k

            cat = question["category"]
            dominant_in_q = _dominant_for_weights(w_v, w_p, w_k)
            if dominant_in_q and dominant_in_q != "balanced":
                if cat not in category_contributions:
                    category_contributions[cat] = []
                category_contributions[cat].append(dominant_in_q)
        except (ValueError, TypeError, IndexError):
            continue

    total = vata + pitta + kapha
    if total == 0:
        total = 1  # prevent division by zero

    vata_pct = round((vata / total) * 100, 1)
    pitta_pct = round((pitta / total) * 100, 1)
    kapha_pct = round((kapha / total) * 100, 1)

    # Determine dominant + secondary
    scores = {"Vata": vata, "Pitta": pitta, "Kapha": kapha}
    sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dominant = sorted_doshas[0][0]
    secondary_name = sorted_doshas[1][0]
    secondary_score = sorted_doshas[1][1]

    # Confidence: how far ahead is the dominant vs secondary
    if total > 0:
        confidence = round(min(1.0, (sorted_doshas[0][1] - secondary_score) / total + 0.5), 2)
    else:
        confidence = 0.5

    # Show secondary only if it's meaningfully present
    secondary = secondary_name if (secondary_score / total) > 0.28 else None

    # Build reasoning points from category contributions
    reasoning_points = _build_reasoning(category_contributions, dominant)

    # Build explanation
    explanation = _build_explanation(dominant, secondary, vata_pct, pitta_pct, kapha_pct)

    return {
        "vata_score": round(vata, 1),
        "pitta_score": round(pitta, 1),
        "kapha_score": round(kapha, 1),
        "vata_pct": vata_pct,
        "pitta_pct": pitta_pct,
        "kapha_pct": kapha_pct,
        "dominant": dominant,
        "secondary": secondary,
        "confidence": confidence,
        "explanation": explanation,
        "reasoning_points": reasoning_points,
    }


def _dominant_for_weights(v, p, k) -> str:
    max_w = max(v, p, k)
    if max_w == 0:
        return "balanced"
    if v == p == k:
        return "balanced"
    if v == max_w:
        return "Vata"
    if p == max_w:
        return "Pitta"
    return "Kapha"


def _build_reasoning(contributions: Dict[str, List[str]], dominant: str) -> List[str]:
    points = []
    category_labels = {
        "Sleep": "sleep patterns",
        "Digestion": "digestion patterns",
        "Stress": "stress response",
        "Energy": "energy rhythm",
        "Body": "body tendencies",
        "Lifestyle": "lifestyle choices",
    }
    for cat, doshas in contributions.items():
        cat_label = category_labels.get(cat, cat.lower())
        dosha_counts = {}
        for d in doshas:
            dosha_counts[d] = dosha_counts.get(d, 0) + 1
        if dosha_counts:
            primary = max(dosha_counts, key=dosha_counts.get)
            if primary == dominant:
                points.append(f"Your {cat_label} contributed to the {primary} tendency.")
            else:
                points.append(f"Your {cat_label} showed some {primary} characteristics.")
    return points[:5]  # limit to 5


def _build_explanation(dominant: str, secondary, vata_pct, pitta_pct, kapha_pct) -> str:
    desc = {
        "Vata": "movement, creativity, and change",
        "Pitta": "focus, transformation, and warmth",
        "Kapha": "stability, strength, and nourishment",
    }
    base = (
        f"Your responses reflect a stronger {dominant} tendency — associated with "
        f"{desc.get(dominant, dominant)}."
    )
    if secondary:
        base += (
            f" You also show meaningful {secondary} characteristics, suggesting a "
            f"{dominant}-{secondary} constitution."
        )
    base += (
        " This result reflects patterns in your sleep, energy, digestion, "
        "and lifestyle responses as shared in the assessment."
    )
    return sanitize_text(base)


def get_questions() -> list:
    """Return the question bank for the frontend."""
    return [
        {
            "id": q["id"],
            "category": q["category"],
            "text": q["text"],
            "options": [{"label": o["label"]} for o in q["options"]],
        }
        for q in QUESTIONS
    ]
