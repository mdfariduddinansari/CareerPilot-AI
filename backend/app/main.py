from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import ats, auth, cover_letter, dashboard, health, interview, job_tracker, linkedin, resume, skill_gap
from app.config import settings
from app.database.base import Base
from app.database.session import engine

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins.split(',')],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS'],
    allow_headers=['*'],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={'success': False, 'data': None, 'message': 'Validation error', 'errors': [str(err['msg']) for err in exc.errors()]})


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    errors = exc.detail if isinstance(exc.detail, list) else [str(exc.detail)]
    return JSONResponse(status_code=exc.status_code, content={'success': False, 'data': None, 'message': 'Request failed', 'errors': errors})


@app.exception_handler(Exception)
async def common_exception_handler(_, exc: Exception):
    return JSONResponse(status_code=500, content={'success': False, 'data': None, 'message': 'Internal server error', 'errors': [str(exc)]})


@app.on_event('startup')
def startup_event():
    Base.metadata.create_all(bind=engine)


app.include_router(health.router, prefix='/api/v1')
app.include_router(auth.router, prefix='/api/v1')
app.include_router(dashboard.router, prefix='/api/v1')
app.include_router(resume.router, prefix='/api/v1')
app.include_router(ats.router, prefix='/api/v1')
app.include_router(cover_letter.router, prefix='/api/v1')
app.include_router(interview.router, prefix='/api/v1')
app.include_router(linkedin.router, prefix='/api/v1')
app.include_router(job_tracker.router, prefix='/api/v1')
app.include_router(skill_gap.router, prefix='/api/v1')
