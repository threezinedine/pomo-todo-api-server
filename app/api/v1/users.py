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
)
from app.schemas import (
    RegisterRequestUser,
)
from app.controllers import (
    UserController,
)
from databases.base import get_session


router = APIRouter(prefix=USER_BASE_ROUTE)


@router.post(USER_REGISTER_ROUTE, 
        status_code=HTTP_200_OK)
def register_new_user(register_request_infor: RegisterRequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)

    status, user = user_controller.create_new_user(username=register_request_infor.username, password=register_request_infor.password)

    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY],
                                detail=status[DETAIL_MESSAGE_KEY])

    return user
