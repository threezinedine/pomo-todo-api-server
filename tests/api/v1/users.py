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
from app.utils.database import (
    clear_database,
)
from app.controllers import (
    UserController,
)
from tests.constants import (
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
)
from tests.database import get_testing_session


class UserEndToEndTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        app.dependency_overrides[get_session] = get_testing_session
        self.test_client = TestClient(app)
        user_controller = UserController(self.session)

    def tearDown(self):
        clear_database(self.session)
        self.session.close()

    def test_register_successfully_feature(self):
        response = self.test_client.post(
            USER_REGISTER_ROUTE,
            json={
                USERNAME_KEY: FIRST_USER_USERNAME,
                PASSWORD_KEY: FIRST_USER_PASSWORD,
            }
        )

        assert response.status_code == HTTP_200_OK
