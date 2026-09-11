import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { AssessmentResponse } from '../api/client';

export function ResultPage() {
  const navigate = useNavigate();
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem('ayupulse_assessment');
    if (stored) {
      try {
        setAssessment(JSON.parse(stored));
      } catch {
        setAssessment(null);
      }
    }
    setLoading(false);
  }, []);

  if (loading) {
    return <div className="container--narrow" style={{ paddingTop: 80, textAlign: 'center' }}>Loading assessment result…</div>;
  }

  if (!assessment) {
    return (
      <div className="container--narrow" style={{ paddingTop: 80, textAlign: 'center' }}>
        <h2 style={{ marginBottom: 12 }}>No assessment result found</h2>
        <p style={{ color: 'var(--color-text-muted)', marginBottom: 24 }}>Complete the AYUSH assessment to see your wellness profile.</p>
        <button className="btn btn--primary" onClick={() => navigate('/assessment')}>
          Start assessment →
        </button>
      </div>
    );
  }

  const dominantColor =
    assessment.dominant === 'Vata' ? 'var(--color-vata)' :
    assessment.dominant === 'Pitta' ? 'var(--color-pitta)' : 'var(--color-kapha)';

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '40px 20px 80px' }}>
      <div className="container--narrow fade-in">
        <div className="card card--elevated" style={{ padding: '30px 24px', textAlign: 'center' }}>
          <span className="badge badge--brand" style={{ marginBottom: 12 }}>Assessment complete</span>
          <h1 style={{ marginBottom: 8 }}>Your wellness tendency</h1>
          <div style={{
            display: 'inline-block',
            padding: '8px 16px',
            borderRadius: 'var(--radius-full)',
            background: `${dominantColor}15`,
            color: dominantColor,
            fontWeight: 700,
            marginBottom: 20,
          }}>
            {assessment.dominant} dominant
          </div>

          <div style={{ display: 'grid', gap: 12, textAlign: 'left', marginBottom: 22 }}>
            {[
              { label: 'Vata', value: assessment.vata },
              { label: 'Pitta', value: assessment.pitta },
              { label: 'Kapha', value: assessment.kapha },
            ].map(item => (
              <div key={item.label}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                  <span>{item.label}</span>
                  <strong>{item.value}%</strong>
                </div>
                <div className="progress-bar-track" style={{ height: 8 }}>
                  <div className="progress-bar-fill" style={{ width: `${item.value}%`, background: dominantColor }} />
                </div>
              </div>
            ))}
          </div>

          <p style={{ color: 'var(--color-text-muted)', lineHeight: 1.7, marginBottom: 20 }}>
            {assessment.summary}
          </p>

          <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
            <button className="btn btn--primary" onClick={() => navigate('/plan')}>
              View preventive plan →
            </button>
            <button className="btn btn--ghost" onClick={() => navigate('/assessment')}>
              Retake assessment
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
