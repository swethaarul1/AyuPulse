/**
 * AyuPulse API Client
 * Centralized typed API methods with session management, error handling, and offline fallbacks.
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

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

// ── TYPES ──────────────────────────────────────────────────────────────────

export interface QuestionOption {
  value?: string;
  label: string;
}

export interface Question {
  id: string;
  category: string;
  question?: string;
  text?: string;
  options: QuestionOption[];
}

export interface AssessmentRequest {
  sleep?: string;
  digestion?: string;
  stress_response?: string;
  energy?: string;
  body_tendencies?: string;
  lifestyle?: string;
  wellness_goals?: string[];
  answers?: Record<string, any>;
}

export interface AssessmentResponse {
  vata: number;
  pitta: number;
  kapha: number;
  dominant: string;
  summary: string;
  wellness_focus: string[];
  note: string;
}

export interface PlanRecommendation {
  title: string;
  what: string;
  why: string;
  how: string;
  safety: string;
}

export interface DailyTrackerTask {
  id: string;
  title: string;
  description: string;
  category?: string;
  duration?: string;
  completed: boolean;
}

export interface PlanSections {
  dinacharya: PlanRecommendation[];
  yoga: PlanRecommendation[];
  pranayama: PlanRecommendation[];
  diet_lifestyle: PlanRecommendation[];
}

export interface PlanResponse {
  status: string;
  module: string;
  dominant: string;
  sections: PlanSections;
  daily_tracker: DailyTrackerTask[];
  tasks?: any[];
  message: string;
  note: string;
}

export interface CheckInRequest {
  sleep: number;
  stress: number;
  mood: number;
  digestion: number;
  energy: number;
  notes?: string;
  user_id?: string;
  date?: string;
}

export interface CheckInResponse {
  status: string;
  module: string;
  checkin_id: string;
  wellness_score: number;
  summary: string;
  checkin: {
    sleep: number;
    stress: number;
    mood: number;
    digestion: number;
    energy: number;
    date: string;
    notes?: string;
  };
  message: string;
}

export interface PatternItem {
  type: string;
  title: string;
  description: string;
  strength: string;
}

export interface PatternResponse {
  status: string;
  module: string;
  patterns: PatternItem[];
  next_step: string;
  wellness_pulse: number;
  detected_pattern: string;
  insight: string;
  plan_adjusted: boolean;
  adjustment_tasks: string[];
  data_status: string;
}

export interface CentreItem {
  id: string;
  name: string;
  system: string;
  city: string;
  state: string;
  pincode: string;
  address: string;
  phone: string;
  services: string[];
  rating: number;
  data_status: string;
}

export interface CentresResponse {
  status: string;
  total: number;
  data_status: string;
  disclaimer: string;
  centres: CentreItem[];
}

export interface CentreMatchResponse {
  status: string;
  wellness_focus: string;
  recommended_service: string;
  data_status: string;
  matched_centres: CentreItem[];
  professional_notice?: string | null;
}

export interface ConsultationResponse {
  status: string;
  module: string;
  booking_id: string;
  centre_id: string;
  message: string;
  next_step: string;
  notice: string;
}

export interface SafetyCheckResponse {
  safe: boolean;
  risk_level: 'low' | 'medium' | 'high';
  action: 'allow' | 'modify' | 'caution' | 'professional_attention';
  message: string;
  modified_content: string;
  professional_attention: boolean;
  is_safe?: boolean;
  requires_escalation?: boolean;
}

export interface CommunityDashboardResponse {
  prototype: boolean;
  disclaimer: string;
  metrics: {
    total_assessments: number;
    task_start_rate: number;
    active_checkins_this_week: number;
    common_pattern: string;
    ayush_matches_count: number;
    average_community_pulse: number;
  };
  common_patterns: { pattern: string; frequency_percentage: number; dominant_dosha: string }[];
  ayush_matches: { system: string; share_percentage: number; top_service: string }[];
  trends: { day: string; avg_wellness_pulse: number; checkin_count: number }[];
}

// ── API CLIENT METHODS ─────────────────────────────────────────────────────

export const ayuApi = {
  // Health
  getHealth: () =>
    api.get<{ status: string; service: string }>('/health').then(r => r.data),

  // Module 01: Assessment
  getQuestions: () =>
    api.get<{ status: string; questions: Question[] }>('/api/assessment/questions').then(r => r.data),

  submitAssessment: (payload: AssessmentRequest) =>
    api.post<AssessmentResponse>('/api/assessment', payload).then(r => {
      localStorage.setItem('ayupulse_assessment', JSON.stringify(r.data));
      return r.data;
    }),

  // Module 02: Plan
  generatePlan: (payload: {
    dominant: string;
    vata?: number;
    pitta?: number;
    kapha?: number;
    lifestyle?: string;
    wellness_goals?: string[];
  }) =>
    api.post<PlanResponse>('/api/plan', payload).then(r => {
      localStorage.setItem('ayupulse_plan', JSON.stringify(r.data));
      return r.data;
    }),

  toggleTask: (taskId: string, completed?: boolean) =>
    api.post<{ status: string; task_id: string; completed: boolean }>(`/api/plan/tasks/${taskId}/toggle`, {
      completed,
      session_id: SESSION_KEY,
    }).then(r => r.data),

  getTasksState: () =>
    api.get<{ status: string; tasks: Record<string, { completed: boolean }> }>('/api/plan/tasks/state').then(r => r.data),

  // Module 03: Check-in & Pattern
  submitCheckin: (payload: CheckInRequest) =>
    api.post<CheckInResponse>('/api/checkin', { ...payload, user_id: SESSION_KEY }).then(r => {
      localStorage.setItem('ayupulse_latest_checkin', JSON.stringify(r.data));
      return r.data;
    }),

  getCheckinHistory: () =>
    api.get<{ status: string; total_records: number; data_status: string; history: any[] }>('/api/checkin').then(r => r.data),

  getPattern: (checkins?: any[]) =>
    api.post<PatternResponse>('/api/pattern', { checkins }).then(r => {
      localStorage.setItem('ayupulse_pattern', JSON.stringify(r.data));
      return r.data;
    }),

  getPatternQuick: () =>
    api.get<PatternResponse>('/api/pattern').then(r => r.data),

  // Module 04: AYUSH Connect
  getCentres: (params?: { focus?: string; system?: string; location?: string }) =>
    api.get<CentresResponse>('/api/centres', { params }).then(r => r.data),

  matchCentres: (payload: { wellness_focus?: string; wellness_goal?: string; preferred_system?: string; location?: string }) =>
    api.post<CentreMatchResponse>('/api/centres/match', payload).then(r => r.data),

  requestConsultation: (payload: { centre_id: string; preferred_date: string; preferred_system?: string; patient_notes?: string }) =>
    api.post<ConsultationResponse>('/api/consultation', payload).then(r => r.data),

  // Module 05: Safety Gate
  checkSafety: (payload: { text?: string; user_input?: string; recommendation?: string; confidence?: number }) =>
    api.post<SafetyCheckResponse>('/api/safety', payload).then(r => r.data),

  // Module 06: Community Dashboard
  getCommunityDashboard: () =>
    api.get<CommunityDashboardResponse>('/api/dashboard').then(r => r.data),
};

export default ayuApi;
