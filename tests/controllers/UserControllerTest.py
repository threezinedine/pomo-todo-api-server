import unittest

from databases.base import (
    Base,
    get_session,
)
from app.controllers import UserController
from app.constants import (
    HTTP_200_OK,
)
from tests.utils import (
    assertStatus, 
    assertUserWithDict,
)
from tests.constants import (
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
)


class UserControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_session())
        self.user_controller = UserController(self.session) 

    def tearDown(self):
        self.session.close()

    def test_given_no_users_exist_when_get_all_users_then_returns_empty_array(self):
        status, response = self.user_controller.get_all_users()

        assertStatus(status, HTTP_200_OK)
        self.assertListEqual(response, [])

    def test_given_no_users_exist_when_create_new_users_then_returns_HTTP_200_OK_and_that_new_user(self):
        status, response = self.user_controller.create_new_user(username=FIRST_USER_USERNAME, 
                                                                    password=FIRST_USER_PASSWORD)

        assertStatus(status, HTTP_200_OK)
        assertUserWithDict(response,
                            username=FIRST_USER_USERNAME,
                            password=FIRST_USER_PASSWORD)
