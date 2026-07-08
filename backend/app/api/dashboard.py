from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.entities import User
from app.services.dashboard_service import get_dashboard_summary
from app.utils.response import success_response

router = APIRouter(prefix='/dashboard', tags=['dashboard'])


@router.get('/summary')
def dashboard_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return success_response(get_dashboard_summary(db, current_user.id))
