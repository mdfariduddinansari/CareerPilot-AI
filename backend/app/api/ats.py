import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.entities import AIUsage, ATSReport, User
from app.schemas.feature import ATSCheckRequest
from app.services.ai_provider import ai_provider
from app.utils.response import success_response

router = APIRouter(prefix='/ats', tags=['ats'])


@router.post('/check')
def ats_check(payload: ATSCheckRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = ai_provider.ats_check(payload.resume_text, payload.job_description)
    report = ATSReport(user_id=current_user.id, resume_text=payload.resume_text, job_description=payload.job_description, match_percent=result['match_percent'])
    usage = AIUsage(user_id=current_user.id, feature='ats_check', provider=result['provider'], meta=json.dumps({'match': result['match_percent']}))
    db.add_all([report, usage])
    db.commit()
    return success_response(result)
