# CAPACITY CONNECT living spec

## Product
CAPACITY CONNECT is a hackathon-ready IMD / MoES capacity intelligence prototype. It connects trainee profiles, competency gaps, learning paths, courses, assessments, trainer expertise and organizational impact.

## Roles and access
- Trainee: Dr. Ananya Sharma demo account.
- Trainer: Dr. Rajesh Kumar demo account.
- Admin: Shri Vikramaditya demo account.
- Authentication uses email/password with an httpOnly JWT cookie session. The three accounts are demo-only and are seeded by the backend.

## Core demo flow
Login → trainee competency radar and skill gaps → generate learning path → enroll in NWP course → submit smart assessment → view competency feedback → request a trainer mentor → switch to trainer → review AI-generated assessment before publishing → switch to admin → inspect competency heatmap and training impact.

## Data model
MongoDB stores users, courses, enrollments, learning paths, assessment attempts, mentorship requests, resources, trainers, competencies, assessments, certificates, announcements, notifications and discussions. Demo overview data is returned by `/api/demo/overview` and action endpoints persist the key interactions.

## AI behavior
AI responses are deterministic, domain-rich mocked responses for the prototype. No external AI provider or key is used.

## Storage
Trainer resource uploads validate extensions and a 10 MB size limit, save files under the backend uploads abstraction, and persist metadata in MongoDB. This is local prototype storage, not production object storage.