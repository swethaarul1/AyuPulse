/**
 * AyuPulse API Client
 * Central axios instance + typed API methods.
 */
import axios from 'axios';

export const SESSION_KEY = (() => {
  let key = localStorage.getItem('ayupulse_session');
  if (!key) {
    key = 'session-' + Math.random().toString(36).slice(2) + Date.now();
    localStorage.setItem('ayupulse_session', key);
  }
  return key;
})();

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Types ─────────────────────────────────────────────────────────────────

export interface Question {
  id: string;
  category: string;
  text: string;
  options: { label: string }[];
}

export interface DoshaResult {
  id: string;
  assessment_id: string;
  vata_score: number;
  pitta_score: number;
  kapha_score: number;
  vata_pct: number;
  pitta_pct: number;
  kapha_pct: number;
  dominant: string;
  secondary: string | null;
  confidence: number;
  explanation: string | null;
  reasoning_points: string[] | null;
  created_at: string;
}

export interface Assessment {
  id: string;
  user_id: string;
  created_at: string;
  dosha_result: DoshaResult | null;
}

export interface PlanTask {
  id: string;
  plan_id: string;
  title: string;
  category: string;
  duration: string | null;
  what: string;
  why: string;
  how: string;
  safety: string;
  sort_order: number;
  is_adjusted: boolean;
  is_completed_today: boolean;
}

export interface PreventivePlan {
  id: string;
  user_id: string;
  dosha_result_id: string;
  created_at: string;
  tasks: PlanTask[];
}

export interface CheckIn {
  id: string;
  user_id: string;
  sleep_score: number;
  stress_score: number;
  mood_score: number;
  digestion_score: number;
  created_at: string;
  is_seeded: boolean;
}

export interface WellnessScore {
  score: number;
  trend: string | null;
  label: string;
  message: string;
}

export interface PatternInsight {
  pattern_type: string;
  insight_text: string;
  adjustment_tasks: { title: string; category: string; duration: string }[] | null;
  has_adjustment: boolean;
}

export interface Dashboard {
  wellness_score: WellnessScore;
  weekly_averages: { sleep: number; stress: number; mood: number; digestion: number };
  pattern_insight: PatternInsight | null;
  recent_check_ins: CheckIn[];
  has_plan: boolean;
  plan_id: string | null;
  dosha_result: DoshaResult | null;
}

export interface TaskCompleteResponse {
  task_id: string;
  completed: boolean;
  completed_at: string | null;
}

// ── API Methods ────────────────────────────────────────────────────────────

export const ayuApi = {
  // Assessment
  getQuestions: () =>
    api.get<{ questions: Question[] }>('/assessment/questions').then(r => r.data),

  submitAssessment: (answers: Record<string, number>) =>
    api.post<Assessment>('/assessment', {
      session_key: SESSION_KEY,
      answers,
    }).then(r => r.data),

  getAssessment: (id: string) =>
    api.get<Assessment>(`/assessment/${id}`).then(r => r.data),

  getDoshaResult: (id: string) =>
    api.get<DoshaResult>(`/assessment/result/${id}`).then(r => r.data),

  // Plan
  createPlan: (doshaResultId: string) =>
    api.post<PreventivePlan>('/plan', {
      session_key: SESSION_KEY,
      dosha_result_id: doshaResultId,
    }).then(r => r.data),

  getPlan: (planId: string) =>
    api.get<PreventivePlan>(`/plan/${planId}`).then(r => r.data),

  getPlanBySession: () =>
    api.get<PreventivePlan>(`/plan/by-session/${SESSION_KEY}`).then(r => r.data),

  completeTask: (taskId: string) =>
    api.post<TaskCompleteResponse>(`/plan/tasks/${taskId}/complete`, {}).then(r => r.data),

  // CheckIn
  submitCheckIn: (data: { sleep_score: number; stress_score: number; mood_score: number; digestion_score: number }) =>
    api.post<CheckIn>('/checkins', { session_key: SESSION_KEY, ...data }).then(r => r.data),

  getCheckIns: () =>
    api.get<CheckIn[]>('/checkins', { params: { session_key: SESSION_KEY } }).then(r => r.data),

  getWellnessScore: () =>
    api.get<WellnessScore>('/wellness-score', { params: { session_key: SESSION_KEY } }).then(r => r.data),

  getPatternInsight: () =>
    api.get<PatternInsight | null>('/pattern-insight', { params: { session_key: SESSION_KEY } }).then(r => r.data),

  getDashboard: () =>
    api.get<Dashboard>('/dashboard', { params: { session_key: SESSION_KEY } }).then(r => r.data),
};

export default ayuApi;
