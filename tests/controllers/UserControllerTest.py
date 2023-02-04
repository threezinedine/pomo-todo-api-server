import unittest
import os

from databases.base import (
    Base,
    get_session,
)
from databases.models import (
    User,
)
from app.controllers import UserController
from constants import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from constants.message import (
    USERNAME_EXISTS_MESSAGE,
    USERNAME_DOES_NOT_EXIST_MESSAGE,
    PASSWORD_IS_INCORRECT_MESSAGE,
)
from app.utils.database import (
    clear_database,
)
from tests.utils import (
    assertStatus,
    assertUserWithDict,
    createFirstUserBy,
)
from constants.test.user import (
    FIRST_USER_USERNAME,
    FIRST_USER_PASSWORD,
    FIRST_USER_WRONG_PASSWORD,
    FIRST_USER_NEW_USER_DESCRIPTION,
    FIRST_USER_TEST_IMAGE_PATH,
    FIRST_USER_FULL_DICT_NO_DESC_NO_IMAG,
    FIRST_USER_FULL_DICT_DESC_NO_IMAG,
    FIRST_USER_FULL_DICT_NO_DESC_IMAG,
)
from constants.database.user import (
    IMAGE_FOLDER,
    USER_IMAGE_DEFAULT,
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
        assertUserWithDict(response[0], **FIRST_USER_FULL_DICT_NO_DESC_NO_IMAG)

    def test_given_no_users_exist_when_create_new_users_then_returns_HTTP_200_OK_and_that_new_user(self):
        status, response = self.user_controller.create_new_user(username=FIRST_USER_USERNAME,
                                                                password=FIRST_USER_PASSWORD)

        assertStatus(status, HTTP_200_OK)
        assertUserWithDict(response, **FIRST_USER_FULL_DICT_NO_DESC_NO_IMAG)

    def test_given_no_users_exist_when_create_new_users_then_that_user_exist_inside_the_database(self):
        _, _ = self.user_controller.create_new_user(username=FIRST_USER_USERNAME,
                                                    password=FIRST_USER_PASSWORD)

        user = self.session.query(User).filter(
            User.username == FIRST_USER_USERNAME).first()
        assertUserWithDict(user, **FIRST_USER_FULL_DICT_NO_DESC_NO_IMAG)

    def test_given_a_user_exist_when_create_new_user_then_returns_HTTP_409_CONFLICT_and_None(self):
        createFirstUserBy(self.user_controller)

        status, response = self.user_controller.create_new_user(username=FIRST_USER_USERNAME,
                                                                password=FIRST_USER_PASSWORD)

        assertStatus(status, HTTP_409_CONFLICT, USERNAME_EXISTS_MESSAGE)
        assert response is None

    def test_given_a_user_exist_when_get_a_user_with_username_and_password_then_return_HTTP_200_OK_and_that_user(self):
        createFirstUserBy(self.user_controller)

        status, response = self.user_controller.get_user_by_username_and_password(username=FIRST_USER_USERNAME,
                                                                                  password=FIRST_USER_PASSWORD)

        assertStatus(status, HTTP_200_OK)
        assertUserWithDict(response, **FIRST_USER_FULL_DICT_NO_DESC_NO_IMAG)

    def test_given_when_get_a_user_with_non_existed_username_then_return_HTTP_404_NOT_FOUND_and_None(self):
        status, response = self.user_controller.get_user_by_username_and_password(username=FIRST_USER_USERNAME,
                                                                                  password=FIRST_USER_PASSWORD)

        assertStatus(status, HTTP_404_NOT_FOUND,
                     USERNAME_DOES_NOT_EXIST_MESSAGE)
        assert response is None

    def test_given_when_get_a_user_with_existed_username_and_not_valid_password_then_return_HTTP_401_UNAUTHORIZED_and_None(self):
        createFirstUserBy(self.user_controller)

        status, response = self.user_controller.get_user_by_username_and_password(username=FIRST_USER_USERNAME,
                                                                                  password=FIRST_USER_WRONG_PASSWORD)

        assertStatus(status, HTTP_401_UNAUTHORIZED,
                     PASSWORD_IS_INCORRECT_MESSAGE)
        assert response is None

    def test_given_a_user_is_created_when_change_the_description_by_valid_username_then_return_HTTP_200_OK_and_that_user(self):
        createFirstUserBy(self.user_controller)

        status, response = self.user_controller.change_description_by_username(username=FIRST_USER_USERNAME,
                                                                               description=FIRST_USER_NEW_USER_DESCRIPTION)

        assertStatus(status, HTTP_200_OK)
        assertUserWithDict(response, **FIRST_USER_FULL_DICT_DESC_NO_IMAG)

    def test_given_a_user_is_created_when_upload_the_description_by_a_valid_file_then_return_the_HTTP_200_OK_and_that_user(self):
        createFirstUserBy(self.user_controller)

        status, response = self.user_controller.change_user_image_path_by_username(username=FIRST_USER_USERNAME,
                                                                                   imagePath=FIRST_USER_TEST_IMAGE_PATH)

        assertStatus(status, HTTP_200_OK)
        assertUserWithDict(response, **FIRST_USER_FULL_DICT_NO_DESC_IMAG)

    def test_given_a_user_is_created_and_the_image_is_uploaded_when_get_the_image_path_by_username_then_return_HTTP_200_OK_and_image_path(self):
        createFirstUserBy(self.user_controller)
        self.user_controller.change_user_image_path_by_username(
            username=FIRST_USER_USERNAME, imagePath=FIRST_USER_TEST_IMAGE_PATH)

        status, response = self.user_controller.get_user_image_path_by_username(
            username=FIRST_USER_USERNAME)

        assertStatus(status, HTTP_200_OK)
        assert response == FIRST_USER_TEST_IMAGE_PATH

    def test_given_a_user_is_created_and_the_image_is_no_uploaded_when_get_the_image_path_by_username_then_return_HTTP_200_OK_and_default_image(self):
        createFirstUserBy(self.user_controller)

        status, response = self.user_controller.get_user_image_path_by_username(
            username=FIRST_USER_USERNAME)

        assertStatus(status, HTTP_200_OK)
        assert response == USER_IMAGE_DEFAULT
