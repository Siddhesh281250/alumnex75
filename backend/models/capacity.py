from typing import Any

from pydantic import BaseModel, Field


class DemoUser(BaseModel):
    id: str
    email: str
    name: str
    role: str
    title: str
    organization: str
    initials: str


class LoginRequest(BaseModel):
    email: str
    password: str


class StatItem(BaseModel):
    label: str
    value: str
    trend: str
    tone: str


class CompetencyItem(BaseModel):
    name: str
    score: int
    status: str
    gap: int
    target: int
    recommended_course: str
    recommended_trainer: str
    hours: int


class LearningPathStep(BaseModel):
    id: str
    title: str
    status: str
    meta: str
    description: str


class CourseItem(BaseModel):
    id: str
    title: str
    category: str
    description: str
    trainer: str
    progress: int
    lessons: int
    duration: str
    level: str
    tag: str
    accent: str
    enrolled: bool = False


class TrainerItem(BaseModel):
    id: str
    name: str
    title: str
    expertise: list[str]
    experience: str
    match: int
    availability: str
    sessions: int
    verified: bool = True


class AlertItem(BaseModel):
    id: str
    title: str
    description: str
    level: str
    action: str


class HeatmapRow(BaseModel):
    competency: str
    beginner: int
    intermediate: int
    advanced: int
    expert: int


class ImpactMetric(BaseModel):
    label: str
    value: str
    change: str


class NotificationItem(BaseModel):
    id: str
    title: str
    description: str
    time: str
    read: bool
    type: str


class OverviewResponse(BaseModel):
    current_user: DemoUser
    role: str
    stats: list[StatItem]
    competencies: list[CompetencyItem]
    learning_path: list[LearningPathStep]
    courses: list[CourseItem]
    trainers: list[TrainerItem]
    alerts: list[AlertItem]
    heatmap: list[HeatmapRow]
    impact: list[ImpactMetric]
    notifications: list[NotificationItem]
    ai_summary: str


class CourseActionRequest(BaseModel):
    course_id: str


class LearningPathRequest(BaseModel):
    focus: str = "Cybersecurity and Data Analytics"


class AssessmentSubmitRequest(BaseModel):
    assessment_id: str
    answers: dict[str, str] = Field(default_factory=dict)


class MentorshipRequest(BaseModel):
    trainer_id: str
    message: str = "I would like guidance on my next competency milestone."


class GenerateAssessmentRequest(BaseModel):
    subject: str = "Numerical Weather Prediction"
    topic: str = "Model validation and forecast verification"
    questions: int = 5
    difficulty: str = "Intermediate"


class GeneratedQuestion(BaseModel):
    id: str
    prompt: str
    options: list[str]
    answer: str
    explanation: str
    difficulty: str


class GeneratedAssessment(BaseModel):
    id: str
    title: str
    subject: str
    topic: str
    difficulty: str
    status: str
    questions: list[GeneratedQuestion]


class AssessmentResult(BaseModel):
    score: int
    correct: int
    wrong: int
    skipped: int
    feedback: str
    competency_breakdown: dict[str, int]
    next_activity: str


class ActionResponse(BaseModel):
    status: str
    message: str
    data: dict[str, Any] = Field(default_factory=dict)


class ResourceResponse(BaseModel):
    id: str
    filename: str
    resource_type: str
    size_bytes: int
    uploaded_by: str