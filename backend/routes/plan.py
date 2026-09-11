"""
Plan API Routes for AyuPulse Module 02: AI Personalized Preventive Plan.
"""
from fastapi import APIRouter
from schemas import PlanRequest, PlanResponse, PlanTaskItem

router = APIRouter(prefix="/api/plan", tags=["Module 02 - Preventive Plan"])

DEFAULT_TASKS = {
    "Vata": [
        PlanTaskItem(
            id="task-v1",
            title="Warm Water on Waking",
            category="Dinacharya",
            duration="5 min",
            what="Drink one glass of lukewarm water immediately upon waking, before consuming tea or breakfast.",
            why="Vata constitution tends toward dryness and irregularity. Warm water kindles digestive fire (Agni) and provides gentle grounding hydration.",
            how="Heat water to roughly 40°C. Sip mindfully while seated. Optional: add 2-3 drops of fresh lemon juice.",
            safety="Water should be comfortably warm, never boiling. Consult a doctor for restricted fluid intake conditions."
        ),
        PlanTaskItem(
            id="task-v2",
            title="Nadi Shodhana (Alternate Nostril Breathing)",
            category="Pranayama",
            duration="8 min",
            what="Classical balanced alternate nostril pranayama.",
            why="Directly calms the sympathetic nervous system and grounds the fast, fluctuating movement of Vata.",
            how="Sit comfortably with a straight spine. Close right nostril with thumb, inhale left for 4 counts. Close left, exhale right for 4 counts. Inhale right, exhale left. Repeat 6-10 cycles.",
            safety="Practice on an empty stomach. Never strain or force retention. Stop immediately if lightheaded."
        ),
        PlanTaskItem(
            id="task-v3",
            title="Gentle Grounding Asana",
            category="Yoga",
            duration="15 min",
            what="Slow restorative yoga: Child's Pose (Balasana), Cat-Cow (Marjaryasana-Bitilasana), and Corpse Pose (Shavasana).",
            why="Gentle, slow floor postures anchor excessive Vata mobility and release spinal tension.",
            how="Hold each posture for 5-8 conscious breaths. Keep movements slow, deliberate, and relaxed.",
            safety="Never push into joint pain. Modify postures if you have lower back or knee sensitivity."
        ),
        PlanTaskItem(
            id="task-v4",
            title="Warm, Cooked Evening Meal",
            category="Diet",
            duration="Evening",
            what="Nourishing, warm, freshly prepared meal with mild spices (cumin, ginger, turmeric, ghee).",
            why="Vata is aggravated by cold, raw, or dry foods. Warm, slightly moist meals support assimilation and nighttime grounding.",
            how="Enjoy soups, khichdi, or stewed vegetables with basmati rice at least 2 hours before sleep. Avoid raw salads at night.",
            safety="Personal dietary needs vary. Check with a nutritionist if you have allergies or dietary restrictions."
        ),
        PlanTaskItem(
            id="task-v5",
            title="Consistent Evening Wind-Down",
            category="Lifestyle",
            duration="30 min",
            what="Screen-free transition hour, dim warm lighting, and calm reflection or reading before sleep.",
            why="Irregular sleep deeply destabilizes Vata dosha. An evening anchor stabilizes melatonin production and mental stillness.",
            how="Power down devices by 10:00 PM. Keep bedroom cool and dark. Sip warm nutmeg milk or chamomile tea.",
            safety="Not a treatment for chronic clinical insomnia. Seek medical guidance if sleep disturbance persists."
        )
    ],
    "Pitta": [
        PlanTaskItem(
            id="task-p1",
            title="Cool Water Morning Cleanse",
            category="Dinacharya",
            duration="5 min",
            what="Splash face and eyes with cool water upon waking. Drink room-temperature water.",
            why="Soothes excess internal heat and relieves morning irritability or ocular strain.",
            how="Use fresh cool water. Wash eyelids and wrists. Sip room-temperature water slowly.",
            safety="Avoid ice-cold water if you have sinus congestion."
        ),
        PlanTaskItem(
            id="task-p2",
            title="Sheetali Pranayama (Cooling Breath)",
            category="Pranayama",
            duration="5 min",
            what="Cooling tongue-curling or teeth-breathing pranayama.",
            why="Directly reduces heat in the digestive tract and tempers sharp, frustrated emotional spikes.",
            how="Inhale slowly through curled tongue. Close mouth, exhale gently through nose. 10 rounds.",
            safety="Do not practice in freezing environments or if experiencing acute respiratory chills."
        ),
        PlanTaskItem(
            id="task-p3",
            title="Moderate Non-Competitive Asana",
            category="Yoga",
            duration="20 min",
            what="Heart-opening and cooling twists: Moon Salutations, Seated Twists, Pigeon Pose.",
            why="Releases liver and abdominal tension without generating excessive internal heat.",
            how="Practice at an easy 70% effort. Focus on breath ease rather than pushing for perfection.",
            safety="Avoid hot yoga or vigorous cardio during peak midday heat."
        ),
        PlanTaskItem(
            id="task-p4",
            title="Cooling Midday Nourishment",
            category="Diet",
            duration="Lunch",
            what="Largest meal at noon with cooling foods: leafy greens, cucumber, coconut, ghee, sweet fruits.",
            why="Pitta digestive fire peaks between 11 AM and 1 PM. Feeding it appropriately prevents hyperacidity.",
            how="Eat quietly without screens. Avoid excessively spicy, fermented, or deeply fried foods.",
            safety="Consult your doctor if you have diagnosed GERD or peptic ulcer conditions."
        )
    ],
    "Kapha": [
        PlanTaskItem(
            id="task-k1",
            title="Early Awakening & Surya Namaskar",
            category="Yoga",
            duration="20 min",
            what="Rise before 6:30 AM and practice 6-8 dynamic rounds of Sun Salutations.",
            why="Dispels morning lethargy and heaviness (Tamas) and stimulates sluggish metabolism.",
            how="Move briskly with the breath, generating warmth and light perspiration.",
            safety="Build intensity gradually. Stop if experiencing acute shortness of breath."
        ),
        PlanTaskItem(
            id="task-k2",
            title="Kapalabhati (Skull Shining Breath)",
            category="Pranayama",
            duration="5 min",
            what="Active rhythmic abdominal exhalations with passive inhalations.",
            why="Clears congestion from respiratory channels and activates metabolic fire (Agni).",
            how="Sit tall. Exhale sharply pulling navel in, 1 stroke per second. 3 rounds of 30 strokes.",
            safety="Contraindicated during pregnancy, uncontrolled hypertension, or abdominal surgery."
        ),
        PlanTaskItem(
            id="task-k3",
            title="Light, Warm Spiced Meals",
            category="Diet",
            duration="Day",
            what="Warm, dry, well-spiced meals featuring ginger, black pepper, turmeric, and lentils.",
            why="Counters heavy, slow digestion and helps maintain healthy lipid and metabolic balance.",
            how="Keep breakfast light. Avoid dairy, iced drinks, and heavy desserts in the evening.",
            safety="Do not overly restrict caloric needs. Maintain balanced nutrient diversity."
        ),
        PlanTaskItem(
            id="task-k4",
            title="Brisk Midday Walk in Sunlight",
            category="Lifestyle",
            duration="15 min",
            what="Vigorous walking outdoors in natural daylight.",
            why="Stimulates lymphatic circulation and breaks sedentary midday drowsiness.",
            how="Walk briskly enough to elevate heart rate comfortably. Take deep diaphragmatic breaths.",
            safety="Wear supportive footwear. Adjust pace if you have knee or hip pain."
        )
    ]
}


@router.post("", response_model=PlanResponse)
def get_or_generate_plan(payload: PlanRequest):
    """
    Generates or retrieves a personalized preventive daily plan
    based on the user's assessed dominant dosha.
    """
    dominant = payload.dominant.capitalize() if payload.dominant else "Vata"
    tasks = DEFAULT_TASKS.get(dominant, DEFAULT_TASKS["Vata"])

    return PlanResponse(
        status="success",
        module="plan",
        dominant=dominant,
        tasks=tasks,
        message=f"Generated {len(tasks)} personalized preventive practices tailored for {dominant} constitution."
    )
