import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.entities import AIUsage, User
from app.schemas.feature import LinkedInRequest
from app.services.ai_provider import ai_provider
from app.utils.response import success_response

router = APIRouter(prefix='/linkedin', tags=['linkedin'])


@router.post('/generate')
def generate_linkedin(payload: LinkedInRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    variants = ai_provider.linkedin_variants(payload.post_type, payload.tone, payload.context)
    usage = AIUsage(user_id=current_user.id, feature='linkedin_post', provider=ai_provider.provider, meta=json.dumps({'type': payload.post_type}))
    db.add(usage)
    db.commit()
    return success_response({'variants': variants, 'provider': ai_provider.provider})
