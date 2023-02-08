import os
from fastapi import (
    APIRouter,
    Depends,
    Body,
    File,
    UploadFile,
    Response,
)
from sqlalchemy.orm import Session

from constants import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    READ_BINARY_MODE,
    WRITE_BINARY_MODE,
)
from constants.database.user import (
    USER_KEY,
    USERNAME_KEY,
    USERID_KEY,
    TOKEN_KEY,
    USER_DESCRIPTION_KEY,
)
from constants.routes import (
    USER_BASE_ROUTE,
    USER_GET_IMAGE_ROUTE,
    USER_REGISTER_ROUTE,
    USER_LOGIN_ROUTE,
    USER_CHANGE_DESCRIPTION_ROUTE,
    USER_UPLOAD_IMAGE_ROUTE,
)
from app.schemas import (
    RegisterRequestUser,
    LoginRequestUser,
    LoginResultUser,
    ResponseUser,
)
from app.controllers import (
    UserController,
)
from app.utils.api import (
    handleStatus,
)
from app.utils.database import (
    create_the_saved_image_path,
)
from app.utils.auth import (
    generate_token,
    get_token,
)
from databases.base import get_session


router = APIRouter(prefix=USER_BASE_ROUTE)


@router.post(
    USER_REGISTER_ROUTE,
    status_code=HTTP_201_CREATED
)
def register_new_user(register_request_infor: RegisterRequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)

    status, _ = user_controller.create_new_user(
        username=register_request_infor.username, password=register_request_infor.password)

    handleStatus(status)

    return None


@router.post(
    USER_LOGIN_ROUTE,
    status_code=HTTP_200_OK,
    response_model=LoginResultUser,
)
def login(user: LoginRequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)

    status, user = user_controller.get_user_by_username_and_password(
        user.username, user.password)

    handleStatus(status)

    return {
        USER_KEY: user,
        TOKEN_KEY: generate_token({
            USERID_KEY: user.userId,
            USERNAME_KEY: user.username,
        }, user.password)
    }


@router.post(
    USER_CHANGE_DESCRIPTION_ROUTE,
    status_code=HTTP_200_OK,
    response_model=ResponseUser,
)
def change_description(description: dict = Body(),
                       session=Depends(get_session),
                       data: dict = Depends(get_token)):
    user_controller = UserController(session)

    _, response = user_controller.change_description_by_username(username=data[USERNAME_KEY],
                                                                 description=description[USER_DESCRIPTION_KEY])

    return response


@router.post(
    USER_UPLOAD_IMAGE_ROUTE,
    status_code=HTTP_200_OK,
    response_model=ResponseUser,
)
async def upload_image(userImage: UploadFile = File(),
                       session: Session = Depends(get_session),
                       userInfo: dict = Depends(get_token)):
    user_controller = UserController(session=session)

    file_full_path = create_the_saved_image_path(userInfo[USERNAME_KEY])
    _, response = user_controller.change_user_image_path_by_username(
        username=userInfo[USERNAME_KEY],
        imagePath=file_full_path)

    with open(file_full_path, WRITE_BINARY_MODE) as f:
        f.write(await userImage.read())

    return response


@router.get(
    USER_GET_IMAGE_ROUTE,
    status_code=HTTP_200_OK,
)
async def get_image(session: Session = Depends(get_session),
                    userInfo: dict = Depends(get_token)):
    user_controller = UserController(session=session)

    status, imagePath = user_controller.get_user_image_path_by_username(
        username=userInfo[USERNAME_KEY])

    handleStatus(status)

    with open(imagePath, READ_BINARY_MODE) as f:
        content = f.read()

    return Response(content=content, media_type="image/png")
