export type Role = "trainee" | "trainer" | "admin";

export interface User {
  id: string;
  email: string;
  name: string;
  role: Role;
  title: string;
  organization: string;
  initials: string;
}

export interface StatItem {
  label: string;
  value: string;
  trend: string;
  tone: string;
}

export interface CompetencyItem {
  name: string;
  score: number;
  status: string;
  gap: number;
  target: number;
  recommended_course: string;
  recommended_trainer: string;
  hours: number;
}

export interface LearningPathStep {
  id: string;
  title: string;
  status: string;
  meta: string;
  description: string;
}

export interface CourseItem {
  id: string;
  title: string;
  category: string;
  description: string;
  trainer: string;
  progress: number;
  lessons: number;
  duration: string;
  level: string;
  tag: string;
  accent: string;
  enrolled: boolean;
}

export interface TrainerItem {
  id: string;
  name: string;
  title: string;
  expertise: string[];
  experience: string;
  match: number;
  availability: string;
  sessions: number;
  verified: boolean;
}

export interface AlertItem {
  id: string;
  title: string;
  description: string;
  level: string;
  action: string;
}

export interface HeatmapRow {
  competency: string;
  beginner: number;
  intermediate: number;
  advanced: number;
  expert: number;
}

export interface ImpactMetric {
  label: string;
  value: string;
  change: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  description: string;
  time: string;
  read: boolean;
  type: string;
}

export interface OverviewResponse {
  current_user: User;
  role: Role;
  stats: StatItem[];
  competencies: CompetencyItem[];
  learning_path: LearningPathStep[];
  courses: CourseItem[];
  trainers: TrainerItem[];
  alerts: AlertItem[];
  heatmap: HeatmapRow[];
  impact: ImpactMetric[];
  notifications: NotificationItem[];
  ai_summary: string;
}

export interface ActionResponse {
  status: string;
  message: string;
  data: Record<string, unknown>;
}

export interface AssessmentResult {
  score: number;
  correct: number;
  wrong: number;
  skipped: number;
  feedback: string;
  competency_breakdown: Record<string, number>;
  next_activity: string;
}

export interface GeneratedQuestion {
  id: string;
  prompt: string;
  options: string[];
  answer: string;
  explanation: string;
  difficulty: string;
}

export interface GeneratedAssessment {
  id: string;
  title: string;
  subject: string;
  topic: string;
  difficulty: string;
  status: string;
  questions: GeneratedQuestion[];
}

export interface ResourceResponse {
  id: string;
  filename: string;
  resource_type: string;
  size_bytes: number;
  uploaded_by: string;
}