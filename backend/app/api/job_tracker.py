from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.entities import JobApplication, User
from app.schemas.feature import JobCreateRequest, JobUpdateRequest
from app.utils.response import success_response

router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.get('')
def list_jobs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    jobs = db.query(JobApplication).filter(JobApplication.user_id == current_user.id).all()
    data = [{'id': job.id, 'company': job.company, 'role': job.role, 'status': job.status} for job in jobs]
    return success_response(data)


@router.post('')
def create_job(payload: JobCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = JobApplication(user_id=current_user.id, company=payload.company, role=payload.role, status=payload.status)
    db.add(job)
    db.commit()
    db.refresh(job)
    return success_response({'id': job.id, 'company': job.company, 'role': job.role, 'status': job.status}, 'Job created')


@router.patch('/{job_id}')
def update_job(job_id: int, payload: JobUpdateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(JobApplication).filter(JobApplication.id == job_id, JobApplication.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    job.status = payload.status
    db.commit()
    return success_response({'id': job.id, 'status': job.status}, 'Job updated')
