"""
Plan Engine — AyuPulse Module 02
Generates a personalized preventive plan based on Dosha result.
"""
from typing import Dict, List, Any
from app.services.safety_engine import validate_plan_task

# ─────────────────────────────────────────────────────────────────────────────
# PRACTICE LIBRARY
# Each practice: title, category, duration, what, why (templates), how, safety
# {dominant} will be replaced with the user's dominant dosha.
# ─────────────────────────────────────────────────────────────────────────────

VATA_PRACTICES = [
    {
        "title": "Warm water on waking",
        "category": "Dinacharya",
        "duration": "5 min",
        "what": "Drink one glass of warm (not hot) water immediately upon waking, before eating or brushing.",
        "why": "Vata constitution tends toward dryness and irregularity. Warm water kindles Agni (digestive fire) and provides gentle grounding moisture at the start of the day.",
        "how": "Heat water to roughly 40–45°C. Sit quietly, sip slowly. Add a few drops of fresh lemon if preferred. Avoid cold or ice water in the morning.",
        "safety": "Use comfortably warm — not boiling — water. If you experience any heartburn, reduce temperature. Not a substitute for medical hydration advice.",
    },
    {
        "title": "Abhyanga — self oil massage",
        "category": "Dinacharya",
        "duration": "10–15 min",
        "what": "A gentle self-massage using warm sesame or almond oil before your morning shower.",
        "why": "Vata is characterized by dryness, lightness, and movement. Warm oil massage deeply grounds and nourishes Vata, calms the nervous system, and improves circulation.",
        "how": "Warm a small amount of sesame or almond oil. Massage in long strokes on limbs and circular strokes on joints. Leave on for 5–10 min, then shower. Aim for 3–5 times per week.",
        "safety": "Avoid if you have open wounds or skin infections. Use unscented, cold-pressed oil. Stop if you develop any skin reaction.",
    },
    {
        "title": "Gentle morning asana",
        "category": "Yoga",
        "duration": "10–15 min",
        "what": "A slow, grounding yoga sequence: Child's Pose, Cat-Cow, Seated Forward Fold, Shavasana.",
        "why": "Vata benefits from slow, steady, grounding movement rather than intense exercise. This sequence calms the nervous system and brings stability without overstimulation.",
        "how": "Move slowly and deliberately. Hold each pose for 5–8 breaths. Focus on the sensation of the floor beneath you. Practice at the same time each morning for best effect.",
        "safety": "Listen to your body — never push into pain. If you have joint concerns, skip poses that cause discomfort. Consult a yoga instructor for proper alignment.",
    },
    {
        "title": "Nadi Shodhana (Alternate Nostril Breathing)",
        "category": "Pranayama",
        "duration": "5–8 min",
        "what": "A classical pranayama practice alternating breath between left and right nostrils.",
        "why": "Nadi Shodhana calms the Vata-driven nervous system, reduces anxiety, and balances the energy channels (nadis). It is one of the most effective practices for Vata imbalance.",
        "how": "Sit comfortably. Use right hand: thumb on right nostril, ring finger on left. Inhale left → close left → exhale right → inhale right → close right → exhale left. Repeat 5–10 cycles. Build to 10 min over time.",
        "safety": "Practice on an empty stomach. Stop if you feel dizzy or breathless. Not recommended during acute respiratory illness.",
    },
    {
        "title": "Warm, regular meals",
        "category": "Diet",
        "duration": "Ongoing",
        "what": "Eat warm, cooked, moist, and mildly spiced meals at consistent times each day.",
        "why": "Vata constitution is weakened by cold, dry, or irregular food. Warm, oily, well-spiced meals support Agni, improve absorption, and counterbalance Vata's tendency toward irregularity.",
        "how": "Aim for meals at the same time daily. Include root vegetables, grains, ghee, warm soups, and cooked greens. Minimize raw salads, cold drinks, and dried/crunchy foods in Vata-dominant states.",
        "safety": "These are general dietary tendencies — individual needs vary. If you have any medical dietary requirements, follow your practitioner's guidance.",
    },
    {
        "title": "Consistent evening wind-down",
        "category": "Lifestyle",
        "duration": "20–30 min",
        "what": "A consistent pre-sleep routine: dim lights, avoid screens, gentle reading or meditation, same bedtime nightly.",
        "why": "Vata's irregular nature is most destabilizing at night. A consistent evening routine deeply supports sleep onset, reduces racing thoughts, and grounds the Vata nervous system.",
        "how": "Start 30 min before target bedtime. Dim all lights. Avoid stimulating content. A warm herbal drink (e.g., golden milk or ashwagandha milk) can support transition to sleep.",
        "safety": "Avoid using sleep aids habitually without guidance. If persistent sleep difficulty continues for more than 2 weeks, consult a qualified practitioner.",
    },
]

PITTA_PRACTICES = [
    {
        "title": "Cool water morning cleanse",
        "category": "Dinacharya",
        "duration": "5 min",
        "what": "Rinse your face and wrists with cool (not cold) water upon waking. Drink a glass of room-temperature water.",
        "why": "Pitta constitution runs warm. A cool morning cleanse immediately tempers excess heat, refreshes the senses, and sets a calmer, less reactive tone for the day.",
        "how": "Use water that feels pleasantly cool — not icy. Splash face gently. Run cool water over inner wrists for 30 seconds. Drink a full glass of water slowly.",
        "safety": "Avoid ice-cold water if you are prone to sinus congestion. Use cool, not cold. If you are in a cold climate, adjust to room temperature.",
    },
    {
        "title": "Sheetali Pranayama (Cooling Breath)",
        "category": "Pranayama",
        "duration": "5–10 min",
        "what": "A cooling pranayama practice: inhale through a curled tongue, exhale through the nose.",
        "why": "Sheetali directly reduces excess Pitta heat, calms aggression and irritability, and soothes the digestive system. It is the classical remedy for Pitta imbalance.",
        "how": "Curl tongue into a tube shape (or use Sitkari — inhale through teeth if tongue curl is not natural). Inhale slowly through the tongue. Close mouth. Exhale slowly through both nostrils. Repeat 10–15 cycles.",
        "safety": "Avoid in cold weather or if you have a cold/flu. Stop if you feel uncomfortable. Not recommended for those with low blood pressure.",
    },
    {
        "title": "Moderate, non-competitive yoga",
        "category": "Yoga",
        "duration": "20–30 min",
        "what": "A balanced yoga practice focusing on cooling, heart-opening postures: Moon Salutation, Seated Twists, Pigeon Pose, Legs-Up-Wall.",
        "why": "Pitta benefits from movement that releases tension and heat without adding competitive intensity. These poses open the chest, cool the body, and discharge built-up pressure.",
        "how": "Practice at a moderate pace, avoiding hot yoga or power classes. Focus on breath and ease rather than achievement. End with a long Shavasana (5+ min).",
        "safety": "Avoid vigorous styles (hot yoga, Bikram) when Pitta is high. Never practice through intense discomfort. Respect your body's signals.",
    },
    {
        "title": "Cool, light midday meal",
        "category": "Diet",
        "duration": "Ongoing",
        "what": "Make lunch your largest meal, choosing cooling, mildly spiced foods: leafy greens, cucumber, sweet fruits, basmati rice, coconut.",
        "why": "Pitta is strongest at midday — this is when its fire supports digestion best. A cooling, nourishing lunch channels this energy productively and prevents acidic buildup.",
        "how": "Avoid very spicy, fried, or fermented foods at lunch. Include bitter and sweet tastes. Eat slowly and calmly — avoid working while eating.",
        "safety": "Individual nutritional needs vary widely. Do not make significant dietary changes if you have a diagnosed condition without consulting your healthcare provider.",
    },
    {
        "title": "Nature walk or cooling movement",
        "category": "Lifestyle",
        "duration": "20–30 min",
        "what": "An easy walk in a cool, natural environment — park, garden, near water — in the early morning or late evening.",
        "why": "Pitta benefits from time in nature, particularly near water or in the shade. This tempers intensity, reduces mental heat, and supports emotional balance.",
        "how": "Walk at a relaxed, non-competitive pace. Leave devices behind or on silent. Notice your environment. Cooler parts of the day are best — avoid peak afternoon heat.",
        "safety": "Protect skin from sun exposure. Stay hydrated. If you have cardiovascular concerns, consult your doctor before new exercise routines.",
    },
    {
        "title": "Evening reflection practice",
        "category": "Lifestyle",
        "duration": "10–15 min",
        "what": "A short journaling or reflective meditation in the evening, releasing the day's intensity.",
        "why": "Pitta's driven nature can carry the day's stress into the night. A brief reflection practice clears mental heat, improves sleep quality, and prevents emotional accumulation.",
        "how": "Write 3–5 sentences about what went well today. Note anything you'd like to approach differently tomorrow. Close with 3 deep breaths.",
        "safety": "Journaling should feel releasing, not stressful. If you feel worse after journaling, switch to a short breathing practice instead.",
    },
]

KAPHA_PRACTICES = [
    {
        "title": "Energizing morning movement",
        "category": "Yoga",
        "duration": "20–30 min",
        "what": "An invigorating yoga or movement practice: Sun Salutations (Surya Namaskar), standing poses, dynamic flows.",
        "why": "Kapha constitution tends toward heaviness, inertia, and slow metabolism. Vigorous morning movement is the most effective way to activate Agni, boost energy, and prevent lethargy.",
        "how": "Start with 5–8 rounds of Sun Salutations. Move briskly, generating warmth. Add standing poses: Warrior I, II, Triangle. Aim for light sweat by the end.",
        "safety": "Build intensity gradually. If you are very sedentary currently, start with 5–10 min and increase over weeks. Stop if you feel chest tightness or shortness of breath.",
    },
    {
        "title": "Kapalabhati (Breath of Fire)",
        "category": "Pranayama",
        "duration": "5–10 min",
        "what": "A dynamic pranayama: rapid, forceful exhalations through the nose with passive inhalations.",
        "why": "Kapalabhati is highly stimulating — it energizes the body, clears Kapha congestion, activates metabolism, and sharpens mental clarity. Ideal for Kapha imbalance.",
        "how": "Sit straight. Take a deep breath. Begin rapid, sharp exhalations through the nose (about 1 per second) — abdomen pumps in sharply. Inhalation is passive. Start with 30 pumps, rest, then 2 more rounds. Build over time.",
        "safety": "Avoid during pregnancy, menstruation, high blood pressure, or hernia. Stop immediately if dizzy or nauseated. Learn from a qualified instructor first.",
    },
    {
        "title": "Dry brushing (Garshana)",
        "category": "Dinacharya",
        "duration": "5–10 min",
        "what": "A traditional Ayurvedic dry massage using a raw silk glove or dry brush before bathing.",
        "why": "Garshana stimulates the lymphatic system, promotes circulation, and moves stagnant Kapha energy. It is one of the most effective Dinacharya practices for Kapha types.",
        "how": "Before showering: brush/massage skin in long strokes toward the heart on limbs, circular on joints. Apply moderate pressure. Follow with a warm shower.",
        "safety": "Avoid on irritated, broken, or sunburned skin. Use a dedicated skin brush or silk glove only. Do not use if you have skin conditions like eczema — consult your practitioner.",
    },
    {
        "title": "Light, warm, spiced meals",
        "category": "Diet",
        "duration": "Ongoing",
        "what": "Favor light, warm, dry, and well-spiced foods: lentil soups, ginger tea, bitter greens, legumes, spices like black pepper, ginger, turmeric.",
        "why": "Kapha is increased by heavy, cold, sweet, or oily foods. Light, warming, stimulating foods and spices counterbalance Kapha sluggishness and support metabolic activation.",
        "how": "Include ginger or black pepper in cooking. Choose smaller, lighter meals. Eat your main meal at midday. Minimize dairy, refined sugar, heavy desserts, and fried foods.",
        "safety": "These are general wellness tendencies. Do not restrict nutrition significantly without guidance from a qualified dietitian, especially if you are underweight or have medical conditions.",
    },
    {
        "title": "Mid-morning active break",
        "category": "Lifestyle",
        "duration": "10–15 min",
        "what": "A brisk 10–15 minute walk or active break mid-morning to prevent the typical Kapha energy dip.",
        "why": "Kapha's sluggishness peaks in the mid-morning (approximately 6–10 AM). An active break at this time counteracts the natural tendency toward inertia and heavy fatigue.",
        "how": "Step outside if possible. Walk briskly — aim to get your heart rate up gently. Or do a short set of jumping jacks, stairs, or any movement you enjoy.",
        "safety": "Adjust intensity to your current fitness level. Stay hydrated. If you have cardiovascular conditions, consult your doctor for appropriate intensity guidance.",
    },
    {
        "title": "Consistent early bedtime",
        "category": "Lifestyle",
        "duration": "Ongoing",
        "what": "Maintain a consistent bedtime — ideally by 10:00 PM — and wake by 6:00 AM.",
        "why": "Oversleeping is a significant Kapha aggravating factor. Consistent, moderate sleep supports energy, lightness, and metabolic balance without adding heaviness.",
        "how": "Set a fixed wake time first — your body will adjust sleep onset naturally. Avoid long afternoon naps. Create a simple wind-down: dim lights, no screens 30 min before bed.",
        "safety": "Adults generally need 7–9 hours of sleep. Do not restrict sleep below 7 hours. If you have persistent sleep concerns, consult a qualified practitioner.",
    },
]

BALANCED_PRACTICES = [
    VATA_PRACTICES[3],   # Nadi Shodhana
    VATA_PRACTICES[0],   # Warm water
    PITTA_PRACTICES[2],  # Moderate yoga
    VATA_PRACTICES[4],   # Regular meals
    VATA_PRACTICES[5],   # Evening wind-down
]

PRACTICE_MAP = {
    "Vata": VATA_PRACTICES,
    "Pitta": PITTA_PRACTICES,
    "Kapha": KAPHA_PRACTICES,
}


def generate_plan(dosha_result: Dict[str, Any], lifestyle_answers: Dict[str, Any] = None) -> List[Dict]:
    """
    Generate a list of 5-6 personalized preventive practices.
    dosha_result: dict with dominant, secondary, vata_pct, pitta_pct, kapha_pct
    lifestyle_answers: optional answer map for further personalization
    """
    dominant = dosha_result.get("dominant", "Vata")
    secondary = dosha_result.get("secondary")

    primary_practices = PRACTICE_MAP.get(dominant, VATA_PRACTICES)[:4]

    # Add 1–2 secondary practices if there's a meaningful secondary dosha
    if secondary and secondary != dominant:
        secondary_practices = PRACTICE_MAP.get(secondary, [])
        # Pick the most impactful one from secondary
        if secondary_practices:
            extra = [p for p in secondary_practices if p not in primary_practices][:2]
            primary_practices = list(primary_practices) + extra

    # Validate each task through the safety layer
    validated = []
    for i, practice in enumerate(primary_practices[:6]):
        task = dict(practice)
        task = validate_plan_task(task)
        task["sort_order"] = i
        validated.append(task)

    return validated


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN-BASED ADJUSTMENT TASKS
# ─────────────────────────────────────────────────────────────────────────────

ADJUSTMENT_TASK_LIBRARY = {
    "sleep_stress": [
        {
            "title": "Consistent evening wind-down",
            "category": "Lifestyle",
            "duration": "20 min",
            "what": "A calming pre-sleep sequence: dim lights, brief journaling, and a cooling breathing exercise.",
            "why": "Your recent check-ins show a recurring sleep and stress pattern. A consistent wind-down routine can interrupt this cycle by preparing the nervous system for rest.",
            "how": "30 min before bed: dim lights, write 3 things you'd like to release from today, then practice 5 minutes of slow 4-7-8 breathing (inhale 4, hold 7, exhale 8).",
            "safety": "If sleep difficulties persist beyond 2–3 weeks, consult a qualified practitioner. These practices are for general wellness only.",
            "is_adjusted": True,
        },
        {
            "title": "Gentle breathing practice",
            "category": "Pranayama",
            "duration": "5–8 min",
            "what": "Slow, extended exhalation breathing practice to calm the stress response.",
            "why": "Prolonged exhalation activates the parasympathetic nervous system, reducing stress hormones and improving sleep quality — both patterns showing in your recent check-ins.",
            "how": "Sit comfortably. Inhale for 4 counts, exhale for 6–8 counts. Repeat for 5–8 minutes. Practice both before sleep and in the morning.",
            "safety": "Stop if you feel dizzy or short of breath. Practice at a pace that feels completely comfortable.",
            "is_adjusted": True,
        },
    ],
    "low_sleep": [
        {
            "title": "Consistent sleep anchor",
            "category": "Lifestyle",
            "duration": "Ongoing",
            "what": "Fix your wake-up time as the same every day, regardless of when you fall asleep.",
            "why": "Your recent sleep scores suggest disrupted sleep patterns. A fixed wake-up time is the most effective way to recalibrate the body's circadian rhythm.",
            "how": "Choose a wake time that works 7 days a week. Stick to it even after a poor night. Within 1–2 weeks, your sleep onset will adjust.",
            "safety": "Acute sleep deprivation can affect safety. If you experience severe or chronic sleep disruption, please consult a qualified healthcare provider.",
            "is_adjusted": True,
        },
    ],
    "high_stress": [
        {
            "title": "Mid-day mindfulness pause",
            "category": "Lifestyle",
            "duration": "5 min",
            "what": "A brief mindful pause at midday: stop all activity, take 10 slow breaths, and observe how you feel.",
            "why": "Your recent check-ins show elevated stress. A brief daily pause interrupts the accumulation of stress before it peaks in the evening.",
            "how": "At midday (12–1 PM): sit away from your screen. Close eyes. Breathe naturally for 10 breaths, noticing each. Note your stress level before and after.",
            "safety": "Mindfulness is a wellness support practice — not a replacement for mental health care. If you are experiencing significant stress or anxiety, please seek professional support.",
            "is_adjusted": True,
        },
    ],
    "mood_decline": [
        {
            "title": "Daily sunlight exposure",
            "category": "Lifestyle",
            "duration": "10–15 min",
            "what": "Spend 10–15 minutes in natural sunlight in the morning.",
            "why": "Your recent mood pattern shows a declining trend. Morning sunlight supports serotonin production, regulates circadian rhythm, and is one of the most reliable natural mood supports.",
            "how": "Step outside within 1 hour of waking. No sunglasses for the first 10 minutes. A simple walk or sitting with your morning tea in the sun both work well.",
            "safety": "Protect skin from prolonged UV exposure. If mood decline is significant or persistent, please connect with a qualified mental health professional.",
            "is_adjusted": True,
        },
    ],
    "digestion_inconsistency": [
        {
            "title": "Ginger tea before meals",
            "category": "Diet",
            "duration": "5 min",
            "what": "Drink a cup of fresh ginger tea 15–30 minutes before your main meals.",
            "why": "Your recent digestion patterns show inconsistency. Ginger is a traditional Ayurvedic digestive support (deepana) that activates Agni and supports regularity.",
            "how": "Grate or slice fresh ginger (1 tsp per cup). Steep in hot water for 5 minutes. Optionally add a few drops of lemon. Sip 15–30 min before eating.",
            "safety": "Avoid if you have acid reflux or are on blood-thinning medication. These are general wellness practices — consult your practitioner for persistent digestive concerns.",
            "is_adjusted": True,
        },
    ],
}


def get_adjustment_tasks(pattern_type: str) -> List[Dict]:
    """Return adjustment tasks for a given pattern type."""
    tasks = ADJUSTMENT_TASK_LIBRARY.get(pattern_type, [])
    return [validate_plan_task(dict(t)) for t in tasks]
