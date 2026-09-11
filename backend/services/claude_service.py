"""
Claude Service for AyuPulse.
Interprets deterministic Prakriti assessment scores using the Anthropic API.
Provides robust JSON parsing and graceful deterministic fallbacks if the API key is not set or calls fail.
"""
import os
import json
import re
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

from prompts.prakriti_prompt import SYSTEM_PROMPT, build_prakriti_prompt
from services.safety import sanitize_wellness_text

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

    def interpret_prakriti(
        self,
        vata: int,
        pitta: int,
        kapha: int,
        dominant: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calls Claude to interpret the calculated Dosha percentages.
        Falls back to high-quality deterministic interpretation if Claude is unavailable.
        """
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

                # Extract response text
                text_response = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        text_response += block.text

                # Parse JSON
                parsed = self._extract_json(text_response)
                if parsed and "summary" in parsed and "wellness_focus" in parsed:
                    # Sanitize to guarantee safety compliance
                    parsed["summary"] = sanitize_wellness_text(parsed["summary"])
                    parsed["wellness_focus"] = [sanitize_wellness_text(f) for f in parsed["wellness_focus"]]
                    parsed["dominant"] = dominant
                    parsed["note"] = "This is a traditional wellness-oriented interpretation, not a medical diagnosis."
                    return parsed
                else:
                    logger.warning("Claude returned malformed JSON. Using fallback.")
            except Exception as ex:
                logger.error(f"Claude API call failed: {ex}. Using fallback.")

        # Fallback interpretation based on dominant tendency
        return self._generate_fallback(vata, pitta, kapha, dominant, context)

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extracts JSON object from text, handling markdown code fences if present."""
        clean = text.strip()
        # Remove code blocks if present
        if clean.startswith("```"):
            clean = re.sub(r"^```(?:json)?", "", clean)
            clean = re.sub(r"```$", "", clean)
            clean = clean.strip()
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            # Try regex to locate first { ... }
            match = re.search(r"\{.*\}", clean, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
        return {}

    def _generate_fallback(
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
