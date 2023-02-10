from fastapi import (
    HTTPException,
)

from constants import (
    HTTP_201_CREATED,
    STATUS_CODE_KEY,
    DETAIL_MESSAGE_KEY,
    HTTP_200_OK,
)


def handleStatus(status):
    if status[STATUS_CODE_KEY] != HTTP_200_OK and status[STATUS_CODE_KEY] != HTTP_201_CREATED:
        raise HTTPException(status_code=status[STATUS_CODE_KEY],
                            detail=status[DETAIL_MESSAGE_KEY])
