import unittest
from fastapi.testclient import TestClient

from databases.base import get_session
from main import app
from app.constants import (
    USER_REGISTER_ROUTE,
    USERNAME_KEY,
    PASSWORD_KEY,
    HTTP_200_OK,
)
from app.controllers import (
    UserController,
)
from tests.constants import (
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
)


class UserEndToEndTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_session())
        self.test_client = TestClient(app)
        user_controller = UserController(self.session)

    def tearDown(self):
        self.session.close()

    def test_register_successfully_feature(self):
        response = self.test_client.post(
            USER_REGISTER_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_PASSWORD,
            }
        )

        print(response.status_code)
        assert response.status_code == HTTP_200_OK
