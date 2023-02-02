from pydantic import BaseModel


class RegisterRequestUser(BaseModel):
    username: str 
    password: str

    class Config:
        orm_mode = True

class LoginRequestUser(RegisterRequestUser):
    pass