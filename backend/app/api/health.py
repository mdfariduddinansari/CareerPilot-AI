from fastapi import APIRouter

from app.utils.response import success_response

router = APIRouter(prefix='/health', tags=['health'])


@router.get('')
def health_check():
    return success_response({'status': 'healthy'}, 'Service is healthy')
