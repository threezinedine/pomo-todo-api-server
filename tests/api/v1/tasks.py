import unittest

from tests import (
    test_client,
)
from tests.database import (
    get_testing_session
)
from app.utils.database import (
    clear_data,
)

from app.controllers.UserController import UserController


class TaskEndToEndTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        clear_data(self.session)

    def test_first_test(self):
        assert True
