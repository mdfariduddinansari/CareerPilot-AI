import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.entities import AIUsage, Roadmap, Skill, User
from app.schemas.feature import SkillGapRequest
from app.services.ai_provider import ai_provider
from app.utils.response import success_response

router = APIRouter(prefix='/skills', tags=['skills'])


@router.post('/analyze')
def analyze_skill_gap(payload: SkillGapRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = ai_provider.skill_gap(payload.target_role, payload.current_skills)
    skill_record = Skill(user_id=current_user.id, target_role=payload.target_role, current_skills=json.dumps(payload.current_skills), analysis=json.dumps(result))
    roadmap_record = Roadmap(user_id=current_user.id, target_role=payload.target_role, roadmap=json.dumps(result['roadmap']))
    usage = AIUsage(user_id=current_user.id, feature='skill_gap', provider=ai_provider.provider, meta=json.dumps({'target_role': payload.target_role}))
    db.add_all([skill_record, roadmap_record, usage])
    db.commit()
    return success_response(result)
