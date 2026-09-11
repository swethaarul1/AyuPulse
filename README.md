# AyuPulse

> **Preventive wellness, rooted in AYUSH. Personalized by AI.**

AyuPulse is an AI-enabled preventive wellness platform that personalizes traditional AYUSH health guidance through deterministic scoring and LLM interpretation.

---

## Overview

AyuPulse moves users through a structured preventive wellness journey:
$$\text{User} \longrightarrow \text{Input} \longrightarrow \text{AI Engine} \longrightarrow \text{Decision} \longrightarrow \text{Action} \longrightarrow \text{Outcome}$$

Instead of offering generic articles or functioning as an open-ended chatbot, AyuPulse translates individual sleep, digestion, stress, energy, and lifestyle tendencies into concrete, daily preventive practices (Dinacharya, Yoga, Pranayama, and Diet).

---

## Modules Implemented

| Module | Name | Status | Description |
|---|---|---|---|
| **01** | **AI Prakriti Assessment** | **Complete** | Deterministic Vata/Pitta/Kapha scoring engine + Claude AI interpretation with offline fallback. |
| **02** | **Personalized Preventive Plan & Daily Tracker** | **Complete** | 4 sections (Dinacharya, Yoga, Pranayama, Diet/Lifestyle) with What/Why/How/Safety + 4–6 daily tracker tasks. |
| **03** | **Check-in, Pattern Insight & Wellness Score** | **Complete** | 30-second check-in (Sleep, Stress, Mood, Digestion, Energy) + 0–100 Wellness Score + recurring pattern detector. |
| **04** | **AYUSH Access Bridge** | **Complete** | Seeded prototype directory filtering and service matching for Yoga, Ayurveda, Naturopathy, Siddha & Unani. |
| **05** | **Preventive Wellness Safety Gate** | **Complete** | Real-time clinical boundary enforcement, red-flag emergency detection, and claim sanitization. |
| **06** | **Community Wellness Dashboard** | **Complete** | Aggregated prototype simulation metrics (assessments, task start rate, common patterns, trends). |

---

## Complete API Endpoints

1. **`GET /health`** — Service health status check.
2. **`GET /api/assessment/questions`** — Questionnaire definitions and selectable options.
3. **`POST /api/assessment`** — Submits questionnaire, computes deterministic dosha scores, returns AI interpretation.
4. **`POST /api/plan`** — Generates personalized 4-section preventive plan and daily tracker tasks.
5. **`POST /api/checkin`** — Records 30-second daily check-in and calculates deterministic 0–100 Wellness Score.
6. **`GET /api/checkin`** — Retrieves check-in history with prototype seeded notice.
7. **`POST /api/pattern` & `GET /api/pattern`** — Analyzes multi-day history to detect recurring patterns (e.g. sleep + stress).
8. **`POST /api/safety`** — Safety Gate checking inputs/recommendations, modifying claims, and flagging emergencies.
9. **`GET /api/centres`** — Lists prototype AYUSH centres with optional `focus`, `system`, and `location` filters.
10. **`POST /api/centres/match`** — Matches user wellness goals to suitable AYUSH service categories and centres.
11. **`POST /api/consultation`** — Simulates a consultation booking request for prototype demonstration.
12. **`GET /api/dashboard`** — Community wellness engagement metrics with explicit simulation disclaimer.

---

## Backend Directory Structure

```
backend/
├── main.py                    # FastAPI entry point, CORS, routers, health check
├── schemas.py                 # Pydantic request/response schemas
├── requirements.txt           # Python dependencies
├── test_api.py                # Standalone development test suite
├── .env.example               # Environment variable templates
├── .gitignore                 # Secret and cache ignore rules
├── routes/
│   ├── __init__.py
│   ├── assessment.py          # POST /api/assessment, GET /api/assessment/questions
│   ├── plan.py                # POST /api/plan
│   ├── checkin.py             # POST /api/checkin, GET /api/checkin
│   ├── pattern.py             # POST /api/pattern, GET /api/pattern
│   ├── safety.py              # POST /api/safety
│   ├── centres.py             # GET /api/centres, POST /api/centres/match, POST /api/consultation
│   └── dashboard.py           # GET /api/dashboard
├── services/
│   ├── __init__.py
│   ├── scoring.py             # Deterministic Vata/Pitta/Kapha scoring & normalization
│   ├── claude_service.py      # Claude API integration with robust offline fallback
│   ├── pattern.py             # 0-100 Wellness Pulse & recurring pattern analysis
│   └── safety.py              # Safety Gate, clinical boundary sanitization & emergency red-flag checks
├── prompts/
│   ├── __init__.py
│   └── prakriti_prompt.py     # Cautious, compliant AI interpretation prompt
└── data/
    ├── history.json           # Prototype seeded 14-day check-in history
    └── centres.json           # Seeded AYUSH centres database
```

---

## Getting Started

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Pip

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the example file and optionally set your Claude API key:
```bash
cp .env.example .env
```
In `.env`:
```env
ANTHROPIC_API_KEY=your_claude_api_key_here  # Optional: Fallback mode works without key
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```
> **Note**: If `ANTHROPIC_API_KEY` is not provided or invalid, the backend automatically runs in deterministic fallback mode with high-quality authentic AYUSH interpretations.

### 3. Run Development Server
```bash
python main.py
# Or with uvicorn directly:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 4. Run Development Tests
```bash
python test_api.py
```

---

## Safety & Medical Non-Claim Notice

AyuPulse adheres strictly to preventive wellness communication:
- Results are presented exclusively as **traditional wellness tendencies**, never medical diagnoses.
- Prescriptive clinical language is sanitized and prohibited.
- Acute or red-flag emergency symptoms are routed toward emergency healthcare facilities.
