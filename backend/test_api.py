"""
Comprehensive Test Suite for AyuPulse Modules 01–06.
Tests all endpoints, deterministic scoring, personalization differences,
pattern recognition, safety gate actions, and prototype disclosures.
"""
import sys
import os

# Ensure backend root is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
from schemas import AssessmentRequest, PlanRequest, CheckInRequest, SafetyCheckRequest, CentreMatchRequest, ConsultationRequest

client = TestClient(app)


def test_suite():
    print("=" * 70)
    print("AYUPULSE FULL BACKEND TEST SUITE (MODULES 01–06)")
    print("=" * 70)

    # ─────────────────────────────────────────────────────────────────
    # 0. HEALTH CHECK
    # ─────────────────────────────────────────────────────────────────
    print("\n[0] Testing GET /health ...")
    r_health = client.get("/health")
    assert r_health.status_code == 200
    data_health = r_health.json()
    assert data_health["status"] == "ok"
    assert "AyuPulse" in data_health.get("service", "")
    print(f"  -> PASS: Health check verified: {data_health}")

    # ─────────────────────────────────────────────────────────────────
    # 1. MODULE 01: AI PRAKRITI ASSESSMENT
    # ─────────────────────────────────────────────────────────────────
    print("\n[1] Testing Module 01: AI Prakriti Assessment ...")
    # User A: Vata candidate
    r_user_a = client.post("/api/assessment", json={
        "sleep": "light_restless",
        "digestion": "irregular_variable",
        "stress_response": "anxious_worry",
        "energy": "variable_bursts",
        "body_tendencies": "dry_cold_slender",
        "lifestyle": "irregular_active",
        "wellness_goals": ["sleep consistency"]
    })
    assert r_user_a.status_code == 200
    res_a = r_user_a.json()
    assert res_a["dominant"] == "Vata"
    assert (res_a["vata"] + res_a["pitta"] + res_a["kapha"]) == 100
    assert len(res_a["wellness_focus"]) >= 2

    # User B: Pitta candidate
    r_user_b = client.post("/api/assessment", json={
        "sleep": "moderate_sound",
        "digestion": "sharp_fast",
        "stress_response": "irritable_intense",
        "energy": "high_sustained",
        "body_tendencies": "warm_medium_athletic",
        "lifestyle": "competitive_demanding",
        "wellness_goals": ["stress management"]
    })
    assert r_user_b.status_code == 200
    res_b = r_user_b.json()
    assert res_b["dominant"] == "Pitta"
    assert res_a["dominant"] != res_b["dominant"]
    print(f"  -> PASS: User A ({res_a['dominant']}: {res_a['vata']}%) != User B ({res_b['dominant']}: {res_b['pitta']}%)")

    # ─────────────────────────────────────────────────────────────────
    # 2. MODULE 02: PERSONALIZED PREVENTIVE PLAN & DAILY TRACKER
    # ─────────────────────────────────────────────────────────────────
    print("\n[2] Testing Module 02: AI Personalized Plan + Daily Tracker ...")
    # Plan for User A (Vata + Sleep goal)
    r_plan_a = client.post("/api/plan", json={
        "dominant": "Vata",
        "vata": res_a["vata"],
        "pitta": res_a["pitta"],
        "kapha": res_a["kapha"],
        "wellness_goals": ["sleep consistency"],
        "lifestyle": "irregular late nights"
    })
    assert r_plan_a.status_code == 200
    plan_a = r_plan_a.json()
    assert plan_a["dominant"] == "Vata"
    assert "sections" in plan_a
    assert len(plan_a["sections"]["dinacharya"]) >= 1
    assert len(plan_a["sections"]["yoga"]) >= 1
    assert len(plan_a["sections"]["pranayama"]) >= 1
    assert len(plan_a["sections"]["diet_lifestyle"]) >= 1
    # Check all required fields in recommendations
    first_rec = plan_a["sections"]["dinacharya"][0]
    for key in ["title", "what", "why", "how", "safety"]:
        assert key in first_rec and len(first_rec[key]) > 0, f"Missing {key} in recommendation"

    # Verify Daily Tracker tasks exist
    assert "daily_tracker" in plan_a
    assert 4 <= len(plan_a["daily_tracker"]) <= 7
    first_task = plan_a["daily_tracker"][0]
    assert "id" in first_task and "title" in first_task and "completed" in first_task
    assert first_task["completed"] is False

    # Plan for User B (Pitta + Stress goal)
    r_plan_b = client.post("/api/plan", json={
        "dominant": "Pitta",
        "vata": res_b["vata"],
        "pitta": res_b["pitta"],
        "kapha": res_b["kapha"],
        "wellness_goals": ["stress management"],
        "lifestyle": "competitive executive"
    })
    assert r_plan_b.status_code == 200
    plan_b = r_plan_b.json()
    assert plan_b["dominant"] == "Pitta"
    # Verify User A and User B receive different plans
    assert plan_a["sections"]["dinacharya"][0]["title"] != plan_b["sections"]["dinacharya"][0]["title"]
    assert plan_a["daily_tracker"][0]["title"] != plan_b["daily_tracker"][0]["title"]
    print(f"  -> PASS: Module 02 generates distinct personalized plans & {len(plan_a['daily_tracker'])} tracker tasks.")

    # ─────────────────────────────────────────────────────────────────
    # 3. MODULE 03: WELLNESS CHECK-IN & SCORE & PATTERN INSIGHT
    # ─────────────────────────────────────────────────────────────────
    print("\n[3] Testing Module 03: Daily Check-in & Pattern Engine ...")
    # Normal Check-in
    r_chk = client.post("/api/checkin", json={
        "sleep": 4,
        "stress": 2,
        "mood": 4,
        "digestion": 4,
        "energy": 4,
        "notes": "Feeling centered"
    })
    assert r_chk.status_code == 200
    chk_res = r_chk.json()
    assert 0 <= chk_res["wellness_score"] <= 100
    assert chk_res["wellness_score"] == 75
    assert "summary" in chk_res

    # Pattern recognition with poor sleep + high stress input
    r_pat = client.post("/api/pattern", json={
        "days": 5,
        "checkins": [
            {"sleep": 2, "stress": 4, "mood": 3, "digestion": 3, "energy": 2},
            {"sleep": 2, "stress": 4, "mood": 2, "digestion": 3, "energy": 2},
            {"sleep": 2, "stress": 5, "mood": 2, "digestion": 2, "energy": 2},
            {"sleep": 1, "stress": 4, "mood": 3, "digestion": 3, "energy": 2},
            {"sleep": 2, "stress": 4, "mood": 2, "digestion": 2, "energy": 2}
        ]
    })
    assert r_pat.status_code == 200
    pat_res = r_pat.json()
    assert pat_res["detected_pattern"] == "sleep_stress"
    assert pat_res["plan_adjusted"] is True
    assert len(pat_res["adjustment_tasks"]) >= 1
    assert "sleep and stress" in pat_res["insight"].lower()
    assert len(pat_res["patterns"]) >= 1
    assert pat_res["data_status"] == "Prototype seeded history"

    # Pattern recognition with improving history
    r_pat_imp = client.post("/api/pattern", json={
        "checkins": [
            {"sleep": 2, "stress": 4, "mood": 2, "digestion": 2, "energy": 2},
            {"sleep": 2, "stress": 4, "mood": 2, "digestion": 2, "energy": 2},
            {"sleep": 3, "stress": 3, "mood": 3, "digestion": 3, "energy": 3},
            {"sleep": 4, "stress": 2, "mood": 4, "digestion": 4, "energy": 4},
            {"sleep": 5, "stress": 1, "mood": 5, "digestion": 4, "energy": 5}
        ]
    })
    assert r_pat_imp.status_code == 200
    assert r_pat_imp.json()["detected_pattern"] in ["improving_wellness", "balanced_steady"]
    print(f"  -> PASS: Module 03 Check-in (Score: {chk_res['wellness_score']}) and Pattern ({pat_res['detected_pattern']}) verified.")

    # ─────────────────────────────────────────────────────────────────
    # 4. MODULE 04: AYUSH ACCESS BRIDGE
    # ─────────────────────────────────────────────────────────────────
    print("\n[4] Testing Module 04: AYUSH Access Bridge ...")
    # List centres
    r_centres = client.get("/api/centres")
    assert r_centres.status_code == 200
    centres_data = r_centres.json()
    assert centres_data["total"] >= 1
    assert centres_data["data_status"] == "Prototype AYUSH centre data"

    # Filter by focus
    r_filter = client.get("/api/centres?focus=stress")
    assert r_filter.status_code == 200
    assert r_filter.json()["total"] >= 1

    # Match centre based on focus
    r_match = client.post("/api/centres/match", json={
        "wellness_focus": "stress relief and calm sleep",
        "preferred_system": "Yoga"
    })
    assert r_match.status_code == 200
    match_res = r_match.json()
    assert len(match_res["matched_centres"]) >= 1
    assert match_res["data_status"] == "Prototype AYUSH centre data"

    # Simulate consultation request
    first_centre_id = centres_data["centres"][0]["id"]
    r_cons = client.post("/api/consultation", json={
        "centre_id": first_centre_id,
        "preferred_date": "2026-09-20",
        "preferred_system": "Ayurveda"
    })
    assert r_cons.status_code == 200
    cons_res = r_cons.json()
    assert cons_res["status"] == "requested"
    assert "prototype demonstration" in cons_res["message"].lower()

    # Centre not found error
    r_bad_centre = client.post("/api/consultation", json={
        "centre_id": "invalid-centre-xyz",
        "preferred_date": "2026-09-20"
    })
    assert r_bad_centre.status_code == 404
    print(f"  -> PASS: Module 04 listing, filtering, matching, and consultation simulation verified.")

    # ─────────────────────────────────────────────────────────────────
    # 5. MODULE 05: PREVENTIVE WELLNESS SAFETY GATE
    # ─────────────────────────────────────────────────────────────────
    print("\n[5] Testing Module 05: Preventive Wellness Safety Gate ...")
    # Safe text
    r_safe = client.post("/api/safety", json={
        "text": "Drink warm water on waking and practice gentle Nadi Shodhana for daily relaxation."
    })
    assert r_safe.status_code == 200
    assert r_safe.json()["safe"] is True
    assert r_safe.json()["action"] == "allow"

    # Unsafe text: cure claim and disease diagnosis
    r_unsafe = client.post("/api/safety", json={
        "text": "This practice guarantees a cure for diabetes and you should stop taking your prescription medication."
    })
    assert r_unsafe.status_code == 200
    res_unsafe = r_unsafe.json()
    assert res_unsafe["safe"] is False
    assert res_unsafe["action"] in ["modify", "professional_attention"]
    assert "stop" not in res_unsafe["modified_content"] or "continue your prescribed care" in res_unsafe["modified_content"]

    # Red-flag emergency symptom
    r_emergency = client.post("/api/safety", json={
        "text": "I have severe crushing chest pain and shortness of breath."
    })
    assert r_emergency.status_code == 200
    res_emerg = r_emergency.json()
    assert res_emerg["safe"] is False
    assert res_emerg["professional_attention"] is True
    assert res_emerg["action"] == "professional_attention"
    assert "emergency" in res_emerg["message"].lower()
    print(f"  -> PASS: Safety Gate correctly allows safe text, modifies claims, and escalates emergencies.")

    # ─────────────────────────────────────────────────────────────────
    # 6. MODULE 06: COMMUNITY WELLNESS DASHBOARD
    # ─────────────────────────────────────────────────────────────────
    print("\n[6] Testing Module 06: Community Wellness Dashboard ...")
    r_dash = client.get("/api/dashboard")
    assert r_dash.status_code == 200
    dash_res = r_dash.json()
    assert dash_res["prototype"] is True
    assert "Prototype simulation" in dash_res["disclaimer"]
    assert dash_res["metrics"]["total_assessments"] == 12480
    assert dash_res["metrics"]["task_start_rate"] == 68
    assert len(dash_res["common_patterns"]) >= 3
    assert len(dash_res["ayush_matches"]) >= 3
    assert len(dash_res["trends"]) >= 5
    print(f"  -> PASS: Community dashboard returns verified prototype metrics: {dash_res['metrics']}")

    # ─────────────────────────────────────────────────────────────────
    # 7. ERROR HANDLING
    # ─────────────────────────────────────────────────────────────────
    print("\n[7] Testing Error Handling ...")
    r_err_malformed = client.post("/api/assessment", content="not json", headers={"Content-Type": "application/json"})
    assert r_err_malformed.status_code in [400, 422]

    r_err_missing = client.post("/api/plan", json={})
    assert r_err_missing.status_code == 422
    print("  -> PASS: Error handling properly catches malformed and missing request bodies with 422.")

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED! BACKEND MODULES 01–06 FULLY VERIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    test_suite()
