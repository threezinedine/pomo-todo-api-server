from pydantic import BaseModel
from typing import (
    Union,
)


class RegisterRequestUser(BaseModel):
    username: str 
    password: str

    class Config:
        orm_mode = True

class LoginRequestUser(RegisterRequestUser):
    pass

class ResponseUser(BaseModel):
    username: str
    description: Union[str, None]

    class Config:
        orm_mode = True

class LoginResultUser(BaseModel):
    user: ResponseUser
    token: str

    class Config:
        orm_mode = True