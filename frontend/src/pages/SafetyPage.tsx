import { AlertTriangle, ShieldCheck, Sparkles } from 'lucide-react';

const safetyChecks = [
  { label: 'Clinical boundary', value: 'Protected', tone: 'safe' },
  { label: 'Diagnostic claims', value: 'Blocked', tone: 'safe' },
  { label: 'Emergency escalation', value: 'Enabled', tone: 'warning' },
];

export function SafetyPage() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '40px 20px 80px' }}>
      <div className="container--narrow fade-in">
        <div style={{ marginBottom: 24 }}>
          <span className="badge badge--brand" style={{ marginBottom: 12 }}>Safety gate</span>
          <h1 style={{ marginBottom: 8 }}>Preventive wellness safety</h1>
          <p style={{ color: 'var(--color-text-muted)' }}>
            AyuPulse keeps wellness guidance non-diagnostic and supports safe boundaries for all recommendations.
          </p>
        </div>

        <div className="card card--elevated" style={{ marginBottom: 20, padding: 24 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 18 }}>
            <ShieldCheck size={22} color="var(--color-brand)" />
            <h3 style={{ margin: 0 }}>Safety status</h3>
          </div>
          <div style={{ display: 'grid', gap: 12 }}>
            {safetyChecks.map((check) => (
              <div key={check.label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 12px', borderRadius: '12px', background: check.tone === 'safe' ? 'var(--color-brand-pale)' : '#FFF7ED', border: '1px solid var(--color-border-light)' }}>
                <span>{check.label}</span>
                <strong style={{ color: check.tone === 'safe' ? 'var(--color-brand)' : '#C26A28' }}>{check.value}</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="card card--elevated" style={{ padding: 24 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
            <AlertTriangle size={20} color="#C26A28" />
            <h3 style={{ margin: 0 }}>Emergency escalation</h3>
          </div>
          <p style={{ color: 'var(--color-text-muted)', lineHeight: 1.7 }}>
            If there are concerning symptoms such as chest pain, severe bleeding, confusion, or acute crisis, AyuPulse directs users toward urgent medical evaluation instead of offering preventive guidance.
          </p>
          <div style={{ marginTop: 18, display: 'inline-flex', alignItems: 'center', gap: 8, color: 'var(--color-brand)', fontWeight: 700 }}>
            <Sparkles size={16} />
            Wellness guidance only — not a diagnosis.
          </div>
        </div>
      </div>
    </div>
  );
}
