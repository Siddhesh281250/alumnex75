import asyncio
import os
import uuid

from lib.db import db, ensure_indexes
from routers.auth import hash_password


DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "Demo@123")


async def seed_demo_data() -> None:
    if await db.users.count_documents({}) == 0:
        users = [
            {"id": "user-trainee", "email": os.environ.get("DEMO_TRAINEE_EMAIL", "trainee@capacityconnect.gov.in"), "password_hash": hash_password(DEMO_PASSWORD), "name": "Dr. Ananya Sharma", "role": "trainee", "title": "Senior Scientific Assistant", "organization": "Regional Meteorological Centre, Pune", "initials": "AS"},
            {"id": "user-trainer", "email": os.environ.get("DEMO_TRAINER_EMAIL", "trainer@capacityconnect.gov.in"), "password_hash": hash_password(DEMO_PASSWORD), "name": "Dr. Rajesh Kumar", "role": "trainer", "title": "Senior Radar Specialist", "organization": "IMD Training Centre, New Delhi", "initials": "RK"},
            {"id": "user-admin", "email": os.environ.get("DEMO_ADMIN_EMAIL", "admin@capacityconnect.gov.in"), "password_hash": hash_password(DEMO_PASSWORD), "name": "Shri Vikramaditya", "role": "admin", "title": "Director General, Capacity Building", "organization": "Ministry of Earth Sciences", "initials": "SV"},
        ]
        await db.users.insert_many(users)

    if await db.courses.count_documents({}) == 0:
        titles = [
            "NWP Model Validation Lab", "Advanced Radar Interpretation", "Cyber Defense for Weather Systems", "Satellite Image Interpretation", "Python for Forecast Operations", "Climate Data Analytics", "Monsoon Forecasting Practicum", "Leadership in Scientific Operations", "Effective Technical Communication", "GIS for Meteorological Services", "Cloud Computing for HPC Workflows", "AI for Early Warning Systems",
        ]
        await db.courses.insert_many([{"id": f"course-{index + 1}", "title": title, "status": "published", "created_by": "user-trainer"} for index, title in enumerate(titles)])
    for collection, count, label in [
        ("trainers", 5, "Trainer"),
        ("competencies", 8, "Competency"),
        ("assessments", 10, "Assessment"),
        ("certificates", 15, "Certificate"),
        ("announcements", 10, "Announcement"),
        ("notifications", 15, "Notification"),
        ("discussions", 10, "Discussion"),
        ("resources", 20, "Resource"),
    ]:
        if await db[collection].count_documents({}) == 0:
            await db[collection].insert_many([{"id": str(uuid.uuid4()), "name": f"{label} {index + 1}", "status": "active"} for index in range(count)])
    await ensure_indexes()


if __name__ == "__main__":
    asyncio.run(seed_demo_data())