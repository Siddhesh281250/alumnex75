import os
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from lib.db import db
from models.capacity import (
    ActionResponse,
    AssessmentResult,
    AssessmentSubmitRequest,
    CourseActionRequest,
    GenerateAssessmentRequest,
    GeneratedAssessment,
    GeneratedQuestion,
    LearningPathRequest,
    MentorshipRequest,
    OverviewResponse,
    ResourceResponse,
)
from routers.auth import CurrentUser


router = APIRouter(prefix="/demo", tags=["demo"])


def overview_for(user: dict) -> dict:
    role = user["role"]
    if role == "admin":
        stats = [
            {"label": "Active learners", "value": "2,486", "trend": "+12.8%", "tone": "teal"},
            {"label": "Active trainers", "value": "128", "trend": "+8.4%", "tone": "blue"},
            {"label": "Completion rate", "value": "78.6%", "trend": "+6.2 pts", "tone": "purple"},
            {"label": "Certificates issued", "value": "1,942", "trend": "+18.9%", "tone": "amber"},
        ]
    elif role == "trainer":
        stats = [
            {"label": "Active courses", "value": "08", "trend": "+2 this quarter", "tone": "blue"},
            {"label": "Total trainees", "value": "486", "trend": "+24 this month", "tone": "teal"},
            {"label": "Avg. completion", "value": "82.4%", "trend": "+4.8 pts", "tone": "purple"},
            {"label": "Feedback score", "value": "4.8/5", "trend": "Top 5%", "tone": "amber"},
        ]
    else:
        stats = [
            {"label": "Courses enrolled", "value": "08", "trend": "+2 this month", "tone": "blue"},
            {"label": "Learning hours", "value": "42.5h", "trend": "+8.2h", "tone": "teal"},
            {"label": "Current competency", "value": "62%", "trend": "+14 pts", "tone": "purple"},
            {"label": "Certificates earned", "value": "06", "trend": "+2 this quarter", "tone": "amber"},
        ]
    return {
        "current_user": user,
        "role": role,
        "stats": stats,
        "competencies": [
            {"name": "Doppler Radar", "score": 80, "status": "Strong", "gap": 20, "target": 90, "recommended_course": "Advanced Radar Interpretation", "recommended_trainer": "Dr. Rajesh Kumar", "hours": 6},
            {"name": "Numerical Weather Modeling", "score": 68, "status": "Developing", "gap": 32, "target": 85, "recommended_course": "NWP Model Validation Lab", "recommended_trainer": "Dr. Meera Nair", "hours": 12},
            {"name": "Satellite Meteorology", "score": 74, "status": "Developing", "gap": 26, "target": 88, "recommended_course": "Satellite Image Interpretation", "recommended_trainer": "Dr. Ananya Bose", "hours": 8},
            {"name": "Cybersecurity", "score": 41, "status": "Needs improvement", "gap": 59, "target": 78, "recommended_course": "Cyber Defense for Weather Systems", "recommended_trainer": "Arjun Menon", "hours": 10},
            {"name": "Python & Data", "score": 58, "status": "Developing", "gap": 42, "target": 82, "recommended_course": "Python for Forecast Operations", "recommended_trainer": "Dr. Meera Nair", "hours": 9},
        ],
        "learning_path": [
            {"id": "lp-1", "title": "Python for Forecast Operations", "status": "completed", "meta": "6 lessons • 4.5 hours", "description": "Build a strong scripting baseline for operational data workflows."},
            {"id": "lp-2", "title": "NWP Model Validation Lab", "status": "current", "meta": "8 lessons • 12 hours", "description": "Compare model output with observations and communicate forecast confidence."},
            {"id": "lp-3", "title": "Cyber Defense for Weather Systems", "status": "locked", "meta": "7 lessons • 10 hours", "description": "Protect radar, HPC and observation networks against common attack paths."},
            {"id": "lp-4", "title": "Advanced Competency Assessment", "status": "locked", "meta": "40 questions • 45 min", "description": "Validate progress across priority IMD operational competencies."},
        ],
        "courses": [
            {"id": "course-nwp", "title": "NWP Model Validation Lab", "category": "Numerical Weather Prediction", "description": "Move from model output to trusted forecast decisions with guided lab work.", "trainer": "Dr. Meera Nair", "progress": 42, "lessons": 8, "duration": "12 hours", "level": "Intermediate", "tag": "Priority path", "accent": "cyan", "enrolled": True},
            {"id": "course-radar", "title": "Advanced Radar Interpretation", "category": "Doppler Radar", "description": "Read signatures, diagnose severe weather and communicate radar intelligence.", "trainer": "Dr. Rajesh Kumar", "progress": 18, "lessons": 10, "duration": "9 hours", "level": "Advanced", "tag": "Recommended", "accent": "indigo", "enrolled": False},
            {"id": "course-cyber", "title": "Cyber Defense for Weather Systems", "category": "Cybersecurity", "description": "Build cyber hygiene for sensor networks, HPC environments and response teams.", "trainer": "Arjun Menon", "progress": 0, "lessons": 7, "duration": "10 hours", "level": "Foundation", "tag": "Closes your gap", "accent": "rose", "enrolled": False},
            {"id": "course-satellite", "title": "Satellite Image Interpretation", "category": "Satellite Meteorology", "description": "Turn multi-spectral imagery into actionable nowcasting insights.", "trainer": "Dr. Ananya Bose", "progress": 64, "lessons": 9, "duration": "8 hours", "level": "Intermediate", "tag": "In progress", "accent": "amber", "enrolled": True},
        ],
        "trainers": [
            {"id": "trainer-rajesh", "name": "Dr. Rajesh Kumar", "title": "Senior Radar Specialist", "expertise": ["Doppler Radar", "Nowcasting", "Severe Weather"], "experience": "18 years", "match": 96, "availability": "2 slots this week", "sessions": 142, "verified": True},
            {"id": "trainer-meera", "name": "Dr. Meera Nair", "title": "NWP & Data Science Lead", "expertise": ["NWP", "Python", "Forecast Verification"], "experience": "14 years", "match": 91, "availability": "Available tomorrow", "sessions": 98, "verified": True},
            {"id": "trainer-arjun", "name": "Arjun Menon", "title": "Weather Systems Security Architect", "expertise": ["Cybersecurity", "HPC Security", "Incident Response"], "experience": "11 years", "match": 88, "availability": "3 slots this week", "sessions": 76, "verified": True},
            {"id": "trainer-ananya", "name": "Dr. Ananya Bose", "title": "Satellite Meteorology Faculty", "expertise": ["Satellite", "GIS", "Remote Sensing"], "experience": "16 years", "match": 84, "availability": "Next week", "sessions": 118, "verified": True},
        ],
        "alerts": [
            {"id": "alert-1", "title": "Attention required", "description": "12 trainees have not accessed an enrolled course for more than 14 days.", "level": "warning", "action": "Send reminder"},
            {"id": "alert-2", "title": "Assessment signal", "description": "SQL joins and model validation are the most frequently missed topics this month.", "level": "info", "action": "View practice"},
        ],
        "heatmap": [
            {"competency": "Python & Data", "beginner": 22, "intermediate": 35, "advanced": 18, "expert": 5},
            {"competency": "Cybersecurity", "beginner": 40, "intermediate": 20, "advanced": 7, "expert": 2},
            {"competency": "Data Analytics", "beginner": 30, "intermediate": 25, "advanced": 10, "expert": 3},
            {"competency": "Radar Intelligence", "beginner": 15, "intermediate": 32, "advanced": 18, "expert": 8},
            {"competency": "Leadership", "beginner": 15, "intermediate": 32, "advanced": 18, "expert": 8},
        ],
        "impact": [
            {"label": "Employees trained", "value": "2,486", "change": "+12.8%"},
            {"label": "Course completion", "value": "78.6%", "change": "+6.2 pts"},
            {"label": "Assessment improvement", "value": "+21 pts", "change": "vs. baseline"},
            {"label": "Competency growth", "value": "+28 pts", "change": "platform measured"},
        ],
        "notifications": [
            {"id": "n-1", "title": "New course recommendation", "description": "Cyber Defense for Weather Systems closes your largest gap.", "time": "12 min ago", "read": False, "type": "recommendation"},
            {"id": "n-2", "title": "Assessment deadline Friday", "description": "NWP Model Validation Lab checkpoint is due this week.", "time": "2 hours ago", "read": False, "type": "deadline"},
            {"id": "n-3", "title": "Certificate issued", "description": "Your Satellite Meteorology certificate is ready to download.", "time": "Yesterday", "read": True, "type": "certificate"},
        ],
        "ai_summary": "Your profile is strongest in Doppler Radar. Closing the Cybersecurity and NWP validation gaps would move your role-readiness score from 62% to an estimated 81%.",
    }


@router.get("/overview", response_model=OverviewResponse)
async def get_overview(user: CurrentUser):
    return overview_for(user)


@router.post("/enroll", response_model=ActionResponse)
async def enroll(input: CourseActionRequest, user: CurrentUser):
    await db.enrollments.update_one(
        {"user_id": user["id"], "course_id": input.course_id},
        {"$set": {"user_id": user["id"], "course_id": input.course_id, "status": "active"}},
        upsert=True,
    )
    return ActionResponse(status="success", message="Course added to your learning plan.", data={"course_id": input.course_id})


@router.post("/learning-path", response_model=ActionResponse)
async def generate_learning_path(input: LearningPathRequest, user: CurrentUser):
    await db.learning_paths.update_one(
        {"user_id": user["id"]},
        {"$set": {"user_id": user["id"], "focus": input.focus, "status": "generated"}},
        upsert=True,
    )
    return ActionResponse(status="success", message="A tailored learning path is ready.", data={"focus": input.focus, "steps": 4})


@router.post("/assessment/submit", response_model=AssessmentResult)
async def submit_assessment(input: AssessmentSubmitRequest, user: CurrentUser):
    await db.assessment_attempts.insert_one({"id": str(uuid.uuid4()), "user_id": user["id"], "assessment_id": input.assessment_id, "answers": input.answers, "score": 78})
    return AssessmentResult(
        score=78,
        correct=39,
        wrong=11,
        skipped=0,
        feedback="You perform strongly in Python fundamentals and radar interpretation, but need additional practice in SQL joins and model validation confidence intervals.",
        competency_breakdown={"Python & Data": 85, "NWP Validation": 62, "Radar Intelligence": 90},
        next_activity="Complete the SQL Joins practice lab, then revisit NWP validation examples.",
    )


@router.post("/mentorship", response_model=ActionResponse)
async def request_mentorship(input: MentorshipRequest, user: CurrentUser):
    await db.mentorship_requests.insert_one({"id": str(uuid.uuid4()), "user_id": user["id"], "trainer_id": input.trainer_id, "message": input.message, "status": "requested"})
    return ActionResponse(status="success", message="Mentorship request sent. The trainer will respond through Capacity Connect.", data={"trainer_id": input.trainer_id})


@router.post("/assessment/generate", response_model=GeneratedAssessment)
async def generate_assessment(input: GenerateAssessmentRequest, user: CurrentUser):
    questions = [
        GeneratedQuestion(id="q-1", prompt="Which verification metric best captures systematic forecast bias?", options=["Mean bias error", "Random forest depth", "Pixel saturation", "File checksum"], answer="Mean bias error", explanation="Mean bias error shows whether forecasts consistently over- or under-predict observations.", difficulty=input.difficulty),
        GeneratedQuestion(id="q-2", prompt="Why is a holdout dataset important in model evaluation?", options=["It tests generalisation", "It increases font size", "It removes all uncertainty", "It replaces observations"], answer="It tests generalisation", explanation="A holdout dataset estimates performance on unseen cases.", difficulty=input.difficulty),
        GeneratedQuestion(id="q-3", prompt="Which input is essential for a reliable radar nowcast?", options=["Quality-controlled reflectivity", "A colour palette", "A meeting invite", "A static logo"], answer="Quality-controlled reflectivity", explanation="Quality-controlled radar observations are a foundation for trustworthy nowcasting.", difficulty=input.difficulty),
    ]
    return GeneratedAssessment(id=str(uuid.uuid4()), title=f"{input.topic} Checkpoint", subject=input.subject, topic=input.topic, difficulty=input.difficulty, status="Needs trainer review", questions=questions[: max(1, min(input.questions, len(questions)))])


@router.post("/assessment/publish", response_model=ActionResponse)
async def publish_assessment(user: CurrentUser):
    if user["role"] not in {"trainer", "admin"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only trainers can publish assessments")
    return ActionResponse(status="success", message="Assessment approved and published to the selected cohort.", data={"published": True})


@router.post("/resources/upload", response_model=ResourceResponse)
async def upload_resource(user: CurrentUser, file: UploadFile = File(...)):
    allowed = {".pdf", ".ppt", ".pptx", ".doc", ".docx", ".mp4", ".png", ".jpg"}
    extension = Path(file.filename or "").suffix.lower()
    if extension not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported resource type")
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Resource must be smaller than 10 MB")
    upload_dir = Path(__file__).resolve().parent.parent / "uploads"
    upload_dir.mkdir(exist_ok=True)
    resource_id = str(uuid.uuid4())
    stored_name = f"{resource_id}{extension}"
    (upload_dir / stored_name).write_bytes(contents)
    await db.resources.insert_one({"id": resource_id, "filename": file.filename, "resource_type": extension.lstrip("."), "size_bytes": len(contents), "uploaded_by": user["id"], "stored_name": stored_name})
    return ResourceResponse(id=resource_id, filename=file.filename or stored_name, resource_type=extension.lstrip("."), size_bytes=len(contents), uploaded_by=user["name"])