import unittest

from databases.base import (
    Base,
    get_session,
)
from databases.models import (
    User,
)
from app.controllers import UserController
from app.constants import (
    HTTP_200_OK,
    HTTP_409_CONFLICT,
    USERNAME_EXISTS_MESSAGE,
)
from app.utils.database import (
    clear_database,
)
from tests.utils import (
    assertStatus, 
    assertUserWithDict,
    createFirstUserBy,
)
from tests.constants import (
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
)
from tests.database import get_testing_session


class UserControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session) 

    def tearDown(self):
        clear_database(self.session)
        self.session.close()

    def test_given_no_users_exist_when_get_all_users_then_returns_empty_array(self):
        status, response = self.user_controller.get_all_users()

        assertStatus(status, HTTP_200_OK)
        self.assertListEqual(response, [])

    def test_given_a_user_exists_when_get_all_users_then_returns_the_array_contains_that_user(self):
        createFirstUserBy(self.user_controller)

        status, response = self.user_controller.get_all_users()
        assertStatus(status, HTTP_200_OK)
        assert len(response) == 1 
        assertUserWithDict(response[0],
                            username=FIRST_USER_USERNAME,
                            password=FIRST_USER_PASSWORD)


    def test_given_no_users_exist_when_create_new_users_then_returns_HTTP_200_OK_and_that_new_user(self):
        status, response = self.user_controller.create_new_user(username=FIRST_USER_USERNAME, 
                                                                    password=FIRST_USER_PASSWORD)

        assertStatus(status, HTTP_200_OK)
        assertUserWithDict(response,
                            username=FIRST_USER_USERNAME,
                            password=FIRST_USER_PASSWORD)

    def test_given_no_users_exist_when_create_new_users_then_that_user_exist_inside_the_database(self):
        status, response = self.user_controller.create_new_user(username=FIRST_USER_USERNAME, 
                                                                    password=FIRST_USER_PASSWORD)

        user = self.session.query(User).filter(User.username==FIRST_USER_USERNAME).first()
        assertUserWithDict(user,
                            username=FIRST_USER_USERNAME,
                            password=FIRST_USER_PASSWORD)

    def test_given_a_user_exist_when_create_new_user_then_returns_HTTP_409_CONFLICT_and_None(self):
        createFirstUserBy(self.user_controller)

        status, response = self.user_controller.create_new_user(username=FIRST_USER_USERNAME, 
                                                                    password=FIRST_USER_PASSWORD)

        assertStatus(status, HTTP_409_CONFLICT, USERNAME_EXISTS_MESSAGE)
        assert response is None
