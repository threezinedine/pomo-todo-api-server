import unittest
from datetime import date, datetime

from app.utils.database import (
    clear_data,
)
from constants import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from constants.database.task import TASK_COMPLETED_TIME_KEY, TASK_ID_KEY
from constants.message import TASK_NOT_FOUND_MESSAGE
from constants.status import TASK_NOT_FOUND_STATUS
from tests.database import (
    get_testing_session,
)
from constants.test.user import (
    FIRST_USER_USERID,
    FIRST_USER_WRONG_USERID,
)
from constants.test.task import (
    FIRST_TASK,
    FIRST_TASK_COMPLETE,
    FIRST_TASK_TASK_NAME,
    FIRST_TASK_TASK_DESCRIPTION,
    FIRST_TASK_TASK_PLANNED_DATE,
)
from app.controllers.TaskController import TaskController
from app.controllers.UserController import UserController
from tests.utils import (
    assertStatus,
    assertTaskWithDict,
    createFirstUserBy
)


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
            plannedDate=date.fromisoformat(FIRST_TASK_TASK_PLANNED_DATE),
        )

        assertStatus(status, HTTP_201_CREATED)
        assertTaskWithDict(task, **FIRST_TASK)

    def test_given_a_task_exists_when_get_all_task_then_return_STATUS_OK_and_the_list_contains_that_task(self):
        createFirstUserBy(self.user_controller)
        self.task_controller.create_new_task(
            userId=FIRST_USER_USERID,
            taskName=FIRST_TASK_TASK_NAME,
            taskDescription=FIRST_TASK_TASK_DESCRIPTION,
            plannedDate=date.fromisoformat(FIRST_TASK_TASK_PLANNED_DATE),
        )

        status, tasks = self.task_controller.get_all_tasks()

        assertStatus(status, HTTP_200_OK)
        assertTaskWithDict(tasks[0], **FIRST_TASK)

    def test_given_an_user_and_a_task_are_created_when_complete_that_task_then_return_OK_STATUS_and_that_task(self):
        createFirstUserBy(self.user_controller)
        self.task_controller.create_new_task(
            userId=FIRST_USER_USERID,
            taskName=FIRST_TASK_TASK_NAME,
            taskDescription=FIRST_TASK_TASK_DESCRIPTION,
            plannedDate=date.fromisoformat(FIRST_TASK_TASK_PLANNED_DATE),
        )

        status, task = self.task_controller.complete_task_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            completedTime=datetime.fromisoformat(
                FIRST_TASK_COMPLETE['completedTime']),
        )

        assertStatus(status, HTTP_200_OK)
        assertTaskWithDict(task, **FIRST_TASK_COMPLETE)

    def test_given_when_complete_a_task_with_non_existed_task_id_then_return_TASK_NOT_FOUND_and_none(self):
        status, task = self.task_controller.complete_task_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            completedTime=datetime.fromisoformat(
                FIRST_TASK_COMPLETE[TASK_COMPLETED_TIME_KEY]),
        )

        assertStatus(status, HTTP_404_NOT_FOUND, TASK_NOT_FOUND_MESSAGE)
        assert task is None

    def test_given_when_complete_a_task_with_wrong_user_id_then_return_NO_PERMISSION_STATUS_and_none(self):
        createFirstUserBy(self.user_controller)
        self.task_controller.create_new_task(
            userId=FIRST_USER_USERID,
            taskName=FIRST_TASK_TASK_NAME,
            taskDescription=FIRST_TASK_TASK_DESCRIPTION,
            plannedDate=date.fromisoformat(FIRST_TASK_TASK_PLANNED_DATE),
        )

        status, task = self.task_controller.complete_task_by_task_id_and_user_id(
            userId=FIRST_USER_WRONG_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            completedTime=datetime.fromisoformat(
                FIRST_TASK_COMPLETE[TASK_COMPLETED_TIME_KEY]),
        )

        assertStatus(status, HTTP_404_NOT_FOUND, TASK_NOT_FOUND_MESSAGE)
        assert task is None