from constants import (
    HTTP_200_OK,
    STATUS_CODE_KEY,
    DETAIL_MESSAGE_KEY,
)

from tests.constants import (
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
)


def assertStatus(status, status_code=HTTP_200_OK, detail_message=None):
    assert status[STATUS_CODE_KEY] == status_code
    assert status[DETAIL_MESSAGE_KEY] == detail_message

def assertUserWithDict(user, **user_data_dict):
    for key, value in user_data_dict.items():
        assert getattr(user, key) == value

def createFirstUserBy(user_controller):
    return user_controller.create_new_user(username=FIRST_USER_USERNAME,
                                            password=FIRST_USER_PASSWORD)
