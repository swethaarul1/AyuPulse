"""
AI Service abstraction — AyuPulse
Provides a unified interface for AI-augmented generation.
Falls back to deterministic engines when no LLM is available.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
from app.config import settings
from app.services.assessment_engine import score_assessment, _build_explanation
from app.services.plan_engine import generate_plan
from app.services.pattern_engine import detect_pattern, compute_wellness_score
from app.services.safety_engine import sanitize_text


class AIService:
    """
    Abstraction layer for AI-enhanced generation.
    All methods have deterministic fallbacks.
    If an LLM key is present, enhanced explanations can be injected here later.
    """

    def __init__(self):
        self.has_openai = bool(settings.OPENAI_API_KEY)
        self.has_gemini = bool(settings.GEMINI_API_KEY)
        self.llm_available = self.has_openai or self.has_gemini

    # ── Assessment Interpretation ─────────────────────────────────────────────

    def interpret_assessment(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Score answers and return a complete dosha result."""
        result = score_assessment(answers)
        result["explanation"] = sanitize_text(result.get("explanation", ""))
        return result

    # ── Plan Generation ───────────────────────────────────────────────────────

    def generate_preventive_plan(
        self,
        dosha_result: Dict[str, Any],
        lifestyle_answers: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """Generate a personalized preventive plan from the dosha result."""
        return generate_plan(dosha_result, lifestyle_answers)

    # ── Pattern Insight ───────────────────────────────────────────────────────

    def analyze_check_in_pattern(self, check_ins: List[Any]) -> Optional[Dict[str, Any]]:
        """Analyze check-in history for patterns."""
        return detect_pattern(check_ins)

    def compute_wellness_score(self, check_ins: List[Any]) -> Dict[str, Any]:
        """Compute wellness score from check-in history."""
        return compute_wellness_score(check_ins)


# Module-level singleton
ai_service = AIService()
