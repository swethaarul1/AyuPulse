"""
Claude Service for AyuPulse.
Interprets deterministic assessment scores, personalizes preventive plans,
and generates human-readable pattern insights.
Provides robust JSON parsing and comprehensive deterministic fallbacks.
"""
import os
import json
import re
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

from prompts.prakriti_prompt import SYSTEM_PROMPT, build_prakriti_prompt
from services.safety import sanitize_wellness_text, inspect_safety_gate

logger = logging.getLogger("ayupulse.claude")


class ClaudeService:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        self.client = None
        if self.api_key and self.api_key != "your_api_key_here":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
                logger.info("Anthropic Claude client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {e}")
                self.client = None
        else:
            logger.info("ANTHROPIC_API_KEY not provided. Running in deterministic fallback mode.")

    # ── MODULE 01: ASSESSMENT INTERPRETATION ──────────────────────────────────
    def interpret_prakriti(
        self,
        vata: int,
        pitta: int,
        kapha: int,
        dominant: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Calls Claude or fallback to interpret the calculated Dosha percentages."""
        if self.client:
            try:
                user_content = build_prakriti_prompt(vata, pitta, kapha, dominant, context)
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=600,
                    temperature=0.2,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": "user", "content": user_content}
                    ]
                )

                text_response = "".join(
                    block.text for block in response.content if hasattr(block, "text")
                )
                parsed = self._extract_json(text_response)
                if parsed and "summary" in parsed and "wellness_focus" in parsed:
                    parsed["summary"] = sanitize_wellness_text(parsed["summary"])
                    parsed["wellness_focus"] = [sanitize_wellness_text(f) for f in parsed["wellness_focus"]]
                    parsed["dominant"] = dominant
                    parsed["note"] = "This is a traditional wellness-oriented interpretation, not a medical diagnosis."
                    return parsed
            except Exception as ex:
                logger.error(f"Claude API call failed: {ex}. Using fallback.")

        return self._generate_fallback_assessment(vata, pitta, kapha, dominant, context)

    # ── MODULE 02: PERSONALIZED PREVENTIVE PLAN ───────────────────────────────
    def generate_personalized_plan(
        self,
        dominant: str,
        vata: Optional[int] = None,
        pitta: Optional[int] = None,
        kapha: Optional[int] = None,
        lifestyle: Optional[str] = None,
        wellness_goals: Optional[List[str]] = None,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates a personalized 4-section plan + 4-6 daily tracker tasks
        based on the user's specific constitution and goals.
        """
        dominant_clean = dominant.capitalize() if dominant else "Vata"

        # Try Claude if available
        if self.client:
            try:
                prompt = (
                    f"User Dosha: {dominant_clean} (Vata: {vata}%, Pitta: {pitta}%, Kapha: {kapha}%)\n"
                    f"Lifestyle: {lifestyle or 'Standard daily schedule'}\n"
                    f"Goals: {', '.join(wellness_goals) if wellness_goals else 'General preventive wellness'}\n\n"
                    "Generate a 4-section AYUSH preventive wellness plan in JSON with sections:\n"
                    "1. dinacharya (list of 1-2 items)\n"
                    "2. yoga (list of 1-2 items)\n"
                    "3. pranayama (list of 1 item)\n"
                    "4. diet_lifestyle (list of 1-2 items)\n"
                    "Each item MUST have: title, what, why, how, safety.\n"
                    "Also include 'daily_tracker' list of 4-6 items with: id, title, description, category, duration, completed: false.\n"
                    "Strict safety: no diagnostic claims or treatment promises. Return JSON only."
                )
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1200,
                    temperature=0.3,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": prompt}]
                )
                text_response = "".join(
                    block.text for block in response.content if hasattr(block, "text")
                )
                parsed = self._extract_json(text_response)
                if parsed and "sections" in parsed and "daily_tracker" in parsed:
                    # Sanitize through safety gate
                    return self._sanitize_plan_dict(parsed, dominant_clean)
            except Exception as ex:
                logger.error(f"Claude plan generation failed: {ex}. Using deterministic personalized fallback.")

        # Fallback personalized plan
        return self._generate_fallback_plan(
            dominant=dominant_clean,
            vata=vata,
            pitta=pitta,
            kapha=kapha,
            lifestyle=lifestyle,
            wellness_goals=wellness_goals
        )

    # ── DETERMINISTIC PERSONALIZED PLAN GENERATION ────────────────────────────
    def _generate_fallback_plan(
        self,
        dominant: str,
        vata: Optional[int],
        pitta: Optional[int],
        kapha: Optional[int],
        lifestyle: Optional[str],
        wellness_goals: Optional[List[str]]
    ) -> Dict[str, Any]:
        """
        Assembles a deeply tailored AYUSH routine based on dominant constitution
        AND specific wellness goals (sleep, stress, digestion, energy).
        """
        goals_lower = " ".join([g.lower() for g in (wellness_goals or [])])
        is_sleep_focus = any(w in goals_lower for w in ["sleep", "insomnia", "rest", "night"])
        is_stress_focus = any(w in goals_lower for w in ["stress", "anxiety", "burnout", "calm", "relax"])
        is_energy_focus = any(w in goals_lower for w in ["energy", "fatigue", "activity", "vitality", "stamina"])
        is_digestion_focus = any(w in goals_lower for w in ["digestion", "bloating", "gut", "metabolism", "appetite"])

        dinacharya: List[Dict[str, str]] = []
        yoga: List[Dict[str, str]] = []
        pranayama: List[Dict[str, str]] = []
        diet_lifestyle: List[Dict[str, str]] = []
        daily_tracker: List[Dict[str, Any]] = []

        # ── VATA ORIENTED ───────────────────────────────────────────────────
        if dominant == "Vata":
            if is_sleep_focus:
                dinacharya.append({
                    "title": "Padabhyanga (Warm Foot Oil Massage)",
                    "what": "Gently massage the soles of your feet with warm sesame or brahmi oil before sleep.",
                    "why": "Vata's excessive movement and coldness pool in the nervous system; grounding the feet reflexively induces deep parasympathetic sleep.",
                    "how": "Warm 1 tsp oil in palms, massage foot arches and toes for 3-5 minutes, wipe excess, and wear cotton socks.",
                    "safety": "Be cautious of slipping on uncarpeted floors. Do not perform if you have active foot skin lesions."
                })
            else:
                dinacharya.append({
                    "title": "Ushapan (Warm Water on Waking)",
                    "what": "Drink one large mug of lukewarm water immediately upon waking, before consuming tea or breakfast.",
                    "why": "Vata constitution is naturally dry and cold; warm hydration grounds the nervous system and kindles morning peristalsis.",
                    "how": "Warm filtered water to roughly 40°C. Sit calmly and sip slowly over 3-5 minutes. Optional: 2 drops lemon juice.",
                    "safety": "Water should feel pleasantly warm, never scalding. Adjust volume if under medical fluid restriction."
                })

            yoga.append({
                "title": "Gentle Grounding Asana Sequence",
                "what": "Slow restorative yoga sequence: Balasana (Child's Pose), Marjaryasana (Cat-Cow), and extended Shavasana.",
                "why": "Slow, sustained floor postures calm erratic Vata circulation and discharge muscular tension from the lower back and hips.",
                "how": "Practice at a steady, meditative pace. Hold each posture for 6-8 deep abdominal breaths, finishing with 5 min Shavasana.",
                "safety": "Never force knee flexion in Child's Pose; place a folded blanket between thighs and calves if needed."
            })

            pranayama.append({
                "title": "Nadi Shodhana (Alternate Nostril Breathing)",
                "what": "Rhythmic alternate nostril pranayama with equal inhalation and exhalation counts.",
                "why": "Harmonizes the autonomic nervous system, quiets racing thoughts, and stabilizes fluctuating Vata mental energy.",
                "how": "Sit with an erect spine. Close right nostril, inhale left 4 counts. Close left, exhale right 4 counts. Inhale right, exhale left. 8 cycles.",
                "safety": "Practice on an empty stomach. Never force retention or strain. Cease immediately if feeling lightheaded."
            })

            if is_sleep_focus:
                diet_lifestyle.append({
                    "title": "Golden Nutmeg Milk & Screen Wind-Down",
                    "what": "Warm spiced almond or dairy milk with a pinch of nutmeg and turmeric 45 minutes before sleep.",
                    "why": "Nutmeg is traditionally known in Ayurveda as a natural mild sedative (Nidrajanana) that anchors hyperactive Vata.",
                    "how": "Warm 1 cup milk with a pinch of nutmeg, cardamom, and turmeric. Turn off screens 30 minutes before bedtime.",
                    "safety": "Use only a small culinary pinch of nutmeg. Consult your physician if taking prescription sleep medications."
                })
            else:
                diet_lifestyle.append({
                    "title": "Nourishing Cooked Warm Meals",
                    "what": "Warm, mildly spiced, cooked meals rich in healthy fats (ghee, olive oil) and root vegetables.",
                    "why": "Cold and dry foods aggravate Vata digestive irregularity; warm, soupy meals provide sustaining nourishment.",
                    "how": "Eat lunch and dinner at consistent hours. Favor khichdi, stewed greens, and grains. Avoid raw salads in the evening.",
                    "safety": "Ensure meal choices comply with any existing dietary restrictions or food allergies."
                })

        # ── PITTA ORIENTED ──────────────────────────────────────────────────
        elif dominant == "Pitta":
            dinacharya.append({
                "title": "Cool Water Morning Cleanse",
                "what": "Rinse face, eyelids, and wrists with cool (room-temperature) water upon waking.",
                "why": "Pitta accumulates excess internal metabolic heat overnight; a cooling morning cleanse calms ocular and hepatic tension.",
                "how": "Splash face with fresh cool water 5 times. Gently bathe closed eyelids. Sip a glass of room-temperature water.",
                "safety": "Do not use ice water if you have acute sinusitis or nasal congestion."
            })

            if is_stress_focus:
                yoga.append({
                    "title": "Chandra Namaskar (Moon Salutations)",
                    "what": "A soothing, fluid sequence of lunar postures focused on hip opening and forward folds.",
                    "why": "Unlike competitive, heat-generating workouts, Chandra Namaskar discharges built-up frustration and pacifies Pitta intensity.",
                    "how": "Perform 4-6 rounds at 60% effort. Move with smooth, relaxed breaths without straining for extreme flexibility.",
                    "safety": "Avoid vigorous inversions if experiencing headaches, dizziness, or high blood pressure."
                })
            else:
                yoga.append({
                    "title": "Non-Competitive Cooling Asana",
                    "what": "Seated forward folds, supported bridge pose (Setu Bandhasana), and reclined bound angle pose (Supta Baddhakonasana).",
                    "why": "Releases tension in the solar plexus and liver channels while cultivating patience and emotional surrender.",
                    "how": "Hold postures comfortably for 1-2 minutes with eyes gently closed. End with cooling abdominal breathing in Shavasana.",
                    "safety": "Do not push through acute knee or hamstring discomfort. Use yoga blocks for support."
                })

            pranayama.append({
                "title": "Sheetali / Sitkari Pranayama (Cooling Breath)",
                "what": "Inhaling cool air through a curled tongue or gently clenched teeth and exhaling warm air through the nose.",
                "why": "Directly reduces core body temperature, eases hyperacidity, and diffuses irritable stress spikes.",
                "how": "Curl tongue into an 'O' shape (or inhale across teeth). Inhale slowly feeling cool air. Close lips, exhale through nose. 10 rounds.",
                "safety": "Do not practice in freezing cold winter air or if you have a productive respiratory cough."
            })

            diet_lifestyle.append({
                "title": "Cooling Midday Nourishment & Evening Nature Walk",
                "what": "Enjoy your main meal at noon featuring sweet, bitter, and astringent tastes; take a 15-min walk in green nature at dusk.",
                "why": "Pitta digestive fire (Pachaka Agni) is peak at midday; nature walks at twilight cool visual and mental overstimulation.",
                "how": "Include cucumbers, fresh cilantro, basmati rice, and ghee at lunch. Take an evening walk away from screen notifications.",
                "safety": "Avoid excessively chili-heavy, oily, or heavily fermented foods if prone to acid reflux."
            })

        # ── KAPHA ORIENTED ──────────────────────────────────────────────────
        else:
            dinacharya.append({
                "title": "Brahma Muhurta Awakening & Dry Brushing (Garshana)",
                "what": "Wake up before 6:30 AM and perform a 5-minute vigorous dry massage with raw silk gloves or dry body brush.",
                "why": "Kapha's heavy, stagnant qualities peak between 6 and 10 AM; early rising and dry brushing stimulate sluggish lymphatic circulation.",
                "how": "Brush limbs in long strokes toward the heart, and circular strokes over joints before taking a warm invigorating shower.",
                "safety": "Do not brush broken, inflamed, or sunburned skin."
            })

            yoga.append({
                "title": "Invigorating Surya Namaskar (Sun Salutations)",
                "what": "Dynamic, brisk sequence of 6-8 Sun Salutations followed by Warrior poses (Virabhadrasana).",
                "why": "Generates internal warmth, expands lung volume, activates sluggish metabolism, and dissolves morning lethargy.",
                "how": "Sync breath with movement. Maintain an active rhythm that elevates heart rate comfortably and produces a light morning glow.",
                "safety": "Build intensity gradually if you are sedentary. Stop immediately if feeling dizzy or breathless."
            })

            pranayama.append({
                "title": "Kapalabhati (Skull Shining Breath)",
                "what": "Active, forceful abdominal exhalations paired with passive, automatic inhalations.",
                "why": "Clears respiratory congestion, burns excess metabolic sluggishness (Ama), and sharpens cognitive clarity.",
                "how": "Sit tall. Exhale sharply by snapping navel toward spine, 1 stroke per second. 3 rounds of 25-30 strokes with pauses.",
                "safety": "Contraindicated during pregnancy, uncontrolled hypertension, cardiac conditions, or recent abdominal surgery."
            })

            diet_lifestyle.append({
                "title": "Light Spiced Meals & Ginger Digestion Tea",
                "what": "Light, warm, freshly spiced meals (black pepper, ginger, cumin); sip fresh ginger tea 20 min before lunch.",
                "why": "Kindles sluggish digestive fire (Manda Agni) and prevents post-meal heaviness and sluggish fluid retention.",
                "how": "Keep breakfast light or optional. Make lunch your main meal. Avoid dairy, cold sugary beverages, and heavy desserts.",
                "safety": "Ensure adequate balanced hydration throughout the day; do not skip essential nutrients."
            })

        # ── COMPILE 4-6 DAILY TRACKER TASKS ──────────────────────────────────
        # Distinct task list matching the personalized sections
        task_id = 1
        for sec_name, sec_items in [("Dinacharya", dinacharya), ("Yoga", yoga), ("Pranayama", pranayama), ("Diet & Lifestyle", diet_lifestyle)]:
            for item in sec_items:
                daily_tracker.append({
                    "id": f"task_{task_id}",
                    "title": item["title"],
                    "description": item["what"][:90] + "...",
                    "category": sec_name,
                    "duration": "5-15 min",
                    "completed": False
                })
                task_id += 1

        # Build backwards-compatible PlanTaskItem list
        tasks_compat = []
        for t in daily_tracker:
            tasks_compat.append({
                "id": t["id"],
                "title": t["title"],
                "category": t.get("category", "General"),
                "duration": t.get("duration", "10 min"),
                "what": t["description"],
                "why": f"Tailored for {dominant} constitution wellness balance.",
                "how": "Follow daily preventive routine guidelines.",
                "safety": "Consult a healthcare provider for any medical concerns.",
                "is_completed": False,
                "is_adjusted": False
            })

        return {
            "status": "success",
            "module": "plan",
            "dominant": dominant,
            "sections": {
                "dinacharya": dinacharya,
                "yoga": yoga,
                "pranayama": pranayama,
                "diet_lifestyle": diet_lifestyle
            },
            "daily_tracker": daily_tracker,
            "tasks": tasks_compat,
            "message": f"Generated personalized AYUSH preventive plan tailored for {dominant} constitution with focus on {wellness_goals or 'daily balance'}.",
            "note": "AyuPulse provides preventive wellness guidance, not medical diagnosis or treatment."
        }

    def _sanitize_plan_dict(self, data: Dict[str, Any], dominant: str) -> Dict[str, Any]:
        """Ensures all fields in AI-generated plan pass through the safety gate."""
        sections = data.get("sections", {})
        for sec_name, items in sections.items():
            for item in items:
                item["what"] = sanitize_wellness_text(item.get("what", ""))
                item["why"] = sanitize_wellness_text(item.get("why", ""))
                item["how"] = sanitize_wellness_text(item.get("how", ""))
                item["safety"] = sanitize_wellness_text(item.get("safety", "Consult a physician for any health condition."))

        daily_tracker = data.get("daily_tracker", [])
        for t in daily_tracker:
            t["completed"] = False
            t["title"] = sanitize_wellness_text(t.get("title", ""))
            t["description"] = sanitize_wellness_text(t.get("description", ""))

        data["status"] = "success"
        data["module"] = "plan"
        data["dominant"] = dominant
        data["note"] = "AyuPulse provides preventive wellness guidance, not medical diagnosis or treatment."
        return data

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extracts JSON object from text, handling markdown code fences if present."""
        clean = text.strip()
        if clean.startswith("```"):
            clean = re.sub(r"^```(?:json)?", "", clean)
            clean = re.sub(r"```$", "", clean)
            clean = clean.strip()
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", clean, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
        return {}

    def _generate_fallback_assessment(
        self,
        vata: int,
        pitta: int,
        kapha: int,
        dominant: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Deterministic fallback that generates clean, authentic AYUSH wellness interpretation."""
        dominant_title = dominant.capitalize()

        summaries = {
            "Vata": (
                f"Your responses indicate a prominent Vata constitution ({vata}%), characterized by qualities of "
                "air and ether — lightness, creativity, agility, and natural adaptability. In daily rhythm, "
                "this tendency often manifests as energetic bursts followed by a need for grounding, warmth, "
                "and consistent restorative sleep."
            ),
            "Pitta": (
                f"Your responses indicate a prominent Pitta constitution ({pitta}%), characterized by qualities of "
                "fire and water — sharp focus, strong digestion, purposeful drive, and natural leadership. "
                "In daily rhythm, this tendency thrives with cooling routines, moderate exercise, and balanced "
                "stress relief."
            ),
            "Kapha": (
                f"Your responses indicate a prominent Kapha constitution ({kapha}%), characterized by qualities of "
                "earth and water — natural endurance, calm emotional stability, strength, and deep loyalty. "
                "In daily rhythm, this tendency benefits from energizing movement, light warm foods, and active morning starts."
            )
        }

        focus_areas = {
            "Vata": [
                "Warm water and grounding herbal teas on waking",
                "Gentle morning asana (Child's pose, gentle forward bends)",
                "Nadi Shodhana (alternate nostril breathing) for nervous system balance",
                "Regular warm, cooked meals and fixed bedtime routine"
            ],
            "Pitta": [
                "Cooling morning cleanse and room-temperature hydration",
                "Sheetali pranayama (cooling breath) during afternoon intensity",
                "Moderate, non-competitive yoga and evening nature walks",
                "Favoring sweet, bitter, and cooling foods over spicy or acidic meals"
            ],
            "Kapha": [
                "Vigorous morning movement (Surya Namaskar / brisk walking)",
                "Kapalabhati (breath of fire) for respiratory clarity and vitality",
                "Light, warm, freshly spiced meals (ginger, black pepper, cumin)",
                "Consistent early wake-up before sunrise to counter heaviness"
            ]
        }

        summary = summaries.get(dominant_title, summaries["Vata"])
        wellness_focus = focus_areas.get(dominant_title, focus_areas["Vata"])

        return {
            "dominant": dominant_title,
            "summary": summary,
            "wellness_focus": wellness_focus,
            "note": "This is a traditional wellness-oriented interpretation, not a medical diagnosis."
        }


# Singleton service instance
claude_service = ClaudeService()
