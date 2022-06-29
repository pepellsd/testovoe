from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.services.database.dao.user_dao import UserDAO
from app.services.database.base import get_dao
from app.schemas.user_schemas import JWTTokenScheme, UserCreateScheme
from app.services.security.jwt import create_access_token


router = APIRouter(
    prefix="/api/v1/account",
    tags=["account/user"]
)


@router.post("/login", response_model=JWTTokenScheme)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_dao: UserDAO = Depends(get_dao(UserDAO))
):
    user_db = await user_dao.authenticate_user(username=form_data.username, user_password=form_data.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user_db.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users")
async def create_user(user: UserCreateScheme, user_dao: UserDAO = Depends(get_dao(UserDAO))):
    new_user = await user_dao.create_user(name=user.name, password=user.password, username=user.username)
    if new_user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "username already registered"})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "successfully created"})
