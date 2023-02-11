import unittest
from app.controllers.TaskController import TaskController
from constants import (
    AUTHORIZATION_KEY,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from constants.database.user import USERID_KEY
from constants.database.task import (
    TASK_ID_KEY,
    TASK_DESCRIPTION_KEY,
    TASK_NAME_KEY,
    TASK_PLANNED_DATE_KEY
)
from constants.test.task import (
    FIRST_TASK,
    FIRST_TASK_COMPLETE,
    FIRST_TASK_TASK_DESCRIPTION,
    FIRST_TASK_TASK_ID,
    FIRST_TASK_TASK_NAME,
    FIRST_TASK_TASK_PLANNED_DATE,
)
from constants.routes import (
    TASK_CREATE_FULL_ROUTE,
    TASK_COMPLETE_FULL_ROUTE,
)
from constants.test.user import FIRST_USER_USERID

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
from tests.utils import assertTaskWithDict, createFirstUserBy, getFirstUserTokenBy


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
        token = getFirstUserTokenBy()

        test_client.post(
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

        response = test_client.put(
            TASK_COMPLETE_FULL_ROUTE,
            headers={
                AUTHORIZATION_KEY: token,
                USERID_KEY: str(FIRST_USER_USERID),
            },
            json={
                TASK_ID_KEY: FIRST_TASK_TASK_ID,
            }
        )

        assert response.status_code == HTTP_200_OK
        assertTaskWithDict(response.json(), **FIRST_TASK_COMPLETE)
