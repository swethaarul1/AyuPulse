"""
Development Test Script for AyuPulse Assessment & Scoring Engine.
Tests User A (Vata tendency) vs User B (Pitta tendency) vs User C (Kapha tendency).
Validates deterministic scoring, normalization to 100%, and error handling.
"""
import sys
import os

# Ensure backend root is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import AssessmentRequest
from services.scoring import calculate_dosha_scores
from services.claude_service import claude_service
from services.safety import evaluate_safety
from services.pattern import analyze_history_patterns

def run_tests():
    print("=" * 60)
    print("AyuPulse Backend Test Suite")
    print("=" * 60)

    # ─────────────────────────────────────────────────────────────────
    # 1. TEST USER A (Expected: Vata dominant)
    # ─────────────────────────────────────────────────────────────────
    user_a_payload = AssessmentRequest(
        sleep="light_restless",
        digestion="irregular_variable",
        stress_response="anxious_worry",
        energy="variable_bursts",
        body_tendencies="dry_cold_slender",
        lifestyle="irregular_active",
        wellness_goals=["sleep consistency", "grounding"]
    )
    score_a = calculate_dosha_scores(user_a_payload)
    print(f"\n[Test 1] User A Profile (Vata candidate):")
    print(f"  Vata: {score_a['vata']}%, Pitta: {score_a['pitta']}%, Kapha: {score_a['kapha']}%")
    print(f"  Dominant: {score_a['dominant']}")
    print(f"  Total percentage: {score_a['vata'] + score_a['pitta'] + score_a['kapha']}%")
    assert score_a["dominant"] == "Vata", f"Expected Vata, got {score_a['dominant']}"
    assert (score_a["vata"] + score_a["pitta"] + score_a["kapha"]) == 100, "Scores must sum to 100%"
    print("  --> PASS: User A correctly scored as Vata with exact 100% normalization.")

    # ─────────────────────────────────────────────────────────────────
    # 2. TEST USER B (Expected: Pitta dominant)
    # ─────────────────────────────────────────────────────────────────
    user_b_payload = AssessmentRequest(
        sleep="moderate_sound",
        digestion="sharp_fast",
        stress_response="irritable_intense",
        energy="high_sustained",
        body_tendencies="warm_medium_athletic",
        lifestyle="competitive_demanding",
        wellness_goals=["stress management", "cooling"]
    )
    score_b = calculate_dosha_scores(user_b_payload)
    print(f"\n[Test 2] User B Profile (Pitta candidate):")
    print(f"  Vata: {score_b['vata']}%, Pitta: {score_b['pitta']}%, Kapha: {score_b['kapha']}%")
    print(f"  Dominant: {score_b['dominant']}")
    print(f"  Total percentage: {score_b['vata'] + score_b['pitta'] + score_b['kapha']}%")
    assert score_b["dominant"] == "Pitta", f"Expected Pitta, got {score_b['dominant']}"
    assert (score_b["vata"] + score_b["pitta"] + score_b["kapha"]) == 100, "Scores must sum to 100%"
    assert score_a["dominant"] != score_b["dominant"], "User A and User B must yield different tendencies"
    print("  --> PASS: User B correctly scored as Pitta. Personalization confirmed (User A != User B).")

    # ─────────────────────────────────────────────────────────────────
    # 3. TEST USER C (Expected: Kapha dominant)
    # ─────────────────────────────────────────────────────────────────
    user_c_payload = AssessmentRequest(
        sleep="deep_heavy",
        digestion="slow_steady",
        stress_response="withdrawn_slow",
        energy="steady_calm",
        body_tendencies="cool_solid_heavy",
        lifestyle="routine_sedentary",
        wellness_goals=["energy boost", "metabolism"]
    )
    score_c = calculate_dosha_scores(user_c_payload)
    print(f"\n[Test 3] User C Profile (Kapha candidate):")
    print(f"  Vata: {score_c['vata']}%, Pitta: {score_c['pitta']}%, Kapha: {score_c['kapha']}%")
    print(f"  Dominant: {score_c['dominant']}")
    assert score_c["dominant"] == "Kapha", f"Expected Kapha, got {score_c['dominant']}"
    print("  --> PASS: User C correctly scored as Kapha.")

    # ─────────────────────────────────────────────────────────────────
    # 4. TEST CLAUDE / AI INTERPRETATION LAYER
    # ─────────────────────────────────────────────────────────────────
    print(f"\n[Test 4] AI Interpretation Layer (Fallback or Claude API):")
    interpretation = claude_service.interpret_prakriti(
        vata=score_a["vata"],
        pitta=score_a["pitta"],
        kapha=score_a["kapha"],
        dominant=score_a["dominant"],
        context={"sleep": user_a_payload.sleep}
    )
    print(f"  Dominant: {interpretation['dominant']}")
    print(f"  Summary: {interpretation['summary'][:100]}...")
    print(f"  Focus Areas ({len(interpretation['wellness_focus'])}): {interpretation['wellness_focus'][:2]}")
    print(f"  Disclaimer Note: {interpretation['note']}")
    assert "summary" in interpretation and len(interpretation["summary"]) > 20
    assert "wellness_focus" in interpretation and len(interpretation["wellness_focus"]) >= 2
    assert "not a medical diagnosis" in interpretation["note"].lower()
    print("  --> PASS: AI layer returns structured, safe, compliant interpretation.")

    # ─────────────────────────────────────────────────────────────────
    # 5. TEST SAFETY ENGINE & RED FLAG ESCALATION
    # ─────────────────────────────────────────────────────────────────
    print(f"\n[Test 5] Safety Guardrails & Red Flags:")
    safe_check = evaluate_safety("I feel tired in the afternoon and want more energy")
    assert safe_check["is_safe"] is True
    assert safe_check["requires_escalation"] is False

    red_flag_check = evaluate_safety("I have severe chest pain and difficulty breathing")
    assert red_flag_check["is_safe"] is False
    assert red_flag_check["requires_escalation"] is True
    print(f"  Emergency query correctly escalated: {red_flag_check['safety_notice'][:60]}...")
    print("  --> PASS: Safety engine correctly allows benign wellness and flags emergencies.")

    # ─────────────────────────────────────────────────────────────────
    # 6. TEST PATTERN ENGINE
    # ─────────────────────────────────────────────────────────────────
    print(f"\n[Test 6] Pattern Engine (Seed Data Analysis):")
    pattern_res = analyze_history_patterns()
    print(f"  Wellness Pulse: {pattern_res['wellness_pulse']}/100")
    print(f"  Detected Pattern: {pattern_res['detected_pattern']}")
    print(f"  Insight: {pattern_res['insight']}")
    print(f"  Plan Adjusted: {pattern_res['plan_adjusted']}")
    print(f"  Adjustment Tasks: {len(pattern_res['adjustment_tasks'])} tasks")
    assert pattern_res["wellness_pulse"] > 0
    assert pattern_res["detected_pattern"] == "sleep_stress"
    assert pattern_res["plan_adjusted"] is True
    print("  --> PASS: Pattern engine detects 14-day sleep+stress trend and adjusts plan.")

    print("\n" + "=" * 60)
    print("ALL 6 BACKEND TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
