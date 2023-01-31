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
