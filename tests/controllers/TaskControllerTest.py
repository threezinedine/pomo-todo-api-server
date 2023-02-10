import unittest

from app.utils.database import (
    clear_data,
)
from tests.database import (
    get_testing_session,
)
from app.controllers.TaskController import TaskController
from app.controllers.UserController import UserController


class TaskControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)
        self.task_controller = TaskController(self.session)

    def tearDown(self):
        clear_data(self.session)

    def test_first_test(self):
        assert True
