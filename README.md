# CareerPilot AI

**Tagline:** _Everything you need to land your dream job — powered by AI._

**Website:** [http://localhost:5173](http://localhost:5173)

CareerPilot AI is a production-ready v1 AI career operating system with authentication, analytics dashboard, resume/ATS intelligence, interview prep, job tracking, and roadmap generation.

## Features (v1)

- Email/password authentication with JWT session flow
- Mission-control dashboard with key career metrics
- AI Resume Analyzer (provider abstraction + heuristic fallback)
- ATS Checker (match %, keyword gaps, recommendations)
- Cover Letter Generator (editable + PDF export)
- Interview Coach (question generation + answer scoring)
- LinkedIn Post Generator (multi-variant output)
- Job Tracker Kanban with drag/drop status updates
- Skill Gap Analyzer + 4-week Learning Roadmap
- Dark mode, responsive UI, and protected routes

## Architecture

- **Frontend:** React 18 + Vite + Tailwind + React Router + React Query + Axios + RHF/Zod + Recharts + Framer Motion
- **Backend:** FastAPI + SQLAlchemy + Alembic + JWT auth + Pydantic validation
- **Database:** PostgreSQL in Docker/local production setups; SQLite fallback for quick local startup
- **Deployment:** Vercel (frontend) + Render (backend) + Supabase/Render Postgres

## Folder Structure

```text
CareerPilot-AI/
├── frontend/
├── backend/
├── docs/
├── screenshots/
├── tests/
├── docker/
├── docker-compose.yml
├── vercel.json
├── .gitignore
├── LICENSE
└── README.md
```

## Environment Variables

### Frontend (`frontend/.env`)

| Variable | Description | Example |
|---|---|---|
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000/api/v1` |

### Backend (`backend/.env`)

| Variable | Description | Example |
|---|---|---|
| `APP_NAME` | API title | `CareerPilot AI API` |
| `SECRET_KEY` | JWT signing key | `change-me` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiry minutes | `1440` |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./careerpilot.db` |
| `DB_HOST`/`DB_PORT`/`DB_USER`/`DB_PASSWORD`/`DB_NAME` | Postgres parts (optional if DATABASE_URL set) | `postgres` etc. |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins | `http://localhost:5173` |
| `OPENAI_API_KEY` | Optional AI provider key | empty |
| `GEMINI_API_KEY` | Optional AI provider key | empty |

## Local Setup

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### 2) Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Migrations (Alembic)

```bash
cd backend
alembic upgrade head
```

## Docker Full Stack

```bash
docker compose up --build
```

Services:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## API Response Shape

All endpoints use this contract:

```json
{
  "success": true,
  "data": {},
  "message": "OK",
  "errors": []
}
```

## Deployment

### Vercel (Frontend)
1. Import repo, set root directory to `frontend`
2. Build command: `npm run build`
3. Output: `dist`
4. Set env: `VITE_API_BASE_URL`

### Render (Backend)
1. New Web Service, root directory `backend`
2. Build: `pip install -r requirements.txt`
3. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables from `.env.example`

### Postgres (Render/Supabase)
- Provision DB and set either `DATABASE_URL` or DB component env vars.

## Additional Docs

- `docs/api-overview.md`
- `docs/deployment-checklist.md`

## Future Roadmap

- Real OpenAI/Gemini adapters with streaming completions
- File parsing for PDF/DOCX resume uploads
- DOCX export support
- Voice mock interviews
- GitHub/LinkedIn profile enrichment
