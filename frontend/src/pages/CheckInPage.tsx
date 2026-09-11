import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { CheckInResponse } from '../api/client';

export function CheckInPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    sleep: 76,
    stress: 52,
    mood: 78,
    digestion: 68,
    energy: 81,
    notes: 'Balanced routine with improved hydration and grounding practice.',
  });

  const updateField = (field: keyof typeof form, value: string | number) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = () => {
    const response: CheckInResponse = {
      status: 'ok',
      module: 'checkin',
      checkin_id: 'prototype-checkin',
      wellness_score: Math.round((form.sleep + form.mood + form.digestion + form.energy + (100 - form.stress)) / 5),
      summary: 'Your rhythm is stable today. Mild stress is present, but your sleep, energy, and overall mood remain in a supportive range.',
      checkin: {
        sleep: form.sleep,
        stress: form.stress,
        mood: form.mood,
        digestion: form.digestion,
        energy: form.energy,
        date: new Date().toISOString(),
        notes: form.notes,
      },
      message: 'Daily check-in recorded successfully.',
    };

    localStorage.setItem('ayupulse_latest_checkin', JSON.stringify(response));
    navigate('/checkin/result', { state: { result: response } });
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '40px 20px 80px' }}>
      <div className="container--narrow fade-in">
        <div style={{ marginBottom: 28 }}>
          <span className="badge badge--brand" style={{ marginBottom: 12 }}>Daily check-in</span>
          <h1 style={{ marginBottom: 8 }}>30-second wellness pulse</h1>
          <p style={{ color: 'var(--color-text-muted)' }}>
            Track how your body is feeling today to keep your AYUSH rhythm steady.
          </p>
        </div>

        <div className="card card--elevated" style={{ padding: 24 }}>
          <div style={{ display: 'grid', gap: 18 }}>
            {[
              ['sleep', 'Sleep quality', 0, 100],
              ['stress', 'Stress load', 0, 100],
              ['mood', 'Mood balance', 0, 100],
              ['digestion', 'Digestion comfort', 0, 100],
              ['energy', 'Energy level', 0, 100],
            ].map(([key, label, min, max]) => (
              <div key={key}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontWeight: 600 }}>
                  <span>{label}</span>
                  <span style={{ color: 'var(--color-brand)' }}>{form[key as keyof typeof form]}%</span>
                </div>
                <input
                  type="range"
                  min={min}
                  max={max}
                  value={Number(form[key as keyof typeof form])}
                  onChange={(e) => updateField(key as keyof typeof form, Number(e.target.value))}
                  style={{ width: '100%' }}
                />
              </div>
            ))}

            <div>
              <label style={{ display: 'block', fontWeight: 600, marginBottom: 8 }}>Notes</label>
              <textarea
                value={form.notes}
                onChange={(e) => updateField('notes', e.target.value)}
                rows={4}
                style={{
                  width: '100%',
                  borderRadius: '12px',
                  border: '1px solid var(--color-border)',
                  padding: '12px 14px',
                  fontFamily: 'inherit',
                  resize: 'vertical',
                }}
              />
            </div>

            <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end', flexWrap: 'wrap' }}>
              <button className="btn btn--ghost" onClick={() => navigate('/plan')}>
                Back to plan
              </button>
              <button className="btn btn--primary" onClick={handleSubmit}>
                Save check-in →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
