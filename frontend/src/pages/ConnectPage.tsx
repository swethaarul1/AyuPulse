import { ArrowRight, MapPin, ShieldCheck, Sparkles, Stethoscope } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const matches = [
  { system: 'Ayurveda', focus: 'Prakriti guidance', service: 'Consultation + daily routine support', match: '92%', route: 'ayurveda' },
  { system: 'Yoga', focus: 'Stress regulation', service: 'Breath and movement practice', match: '84%', route: 'yoga' },
  { system: 'Naturopathy', focus: 'Digestive reset', service: 'Lifestyle & nutrition planning', match: '78%', route: 'naturopathy' },
];

const centres = [
  { name: 'Swasthya Ayurveda Hub', city: 'Bengaluru', rating: 4.8, route: 'ayurveda' },
  { name: 'Harmony Yoga Wellness Studio', city: 'Pune', rating: 4.7, route: 'yoga' },
  { name: 'Veda Life Naturopathy Clinic', city: 'Delhi', rating: 4.9, route: 'naturopathy' },
];

export function ConnectPage() {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '40px 20px 80px' }}>
      <div className="container fade-in">
        <div style={{ marginBottom: 24 }}>
          <span className="badge badge--brand" style={{ marginBottom: 12 }}>AYUSH access</span>
          <h1 style={{ marginBottom: 8 }}>Connect to AYUSH</h1>
          <p style={{ color: 'var(--color-text-muted)', maxWidth: 720 }}>
            Match your wellness goals with suitable preventive pathways, verified service styles, and a supportive consultation flow.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 20, marginBottom: 28 }}>
          {matches.map((match) => (
            <div key={match.system} className="card card--elevated" onClick={() => navigate(`/connect/${match.route}`)} style={{ cursor: 'pointer' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
                <span className="badge badge--brand">{match.system}</span>
                <span style={{ fontWeight: 700, color: 'var(--color-brand)' }}>{match.match}</span>
              </div>
              <div style={{ fontWeight: 700, marginBottom: 8 }}>{match.focus}</div>
              <div style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>{match.service}</div>
            </div>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.3fr 0.7fr', gap: 24 }}>
          <div className="card card--elevated">
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 18 }}>
              <MapPin size={18} color="var(--color-brand)" />
              <h3 style={{ margin: 0 }}>Recommended centres</h3>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              {centres.map((centre) => (
                <div key={centre.name} onClick={() => navigate(`/connect/${centre.route}`)} style={{ border: '1px solid var(--color-border-light)', borderRadius: 'var(--radius-md)', padding: '12px 14px', cursor: 'pointer' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, marginBottom: 6 }}>
                    <strong>{centre.name}</strong>
                    <span style={{ color: 'var(--color-brand)', fontWeight: 700 }}>★ {centre.rating}</span>
                  </div>
                  <div style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>{centre.city}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="card card--elevated">
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 18 }}>
              <Stethoscope size={18} color="var(--color-earth)" />
              <h3 style={{ margin: 0 }}>Next steps</h3>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <Sparkles size={16} color="var(--color-brand)" />
                <span>Review the best-fit AYUSH system</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <ShieldCheck size={16} color="var(--color-brand)" />
                <span>Ensure any consult is preventive and aligned</span>
              </div>
              <button className="btn btn--primary" style={{ marginTop: 10 }} onClick={() => navigate('/connect/ayurveda')}>
                Book consultation <ArrowRight size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
