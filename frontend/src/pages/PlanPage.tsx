import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, ArrowRight, Check, ChevronDown, ChevronUp, MoonStar, Sparkles, Stethoscope } from 'lucide-react';
import ayuApi, { type PlanResponse, type DailyTrackerTask } from '../api/client';

function deriveTaskCategory(task: DailyTrackerTask) {
  const text = `${task.title} ${task.description}`.toLowerCase();
  if (text.includes('water') || text.includes('hydrate')) return 'Hydration';
  if (text.includes('breath') || text.includes('pranayama') || text.includes('breathe')) return 'Breath';
  if (text.includes('meal') || text.includes('food') || text.includes('diet')) return 'Nutrition';
  if (text.includes('stretch') || text.includes('move') || text.includes('yoga')) return 'Movement';
  if (text.includes('sleep') || text.includes('rest') || text.includes('ground')) return 'Recovery';
  return 'Wellness';
}

export function PlanPage() {
  const navigate = useNavigate();
  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [expandedTaskId, setExpandedTaskId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedPlan = localStorage.getItem('ayupulse_plan');
    if (savedPlan) {
      try {
        setPlan(JSON.parse(savedPlan));
      } catch {
        setPlan(null);
      }
    }
    setLoading(false);
  }, []);

  const tasks: DailyTrackerTask[] = useMemo(() => {
    const baseTasks = plan?.daily_tracker ?? [
      { id: 'wake', title: 'Wake and hydrate', description: 'Drink warm water and begin with a gentle stretch.', completed: false },
      { id: 'breath', title: 'Breath reset', description: 'A 5-minute pranayama cycle to settle the nervous system.', completed: false },
      { id: 'meal', title: 'Balanced meals', description: 'Prioritize warm, grounding meals and consistent timing.', completed: false },
    ];

    return baseTasks.map(task => ({
      ...task,
      category: task.category ?? deriveTaskCategory(task),
    }));
  }, [plan]);

  const completed = tasks.filter(task => task.completed).length;
  const pct = tasks.length > 0 ? Math.round((completed / tasks.length) * 100) : 0;

  const assessment = useMemo(() => {
    try {
      const raw = localStorage.getItem('ayupulse_assessment');
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }, []);

  const dominant = plan?.dominant ?? assessment?.dominant ?? 'Balanced';
  const wellnessScore = useMemo(() => {
    const checkin = localStorage.getItem('ayupulse_latest_checkin');
    if (!checkin) return null;
    try {
      return JSON.parse(checkin).wellness_score ?? null;
    } catch {
      return null;
    }
  }, []);

  const focusCopy = useMemo(() => {
    if (plan?.message) return plan.message;
    if (dominant === 'Vata') return 'Your Vata-supportive rhythm for today.';
    if (dominant === 'Pitta') return 'Your steady, focused rhythm for today.';
    if (dominant === 'Kapha') return 'Your grounding, lightened rhythm for today.';
    return 'Small, grounding actions shaped around your wellness profile.';
  }, [dominant, plan]);

  const progressMessage = pct === 0
    ? 'Your rhythm starts with one small step.'
    : pct < 50
      ? 'You are building a steady rhythm.'
      : pct < 100
        ? 'You are halfway into today\'s rhythm.'
        : 'Beautiful — today\'s rhythm is complete.';

  const handleToggleTask = async (task: DailyTrackerTask) => {
    const nextTasks = tasks.map(item =>
      item.id === task.id ? { ...item, completed: !item.completed } : item
    );

    setPlan(current => current ? { ...current, daily_tracker: nextTasks } : current);
    localStorage.setItem('ayupulse_plan', JSON.stringify({ ...(plan ?? {}), daily_tracker: nextTasks }));

    try {
      await ayuApi.toggleTask(task.id, !task.completed);
    } catch {
      // Keep local update when backend is unavailable; the UI remains functional without breaking the page.
    }
  };

  if (loading) {
    return <div className="container--narrow" style={{ paddingTop: 80, textAlign: 'center' }}>Loading plan…</div>;
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '40px 20px 80px' }}>
      <div className="container--narrow fade-in">
        <div style={{ marginBottom: 22 }}>
          <span className="badge badge--brand" style={{ marginBottom: 12 }}>YOUR DAILY PULSE</span>
          <h1 style={{ marginBottom: 8 }}>Today&apos;s rhythm</h1>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '1.05rem', lineHeight: 1.7, maxWidth: 620 }}>
            {focusCopy}
          </p>
        </div>

        <div className="card card--elevated" style={{ marginBottom: 22, padding: 22 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <div>
              <div style={{ fontSize: '0.73rem', letterSpacing: '0.08em', color: 'var(--color-text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>
                Your wellness snapshot
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--color-brand)', fontWeight: 700 }}>
              <Sparkles size={16} />
              {dominant}
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 12 }}>
            {dominant !== 'Balanced' && (
              <div style={{ background: 'var(--color-brand-pale)', borderRadius: 'var(--radius-md)', padding: '12px 14px', border: '1px solid var(--color-brand-border)' }}>
                <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Dosha</div>
                <div style={{ fontWeight: 700, color: 'var(--color-brand)', marginTop: 4 }}>{dominant}</div>
              </div>
            )}
            {wellnessScore !== null && (
              <div style={{ background: 'var(--color-bg)', borderRadius: 'var(--radius-md)', padding: '12px 14px', border: '1px solid var(--color-border-light)' }}>
                <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Wellness score</div>
                <div style={{ fontWeight: 700, marginTop: 4 }}>{wellnessScore}</div>
              </div>
            )}
            <div style={{ background: 'var(--color-bg)', borderRadius: 'var(--radius-md)', padding: '12px 14px', border: '1px solid var(--color-border-light)' }}>
              <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Today</div>
              <div style={{ fontWeight: 700, marginTop: 4 }}>{completed} of {tasks.length} done</div>
            </div>
            {tasks[0] && (
              <div style={{ background: 'var(--color-bg)', borderRadius: 'var(--radius-md)', padding: '12px 14px', border: '1px solid var(--color-border-light)' }}>
                <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Today&apos;s focus</div>
                <div style={{ fontWeight: 700, marginTop: 4 }}>{tasks[0].category}</div>
              </div>
            )}
          </div>
        </div>

        <div className="card card--elevated" style={{ marginBottom: 22, padding: 22 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 18, flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
              <div
                aria-label="Task completion progress"
                style={{
                  width: 88,
                  height: 88,
                  borderRadius: '50%',
                  background: `conic-gradient(var(--color-brand) ${pct}%, var(--color-brand-pale) ${pct}% 100%)`,
                  display: 'grid',
                  placeItems: 'center',
                  boxShadow: 'inset 0 0 0 1px rgba(30,92,65,0.08)',
                }}
              >
                <div style={{ width: 58, height: 58, borderRadius: '50%', background: 'white', display: 'grid', placeItems: 'center', fontWeight: 700, color: 'var(--color-brand)' }}>
                  {pct}%
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.75rem', letterSpacing: '0.08em', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
                  Progress
                </div>
                <div style={{ fontSize: '1.75rem', fontWeight: 700, lineHeight: 1.2, marginTop: 6 }}>
                  {completed} of {tasks.length} complete
                </div>
                <div style={{ color: 'var(--color-text-muted)', marginTop: 4 }}>{progressMessage}</div>
              </div>
            </div>
            <button className="btn btn--primary" onClick={() => navigate('/checkin')}>
              <Activity size={16} />
              <span>Check in now</span>
            </button>
          </div>
        </div>

        <div className="card card--elevated" style={{ marginBottom: 22, padding: 20 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
            <Stethoscope size={18} color="var(--color-brand)" />
            <div style={{ fontSize: '0.76rem', letterSpacing: '0.08em', textTransform: 'uppercase', fontWeight: 700, color: 'var(--color-text-muted)' }}>
              Today&apos;s focus
            </div>
          </div>
          <div style={{ fontSize: '1.35rem', fontWeight: 700, marginBottom: 4 }}>{plan?.dominant ? `${plan.dominant}-supportive rhythm` : 'Gentle, steady wellness rhythm'}</div>
          <div style={{ color: 'var(--color-text-muted)', lineHeight: 1.7 }}>
            {plan?.message ?? 'Hydration, gentle movement, and regular meal timing support your day.'}
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {tasks.map((task, index) => {
            const isExpanded = expandedTaskId === task.id;
            const isCompleted = task.completed;

            return (
              <div
                key={task.id}
                className="card card--elevated"
                style={{
                  display: 'flex',
                  gap: 16,
                  alignItems: 'flex-start',
                  padding: 18,
                  border: isCompleted ? '1px solid var(--color-brand-border)' : '1px solid var(--color-border-light)',
                  background: isCompleted ? '#F5FBF8' : '#FFFFFF',
                  opacity: isCompleted ? 0.9 : 1,
                }}
              >
                <div style={{ minWidth: 54, textAlign: 'center', paddingTop: 10 }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase', fontWeight: 700 }}>0{index + 1}</div>
                </div>

                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12, flexWrap: 'wrap', marginBottom: 8 }}>
                    <span className="badge badge--brand" style={{ fontSize: '0.7rem' }}>{task.category}</span>
                    {isCompleted && (
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, background: 'var(--color-brand-pale)', color: 'var(--color-brand)', borderRadius: '999px', padding: '6px 10px', fontSize: '0.74rem', fontWeight: 700 }}>
                        <Check size={14} />
                        Completed
                      </span>
                    )}
                  </div>

                  <div style={{ fontWeight: 700, fontSize: '1.15rem', marginBottom: 6 }}>{task.title}</div>
                  <div style={{ color: 'var(--color-text-muted)', lineHeight: 1.65, marginBottom: 10 }}>{task.description}</div>

                  <button
                    className="btn btn--ghost btn--sm"
                    onClick={() => setExpandedTaskId(isExpanded ? null : task.id)}
                    style={{ marginBottom: 10 }}
                  >
                    {isExpanded ? <><ChevronUp size={14} /> View less</> : <><ChevronDown size={14} /> Why this?</>}
                  </button>

                  {isExpanded && (
                    <div style={{ background: 'var(--color-bg)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border-light)', padding: '12px 14px', color: 'var(--color-text-muted)', lineHeight: 1.7 }}>
                      {task.description}
                    </div>
                  )}
                </div>

                <button
                  className={isCompleted ? 'btn btn--ghost' : 'btn btn--secondary'}
                  onClick={() => handleToggleTask(task)}
                  style={{ minWidth: 132 }}
                >
                  {isCompleted ? 'Undo' : 'Mark done'}
                </button>
              </div>
            );
          })}
        </div>

        <div className="card card--elevated" style={{ marginTop: 24, padding: 20 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10 }}>
            <MoonStar size={18} color="var(--color-brand)" />
            <h3 style={{ margin: 0 }}>30-second check-in</h3>
          </div>
          <div style={{ color: 'var(--color-text-muted)', marginBottom: 16 }}>How are you feeling today?</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))', gap: 10, marginBottom: 18 }}>
            {['Sleep', 'Stress', 'Mood', 'Digestion'].map((label) => (
              <div key={label} style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border-light)', borderRadius: 'var(--radius-md)', padding: '12px 10px', textAlign: 'center', fontWeight: 600 }}>
                {label}
              </div>
            ))}
          </div>
          <button className="btn btn--primary" onClick={() => navigate('/checkin')}>
            <ArrowRight size={16} />
            <span>Open check-in</span>
          </button>
        </div>

        <div className="disclaimer" style={{ marginTop: 24 }}>
          <span>⚠️</span>
          <span>Traditional AYUSH wellness guidance for preventive wellbeing — not a medical diagnosis.</span>
        </div>
      </div>
    </div>
  );
}
