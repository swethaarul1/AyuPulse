import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import ayuApi, { Assessment, DoshaResult } from '../api/client';

const DOSHA_COLORS = {
  Vata: '#5B7FA6',
  Pitta: '#C77D3A',
  Kapha: '#4D8B72',
};

const DOSHA_DESCS: Record<string, { title: string; keywords: string; emoji: string }> = {
  Vata: {
    emoji: '🌬️',
    title: 'Vata Constitution',
    keywords: 'Movement · Creativity · Change · Air & Space',
  },
  Pitta: {
    emoji: '🔥',
    title: 'Pitta Constitution',
    keywords: 'Transformation · Focus · Warmth · Fire & Water',
  },
  Kapha: {
    emoji: '🌍',
    title: 'Kapha Constitution',
    keywords: 'Stability · Strength · Nourishment · Earth & Water',
  },
};

function DonutChart({ vata, pitta, kapha, dominant }: { vata: number; pitta: number; kapha: number; dominant: string }) {
  const data = [
    { name: 'Vata', value: vata, color: DOSHA_COLORS.Vata },
    { name: 'Pitta', value: pitta, color: DOSHA_COLORS.Pitta },
    { name: 'Kapha', value: kapha, color: DOSHA_COLORS.Kapha },
  ];

  return (
    <div style={{ position: 'relative', width: 200, height: 200, margin: '0 auto' }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={65}
            outerRadius={90}
            dataKey="value"
            startAngle={90}
            endAngle={450}
          >
            {data.map((d, i) => (
              <Cell key={i} fill={d.color} strokeWidth={2} stroke="#fff" />
            ))}
          </Pie>
          <Tooltip formatter={(val: number) => `${val}%`} />
        </PieChart>
      </ResponsiveContainer>
      <div style={{
        position: 'absolute', top: '50%', left: '50%',
        transform: 'translate(-50%, -50%)',
        textAlign: 'center',
      }}>
        <div style={{ fontSize: '1.5rem' }}>{DOSHA_DESCS[dominant]?.emoji}</div>
        <div style={{ fontFamily: 'var(--font-serif)', fontWeight: 700, fontSize: '1.1rem', color: DOSHA_COLORS[dominant as keyof typeof DOSHA_COLORS] }}>
          {dominant}
        </div>
      </div>
    </div>
  );
}

function DoshaBar({ label, pct, color }: { label: string; pct: number; color: string }) {
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span style={{ fontWeight: 600, fontSize: '0.9rem', color }}>{label}</span>
        <span style={{ fontWeight: 700, color }}>{pct}%</span>
      </div>
      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
    </div>
  );
}

export function ResultPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [buildingPlan, setBuildingPlan] = useState(false);

  useEffect(() => {
    const stateData = location.state?.assessment as Assessment | undefined;
    if (stateData) {
      setAssessment(stateData);
      setLoading(false);
      return;
    }
    // Try localStorage
    const stored = localStorage.getItem('ayupulse_assessment');
    if (stored) {
      setAssessment(JSON.parse(stored));
      setLoading(false);
    } else {
      setLoading(false);
    }
  }, []);

  const handleBuildPlan = async () => {
    if (!assessment?.dosha_result) return;
    setBuildingPlan(true);
    try {
      const plan = await ayuApi.createPlan(assessment.dosha_result.id);
      localStorage.setItem('ayupulse_plan_id', plan.id);
      navigate('/plan', { state: { plan } });
    } catch (e) {
      console.error(e);
      setBuildingPlan(false);
    }
  };

  if (loading) {
    return <div className="loading-center"><div className="loading-spinner" /><p>Loading result…</p></div>;
  }

  if (!assessment?.dosha_result) {
    return (
      <div className="container--narrow" style={{ paddingTop: 60, textAlign: 'center' }}>
        <h2 style={{ marginBottom: 16 }}>No result found</h2>
        <p style={{ color: 'var(--color-text-muted)', marginBottom: 24 }}>
          Please complete the assessment first.
        </p>
        <button className="btn btn--primary" onClick={() => navigate('/assessment')}>
          Start Assessment →
        </button>
      </div>
    );
  }

  const dr = assessment.dosha_result;
  const dom = dr.dominant as keyof typeof DOSHA_COLORS;
  const domColor = DOSHA_COLORS[dom] || 'var(--color-brand)';

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', paddingBottom: 64 }}>
      <div className="container--narrow" style={{ paddingTop: 40 }}>

        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 40 }} className="fade-in">
          <div className="badge badge--brand" style={{ marginBottom: 12 }}>Your Traditional Wellness Tendency</div>
          <h1 style={{ marginBottom: 8 }}>
            {DOSHA_DESCS[dr.dominant]?.emoji} {DOSHA_DESCS[dr.dominant]?.title}
          </h1>
          <p style={{ color: 'var(--color-text-muted)' }}>
            {DOSHA_DESCS[dr.dominant]?.keywords}
          </p>
          {dr.secondary && (
            <p style={{ marginTop: 8, fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
              with {dr.secondary} characteristics
            </p>
          )}
        </div>

        {/* Visual: Donut + Bars */}
        <div className="card card--elevated fade-in" style={{ marginBottom: 24 }}>
          <DonutChart vata={dr.vata_pct} pitta={dr.pitta_pct} kapha={dr.kapha_pct} dominant={dr.dominant} />
          <div style={{ marginTop: 28 }}>
            <DoshaBar label="Vata" pct={dr.vata_pct} color={DOSHA_COLORS.Vata} />
            <DoshaBar label="Pitta" pct={dr.pitta_pct} color={DOSHA_COLORS.Pitta} />
            <DoshaBar label="Kapha" pct={dr.kapha_pct} color={DOSHA_COLORS.Kapha} />
          </div>
          <div style={{
            marginTop: 16, padding: '10px 14px',
            background: `${domColor}15`, borderRadius: 'var(--radius-md)',
            fontSize: '0.82rem', color: domColor, fontWeight: 600,
          }}>
            Confidence: {Math.round(dr.confidence * 100)}% · Dominant: {dr.dominant}
            {dr.secondary ? ` · Secondary: ${dr.secondary}` : ''}
          </div>
        </div>

        {/* Explanation */}
        <div className="card fade-in" style={{ marginBottom: 24 }}>
          <h3 style={{ marginBottom: 12 }}>🧠 What this means</h3>
          <p style={{ color: 'var(--color-text-muted)', lineHeight: 1.7 }}>
            {dr.explanation}
          </p>
        </div>

        {/* Reasoning */}
        {dr.reasoning_points && dr.reasoning_points.length > 0 && (
          <div className="card fade-in" style={{ marginBottom: 24 }}>
            <h3 style={{ marginBottom: 12 }}>🔍 Why we reached this result</h3>
            <ul style={{ paddingLeft: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 10 }}>
              {dr.reasoning_points.map((pt, i) => (
                <li key={i} style={{
                  display: 'flex', gap: 10, alignItems: 'flex-start',
                  padding: '10px 14px', background: 'var(--color-bg)',
                  borderRadius: 'var(--radius-md)', fontSize: '0.9rem',
                  color: 'var(--color-text)',
                }}>
                  <span style={{ color: 'var(--color-brand)', flexShrink: 0 }}>✓</span>
                  {pt}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Disclaimer */}
        <div className="disclaimer fade-in" style={{ marginBottom: 32 }}>
          <span>⚠️</span>
          <span>Traditional wellness tendency — not a medical diagnosis. This result reflects patterns shared in your assessment responses.</span>
        </div>

        {/* CTA */}
        <div style={{ textAlign: 'center' }} className="fade-in">
          <button
            className="btn btn--primary btn--lg"
            onClick={handleBuildPlan}
            disabled={buildingPlan}
            style={{ marginBottom: 12 }}
          >
            {buildingPlan ? '⏳ Building your plan…' : '🌿 Build My Preventive Plan →'}
          </button>
          <p style={{ fontSize: '0.82rem', color: 'var(--color-text-light)' }}>
            Your plan will be personalized to your {dr.dominant} tendency
          </p>
        </div>
      </div>
    </div>
  );
}
