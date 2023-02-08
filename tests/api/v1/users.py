import unittest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from databases.base import get_session
from main import app
from app.utils.database import (
    clear_data,
)
from app.controllers import (
    UserController,
)
from constants import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    ERROR_RESPONSE_DETAIL_KEY,
    READ_BINARY_MODE,
    IMAGE_PNG_CONTENT_TYPE,
)
from constants.routes import (
    USER_REGISTER_FULL_ROUTE,
    USER_LOGIN_FULL_ROUTE,
    USER_CHANGE_DESCRIPION_FULL_ROUTE,
    USER_UPLOAD_IMAGE_FULL_ROUTE,
    USER_GET_IMAGE_FULL_ROUTE,
)
from constants.database.user import (
    USERNAME_KEY,
    PASSWORD_KEY,
    USER_KEY,
    TOKEN_KEY,
    USER_DESCRIPTION_KEY,
    USERID_KEY,
    USER_IMAGE_KEY,
)
from constants.database import (
    AUTHORIZATION_KEY,
)
from constants.message import (
    USERNAME_EXISTS_MESSAGE,
    USERNAME_DOES_NOT_EXIST_MESSAGE,
    PASSWORD_IS_INCORRECT_MESSAGE,
    TOKEN_IS_NOT_VALID_MESSAGE,
    USERID_DOES_NOT_EXIST_MESSAGE,
)
from constants.test.user import (
    FIRST_USER_USERID,
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
    FIRST_USER_WRONG_USERNAME,
    FIRST_USER_WRONG_PASSWORD,
    FIRST_USER_NEW_USER_DESCRIPTION,
    FIRST_USER_WRONG_TOKEN,
    FIRST_USER_WRONG_USERID,
    FIRST_USER_TEST_IMAGE_PATH,
    FIRST_USER_TEST_IMAGE_NAME,
    FIRST_USER_DICT_WITH_DESCRIPTION,
    FIRST_USER_DICT_WITHOUT_DESCRIPTION,
)
from tests.database import get_testing_session
from tests.utils import (
    createFirstUserBy,
    assertDictSubset,
    getFirstUserTokenBy,
)
from tests import test_client


class UserEndToEndTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        app.dependency_overrides[get_session] = get_testing_session
        self.user_controller = UserController(self.session)

    def tearDown(self):
        clear_data(self.session)
        self.session.close()

    def test_register_successfully_feature(self):
        response = test_client.post(
            USER_REGISTER_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_PASSWORD,
            }
        )

        assert response.status_code == HTTP_201_CREATED
        assert response.json() is None

    def test_register_with_existed_username_feature(self):
        self.user_controller.create_new_user(username=FIRST_USER_USERNAME,
                                             password=FIRST_USER_PASSWORD)

        response = test_client.post(
            USER_REGISTER_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_PASSWORD,
            }
        )

        assert response.status_code == HTTP_409_CONFLICT
        assert response.json()[
            ERROR_RESPONSE_DETAIL_KEY] == USERNAME_EXISTS_MESSAGE

    def test_login_with_valid_username_and_password(self):
        createFirstUserBy(self.user_controller)

        response = test_client.post(
            USER_LOGIN_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_PASSWORD,
            }
        )

        assert response.status_code == HTTP_200_OK
        assertDictSubset(
            response.json()[USER_KEY], FIRST_USER_DICT_WITHOUT_DESCRIPTION)
        assert response.json()[TOKEN_KEY] is not None

    def test_login_user_non_existed_username(self):
        createFirstUserBy(self.user_controller)

        response = test_client.post(
            USER_LOGIN_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_WRONG_USERNAME,
                PASSWORD_KEY: FIRST_USER_WRONG_PASSWORD,
            }
        )

        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json()[
            ERROR_RESPONSE_DETAIL_KEY] == USERNAME_DOES_NOT_EXIST_MESSAGE

    def test_login_user_with_existed_username_and_non_match_password(self):
        createFirstUserBy(self.user_controller)

        response = test_client.post(
            USER_LOGIN_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_WRONG_PASSWORD,
            }
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json()[
            ERROR_RESPONSE_DETAIL_KEY] == PASSWORD_IS_INCORRECT_MESSAGE

    def test_the_update_user_description_successfully(self):
        createFirstUserBy(self.user_controller)
        token = getFirstUserTokenBy()

        response = test_client.post(
            USER_CHANGE_DESCRIPION_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            json={
                USER_DESCRIPTION_KEY: FIRST_USER_NEW_USER_DESCRIPTION,
            }
        )

        assert response.status_code == HTTP_200_OK

        assertDictSubset(response.json(), FIRST_USER_DICT_WITH_DESCRIPTION)

    def test_change_user_description_with_invalid_token(self):
        createFirstUserBy(self.user_controller)

        response = test_client.post(
            USER_CHANGE_DESCRIPION_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: FIRST_USER_WRONG_TOKEN,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            json={
                USER_DESCRIPTION_KEY: FIRST_USER_NEW_USER_DESCRIPTION,
            }
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json()[
            ERROR_RESPONSE_DETAIL_KEY] == TOKEN_IS_NOT_VALID_MESSAGE

    def test_change_user_description_with_not_match_userId(self):
        createFirstUserBy(self.user_controller)
        token = getFirstUserTokenBy()

        response = test_client.post(
            USER_CHANGE_DESCRIPION_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_WRONG_USERID),
            },
            json={
                USER_DESCRIPTION_KEY: FIRST_USER_NEW_USER_DESCRIPTION,
            }
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json()[
            ERROR_RESPONSE_DETAIL_KEY] == USERID_DOES_NOT_EXIST_MESSAGE

    def test_user_uploading_the_user_image_succesfully(self):
        createFirstUserBy(self.user_controller)
        token = getFirstUserTokenBy()

        with open(FIRST_USER_TEST_IMAGE_PATH, READ_BINARY_MODE) as file:
            file_data = file.read()

        userImage = (FIRST_USER_TEST_IMAGE_NAME,
                     file_data, IMAGE_PNG_CONTENT_TYPE)

        response = test_client.post(
            USER_UPLOAD_IMAGE_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            files={
                USER_IMAGE_KEY: userImage,
            }
        )

        assert response.status_code == HTTP_200_OK
        assertDictSubset(response.json(), FIRST_USER_DICT_WITHOUT_DESCRIPTION)

    def test_get_user_image_with_existed_one_feature(self):
        createFirstUserBy(self.user_controller)
        token = getFirstUserTokenBy()

        with open(FIRST_USER_TEST_IMAGE_PATH, READ_BINARY_MODE) as file:
            file_data = file.read()

        userImage = (FIRST_USER_TEST_IMAGE_NAME,
                     file_data, IMAGE_PNG_CONTENT_TYPE)
        response = test_client.post(
            USER_UPLOAD_IMAGE_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            files={
                USER_IMAGE_KEY: userImage,
            }
        )

        response = test_client.get(
            USER_GET_IMAGE_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
        )

        assert response.status_code == HTTP_200_OK
        assert response.content is not None
