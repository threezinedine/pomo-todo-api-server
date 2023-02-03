from constants import (
    STATUS_CODE_KEY,
    DETAIL_MESSAGE_KEY,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from constants.message import (
    USERNAME_EXISTS_MESSAGE,
    USERNAME_DOES_NOT_EXIST_MESSAGE,
    PASSWORD_IS_INCORRECT_MESSAGE,
)

OK_STATUS = {
    STATUS_CODE_KEY: HTTP_200_OK,
    DETAIL_MESSAGE_KEY: None
}

USERNAME_EXIST_STATUS = {
    STATUS_CODE_KEY: HTTP_409_CONFLICT,
    DETAIL_MESSAGE_KEY: USERNAME_EXISTS_MESSAGE,
}

USERNAME_DOES_NOT_EXIST_STATUS = {
    STATUS_CODE_KEY: HTTP_404_NOT_FOUND,
    DETAIL_MESSAGE_KEY: USERNAME_DOES_NOT_EXIST_MESSAGE,
}

PASSWORD_IS_INCORRECT_STATUS = {
    STATUS_CODE_KEY: HTTP_401_UNAUTHORIZED,
    DETAIL_MESSAGE_KEY: PASSWORD_IS_INCORRECT_MESSAGE,
}
