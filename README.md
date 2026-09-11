# AyuPulse

> **Preventive wellness, rooted in AYUSH. Personalized by AI.**

AyuPulse is an AI-enabled preventive wellness platform that personalizes traditional AYUSH health guidance through deterministic scoring and LLM interpretation.

---

## Overview

AyuPulse moves users through a structured preventive wellness journey:
$$\text{User} \longrightarrow \text{Input} \longrightarrow \text{AI Engine} \longrightarrow \text{Decision} \longrightarrow \text{Action} \longrightarrow \text{Outcome}$$

Instead of offering generic articles or functioning as an open-ended chatbot, AyuPulse translates individual sleep, digestion, stress, energy, and lifestyle tendencies into concrete, daily preventive practices (Dinacharya, Yoga, Pranayama, and Diet).

---

## Modules Architecture

| Module | Name | Status | Description |
|---|---|---|---|
| **01** | **AI Prakriti Assessment** | **Complete** | Deterministic Vata/Pitta/Kapha scoring engine + Claude AI interpretation with graceful offline fallback. |
| **02** | **Personalized Preventive Plan** | **Active Contract** | Structured daily routines (What, Why, How, Safety) tailored to dominant constitution. |
| **03** | **Check-in & Pattern Insight** | **Active Contract** | 30-second check-in (Sleep, Stress, Mood, Digestion) + 0–100 Wellness Pulse + plan adjustment trigger. |
| **04** | **Guardrails & Escalation** | **Ready** | Real-time clinical boundary enforcement and red-flag emergency detection. |
| **05** | **AYUSH Centres Connect** | **Ready** | Directory of verified national AYUSH institutes and consultation booking. |
| **06** | **Population Scale** | **Roadmap** | Anonymized longitudinal epidemiological pattern aggregation. |

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
│   └── centres.py             # GET /api/centres, POST /api/consultation
├── services/
│   ├── __init__.py
│   ├── scoring.py             # Deterministic Vata/Pitta/Kapha scoring & normalization
│   ├── claude_service.py      # Claude API integration with robust offline fallback
│   ├── pattern.py             # 0-100 Wellness Pulse & recurring pattern analysis
│   └── safety.py              # Clinical boundary sanitization & emergency red-flag checks
├── prompts/
│   ├── __init__.py
│   └── prakriti_prompt.py     # Cautious, compliant AI interpretation prompt
└── data/
    ├── history.json           # Prototype seeded 14-day check-in history
    └── centres.json           # Verified AYUSH institutes database
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

## API Contract: `POST /api/assessment`

### Request Payload (`AssessmentRequest`)
```json
{
  "sleep": "light_restless",
  "digestion": "sharp_fast",
  "stress_response": "anxious_worry",
  "energy": "high_sustained",
  "body_tendencies": "cool_solid_heavy",
  "lifestyle": "irregular_active",
  "wellness_goals": ["sleep consistency", "stress relief"]
}
```

### Response Payload (`AssessmentResponse`)
```json
{
  "vata": 50,
  "pitta": 33,
  "kapha": 17,
  "dominant": "Vata",
  "summary": "Your responses indicate a prominent Vata constitution (50%), characterized by qualities of air and ether — lightness, creativity, agility, and natural adaptability...",
  "wellness_focus": [
    "Warm water and grounding herbal teas on waking",
    "Gentle morning asana (Child's pose, gentle forward bends)",
    "Nadi Shodhana (alternate nostril breathing) for nervous system balance",
    "Regular warm, cooked meals and fixed bedtime routine"
  ],
  "note": "This is a traditional wellness-oriented interpretation, not a medical diagnosis."
}
```

---

## Safety & Medical Non-Claim Notice

AyuPulse adheres strictly to preventive wellness communication:
- Results are presented exclusively as **traditional wellness tendencies**, never medical diagnoses.
- Prescriptive clinical language is sanitized and prohibited.
- Acute or red-flag emergency symptoms are routed toward emergency healthcare facilities.
