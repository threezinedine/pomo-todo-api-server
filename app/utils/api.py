from fastapi import (
    HTTPException,
)

from app.constants import (
    STATUS_CODE_KEY,
    DETAIL_MESSAGE_KEY,
    HTTP_200_OK,
)


def handleStatus(status):
    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY],
                                detail=status[DETAIL_MESSAGE_KEY])