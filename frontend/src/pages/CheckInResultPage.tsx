import { useLocation, useNavigate } from 'react-router-dom';
import type { CheckInResponse } from '../api/client';

export function CheckInResultPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const result = (location.state as { result?: CheckInResponse } | undefined)?.result ??
    JSON.parse(localStorage.getItem('ayupulse_latest_checkin') || 'null') as CheckInResponse | null;

  const wellnessScore = result?.wellness_score ?? 82;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '40px 20px 80px' }}>
      <div className="container--narrow fade-in">
        <div className="card card--elevated" style={{ textAlign: 'center', padding: '32px 24px' }}>
          <span className="badge badge--brand" style={{ marginBottom: 12 }}>Check-in complete</span>
          <h1 style={{ marginBottom: 12 }}>Your wellness pulse</h1>

          <div style={{
            width: 110,
            height: 110,
            borderRadius: '50%',
            margin: '0 auto 18px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'conic-gradient(var(--color-brand) 0deg 290deg, var(--color-border-light) 290deg 360deg)',
            boxShadow: 'var(--shadow-md)',
          }}>
            <div style={{
              width: 80,
              height: 80,
              borderRadius: '50%',
              background: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: 'var(--font-serif)',
              fontSize: '1.5rem',
              fontWeight: 700,
              color: 'var(--color-brand)',
            }}>
              {wellnessScore}
            </div>
          </div>

          <p style={{ color: 'var(--color-text-muted)', lineHeight: 1.7, marginBottom: 18 }}>
            {result?.summary ?? 'Your wellness rhythm is trending positively. Keep supporting sleep, digestion, and a steady morning routine.'}
          </p>

          <div style={{ display: 'flex', justifyContent: 'center', gap: 12, flexWrap: 'wrap' }}>
            <button className="btn btn--primary" onClick={() => navigate('/dashboard')}>
              View community dashboard
            </button>
            <button className="btn btn--ghost" onClick={() => navigate('/plan')}>
              Return to plan
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
