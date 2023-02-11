import unittest
from app.controllers.TaskController import TaskController
from constants import (
    AUTHORIZATION_KEY,
    ERROR_RESPONSE_DETAIL_KEY,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
)
from constants.database.user import USERID_KEY
from constants.database.task import (
    TASK_COMPLETED_TIME_KEY,
    TASK_ID_KEY,
    TASK_DESCRIPTION_KEY,
    TASK_NAME_KEY,
    TASK_PLANNED_DATE_KEY
)
from constants.message import NO_PERMISSION_MESSAGE
from constants.test.task import (
    FIRST_TASK,
    FIRST_TASK_CHANGE_TASK_NAME,
    FIRST_TASK_CHANGED_TASK_NAME_TASK,
    FIRST_TASK_COMPLETE,
    FIRST_TASK_COMPLETED_TIME,
    FIRST_TASK_TASK_DESCRIPTION,
    FIRST_TASK_TASK_ID,
    FIRST_TASK_TASK_NAME,
    FIRST_TASK_TASK_PLANNED_DATE,
    FIRST_TASK_CHANGE_TASK_DESCRIPTION,
    FIRST_TASK_CHANGE_TASK_DESCRIPTION_TASK,
)
from constants.routes import (
    TASK_CREATE_FULL_ROUTE,
    TASK_COMPLETE_FULL_ROUTE,
    TASK_ROUTE_PREFIX,
)
from constants.test.user import FIRST_USER_USERID, SECOND_USER_USERID

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
from tests.utils import assertTaskWithDict, createFirstTaskForFirstUserBy, createFirstUserBy, createSecondUserBy, getFirstUserTokenBy, getSecondUserTokenBy


class TaskEndToEndTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)
        self.task_controller = TaskController(self.session)

    def tearDown(self):
        clear_data(self.session)

    def test_given_when_creating_a_new_task_by_user_id_then_return_OK_STATUS_and_that_task(self):
        createFirstUserBy(self.user_controller)
        token = getFirstUserTokenBy()

        response = test_client.post(
            TASK_CREATE_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            json={
                TASK_NAME_KEY: FIRST_TASK_TASK_NAME,
                TASK_DESCRIPTION_KEY: FIRST_TASK_TASK_DESCRIPTION,
                TASK_PLANNED_DATE_KEY: FIRST_TASK_TASK_PLANNED_DATE,
            }
        )

        assert response.status_code == HTTP_201_CREATED
        assertTaskWithDict(response.json(), **FIRST_TASK)

    def test_complete_task_feature(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)
        token = getFirstUserTokenBy()

        response = test_client.put(
            TASK_COMPLETE_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            json={
                TASK_ID_KEY: FIRST_TASK_TASK_ID,
                TASK_COMPLETED_TIME_KEY: FIRST_TASK_COMPLETED_TIME,
            }
        )

        response_data = response.json()
        response_data[TASK_COMPLETED_TIME_KEY] = response_data[TASK_COMPLETED_TIME_KEY].replace(
            "T", " ")
        assert response.status_code == HTTP_200_OK
        assertTaskWithDict(response_data, **FIRST_TASK_COMPLETE)

    def test_complete_task_which_have_no_permission(self):
        createFirstUserBy(self.user_controller)
        createSecondUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)
        token = getFirstUserTokenBy()
        token_2 = getSecondUserTokenBy()

        response = test_client.put(
            TASK_COMPLETE_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token_2,
                USERID_KEY: str(SECOND_USER_USERID),
            },
            json={
                TASK_ID_KEY: FIRST_TASK_TASK_ID,
                TASK_COMPLETED_TIME_KEY: FIRST_TASK_COMPLETED_TIME,
            }
        )

        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.json()[
            ERROR_RESPONSE_DETAIL_KEY] == NO_PERMISSION_MESSAGE

    # e2e test for getting a task by task id
    def test_get_task_by_task_id(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)
        token = getFirstUserTokenBy()

        response = test_client.get(
            f"{TASK_ROUTE_PREFIX}/{FIRST_TASK_TASK_ID}",
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
        )

        assert response.status_code == HTTP_200_OK
        assertTaskWithDict(response.json(), **FIRST_TASK)

    # e2e test for getting all tasks of the user
    def test_get_all_tasks_of_the_user(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)
        token = getFirstUserTokenBy()

        response = test_client.get(
            TASK_ROUTE_PREFIX,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
        )

        assert response.status_code == HTTP_200_OK
        assertTaskWithDict(response.json()[0], **FIRST_TASK)

    # e2e test for changing the task name
    def test_change_task_name(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)
        token = getFirstUserTokenBy()

        response = test_client.put(
            f"{TASK_ROUTE_PREFIX}/task-name/{FIRST_TASK_TASK_ID}",
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            json={
                TASK_ID_KEY: FIRST_TASK_TASK_ID,
                TASK_NAME_KEY: FIRST_TASK_CHANGE_TASK_NAME,
            }
        )

        print(response, response.json())
        assert response.status_code == HTTP_200_OK
        assertTaskWithDict(response.json(), **
                           FIRST_TASK_CHANGED_TASK_NAME_TASK)

    # e2e test for changing the task description
    def test_change_task_description(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)
        token = getFirstUserTokenBy()

        response = test_client.put(
            f"{TASK_ROUTE_PREFIX}/task-description/{FIRST_TASK_TASK_ID}",
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            json={
                TASK_ID_KEY: FIRST_TASK_TASK_ID,
                TASK_DESCRIPTION_KEY: FIRST_TASK_CHANGE_TASK_DESCRIPTION,
            }
        )

        print(response, response.json())
        assert response.status_code == HTTP_200_OK
        assertTaskWithDict(response.json(), **
                           FIRST_TASK_CHANGE_TASK_DESCRIPTION_TASK)

    # e2e test for deleting a task by task id
    def test_delete_task_by_task_id(self):
        createFirstUserBy(self.user_controller)
        createFirstTaskForFirstUserBy(self.task_controller)
        token = getFirstUserTokenBy()

        response = test_client.delete(
            f"{TASK_ROUTE_PREFIX}/{FIRST_TASK_TASK_ID}",
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
        )

        assert response.status_code == HTTP_200_OK
        assert response.json() is None
