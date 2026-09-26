# Capacity Connect authentication testing

Demo accounts are seeded on backend startup. Use the public preview URL or the local Vite URL and log in through `/login`.

- trainee@capacityconnect.gov.in / Demo@123
- trainer@capacityconnect.gov.in / Demo@123
- admin@capacityconnect.gov.in / Demo@123

Key routes:

- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/logout`
- `GET /api/demo/overview`

The access session is an httpOnly cookie. A successful login followed by `/api/auth/me` should return the same role and name without exposing a token in JSON.