import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Activity, Compass, ShieldCheck, Users, ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';
import ayuApi from '../api/client';
import type { AssessmentResponse, PlanResponse, CheckInResponse } from '../api/client';

export function LandingPage() {
  const navigate = useNavigate();
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null);
  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [latestCheckin, setLatestCheckin] = useState<CheckInResponse | null>(null);
  const [wellnessPulse, setWellnessPulse] = useState<number>(75);
  const [patternSummary, setPatternSummary] = useState<string>('Recurring sleep and stress relationship identified');

  useEffect(() => {
    // Load local stored state if available
    const storedAssessment = localStorage.getItem('ayupulse_assessment');
    if (storedAssessment) {
      try { setAssessment(JSON.parse(storedAssessment)); } catch {}
    }

    const storedPlan = localStorage.getItem('ayupulse_plan');
    if (storedPlan) {
      try { setPlan(JSON.parse(storedPlan)); } catch {}
    }

    const storedCheckin = localStorage.getItem('ayupulse_latest_checkin');
    if (storedCheckin) {
      try {
        const parsed = JSON.parse(storedCheckin);
        setLatestCheckin(parsed);
        if (parsed.wellness_score) setWellnessPulse(parsed.wellness_score);
      } catch {}
    }

    // Fetch live pattern insight
    ayuApi.getPatternQuick().then(data => {
      if (data && data.wellness_pulse) setWellnessPulse(data.wellness_pulse);
      if (data && data.insight) setPatternSummary(data.insight);
    }).catch(() => {});
  }, []);

  const tasks = plan?.daily_tracker || [];
  const completedTasks = tasks.filter(t => t.completed).length;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', paddingBottom: 64 }}>
      {/* Hero Section */}
      <section style={{
        background: 'linear-gradient(180deg, #EDF7F2 0%, #FAF8F4 100%)',
        padding: '64px 20px 72px',
        borderBottom: '1px solid var(--color-border-light)',
      }}>
        <div className="container--narrow fade-in" style={{ textAlign: 'center' }}>
          {/* Eyebrow badge */}
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 8,
            background: 'var(--color-brand-pale)', border: '1px solid var(--color-brand-border)',
            borderRadius: 'var(--radius-full)', padding: '6px 16px', marginBottom: 24,
          }}>
            <Sparkles size={16} color="var(--color-brand)" />
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--color-brand)', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
              Preventive Wellness · Rooted in AYUSH · Powered by AI
            </span>
          </div>

          <h1 style={{ marginBottom: 16, fontSize: 'clamp(2rem, 5vw, 3rem)', lineHeight: 1.15 }}>
            Preventive wellness,<br />
            <span style={{ color: 'var(--color-brand)' }}>rooted in AYUSH.</span><br />
            <span style={{ fontStyle: 'italic', fontWeight: 400 }}>Personalized by AI.</span>
          </h1>

          <p style={{
            fontSize: '1.15rem', color: 'var(--color-text-muted)', maxWidth: 540,
            margin: '0 auto 36px', lineHeight: 1.65,
          }}>
            Understand your traditional constitution. Receive a personalized daily Dinacharya and yoga routine.
            Track your wellness pulse in 30 seconds with automatic plan adaptations.
          </p>

          {/* Primary Action Buttons */}
          <div style={{ display: 'flex', gap: 14, justifyContent: 'center', flexWrap: 'wrap', marginBottom: 24 }}>
            <button
              className="btn btn--primary btn--lg"
              onClick={() => navigate('/assessment')}
              style={{ minWidth: 200 }}
            >
              <Compass size={18} />
              <span>Start Assessment</span>
            </button>

            <button
              className="btn btn--pulse btn--lg pulse-glow"
              onClick={() => navigate('/tracker')}
              style={{ minWidth: 200 }}
            >
              <Activity size={18} className="pulse-icon" />
              <span>My Daily Pulse</span>
              <ArrowRight size={16} />
            </button>
          </div>

          <div className="disclaimer disclaimer--prototype" style={{ maxWidth: 500, margin: '0 auto' }}>
            <span>🌿</span>
            <span>
              Traditional AYUSH constitutional assessment for preventive wellbeing — not a medical diagnosis system.
            </span>
          </div>
        </div>
      </section>

      {/* Command Center Snapshot */}
      <section style={{ padding: '48px 20px 64px' }}>
        <div className="container">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 24, flexWrap: 'wrap', gap: 12 }}>
            <div>
              <span className="badge badge--brand" style={{ marginBottom: 6 }}>Live Command Center</span>
              <h2>Your Wellness Overview</h2>
            </div>
            <Link to="/tracker" style={{ color: 'var(--color-brand)', fontWeight: 600, fontSize: '0.92rem', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 4 }}>
              Open My Daily Pulse →
            </Link>
          </div>

          {/* Grid of Command Center Cards */}
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20,
          }}>
            {/* 1. Daily Wellness Pulse */}
            <div className="card card--interactive fade-in" onClick={() => navigate('/tracker')}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                <div>
                  <span className="badge badge--brand">Module 03</span>
                  <h3 style={{ marginTop: 8 }}>Daily Wellness Pulse</h3>
                </div>
                <div style={{
                  width: 44, height: 44, borderRadius: '50%', background: 'var(--color-brand-pale)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-brand)',
                }}>
                  <Activity size={22} className="pulse-icon" />
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 8 }}>
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '2.8rem', fontWeight: 700, color: 'var(--color-brand)' }}>
                  {wellnessPulse}
                </span>
                <span style={{ color: 'var(--color-text-muted)', fontSize: '1.1rem' }}>/ 100</span>
              </div>
              <p style={{ fontSize: '0.88rem', color: 'var(--color-text-muted)', marginBottom: 14 }}>
                {latestCheckin ? latestCheckin.summary : 'Computed from your daily sleep, stress, mood, digestion & energy.'}
              </p>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', color: 'var(--color-brand)', fontWeight: 600 }}>
                <span>Take 30-sec Check-in →</span>
                <span className="badge badge--seeded">Seeded Trend</span>
              </div>
            </div>

            {/* 2. Today's Task Progress */}
            <div className="card card--interactive fade-in" onClick={() => navigate('/plan')}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                <div>
                  <span className="badge badge--earth">Module 02</span>
                  <h3 style={{ marginTop: 8 }}>Today's Tasks</h3>
                </div>
                <div style={{
                  width: 44, height: 44, borderRadius: '50%', background: 'var(--color-earth-pale)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-earth)',
                }}>
                  <CheckCircle2 size={22} />
                </div>
              </div>
              {tasks.length > 0 ? (
                <>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 8 }}>
                    <span style={{ fontFamily: 'var(--font-serif)', fontSize: '2.4rem', fontWeight: 700, color: 'var(--color-earth)' }}>
                      {completedTasks} / {tasks.length}
                    </span>
                    <span style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>completed</span>
                  </div>
                  <div className="progress-bar-track" style={{ marginBottom: 12 }}>
                    <div className="progress-bar-fill" style={{ width: `${(completedTasks / tasks.length) * 100}%`, background: 'var(--color-earth)' }} />
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>
                    Personalized daily Dinacharya, Yoga, and Pranayama checklist.
                  </p>
                </>
              ) : (
                <>
                  <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem', marginBottom: 16 }}>
                    No preventive plan loaded yet. Take the 3-minute assessment to unlock your daily tasks.
                  </p>
                  <button className="btn btn--secondary btn--sm" onClick={(e) => { e.stopPropagation(); navigate('/assessment'); }}>
                    Start Assessment →
                  </button>
                </>
              )}
            </div>

            {/* 3. Dosha Constitution */}
            <div className="card card--interactive fade-in" onClick={() => navigate('/assessment')}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                <div>
                  <span className="badge badge--vata">Module 01</span>
                  <h3 style={{ marginTop: 8 }}>Prakriti Tendency</h3>
                </div>
                <div style={{
                  width: 44, height: 44, borderRadius: '50%', background: 'var(--color-vata-pale)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-vata)',
                }}>
                  <Compass size={22} />
                </div>
              </div>
              {assessment ? (
                <>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-brand)', marginBottom: 8 }}>
                    {assessment.dominant} Dominant
                  </div>
                  <div style={{ display: 'flex', gap: 10, fontSize: '0.85rem', marginBottom: 12 }}>
                    <span>Vata: <strong>{assessment.vata}%</strong></span>
                    <span>Pitta: <strong>{assessment.pitta}%</strong></span>
                    <span>Kapha: <strong>{assessment.kapha}%</strong></span>
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>
                    {assessment.summary ? assessment.summary.slice(0, 95) + '...' : 'Traditional constitutional evaluation.'}
                  </p>
                </>
              ) : (
                <>
                  <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem', marginBottom: 16 }}>
                    Assess your natural Vata, Pitta, and Kapha constitution through 12 lifestyle questions.
                  </p>
                  <button className="btn btn--secondary btn--sm" onClick={(e) => { e.stopPropagation(); navigate('/assessment'); }}>
                    Take Assessment →
                  </button>
                </>
              )}
            </div>

            {/* 4. Latest Pattern Insight */}
            <div className="card card--interactive fade-in" onClick={() => navigate('/tracker')}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                <div>
                  <span className="badge badge--pitta">Module 03</span>
                  <h3 style={{ marginTop: 8 }}>Pattern Insight</h3>
                </div>
                <div style={{
                  width: 44, height: 44, borderRadius: '50%', background: 'var(--color-pitta-pale)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-pitta)',
                }}>
                  <Sparkles size={22} />
                </div>
              </div>
              <p style={{ fontSize: '0.9rem', color: 'var(--color-text)', lineHeight: 1.6, marginBottom: 12 }}>
                "{patternSummary}"
              </p>
              <div style={{ fontSize: '0.82rem', color: 'var(--color-pitta)', fontWeight: 600 }}>
                View Plan Adaptation in Daily Pulse →
              </div>
            </div>

            {/* 5. Safety Gate Status */}
            <div className="card card--interactive fade-in" onClick={() => navigate('/safety')}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                <div>
                  <span className="badge badge--safe">Module 05</span>
                  <h3 style={{ marginTop: 8 }}>Safety Gate</h3>
                </div>
                <div style={{
                  width: 44, height: 44, borderRadius: '50%', background: '#D1FAE5',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#065F46',
                }}>
                  <ShieldCheck size={22} />
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#10B981' }} />
                <span style={{ fontWeight: 600, color: '#065F46' }}>Gate Active & Enforced</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: 12 }}>
                Sanitizes non-clinical language, blocks diagnostic claims, and flags red-flag health emergencies.
              </p>
              <span style={{ fontSize: '0.82rem', color: 'var(--color-brand)', fontWeight: 600 }}>
                Inspect Safety Gate Demo →
              </span>
            </div>

            {/* 6. Community Wellness Snapshot */}
            <div className="card card--interactive fade-in" onClick={() => navigate('/community')}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                <div>
                  <span className="badge badge--brand">Module 06</span>
                  <h3 style={{ marginTop: 8 }}>Community Pulse</h3>
                </div>
                <div style={{
                  width: 44, height: 44, borderRadius: '50%', background: 'var(--color-brand-pale)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-brand)',
                }}>
                  <Users size={22} />
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 6 }}>
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '2.2rem', fontWeight: 700, color: 'var(--color-brand)' }}>
                  12,480
                </span>
                <span style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>assessments</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: 8 }}>
                68% active task adoption · Top pattern: Sleep + Stress
              </p>
              <div className="badge badge--seeded" style={{ fontSize: '0.72rem' }}>
                Prototype Simulation Data
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Core Product Journey */}
      <section style={{ background: 'var(--color-brand-pale)', padding: '56px 20px', borderTop: '1px solid var(--color-border-light)' }}>
        <div className="container">
          <h2 style={{ textAlign: 'center', marginBottom: 8 }}>The AyuPulse Experience</h2>
          <p style={{ textAlign: 'center', color: 'var(--color-text-muted)', marginBottom: 36, maxWidth: 520, margin: '0 auto 40px' }}>
            A complete preventive health action loop — connecting assessment to daily tracking, safety verification, and verified AYUSH access.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 16 }}>
            {[
              { num: '01', title: 'Assess Tendency', desc: '12-question deterministic scoring for Vata, Pitta & Kapha percentages.', path: '/assessment' },
              { num: '02', title: 'Personalize Plan', desc: 'Custom Dinacharya, Yoga, Pranayama & Diet routines with safety guidance.', path: '/plan' },
              { num: '03', title: 'Track Daily Pulse', desc: '30-second check-in with 0-100 score, pattern detection & adaptive focus.', path: '/tracker' },
              { num: '04', title: 'Connect to AYUSH', desc: 'Match your wellness goals with verified institutes and consultation simulation.', path: '/connect' },
            ].map(step => (
              <div key={step.num} className="card" style={{ background: 'white' }}>
                <div style={{ fontFamily: 'var(--font-serif)', fontSize: '1.8rem', fontWeight: 700, color: 'var(--color-brand)', marginBottom: 6 }}>
                  {step.num}
                </div>
                <h4 style={{ marginBottom: 6 }}>{step.title}</h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: 14 }}>{step.desc}</p>
                <Link to={step.path} style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--color-brand)', textDecoration: 'none' }}>
                  Explore Step →
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
