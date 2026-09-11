import { Activity, ArrowUpRight, HeartPulse, Sparkles, Users } from 'lucide-react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const dashboardData = {
  prototype: true,
  disclaimer: 'Prototype simulation for demo preview only. Community data is seeded for UI validation.',
  metrics: {
    total_assessments: 1842,
    task_start_rate: 72,
    active_checkins_this_week: 318,
    common_pattern: 'Sleep quality + stress rhythm',
    ayush_matches_count: 28,
    average_community_pulse: 81,
  },
  common_patterns: [
    { pattern: 'Sleep quality + stress rhythm', frequency_percentage: 38, dominant_dosha: 'Vata' },
    { pattern: 'Digestive consistency', frequency_percentage: 27, dominant_dosha: 'Pitta' },
    { pattern: 'Steady morning energy', frequency_percentage: 21, dominant_dosha: 'Kapha' },
  ],
  ayush_matches: [
    { system: 'Ayurveda', share_percentage: 45, top_service: 'Prakriti consultation' },
    { system: 'Yoga', share_percentage: 32, top_service: 'Breath + mobility support' },
    { system: 'Naturopathy', share_percentage: 23, top_service: 'Lifestyle reset plan' },
  ],
  trends: [
    { day: 'Mon', avg_wellness_pulse: 74, checkin_count: 42 },
    { day: 'Tue', avg_wellness_pulse: 76, checkin_count: 48 },
    { day: 'Wed', avg_wellness_pulse: 79, checkin_count: 56 },
    { day: 'Thu', avg_wellness_pulse: 81, checkin_count: 60 },
    { day: 'Fri', avg_wellness_pulse: 78, checkin_count: 52 },
    { day: 'Sat', avg_wellness_pulse: 86, checkin_count: 67 },
    { day: 'Sun', avg_wellness_pulse: 84, checkin_count: 61 },
  ],
};

const trendColors = ['#1E5C41', '#7A4E2D', '#456E94', '#C26A28'];

export function DashboardPage() {
  const { metrics, common_patterns, ayush_matches, trends } = dashboardData;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-bg)', padding: '40px 20px 80px' }}>
      <div className="container fade-in">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', gap: 12, flexWrap: 'wrap', marginBottom: 24 }}>
          <div>
            <span className="badge badge--brand" style={{ marginBottom: 12 }}>Community view</span>
            <h1 style={{ marginBottom: 8 }}>Community Wellness Dashboard</h1>
            <p style={{ color: 'var(--color-text-muted)', maxWidth: 720 }}>
              Real-time community signals for wellbeing rhythm, preventive habits, and AYUSH alignment.
            </p>
          </div>
          <div className="badge badge--seeded" style={{ display: 'inline-flex' }}>
            <Sparkles size={14} />
            Prototype simulation
          </div>
        </div>

        <div className="disclaimer" style={{ marginBottom: 28 }}>
          <span>⚠️</span>
          <span>{dashboardData.disclaimer}</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 20, marginBottom: 28 }}>
          <div className="card card--elevated">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
              <span className="badge badge--brand">Assessments</span>
              <Users size={18} color="var(--color-brand)" />
            </div>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: '2.2rem', fontWeight: 700, color: 'var(--color-brand)' }}>
              {metrics.total_assessments.toLocaleString()}
            </div>
            <div style={{ color: 'var(--color-text-muted)', fontSize: '0.82rem' }}>total assessments</div>
          </div>

          <div className="card card--elevated">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
              <span className="badge badge--earth">Engagement</span>
              <Activity size={18} color="var(--color-earth)" />
            </div>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: '2.2rem', fontWeight: 700, color: 'var(--color-earth)' }}>
              {metrics.task_start_rate}%
            </div>
            <div style={{ color: 'var(--color-text-muted)', fontSize: '0.82rem' }}>daily task engagement</div>
          </div>

          <div className="card card--elevated">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
              <span className="badge badge--vata">Pattern</span>
              <HeartPulse size={18} color="var(--color-vata)" />
            </div>
            <div style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--color-vata)', marginBottom: 6 }}>
              {metrics.common_pattern}
            </div>
            <div style={{ color: 'var(--color-text-muted)', fontSize: '0.82rem' }}>common wellness pattern</div>
          </div>

          <div className="card card--elevated">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
              <span className="badge badge--kapha">AYUSH fit</span>
              <ArrowUpRight size={18} color="var(--color-kapha)" />
            </div>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: '2.2rem', fontWeight: 700, color: 'var(--color-kapha)' }}>
              {metrics.ayush_matches_count}
            </div>
            <div style={{ color: 'var(--color-text-muted)', fontSize: '0.82rem' }}>AYUSH service matches</div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 24 }}>
          <div className="card card--elevated">
            <div style={{ marginBottom: 18 }}>
              <h3 style={{ marginBottom: 6 }}>Community pulse trend</h3>
              <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>Average wellness pulse over the last 7 days</p>
            </div>
            <div style={{ width: '100%', height: 260 }}>
              <ResponsiveContainer>
                <LineChart data={trends}>
                  <CartesianGrid stroke="rgba(87, 101, 96, 0.12)" vertical={false} />
                  <XAxis dataKey="day" tickLine={false} axisLine={false} tick={{ fill: '#576560', fontSize: 12 }} />
                  <YAxis domain={[60, 100]} tickLine={false} axisLine={false} tick={{ fill: '#576560', fontSize: 12 }} />
                  <Tooltip formatter={(value: number | string | readonly (number | string)[] | undefined) => {
                    const numericValue = Array.isArray(value) ? value[0] : value;
                    return [`${numericValue ?? 0}`, 'Wellness pulse'] as [string, string];
                  }} />
                  <Line type="monotone" dataKey="avg_wellness_pulse" stroke="#1E5C41" strokeWidth={3} dot={{ r: 4, fill: '#1E5C41' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card card--elevated">
            <div style={{ marginBottom: 18 }}>
              <h3 style={{ marginBottom: 6 }}>Common patterns</h3>
              <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>Most frequent wellness themes in the community</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              {common_patterns.map((item, index) => (
                <div key={item.pattern} style={{ border: '1px solid var(--color-border-light)', borderRadius: 'var(--radius-md)', padding: 12 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, marginBottom: 8 }}>
                    <strong style={{ fontSize: '0.95rem' }}>{item.pattern}</strong>
                    <span className="badge badge--brand" style={{ fontSize: '0.7rem' }}>{item.dominant_dosha}</span>
                  </div>
                  <div className="progress-bar-track" style={{ height: 8 }}>
                    <div
                      className="progress-bar-fill"
                      style={{ width: `${item.frequency_percentage}%`, background: trendColors[index % trendColors.length] }}
                    />
                  </div>
                  <div style={{ marginTop: 6, color: 'var(--color-text-muted)', fontSize: '0.78rem' }}>
                    {item.frequency_percentage}% of community responses
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div style={{ marginTop: 28, display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: 24 }}>
          <div className="card card--elevated">
            <div style={{ marginBottom: 18 }}>
              <h3 style={{ marginBottom: 6 }}>AYUSH service match overview</h3>
              <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>Preferred service mix across wellness goals</p>
            </div>
            <div style={{ width: '100%', height: 220 }}>
              <ResponsiveContainer>
                <BarChart data={ayush_matches}>
                  <CartesianGrid stroke="rgba(87, 101, 96, 0.12)" vertical={false} />
                  <XAxis dataKey="system" tickLine={false} axisLine={false} tick={{ fill: '#576560', fontSize: 12 }} />
                  <YAxis domain={[0, 100]} tickLine={false} axisLine={false} tick={{ fill: '#576560', fontSize: 12 }} />
                  <Tooltip formatter={(value: number | string | readonly (number | string)[] | undefined) => {
                    const numericValue = Array.isArray(value) ? value[0] : value;
                    return [`${numericValue ?? 0}%`, 'Share'] as [string, string];
                  }} />
                  <Bar dataKey="share_percentage" radius={[8, 8, 0, 0]}>
                    {ayush_matches.map((entry, index) => (
                      <Cell key={entry.system} fill={trendColors[index % trendColors.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card card--elevated">
            <div style={{ marginBottom: 18 }}>
              <h3 style={{ marginBottom: 6 }}>Recommended services</h3>
              <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>Best-fit community recommendations</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              {ayush_matches.map((item, index) => (
                <div key={item.system} style={{ padding: '12px 14px', background: 'var(--color-bg)', borderRadius: 'var(--radius-md)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                    <strong>{item.system}</strong>
                    <span style={{ color: trendColors[index % trendColors.length], fontWeight: 700 }}>{item.share_percentage}%</span>
                  </div>
                  <div style={{ color: 'var(--color-text-muted)', fontSize: '0.82rem' }}>{item.top_service}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
