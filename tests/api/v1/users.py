import unittest
from fastapi.testclient import TestClient

from databases.base import get_session
from main import app
from app.constants import (
    USER_REGISTER_FULL_ROUTE,
    USERNAME_KEY,
    PASSWORD_KEY,
    USER_KEY,
    TOKEN_KEY,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    USERNAME_EXISTS_MESSAGE,
    USERNAME_DOES_NOT_EXIST_MESSAGE,
    PASSWORD_IS_INCORRECT_MESSAGE,
    USER_LOGIN_FULL_ROUTE,
)
from app.utils.database import (
    clear_database,
)
from app.controllers import (
    UserController,
)
from tests.constants import (
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
    FIRST_USER_WRONG_USERNAME,
    FIRST_USER_WRONG_PASSWORD,
    ERROR_RESPONSE_DETAIL_KEY,
)
from tests.database import get_testing_session
from tests.utils import createFirstUserBy


class UserEndToEndTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        app.dependency_overrides[get_session] = get_testing_session
        self.test_client = TestClient(app)
        self.user_controller = UserController(self.session)

    def tearDown(self):
        clear_database(self.session)
        self.session.close()

    def test_register_successfully_feature(self):
        response = self.test_client.post(
            USER_REGISTER_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_PASSWORD,
            }
        )

        assert response.status_code == HTTP_200_OK

    def test_register_with_existed_username_feature(self):
        self.user_controller.create_new_user(username=FIRST_USER_USERNAME, 
                                                password=FIRST_USER_PASSWORD)

        response = self.test_client.post(
            USER_REGISTER_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_PASSWORD,
            }
        )

        assert response.status_code == HTTP_409_CONFLICT
        assert response.json()[ERROR_RESPONSE_DETAIL_KEY] == USERNAME_EXISTS_MESSAGE

    def test_login_with_valid_username_and_password(self):
        createFirstUserBy(self.user_controller)

        response = self.test_client.post(
            USER_LOGIN_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_PASSWORD,
            }
        )

        assert response.status_code == HTTP_200_OK
        assert response.json()[USER_KEY] is not None
        assert response.json()[TOKEN_KEY] is not None

    def test_login_user_non_existed_username(self):
        createFirstUserBy(self.user_controller)

        response = self.test_client.post(
            USER_LOGIN_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_WRONG_USERNAME,
                PASSWORD_KEY: FIRST_USER_WRONG_PASSWORD,
            }
        )

        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json()[ERROR_RESPONSE_DETAIL_KEY] == USERNAME_DOES_NOT_EXIST_MESSAGE

    def test_login_user_with_existed_username_and_non_match_password(self):
        createFirstUserBy(self.user_controller)

        response = self.test_client.post(
            USER_LOGIN_FULL_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_WRONG_PASSWORD,
            }
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json()[ERROR_RESPONSE_DETAIL_KEY] == PASSWORD_IS_INCORRECT_MESSAGE
