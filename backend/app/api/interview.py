import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.entities import AIUsage, Interview, InterviewEvaluation, User
from app.schemas.feature import InterviewEvalRequest, InterviewQuestionRequest
from app.services.ai_provider import ai_provider
from app.utils.response import success_response

router = APIRouter(prefix='/interview', tags=['interview'])


@router.post('/questions')
def generate_questions(payload: InterviewQuestionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    questions = ai_provider.interview_questions(payload.company, payload.round_type)
    record = Interview(user_id=current_user.id, company=payload.company, round_type=payload.round_type, questions=json.dumps(questions))
    usage = AIUsage(user_id=current_user.id, feature='interview_questions', provider=ai_provider.provider, meta=json.dumps({'round_type': payload.round_type}))
    db.add_all([record, usage])
    db.commit()
    return success_response({'questions': questions, 'provider': ai_provider.provider})


@router.post('/evaluate')
def evaluate_answer(payload: InterviewEvalRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    evaluation = ai_provider.evaluate_answer(payload.answer)
    record = InterviewEvaluation(user_id=current_user.id, question=payload.question, answer=payload.answer, overall_score=evaluation['overall'])
    usage = AIUsage(user_id=current_user.id, feature='interview_evaluation', provider=ai_provider.provider, meta=json.dumps(evaluation))
    db.add_all([record, usage])
    db.commit()
    return success_response(evaluation)
