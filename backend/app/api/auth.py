from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token, get_password_hash, verify_password
from app.database.session import get_db
from app.models.entities import User
from app.schemas.auth import LoginRequest, SignupRequest
from app.utils.response import success_response

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/signup')
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(name=payload.name, email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user)
    db.commit()
    return success_response({'id': user.id, 'email': user.email}, 'Signup successful')


@router.post('/login')
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token(user.email)
    return success_response({'access_token': token, 'token_type': 'bearer', 'user': {'id': user.id, 'name': user.name, 'email': user.email}}, 'Login successful')


@router.get('/me')
def me(current_user: User = Depends(get_current_user)):
    return success_response({'id': current_user.id, 'name': current_user.name, 'email': current_user.email})
