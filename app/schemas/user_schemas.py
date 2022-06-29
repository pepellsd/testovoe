from pydantic import BaseModel


class JWTTokenScheme(BaseModel):
    access_token: str
    token_type: str


class UserScheme(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserCreateScheme(BaseModel):
    name: str
    username: str
    password: str
