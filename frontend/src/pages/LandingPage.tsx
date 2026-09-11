import { useNavigate } from 'react-router-dom';

export function LandingPage() {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)' }}>
      {/* Hero */}
      <section style={{
        background: 'linear-gradient(135deg, #F0F7F4 0%, #FDFAF6 50%, #F5EDE3 100%)',
        padding: '80px 20px 100px',
        textAlign: 'center',
        borderBottom: '1px solid var(--color-border-light)',
      }}>
        <div className="container--narrow fade-in">
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 8,
            background: 'var(--color-brand-pale)', borderRadius: 'var(--radius-full)',
            padding: '6px 16px', marginBottom: 24,
          }}>
            <span style={{ fontSize: '1rem' }}>🌿</span>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--color-brand)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
              AYUSH · Preventive Wellness
            </span>
          </div>

          <h1 style={{ marginBottom: 16, color: 'var(--color-text)' }}>
            Preventive wellness,<br />
            <span style={{ color: 'var(--color-brand)' }}>rooted in AYUSH.</span>
          </h1>

          <p style={{
            fontSize: '1.15rem', color: 'var(--color-text-muted)', marginBottom: 40,
            lineHeight: 1.7, maxWidth: 480, margin: '0 auto 40px',
          }}>
            Understand your traditional wellness tendency. Get a personalized
            preventive plan. Track your daily wellbeing — all guided by ancient
            wisdom and modern AI.
          </p>

          <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              className="btn btn--primary btn--lg pulse-glow"
              onClick={() => navigate('/assessment')}
            >
              Start Your Assessment →
            </button>
            <button
              className="btn btn--secondary btn--lg"
              onClick={() => navigate('/dashboard')}
            >
              View Dashboard
            </button>
          </div>

          <p style={{ fontSize: '0.8rem', color: 'var(--color-text-light)', marginTop: 20 }}>
            Takes about 3–5 minutes · Traditional wellness tendency · Not a medical diagnosis
          </p>
        </div>
      </section>

      {/* Journey steps */}
      <section style={{ padding: '64px 20px' }}>
        <div className="container">
          <h2 style={{ textAlign: 'center', marginBottom: 8 }}>Your Wellness Journey</h2>
          <p style={{ textAlign: 'center', color: 'var(--color-text-muted)', marginBottom: 48, fontSize: '1rem' }}>
            A complete preventive action system — not a chatbot.
          </p>
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 20,
          }}>
            {[
              {
                icon: '🔍', num: '01', title: 'Prakriti Assessment',
                desc: 'Answer 15 questions about sleep, digestion, energy, stress and lifestyle. Our scoring engine identifies your Vata, Pitta, and Kapha tendencies.',
                route: '/assessment', cta: 'Start Assessment',
              },
              {
                icon: '📋', num: '02', title: 'Personalized Plan',
                desc: 'Get a daily preventive routine customized to your constitution — Dinacharya, Yoga, Pranayama, Diet and Lifestyle practices with clear guidance.',
                route: '/plan', cta: 'View My Plan',
              },
              {
                icon: '📊', num: '03', title: 'Track & Improve',
                desc: '30-second daily check-ins. Pattern detection. Wellness Score. When recurring patterns emerge, your plan automatically adjusts.',
                route: '/dashboard', cta: 'Open Dashboard',
              },
            ].map(step => (
              <div key={step.num} className="card card--elevated fade-in" style={{ position: 'relative', overflow: 'hidden' }}>
                <div style={{
                  position: 'absolute', top: 12, right: 16,
                  font: '4rem/1 var(--font-serif)', color: 'var(--color-border-light)',
                  fontWeight: 700, userSelect: 'none',
                }}>
                  {step.num}
                </div>
                <div style={{ fontSize: '2rem', marginBottom: 12 }}>{step.icon}</div>
                <h3 style={{ marginBottom: 8 }}>{step.title}</h3>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem', lineHeight: 1.6, marginBottom: 20 }}>
                  {step.desc}
                </p>
                <button
                  className="btn btn--secondary"
                  onClick={() => navigate(step.route)}
                  style={{ fontSize: '0.85rem' }}
                >
                  {step.cta} →
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* What is AYUSH */}
      <section style={{ background: 'var(--color-brand-pale)', padding: '56px 20px' }}>
        <div className="container--narrow" style={{ textAlign: 'center' }}>
          <h2 style={{ marginBottom: 16 }}>What is AYUSH?</h2>
          <p style={{ color: 'var(--color-text-muted)', lineHeight: 1.8, marginBottom: 24 }}>
            AYUSH represents India's traditional health systems —{' '}
            <strong>Ayurveda, Yoga, Unani, Siddha, and Homeopathy</strong>. AyuPulse
            draws primarily from Ayurveda's ancient framework of Prakriti (individual
            constitution) to offer a personalized preventive wellness experience.
          </p>
          <div className="disclaimer">
            <span>⚠️</span>
            <span>
              AyuPulse provides traditional wellness tendency guidance only — not medical diagnoses,
              treatments, or clinical recommendations. For any health concern, please consult a
              qualified healthcare professional.
            </span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid var(--color-border-light)',
        padding: '32px 20px',
        textAlign: 'center',
        color: 'var(--color-text-light)',
        fontSize: '0.85rem',
      }}>
        <strong style={{ color: 'var(--color-brand)', fontFamily: 'var(--font-serif)' }}>AyuPulse</strong>
        {' · '}Preventive wellness, rooted in AYUSH. Personalized by AI.
        <br />
        <span style={{ fontSize: '0.75rem', marginTop: 4, display: 'block' }}>
          Traditional wellness guidance · Not a medical diagnosis system
        </span>
      </footer>
    </div>
  );
}
