import unittest

from app.utils.database import (
    clear_data,
)
from constants import HTTP_201_CREATED
from tests.database import (
    get_testing_session,
)
from constants.test.user import (
    FIRST_USER_USERID,
)
from constants.test.task import (
    FIRST_TASK,
    FIRST_TASK_TASK_NAME,
    FIRST_TASK_TASK_DESCRIPTION,
    FIRST_TASK_TASK_PLANNED_DATE,
)
from app.controllers.TaskController import TaskController
from app.controllers.UserController import UserController
from tests.utils import assertStatus, assertTaskWithDict, createFirstUserBy


class TaskControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)
        self.task_controller = TaskController(self.session)

    def tearDown(self):
        clear_data(self.session)

    def test_given_a_user_exist_when_create_a_task_with_that_user_then_return_STATUS_OK_and_that_task(self):
        createFirstUserBy(self.user_controller)

        status, task = self.task_controller.create_new_task(
            userId=FIRST_USER_USERID,
            taskName=FIRST_TASK_TASK_NAME,
            taskDescription=FIRST_TASK_TASK_DESCRIPTION,
            taskPlannedDate=FIRST_TASK_TASK_PLANNED_DATE,
        )

        assertStatus(status, HTTP_201_CREATED)
        assertTaskWithDict(task, **FIRST_TASK)
