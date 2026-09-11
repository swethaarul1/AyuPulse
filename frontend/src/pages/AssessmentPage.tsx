import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ayuApi, { Question } from '../api/client';

const CATEGORY_COLORS: Record<string, string> = {
  Sleep: '#5B7FA6',
  Digestion: '#4D8B72',
  Stress: '#C77D3A',
  Energy: '#8B5E3C',
  Body: '#6D6875',
  Lifestyle: '#2D6A4F',
};

export function AssessmentPage() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [current, setCurrent] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    ayuApi.getQuestions().then(data => {
      setQuestions(data.questions);
      setLoading(false);
    }).catch(() => {
      setError('Could not load questions. Please ensure the backend is running.');
      setLoading(false);
    });
  }, []);

  const q = questions[current];
  const progress = questions.length > 0 ? ((current) / questions.length) * 100 : 0;
  const totalAnswered = Object.keys(answers).length;

  const handleSelect = (idx: number) => {
    if (!q) return;
    setAnswers(prev => ({ ...prev, [q.id]: idx }));
  };

  const handleNext = () => {
    if (current < questions.length - 1) {
      setCurrent(c => c + 1);
    }
  };

  const handleBack = () => {
    if (current > 0) setCurrent(c => c - 1);
  };

  const handleSubmit = async () => {
    if (totalAnswered < questions.length) {
      setError(`Please answer all ${questions.length} questions before submitting.`);
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      const result = await ayuApi.submitAssessment(answers);
      // Store in localStorage for next page
      localStorage.setItem('ayupulse_assessment', JSON.stringify(result));
      navigate('/assessment/result', { state: { assessment: result } });
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Submission failed. Please try again.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-center">
        <div className="loading-spinner" />
        <p>Loading your assessment…</p>
      </div>
    );
  }

  if (!q) return null;

  const catColor = CATEGORY_COLORS[q.category] || 'var(--color-brand)';
  const isAnswered = q.id in answers;
  const selectedIdx = answers[q.id];
  const isLast = current === questions.length - 1;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', paddingBottom: 48 }}>
      {/* Progress bar */}
      <div style={{ background: 'var(--color-border-light)', height: 4 }}>
        <div style={{
          width: `${progress}%`, height: '100%',
          background: 'var(--color-brand)',
          transition: 'width 0.4s ease',
        }} />
      </div>

      <div className="container--narrow" style={{ paddingTop: 40 }}>
        {/* Header */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <span className="badge" style={{ background: `${catColor}20`, color: catColor }}>
              {q.category}
            </span>
            <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', fontWeight: 500 }}>
              {current + 1} / {questions.length}
            </span>
          </div>

          <h2 style={{ marginBottom: 8, lineHeight: 1.3 }}>{q.text}</h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--color-text-light)' }}>
            Choose the option that best describes your general tendency
          </p>
        </div>

        {/* Options */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 32 }}>
          {q.options.map((opt, idx) => (
            <button
              key={idx}
              className={`option-card ${selectedIdx === idx ? 'option-card--selected' : ''}`}
              onClick={() => handleSelect(idx)}
            >
              <span style={{ marginRight: 10, opacity: 0.5 }}>
                {String.fromCharCode(65 + idx)}.
              </span>
              {opt.label}
            </button>
          ))}
        </div>

        {/* Navigation */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <button
            className="btn btn--ghost"
            onClick={handleBack}
            disabled={current === 0}
          >
            ← Back
          </button>

          {isLast ? (
            <button
              className="btn btn--primary btn--lg"
              onClick={handleSubmit}
              disabled={submitting || !isAnswered}
            >
              {submitting ? 'Analyzing…' : 'Get My Result →'}
            </button>
          ) : (
            <button
              className="btn btn--primary"
              onClick={handleNext}
              disabled={!isAnswered}
            >
              Next →
            </button>
          )}
        </div>

        {/* Jump to unanswered */}
        {isLast && totalAnswered < questions.length && (
          <div style={{ marginTop: 20, textAlign: 'center' }}>
            <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: 12 }}>
              {questions.length - totalAnswered} question(s) unanswered. Click any question number to go back.
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, justifyContent: 'center' }}>
              {questions.map((qq, i) => (
                <button
                  key={i}
                  onClick={() => setCurrent(i)}
                  style={{
                    width: 28, height: 28, borderRadius: '50%', border: 'none',
                    background: qq.id in answers ? 'var(--color-brand)' : 'var(--color-border)',
                    color: qq.id in answers ? 'white' : 'var(--color-text-muted)',
                    fontSize: '0.75rem', cursor: 'pointer', fontWeight: 600,
                  }}
                >
                  {i + 1}
                </button>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div style={{
            marginTop: 20, padding: '12px 16px', background: '#FEE2E2',
            borderRadius: 'var(--radius-md)', color: 'var(--color-error)', fontSize: '0.9rem',
          }}>
            ⚠️ {error}
          </div>
        )}

        {/* Disclaimer */}
        <div className="disclaimer" style={{ marginTop: 32 }}>
          <span>🌿</span>
          <span>Traditional wellness tendency assessment — not a medical diagnosis. Answer based on your general patterns over the past few months.</span>
        </div>
      </div>
    </div>
  );
}
