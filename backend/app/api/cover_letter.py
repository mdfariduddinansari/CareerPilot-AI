import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.entities import AIUsage, CoverLetter, User
from app.schemas.feature import CoverLetterRequest
from app.services.ai_provider import ai_provider
from app.utils.response import success_response

router = APIRouter(prefix='/cover-letter', tags=['cover-letter'])


@router.post('/generate')
def generate_cover_letter(payload: CoverLetterRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    letter = ai_provider.generate_cover_letter(payload.company, payload.role, payload.tone, payload.resume_text)
    record = CoverLetter(user_id=current_user.id, company=payload.company, role=payload.role, tone=payload.tone, content=letter)
    usage = AIUsage(user_id=current_user.id, feature='cover_letter', provider=ai_provider.provider, meta=json.dumps({'tone': payload.tone}))
    db.add_all([record, usage])
    db.commit()
    return success_response({'letter': letter, 'provider': ai_provider.provider})
