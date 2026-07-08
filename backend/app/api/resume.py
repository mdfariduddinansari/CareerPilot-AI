import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.entities import AIUsage, Resume, User
from app.schemas.feature import ResumeAnalyzeRequest
from app.services.ai_provider import ai_provider
from app.utils.response import success_response

router = APIRouter(prefix='/resume', tags=['resume'])


@router.post('/analyze')
def analyze_resume(payload: ResumeAnalyzeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = ai_provider.analyze_resume(payload.resume_text)
    record = Resume(user_id=current_user.id, resume_text=payload.resume_text, overall_score=result['overall_score'], ats_score=result['ats_score'])
    usage = AIUsage(user_id=current_user.id, feature='resume_analysis', provider=result['provider'], meta=json.dumps({'score': result['overall_score']}))
    db.add_all([record, usage])
    db.commit()
    return success_response(result)
