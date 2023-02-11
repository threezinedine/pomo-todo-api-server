import unittest
from datetime import date, datetime

from app.utils.database import (
    clear_data,
)
from constants import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from constants.database.task import TASK_COMPLETED_TIME_KEY, TASK_ID_KEY
from constants.message import NO_PERMISSION_MESSAGE, TASK_NOT_FOUND_MESSAGE
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
    FIRST_TASK_CHANGE_TASK_DESCRIPTION,
    FIRST_TASK_CHANGE_TASK_DESCRIPTION_TASK,
    FIRST_TASK_CHANGE_TASK_NAME,
    FIRST_TASK_CHANGE_TASK_PLANNED_DATE,
    FIRST_TASK_CHANGE_TASK_PLANNED_DATE_TASK,
    FIRST_TASK_CHANGED_TASK_NAME_TASK,
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
    createFirstTaskForFirstUserBy,
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
        createFirstTaskForFirstUserBy(self.task_controller)

        status, tasks = self.task_controller.get_all_tasks()

        assertStatus(status, HTTP_200_OK)
        assertTaskWithDict(tasks[0], **FIRST_TASK)

    def test_given_an_user_and_a_task_are_created_when_complete_that_task_then_return_OK_STATUS_and_that_task(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

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
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.complete_task_by_task_id_and_user_id(
            userId=FIRST_USER_WRONG_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            completedTime=datetime.fromisoformat(
                FIRST_TASK_COMPLETE[TASK_COMPLETED_TIME_KEY]),
        )

        assertStatus(status, HTTP_403_FORBIDDEN, NO_PERMISSION_MESSAGE)
        assert task is None

    # create three cases for get_task_a_task_by_task_id_and_user_id
    def test_given_a_task_exists_when_get_that_task_then_return_STATUS_OK_and_that_task(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.get_task_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
        )

        assertStatus(status, HTTP_200_OK)
        assertTaskWithDict(task, **FIRST_TASK)

    def test_given_when_get_a_task_with_non_existed_task_id_then_return_TASK_NOT_FOUND_and_none(self):
        status, task = self.task_controller.get_task_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
        )

        assertStatus(status, HTTP_404_NOT_FOUND, TASK_NOT_FOUND_MESSAGE)
        assert task is None

    def test_given_when_get_a_task_with_wrong_user_id_then_return_NO_PERMISSION_STATUS_and_none(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.get_task_by_task_id_and_user_id(
            userId=FIRST_USER_WRONG_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
        )

        assertStatus(status, HTTP_403_FORBIDDEN, NO_PERMISSION_MESSAGE)
        assert task is None

    # test for getting all tasks of a user
    def test_given_a_user_and_a_task_are_created_when_get_all_tasks_of_that_user_then_return_STATUS_OK_and_the_list_contains_that_task(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, tasks = self.task_controller.get_all_tasks_of_user(
            userId=FIRST_USER_USERID,
        )

        assertStatus(status, HTTP_200_OK)
        assertTaskWithDict(tasks[0], **FIRST_TASK)

    # test for changing the task name with the task id and user id
    def test_given_a_task_exists_when_change_the_task_name_then_return_STATUS_OK_and_that_task(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.change_task_name_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskName=FIRST_TASK_CHANGE_TASK_NAME,
        )

        assertStatus(status, HTTP_200_OK)
        assertTaskWithDict(task, **FIRST_TASK_CHANGED_TASK_NAME_TASK)

    # test for changing the task name with non existed task id
    def test_given_when_change_the_task_name_with_non_existed_task_id_then_return_TASK_NOT_FOUND_and_none(self):
        status, task = self.task_controller.change_task_name_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskName=FIRST_TASK_CHANGE_TASK_NAME,
        )

        assertStatus(status, HTTP_404_NOT_FOUND, TASK_NOT_FOUND_MESSAGE)
        assert task is None

    # test for changing the task name with wrong user id (no permission)
    def test_given_when_change_the_task_name_with_wrong_user_id_then_return_NO_PERMISSION_STATUS_and_none(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.change_task_name_by_task_id_and_user_id(
            userId=FIRST_USER_WRONG_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskName=FIRST_TASK_CHANGE_TASK_NAME,
        )

        assertStatus(status, HTTP_403_FORBIDDEN, NO_PERMISSION_MESSAGE)
        assert task is None

    # test for changing the task description with the task id
    def test_given_a_task_exists_when_change_the_task_description_then_return_STATUS_OK_and_that_task(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.change_task_description_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskDescription=FIRST_TASK_CHANGE_TASK_DESCRIPTION,
        )

        assertStatus(status, HTTP_200_OK)
        assertTaskWithDict(task, **FIRST_TASK_CHANGE_TASK_DESCRIPTION_TASK)

    # test for changing the task description with non existed task id
    def test_given_when_change_the_task_description_with_non_existed_task_id_then_return_TASK_NOT_FOUND_and_none(self):
        status, task = self.task_controller.change_task_description_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskDescription=FIRST_TASK_CHANGE_TASK_DESCRIPTION,
        )

        assertStatus(status, HTTP_404_NOT_FOUND, TASK_NOT_FOUND_MESSAGE)
        assert task is None

    # test for changing the task description with wrong user id (no permission)
    def test_given_when_change_the_task_description_with_wrong_user_id_then_return_NO_PERMISSION_STATUS_and_none(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.change_task_description_by_task_id_and_user_id(
            userId=FIRST_USER_WRONG_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskDescription=FIRST_TASK_CHANGE_TASK_DESCRIPTION,
        )

        assertStatus(status, HTTP_403_FORBIDDEN, NO_PERMISSION_MESSAGE)
        assert task is None

    # add test for deleting a task by task id
    def test_given_a_task_exists_when_delete_the_task_then_return_STATUS_OK_and_none(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.delete_task_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
        )

        assertStatus(status, HTTP_200_OK)
        assert task is None

    # test for deleting a task with non existed task id -> return TASK_NOT_FOUND, None
    def test_given_when_delete_the_task_with_non_existed_task_id_then_return_TASK_NOT_FOUND_and_none(self):
        status, task = self.task_controller.delete_task_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
        )

        assertStatus(status, HTTP_404_NOT_FOUND, TASK_NOT_FOUND_MESSAGE)
        assert task is None

    # test for deleting a task with wrong user id (no permission)
    def test_given_when_delete_the_task_with_wrong_user_id_then_return_NO_PERMISSION_STATUS_and_none(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.delete_task_by_task_id_and_user_id(
            userId=FIRST_USER_WRONG_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
        )

        assertStatus(status, HTTP_403_FORBIDDEN, NO_PERMISSION_MESSAGE)
        assert task is None

    # test for deleting all tasks by user id
    def test_given_a_task_exists_when_delete_all_tasks_then_return_STATUS_OK_and_none(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.delete_all_tasks_by_user_id(
            userId=FIRST_USER_USERID,
        )

        assertStatus(status, HTTP_200_OK)
        assert task is None

    # test for changing task planned date with the task id and user id
    def test_given_a_task_exists_when_change_the_task_planned_date_then_return_STATUS_OK_and_that_task(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.change_task_planned_date_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskPlannedDate=FIRST_TASK_CHANGE_TASK_PLANNED_DATE,
        )

        assertStatus(status, HTTP_200_OK)
        assertTaskWithDict(task, **FIRST_TASK_CHANGE_TASK_PLANNED_DATE_TASK)

    # test for changing task planned date with non existed task id
    def test_given_when_change_the_task_planned_date_with_non_existed_task_id_then_return_TASK_NOT_FOUND_and_none(self):
        status, task = self.task_controller.change_task_planned_date_by_task_id_and_user_id(
            userId=FIRST_USER_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskPlannedDate=FIRST_TASK_CHANGE_TASK_PLANNED_DATE,
        )

        assertStatus(status, HTTP_404_NOT_FOUND, TASK_NOT_FOUND_MESSAGE)
        assert task is None

    # test for changing task planned date with wrong user id (no permission)
    def test_given_when_change_the_task_planned_date_with_wrong_user_id_then_return_NO_PERMISSION_STATUS_and_none(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)

        status, task = self.task_controller.change_task_planned_date_by_task_id_and_user_id(
            userId=FIRST_USER_WRONG_USERID,
            taskId=FIRST_TASK[TASK_ID_KEY],
            newTaskPlannedDate=FIRST_TASK_CHANGE_TASK_PLANNED_DATE,
        )

        assertStatus(status, HTTP_403_FORBIDDEN, NO_PERMISSION_MESSAGE)
        assert task is None
