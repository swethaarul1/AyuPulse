import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ayuApi, { PreventivePlan, PlanTask } from '../api/client';

const CATEGORY_ICONS: Record<string, string> = {
  Dinacharya: '🌅',
  Yoga: '🧘',
  Pranayama: '💨',
  Diet: '🥗',
  Lifestyle: '🌿',
};

const CATEGORY_COLORS: Record<string, string> = {
  Dinacharya: 'var(--color-brand)',
  Yoga: 'var(--color-vata)',
  Pranayama: 'var(--color-earth)',
  Diet: '#4D8B72',
  Lifestyle: '#6D6875',
};

function TaskDetail({ task, onClose }: { task: PlanTask; onClose: () => void }) {
  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', zIndex: 200,
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20,
    }}
      onClick={onClose}
    >
      <div
        style={{
          background: 'white', borderRadius: 'var(--radius-xl)', padding: 28,
          maxWidth: 500, width: '100%', maxHeight: '80vh', overflowY: 'auto',
        }}
        onClick={e => e.stopPropagation()}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 20 }}>
          <div>
            <span className="badge" style={{
              background: `${CATEGORY_COLORS[task.category] || 'var(--color-brand)'}20`,
              color: CATEGORY_COLORS[task.category] || 'var(--color-brand)',
              marginBottom: 8, display: 'inline-block',
            }}>
              {CATEGORY_ICONS[task.category] || '✦'} {task.category}
              {task.duration && ` · ${task.duration}`}
            </span>
            <h3 style={{ lineHeight: 1.3 }}>{task.title}</h3>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem', color: 'var(--color-text-muted)' }}
          >✕</button>
        </div>

        {[
          { label: 'What', content: task.what, icon: '📌' },
          { label: 'Why', content: task.why, icon: '💡' },
          { label: 'How', content: task.how, icon: '📋' },
        ].map(s => (
          <div key={s.label} style={{ marginBottom: 16 }}>
            <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: 6 }}>
              {s.icon} {s.label.toUpperCase()}
            </div>
            <p style={{ fontSize: '0.9rem', lineHeight: 1.6, color: 'var(--color-text)' }}>{s.content}</p>
          </div>
        ))}

        <div style={{
          background: 'var(--color-earth-pale)', borderRadius: 'var(--radius-md)',
          padding: '10px 14px', fontSize: '0.82rem', color: 'var(--color-earth)',
          display: 'flex', gap: 8,
        }}>
          <span>⚠️</span>
          <span><strong>Safety:</strong> {task.safety}</span>
        </div>

        {task.is_adjusted && (
          <div style={{
            marginTop: 12, background: 'var(--color-pitta-pale)', borderRadius: 'var(--radius-md)',
            padding: '8px 12px', fontSize: '0.82rem', color: 'var(--color-pitta)',
          }}>
            ✦ Adjusted based on your recent wellness pattern
          </div>
        )}
      </div>
    </div>
  );
}

export function PlanPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [plan, setPlan] = useState<PreventivePlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedTask, setSelectedTask] = useState<PlanTask | null>(null);
  const [completing, setCompleting] = useState<string | null>(null);

  useEffect(() => {
    const stateData = location.state?.plan as PreventivePlan | undefined;
    if (stateData) {
      setPlan(stateData);
      setLoading(false);
      return;
    }
    // Try from localStorage
    const planId = localStorage.getItem('ayupulse_plan_id');
    if (planId) {
      ayuApi.getPlan(planId).then(p => {
        setPlan(p);
        setLoading(false);
      }).catch(() => {
        tryBySession();
      });
    } else {
      tryBySession();
    }
  }, []);

  function tryBySession() {
    ayuApi.getPlanBySession().then(p => {
      setPlan(p);
      setLoading(false);
    }).catch(() => {
      setError('No plan found. Complete your assessment first.');
      setLoading(false);
    });
  }

  const handleToggleTask = async (task: PlanTask) => {
    if (completing) return;
    setCompleting(task.id);
    try {
      const result = await ayuApi.completeTask(task.id);
      setPlan(prev => {
        if (!prev) return prev;
        return {
          ...prev,
          tasks: prev.tasks.map(t =>
            t.id === task.id ? { ...t, is_completed_today: result.completed } : t
          ),
        };
      });
    } catch (e) {
      console.error(e);
    } finally {
      setCompleting(null);
    }
  };

  if (loading) return <div className="loading-center"><div className="loading-spinner" /><p>Loading your plan…</p></div>;

  if (error || !plan) {
    return (
      <div className="container--narrow" style={{ paddingTop: 60, textAlign: 'center' }}>
        <div style={{ fontSize: '3rem', marginBottom: 16 }}>🌿</div>
        <h2 style={{ marginBottom: 12 }}>No plan yet</h2>
        <p style={{ color: 'var(--color-text-muted)', marginBottom: 24 }}>{error || 'Complete your assessment to get your personalized plan.'}</p>
        <button className="btn btn--primary" onClick={() => navigate('/assessment')}>
          Start Assessment →
        </button>
      </div>
    );
  }

  const tasks = plan.tasks.sort((a, b) => a.sort_order - b.sort_order);
  const completed = tasks.filter(t => t.is_completed_today).length;
  const completePct = tasks.length > 0 ? Math.round((completed / tasks.length) * 100) : 0;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', paddingBottom: 64 }}>
      {selectedTask && (
        <TaskDetail task={selectedTask} onClose={() => setSelectedTask(null)} />
      )}

      <div className="container--narrow" style={{ paddingTop: 40 }}>
        {/* Header */}
        <div className="fade-in" style={{ marginBottom: 32 }}>
          <div className="badge badge--brand" style={{ marginBottom: 8 }}>Personalized Preventive Plan</div>
          <h2 style={{ marginBottom: 4 }}>Today's Plan</h2>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
            Practices tailored to your wellness tendency
          </p>
        </div>

        {/* Progress card */}
        <div className="card card--elevated fade-in" style={{ marginBottom: 28, background: 'linear-gradient(135deg, #F0F7F4 0%, #FDFAF6 100%)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <div>
              <div style={{ fontSize: '0.82rem', color: 'var(--color-text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 4 }}>
                Today's Progress
              </div>
              <div style={{ fontFamily: 'var(--font-serif)', fontSize: '1.8rem', fontWeight: 700, color: 'var(--color-brand)' }}>
                {completed} / {tasks.length}
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>tasks completed</div>
            </div>
            <div style={{
              width: 72, height: 72, borderRadius: '50%',
              background: `conic-gradient(var(--color-brand) ${completePct * 3.6}deg, var(--color-border-light) 0)`,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <div style={{
                width: 54, height: 54, borderRadius: '50%', background: 'white',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontWeight: 700, color: 'var(--color-brand)', fontSize: '1rem',
              }}>
                {completePct}%
              </div>
            </div>
          </div>
          <div className="progress-bar-track" style={{ height: 8 }}>
            <div
              className="progress-bar-fill"
              style={{ width: `${completePct}%`, background: 'var(--color-brand)' }}
            />
          </div>
          {completePct === 100 && (
            <div style={{
              marginTop: 12, textAlign: 'center', color: 'var(--color-brand)',
              fontWeight: 600, fontSize: '0.9rem',
            }}>
              🎉 All practices completed today! Wonderful work.
            </div>
          )}
        </div>

        {/* Task list */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 32 }}>
          {tasks.map(task => (
            <div
              key={task.id}
              className={`task-item ${task.is_completed_today ? 'task-item--completed' : ''} ${task.is_adjusted ? 'task-item--adjusted' : ''} fade-in`}
              onClick={() => setSelectedTask(task)}
            >
              <button
                className={`task-check ${task.is_completed_today ? 'task-check--done' : ''}`}
                onClick={e => { e.stopPropagation(); handleToggleTask(task); }}
                disabled={completing === task.id}
                style={{ cursor: 'pointer' }}
              >
                {task.is_completed_today && '✓'}
              </button>
              <div style={{ flex: 1 }}>
                <div style={{
                  fontWeight: 600, fontSize: '0.95rem',
                  textDecoration: task.is_completed_today ? 'line-through' : 'none',
                  color: task.is_completed_today ? 'var(--color-brand)' : 'var(--color-text)',
                }}>
                  {task.title}
                </div>
                <div style={{ display: 'flex', gap: 8, marginTop: 4, alignItems: 'center', flexWrap: 'wrap' }}>
                  <span style={{
                    fontSize: '0.77rem', fontWeight: 600, padding: '2px 8px',
                    borderRadius: 'var(--radius-full)',
                    background: `${CATEGORY_COLORS[task.category] || 'var(--color-brand)'}15`,
                    color: CATEGORY_COLORS[task.category] || 'var(--color-brand)',
                  }}>
                    {CATEGORY_ICONS[task.category] || '✦'} {task.category}
                  </span>
                  {task.duration && (
                    <span style={{ fontSize: '0.77rem', color: 'var(--color-text-light)' }}>
                      ⏱ {task.duration}
                    </span>
                  )}
                  {task.is_adjusted && (
                    <span style={{ fontSize: '0.7rem', color: 'var(--color-pitta)', fontWeight: 600 }}>
                      ✦ Adjusted
                    </span>
                  )}
                </div>
              </div>
              <span style={{ color: 'var(--color-text-light)', fontSize: '0.85rem' }}>›</span>
            </div>
          ))}
        </div>

        {/* Tip */}
        <div className="disclaimer" style={{ marginBottom: 24 }}>
          <span>💡</span>
          <span>Tap any practice to see the full guidance — What, Why, How, and Safety notes.</span>
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          <button
            className="btn btn--primary"
            onClick={() => navigate('/checkin')}
          >
            📊 Daily Check-in →
          </button>
          <button
            className="btn btn--ghost"
            onClick={() => navigate('/dashboard')}
          >
            View Dashboard
          </button>
        </div>

        {/* Plan disclaimer */}
        <div className="disclaimer" style={{ marginTop: 24 }}>
          <span>⚠️</span>
          <span>These practices are traditional wellness guidance for preventive wellbeing — not medical treatments. Consult a qualified practitioner for health concerns.</span>
        </div>
      </div>
    </div>
  );
}
