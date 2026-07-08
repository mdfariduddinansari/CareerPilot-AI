from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.security import ALGORITHM
from app.config import settings
from app.database.session import get_db
from app.models.entities import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login', auto_error=False)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    x_auth_token: str | None = Header(default=None, alias='X-Auth-Token'),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    raw_token = token or x_auth_token
    if not raw_token:
        raise credentials_exception

    try:
        payload = jwt.decode(raw_token, settings.secret_key, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return user
