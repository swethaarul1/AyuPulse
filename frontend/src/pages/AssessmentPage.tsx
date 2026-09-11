import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, ArrowRight, CheckCircle2, RotateCcw, Sparkles } from 'lucide-react';
import ayuApi from '../api/client';
import type { Question, AssessmentResponse } from '../api/client';

const CATEGORY_COLORS: Record<string, string> = {
  Sleep: '#456E94',
  Digestion: '#3E7C65',
  'Stress Response': '#C26A28',
  Stress: '#C26A28',
  'Energy Patterns': '#7A4E2D',
  Energy: '#7A4E2D',
  'Body Tendencies': '#52605B',
  Body: '#52605B',
  'Lifestyle Habits': '#1E5C41',
  Lifestyle: '#1E5C41',
};

export function AssessmentPage() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [currentIdx, setCurrentIdx] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<AssessmentResponse | null>(null);

  useEffect(() => {
    // Check if there is already an existing result in localStorage
    const saved = localStorage.getItem('ayupulse_assessment');
    if (saved) {
      try {
        setResult(JSON.parse(saved));
      } catch {}
    }

    // Load dynamic questions from backend
    ayuApi.getQuestions()
      .then(data => {
        if (data && data.questions && data.questions.length > 0) {
          setQuestions(data.questions);
        } else {
          // Fallback static questions if needed
          setQuestions(getDefaultQuestions());
        }
        setLoading(false);
      })
      .catch(() => {
        setQuestions(getDefaultQuestions());
        setLoading(false);
      });
  }, []);

  function getDefaultQuestions(): Question[] {
    return [
      {
        id: 'sleep',
        category: 'Sleep',
        question: 'How would you describe your typical sleep pattern?',
        options: [
          { value: 'light_restless', label: 'Light, easily disrupted, prone to racing thoughts or insomnia' },
          { value: 'moderate_sound', label: 'Moderate and sound, but wake up easily if hot or thirsty' },
          { value: 'deep_heavy', label: 'Deep, heavy, long sleep; difficult to wake up in the morning' },
        ]
      },
      {
        id: 'digestion',
        category: 'Digestion',
        question: 'What is your regular digestion and appetite like?',
        options: [
          { value: 'irregular_variable', label: 'Variable appetite; occasional gas, bloating, or irregular timing' },
          { value: 'sharp_fast', label: 'Strong, intense hunger; irritable if meals are missed; occasional acidity' },
          { value: 'slow_steady', label: 'Steady but slow digestion; feeling heavy or sleepy after meals' },
        ]
      },
      {
        id: 'stress_response',
        category: 'Stress Response',
        question: 'When under acute pressure or stress, how do you typically react?',
        options: [
          { value: 'anxious_worry', label: 'Anxiety, racing thoughts, worry, feeling scattered or restless' },
          { value: 'irritable_intense', label: 'Irritability, impatience, sharp frustration, intense focus' },
          { value: 'withdrawn_slow', label: 'Withdrawal, resistance to change, procrastination, low motivation' },
        ]
      },
      {
        id: 'energy',
        category: 'Energy Patterns',
        question: 'How do your energy levels fluctuate during the day?',
        options: [
          { value: 'variable_bursts', label: 'Bursts of quick energy followed by sudden afternoon fatigue' },
          { value: 'high_sustained', label: 'Strong, focused drive; tendency to push until burned out' },
          { value: 'steady_calm', label: 'Slow to get started, but steady and calm endurance all day' },
        ]
      },
      {
        id: 'body_tendencies',
        category: 'Body Tendencies',
        question: 'Which physical traits best describe your natural frame and skin?',
        options: [
          { value: 'dry_cold_slender', label: 'Slender frame, dry skin or cold extremities, sensitive to chilly weather' },
          { value: 'warm_medium_athletic', label: 'Medium athletic frame, warm body temperature, sensitive or oily skin' },
          { value: 'cool_solid_heavy', label: 'Broad or solid frame, cool smooth skin, tendency to retain fluids' },
        ]
      },
      {
        id: 'lifestyle',
        category: 'Lifestyle Habits',
        question: 'What does your daily routine look like?',
        options: [
          { value: 'irregular_active', label: 'Spontaneous schedule, irregular meal times, frequent multitasking' },
          { value: 'competitive_demanding', label: 'Goal-oriented, intense schedule, high mental or physical activity' },
          { value: 'routine_sedentary', label: 'Consistent routine, relaxed pace, preference for comfort and stability' },
        ]
      }
    ];
  }

  const currentQ = questions[currentIdx];
  const totalQuestions = questions.length;
  const progressPct = totalQuestions > 0 ? ((currentIdx + 1) / totalQuestions) * 100 : 0;
  const isAnswered = currentQ && Boolean(answers[currentQ.id]);

  const handleSelectOption = (val: string) => {
    if (!currentQ) return;
    setAnswers(prev => ({ ...prev, [currentQ.id]: val }));
  };

  const handleNext = () => {
    if (currentIdx < totalQuestions - 1) {
      setCurrentIdx(i => i + 1);
    }
  };

  const handleBack = () => {
    if (currentIdx > 0) {
      setCurrentIdx(i => i - 1);
    }
  };

  const generateFallbackAssessment = (): AssessmentResponse => {
    const vataKeys = ['light_restless', 'anxious_worry', 'variable_bursts', 'dry_cold_slender', 'irregular_active'];
    const pittaKeys = ['sharp_fast', 'irritable_intense', 'high_sustained', 'warm_medium_athletic', 'competitive_demanding'];
    const kaphaKeys = ['deep_heavy', 'withdrawn_slow', 'slow_steady', 'cool_solid_heavy', 'routine_sedentary'];

    const score = { Vata: 0, Pitta: 0, Kapha: 0 };

    Object.values(answers).forEach((value) => {
      if (vataKeys.includes(value)) score.Vata += 1;
      if (pittaKeys.includes(value)) score.Pitta += 1;
      if (kaphaKeys.includes(value)) score.Kapha += 1;
    });

    const total = score.Vata + score.Pitta + score.Kapha || 1;
    const vata = Math.round((score.Vata / total) * 100);
    const pitta = Math.round((score.Pitta / total) * 100);
    const kapha = Math.round((score.Kapha / total) * 100);

    const dominant =
      score.Vata >= score.Pitta && score.Vata >= score.Kapha ? 'Vata' :
      score.Pitta >= score.Kapha ? 'Pitta' : 'Kapha';

    const summary =
      dominant === 'Vata'
        ? 'Your response pattern suggests a light, mobile rhythm with a tendency toward variability in sleep, stress, and daily pacing.'
        : dominant === 'Pitta'
          ? 'Your response pattern suggests a focused, transformation-oriented rhythm with strong drive and heat-sensitive tendencies.'
          : 'Your response pattern suggests a steady, grounding rhythm with stronger stability, comfort, and consistency needs.';

    return {
      vata,
      pitta,
      kapha,
      dominant,
      summary,
      wellness_focus: ['routine rhythm', 'restorative recovery', 'mindful pacing'],
      note: 'Prototype assessment generated locally because the backend service is unavailable.',
    };
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError('');

    try {
      const payload = {
        sleep: answers.sleep,
        digestion: answers.digestion,
        stress_response: answers.stress_response,
        energy: answers.energy,
        body_tendencies: answers.body_tendencies,
        lifestyle: answers.lifestyle,
        wellness_goals: ['daily balance', 'energy rhythm'],
        answers: answers,
      };

      const res = await ayuApi.submitAssessment(payload);
      setResult(res);
      setSubmitting(false);
    } catch {
      const fallback = generateFallbackAssessment();
      setResult(fallback);
      localStorage.setItem('ayupulse_assessment', JSON.stringify(fallback));
      setSubmitting(false);
    }
  };

  const handleBuildPlan = async () => {
    if (!result) return;
    try {
      await ayuApi.generatePlan({
        dominant: result.dominant,
        vata: result.vata,
        pitta: result.pitta,
        kapha: result.kapha,
        lifestyle: answers.lifestyle,
        wellness_goals: result.wellness_focus,
      });
      navigate('/plan');
    } catch {
      const fallbackPlan = {
        status: 'ok',
        module: 'plan',
        dominant: result.dominant,
        sections: {
          dinacharya: [
            { title: 'Grounding wake-up', what: 'Hydrate and begin slowly.', why: 'Supports smooth rhythm and steadiness.', how: 'Drink warm water, stretch lightly, breathe deeply.', safety: 'Keep it gentle and unforced.' },
            { title: 'Daily reset', what: 'Protect one calm pause in the day.', why: 'Helps prevent overwhelm and keeps energy balanced.', how: 'Take 10 minutes to breathe, step away from screens, and reset.', safety: 'Pause if you feel overstimulated.' },
          ],
          yoga: [
            { title: 'Gentle mobility', what: 'Low-intensity movement for ease and grounding.', why: 'Supports Vata, Pitta, or Kapha balancing.', how: 'Move slowly and breathe steadily for 10–15 minutes.', safety: 'Avoid strain or forceful extremes.' },
          ],
          pranayama: [
            { title: 'Calm breath cycle', what: 'Nasal breathing with a slower exhale.', why: 'Encourages nervous system steadiness.', how: 'Take 5 minutes of slow inhale and longer exhale.', safety: 'Stop if dizzy or lightheaded.' },
          ],
          diet_lifestyle: [
            { title: 'Regular rhythm', what: 'Set consistent meal and sleep times.', why: 'Consistency supports sustainable wellness.', how: 'Keep meals regular and reduce last-minute overload.', safety: 'Evening meals should remain light and easy to digest.' },
          ],
        },
        daily_tracker: [
          { id: 'hydrate', title: 'Hydrate and wake gently', description: 'Begin with water and a slow morning routine.', completed: false },
          { id: 'breath', title: 'Breath reset', description: 'Take 5 minutes for calming pranayama.', completed: false },
          { id: 'meal', title: 'Grounding meal rhythm', description: 'Eat warm, consistent meals at regular intervals.', completed: false },
        ],
        message: 'Prototype plan generated locally because the backend is unavailable.',
        note: 'This is a seeded preview plan for demo usage.',
      };

      localStorage.setItem('ayupulse_plan', JSON.stringify(fallbackPlan));
      navigate('/plan');
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 20px' }}>
        <div style={{ width: 44, height: 44, border: '4px solid var(--color-border)', borderTopColor: 'var(--color-brand)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 16px' }} />
        <p style={{ color: 'var(--color-text-muted)' }}>Loading wellness questions...</p>
      </div>
    );
  }

  // ── DISPLAY RESULT STATE ──────────────────────────────────────────────────
  if (result) {
    const dominantColor =
      result.dominant === 'Vata' ? 'var(--color-vata)' :
      result.dominant === 'Pitta' ? 'var(--color-pitta)' : 'var(--color-kapha)';

    return (
      <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '48px 20px 80px' }}>
        <div className="container--narrow fade-in">
          {/* Result Header */}
          <div style={{ textAlign: 'center', marginBottom: 32 }}>
            <span className="badge badge--brand" style={{ marginBottom: 12 }}>
              Module 01 · Assessment Completed
            </span>
            <h1 style={{ marginBottom: 8 }}>Your Wellness Constitution</h1>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '1.05rem' }}>
              Prakriti breakdown derived from deterministic scoring & AI interpretation
            </p>
          </div>

          {/* Constitution Card */}
          <div className="card card--elevated" style={{ marginBottom: 24, textAlign: 'center', padding: '36px 24px' }}>
            <div style={{
              display: 'inline-flex', padding: '6px 16px', borderRadius: 'var(--radius-full)',
              background: `${dominantColor}15`, color: dominantColor, fontWeight: 700,
              fontSize: '0.9rem', marginBottom: 16, textTransform: 'uppercase', letterSpacing: '0.05em'
            }}>
              Dominant Tendency: {result.dominant}
            </div>

            <h2 style={{ fontSize: '2.5rem', color: dominantColor, marginBottom: 20 }}>
              {result.dominant} Constitution
            </h2>

            {/* Dosha Percentages */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, maxWidth: 440, margin: '0 auto 28px' }}>
              {[
                { name: 'Vata', pct: result.vata, color: 'var(--color-vata)' },
                { name: 'Pitta', pct: result.pitta, color: 'var(--color-pitta)' },
                { name: 'Kapha', pct: result.kapha, color: 'var(--color-kapha)' },
              ].map(d => (
                <div key={d.name} style={{
                  background: 'var(--color-bg)', padding: '16px 12px', borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--color-border-light)'
                }}>
                  <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', fontWeight: 600 }}>{d.name}</div>
                  <div style={{ fontFamily: 'var(--font-serif)', fontSize: '1.85rem', fontWeight: 700, color: d.color }}>
                    {d.pct}%
                  </div>
                </div>
              ))}
            </div>

            {/* What this means */}
            <div style={{ textAlign: 'left', background: 'var(--color-bg)', padding: 20, borderRadius: 'var(--radius-md)', marginBottom: 24 }}>
              <h4 style={{ marginBottom: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
                <Sparkles size={18} color="var(--color-brand)" />
                What this means for your daily rhythm
              </h4>
              <p style={{ color: 'var(--color-text)', fontSize: '0.95rem', lineHeight: 1.65 }}>
                {result.summary}
              </p>
            </div>

            {/* Key Daily Wellness Focus Areas */}
            {result.wellness_focus && result.wellness_focus.length > 0 && (
              <div style={{ textAlign: 'left', marginBottom: 24 }}>
                <h4 style={{ marginBottom: 12 }}>Recommended Wellness Focus Areas:</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {result.wellness_focus.map((item, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: '0.9rem', color: 'var(--color-text)' }}>
                      <CheckCircle2 size={16} color="var(--color-brand)" style={{ flexShrink: 0 }} />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Mandatory Non-Diagnostic Disclaimer */}
            <div className="disclaimer" style={{ textAlign: 'left', marginBottom: 28 }}>
              <span>🌿</span>
              <span><strong>Notice:</strong> {result.note}</span>
            </div>

            {/* ACTION CTAs */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <button
                className="btn btn--primary btn--lg"
                onClick={handleBuildPlan}
                style={{ width: '100%' }}
              >
                <span>Build My Personalized Plan →</span>
              </button>

              <button
                className="btn btn--pulse btn--lg pulse-glow"
                onClick={() => navigate('/tracker')}
                style={{ width: '100%' }}
              >
                <Activity size={18} className="pulse-icon" />
                <span>Go to My Daily Pulse</span>
                <ArrowRight size={18} />
              </button>
            </div>

            <button
              className="btn btn--ghost btn--sm"
              onClick={() => { setResult(null); setCurrentIdx(0); }}
              style={{ marginTop: 20 }}
            >
              <RotateCcw size={14} />
              <span>Retake Assessment</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── MULTI-STEP QUESTIONNAIRE STATE ─────────────────────────────────────────
  if (!currentQ) return null;

  const catColor = CATEGORY_COLORS[currentQ.category] || 'var(--color-brand)';
  const isLast = currentIdx === totalQuestions - 1;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', paddingBottom: 64 }}>
      {/* Top progress line */}
      <div style={{ background: 'var(--color-border-light)', height: 5 }}>
        <div style={{
          width: `${progressPct}%`, height: '100%', background: 'var(--color-brand)',
          transition: 'width 0.3s ease',
        }} />
      </div>

      <div className="container--narrow" style={{ paddingTop: 40 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <span className="badge" style={{ background: `${catColor}18`, color: catColor }}>
            {currentQ.category}
          </span>
          <span style={{ fontSize: '0.88rem', color: 'var(--color-text-muted)', fontWeight: 600 }}>
            Question {currentIdx + 1} of {totalQuestions}
          </span>
        </div>

        <h2 style={{ fontSize: '1.65rem', lineHeight: 1.35, marginBottom: 8 }}>
          {currentQ.question || currentQ.text}
        </h2>
        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem', marginBottom: 28 }}>
          Select the tendency that best describes your typical state over recent months.
        </p>

        {/* Options List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 36 }}>
          {currentQ.options.map((opt, i) => {
            const val = opt.value || opt.label;
            const selected = answers[currentQ.id] === val;
            return (
              <div
                key={i}
                onClick={() => handleSelectOption(val)}
                style={{
                  padding: '16px 20px',
                  borderRadius: 'var(--radius-md)',
                  border: selected ? '2px solid var(--color-brand)' : '1.5px solid var(--color-border)',
                  background: selected ? 'var(--color-brand-pale)' : 'white',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 14,
                  transition: 'all 0.2s ease',
                  boxShadow: selected ? 'var(--shadow-sm)' : 'none',
                }}
              >
                <div style={{
                  width: 22, height: 22, borderRadius: '50%',
                  border: selected ? '6px solid var(--color-brand)' : '2px solid var(--color-border)',
                  background: 'white', flexShrink: 0,
                }} />
                <span style={{
                  fontSize: '0.95rem',
                  fontWeight: selected ? 600 : 400,
                  color: selected ? 'var(--color-brand)' : 'var(--color-text)',
                }}>
                  {opt.label}
                </span>
              </div>
            );
          })}
        </div>

        {error && (
          <div style={{ padding: 12, background: '#FEE2E2', color: '#991B1B', borderRadius: 'var(--radius-md)', marginBottom: 20, fontSize: '0.9rem' }}>
            ⚠️ {error}
          </div>
        )}

        {/* Navigation Buttons */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <button
            className="btn btn--ghost"
            onClick={handleBack}
            disabled={currentIdx === 0}
          >
            ← Back
          </button>

          {isLast ? (
            <button
              className="btn btn--primary btn--lg"
              onClick={handleSubmit}
              disabled={!isAnswered || submitting}
            >
              {submitting ? 'Analyzing Responses...' : 'Get My Constitution →'}
            </button>
          ) : (
            <button
              className="btn btn--primary"
              onClick={handleNext}
              disabled={!isAnswered}
            >
              Next Question →
            </button>
          )}
        </div>

        {/* Disclaimer */}
        <div className="disclaimer" style={{ marginTop: 40 }}>
          <span>🌿</span>
          <span>AyuPulse Prakriti Assessment evaluates traditional AYUSH tendencies — not a clinical diagnosis.</span>
        </div>
      </div>
    </div>
  );
}
