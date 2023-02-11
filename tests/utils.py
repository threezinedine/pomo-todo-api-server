from constants import (
    HTTP_200_OK,
    STATUS_CODE_KEY,
    DETAIL_MESSAGE_KEY,
)
from constants.test.user import (
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
)
from constants.database.user import (
    USERNAME_KEY,
    PASSWORD_KEY,
    TOKEN_KEY,
)
from constants.routes import (
    USER_LOGIN_FULL_ROUTE,
)
from app.controllers.UserController import UserController
from tests import test_client


def assertDictSubset(dictionary: dict, subsetDictionary: dict):
    for key, value in subsetDictionary.items():
        assert dictionary[key] == value


def assertStatus(status, status_code=HTTP_200_OK, detail_message=None):
    assert status[STATUS_CODE_KEY] == status_code
    assert status[DETAIL_MESSAGE_KEY] == detail_message


def assertUserWithDict(user, **user_data_dict):
    for key, value in user_data_dict.items():
        print(key, value, getattr(user, key))
        assert getattr(user, key) == value


def assertTaskWithDict(task, **task_data_dict):
    for key, value in task_data_dict.items():
        if not isinstance(task, dict):
            print(getattr(task, key), value, type(getattr(task, key)), type(value))
            assert str(getattr(task, key)) == str(value)
        else:
            print(task[key], value, type(task[key]), type(value))
            assert str(task[key]) == str(value)


def createFirstUserBy(user_controller: UserController):
    return user_controller.create_new_user(username=FIRST_USER_USERNAME,
                                           password=FIRST_USER_PASSWORD)


def getFirstUserTokenBy():
    response = test_client.post(
        USER_LOGIN_FULL_ROUTE,
        json={
            USERNAME_KEY: FIRST_USER_USERNAME,
            PASSWORD_KEY: FIRST_USER_PASSWORD,
        }
    )

    return response.json()[TOKEN_KEY]
