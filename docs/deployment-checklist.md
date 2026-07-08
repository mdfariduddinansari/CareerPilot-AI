# Deployment Checklist

## Frontend (Vercel)
- Set root to `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Env: `VITE_API_BASE_URL`

## Backend (Render)
- Service root: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Env: `DATABASE_URL`, `SECRET_KEY`, `ALLOWED_ORIGINS`, optional AI keys

## Database
- Use managed PostgreSQL (Render/Supabase)
- Run Alembic migrations:
  - `cd backend`
  - `alembic upgrade head`
