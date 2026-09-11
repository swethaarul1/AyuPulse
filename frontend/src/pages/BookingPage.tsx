import { ArrowLeft, CalendarCheck2, Clock3, MapPin, Phone, Star } from 'lucide-react';
import { useNavigate, useParams } from 'react-router-dom';

const centreProfiles = {
  ayurveda: {
    id: 'ayurveda',
    name: 'Swasthya Ayurveda Hub',
    city: 'Bengaluru',
    rating: 4.8,
    system: 'Ayurveda',
    focus: 'Prakriti guidance + daily routine support',
    availability: 'Mon–Sat · 9:00 AM to 7:00 PM',
    contact: '+91 98800 11223',
    description:
      'A preventive AYUSH consultation focused on dosha-based routines, sleep rhythm, digestion, and sustainable wellness planning.',
  },
  yoga: {
    id: 'yoga',
    name: 'Harmony Yoga Wellness Studio',
    city: 'Pune',
    rating: 4.7,
    system: 'Yoga',
    focus: 'Stress regulation + breath and movement practice',
    availability: 'Tue–Sun · 6:00 AM to 8:00 PM',
    contact: '+91 98220 44567',
    description:
      'A mindful consultation pathway blending pranayama, movement, and nervous-system reset practices for stress regulation and restorative balance.',
  },
  naturopathy: {
    id: 'naturopathy',
    name: 'Veda Life Naturopathy Clinic',
    city: 'Delhi',
    rating: 4.9,
    system: 'Naturopathy',
    focus: 'Digestive reset + nutrition planning',
    availability: 'Mon–Sat · 8:30 AM to 6:30 PM',
    contact: '+91 98110 76321',
    description:
      'Lifestyle-first guidance centered on digestion, food rhythm, energy restoration, and preventive care aligned with daily habits.',
  },
};

export function BookingPage() {
  const navigate = useNavigate();
  const { centreId } = useParams();

  const selectedCentre = centreProfiles[(centreId as keyof typeof centreProfiles) ?? 'ayurveda'];

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '40px 20px 80px' }}>
      <div className="container--narrow fade-in">
        <button className="btn btn--ghost" onClick={() => navigate('/connect')} style={{ marginBottom: 18 }}>
          <ArrowLeft size={16} />
          <span>Back to Connect</span>
        </button>

        <div className="card card--elevated" style={{ padding: 28 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 16, marginBottom: 18, flexWrap: 'wrap' }}>
            <div>
              <span className="badge badge--brand" style={{ marginBottom: 10 }}>{selectedCentre.system}</span>
              <h1 style={{ margin: 0, fontSize: '2rem' }}>{selectedCentre.name}</h1>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--color-brand)', fontWeight: 700 }}>
              <Star size={18} fill="currentColor" />
              {selectedCentre.rating}
            </div>
          </div>

          <div style={{ display: 'grid', gap: 14, marginBottom: 22 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--color-text-muted)' }}>
              <MapPin size={18} color="var(--color-brand)" />
              <span>{selectedCentre.city}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--color-text-muted)' }}>
              <Clock3 size={18} color="var(--color-brand)" />
              <span>{selectedCentre.availability}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--color-text-muted)' }}>
              <Phone size={18} color="var(--color-brand)" />
              <span>{selectedCentre.contact}</span>
            </div>
          </div>

          <div style={{ padding: '16px 18px', borderRadius: 'var(--radius-md)', background: 'var(--color-bg)', border: '1px solid var(--color-border-light)', marginBottom: 24 }}>
            <h3 style={{ margin: '0 0 8px' }}>Consultation focus</h3>
            <p style={{ margin: 0, color: 'var(--color-text-muted)', lineHeight: 1.7 }}>{selectedCentre.focus}</p>
          </div>

          <div style={{ marginBottom: 28 }}>
            <h3 style={{ marginBottom: 10 }}>Why this path may suit you</h3>
            <p style={{ color: 'var(--color-text-muted)', lineHeight: 1.8, margin: 0 }}>{selectedCentre.description}</p>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12 }}>
            <button
              className="btn btn--primary"
              onClick={() => window.open(`tel:${selectedCentre.contact.replace(/\s+/g, '')}`, '_self')}
            >
              <CalendarCheck2 size={18} />
              <span>Book consultation</span>
            </button>
            <button className="btn btn--ghost" onClick={() => window.open(`mailto:hello@ayupulse.ai?subject=${encodeURIComponent(`Consultation enquiry - ${selectedCentre.name}`)}`, '_self')}>
              Request more info
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
