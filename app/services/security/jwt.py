from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from app.schemas.user_schemas import UserScheme
from app.services.database.dao.user_dao import UserDAO
from app.services.database.base import get_dao
from app.config import get_settings


settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_DAYS = settings.ACCESS_TOKEN_EXPIRE_DAYS
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/account/login/")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_credentials_exc() -> HTTPException:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exc


def decode_jwt_token(token_to_decode: str) -> int:
    try:
        payload = jwt.decode(token_to_decode, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise get_credentials_exc()
        return int(user_id)
    except (JWTError, ValidationError):
        raise get_credentials_exc()


async def get_current_user_check_jwt(
        token: str = Depends(oauth_scheme),
        user_repo: UserDAO = Depends(get_dao(UserDAO))
) -> UserScheme:
    user_id = decode_jwt_token(token_to_decode=token)
    user = await user_repo.get_user(user_id=user_id)
    if user is None:
        raise get_credentials_exc()
    return user


