from app.constants import (
    HTTP_200_OK,
    STATUS_CODE_KEY,
    DETAIL_MESSAGE_KEY,
)


def assertStatus(status, status_code=HTTP_200_OK, detail_message=None):
    assert status[STATUS_CODE_KEY] == status_code
    assert status[DETAIL_MESSAGE_KEY] == detail_message
