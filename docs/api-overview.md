# CareerPilot AI API Overview

Base URL: `/api/v1`

## Public
- `GET /health`
- `POST /auth/signup`
- `POST /auth/login`

## Protected (JWT via `X-Auth-Token` header)
- `GET /auth/me`
- `GET /dashboard/summary`
- `POST /resume/analyze`
- `POST /ats/check`
- `POST /cover-letter/generate`
- `POST /interview/questions`
- `POST /interview/evaluate`
- `POST /linkedin/generate`
- `GET /jobs`
- `POST /jobs`
- `PATCH /jobs/{id}`
- `POST /skills/analyze`

All APIs return:
```json
{ "success": true, "data": {}, "message": "OK", "errors": [] }
```
