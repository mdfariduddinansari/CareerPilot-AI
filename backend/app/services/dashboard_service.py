from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.entities import JobApplication


DEFAULT_CARDS = [
    {'title': 'Career Score', 'value': '78', 'subtitle': '+4 this week'},
    {'title': 'Resume Strength', 'value': '74', 'subtitle': 'Needs quantified impact'},
    {'title': 'Interview Readiness', 'value': '69', 'subtitle': '2 mock rounds pending'},
    {'title': 'Applications', 'value': '12', 'subtitle': '5 in active stages'},
    {'title': 'Responses', 'value': '4', 'subtitle': '33% response rate'},
    {'title': 'Offers', 'value': '1', 'subtitle': 'Keep momentum'},
    {'title': 'Current Streak', 'value': '9 days', 'subtitle': 'Daily career tasks completed'},
]


def get_dashboard_summary(db: Session, user_id: int) -> dict:
    grouped = (
        db.query(JobApplication.status, func.count(JobApplication.id))
        .filter(JobApplication.user_id == user_id)
        .group_by(JobApplication.status)
        .all()
    )
    chart = [{'stage': status, 'count': count} for status, count in grouped]
    if not chart:
        chart = [{'stage': 'Wishlist', 'count': 3}, {'stage': 'Applied', 'count': 2}, {'stage': 'Interview', 'count': 1}]
    return {'cards': DEFAULT_CARDS, 'applications_by_stage': chart}
