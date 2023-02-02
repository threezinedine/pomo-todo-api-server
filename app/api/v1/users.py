from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.constants import (
    STATUS_CODE_KEY,
    DETAIL_MESSAGE_KEY,
    HTTP_200_OK,
    USER_BASE_ROUTE,
    USER_REGISTER_ROUTE,
    USER_LOGIN_ROUTE,
    USER_KEY,
    TOKEN_KEY,
)
from app.schemas import (
    RegisterRequestUser,
    LoginRequestUser,
    LoginResultUser,
)
from app.controllers import (
    UserController,
)
from app.utils.api import (
    handleStatus,
)
from databases.base import get_session


router = APIRouter(prefix=USER_BASE_ROUTE)


@router.post(
    USER_REGISTER_ROUTE, 
    status_code=HTTP_200_OK
)
def register_new_user(register_request_infor: RegisterRequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)

    status, user = user_controller.create_new_user(username=register_request_infor.username, password=register_request_infor.password)

    handleStatus(status)

    return user

@router.post(
    USER_LOGIN_ROUTE,
    status_code=HTTP_200_OK,
    response_model=LoginResultUser,
)
def login(user: LoginRequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session) 

    status, user = user_controller.get_user_by_username_and_password(user.username, user.password)

    handleStatus(status)

    return {
        USER_KEY: user,
        TOKEN_KEY: "testing_token",
    }