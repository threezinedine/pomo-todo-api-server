from constants.database.user import (
    USERNAME_KEY,
    USER_DESCRIPTION_KEY,
    PASSWORD_KEY,
    IMAGE_PATH_KEY,
)

FIRST_USER_USERID = 1
FIRST_USER_USERNAME = "threezinedineusername"
FIRST_USER_PASSWORD = "threezinedinepassword"
FIRST_USER_WRONG_USERNAME = "threezinedinewrongusername"
FIRST_USER_WRONG_PASSWORD = "threezinedinewrongpassword"

FIRST_USER_NEW_USER_DESCRIPTION = "This is the description for the first_testing_user"

FIRST_USER_WRONG_TOKEN = "firstUserWrongToken"
FIRST_USER_WRONG_USERID = 2

FIRST_USER_TEST_IMAGE_NAME = "user-test.png"
FIRST_USER_TEST_IMAGE_PATH = f"constants/test/images/{FIRST_USER_TEST_IMAGE_NAME}"

FIRST_USER_DICT_WITHOUT_DESCRIPTION = {
    USERNAME_KEY: FIRST_USER_USERNAME,
    USER_DESCRIPTION_KEY: None,
}

FIRST_USER_DICT_WITH_DESCRIPTION = {
    USERNAME_KEY: FIRST_USER_USERNAME,
    USER_DESCRIPTION_KEY: FIRST_USER_NEW_USER_DESCRIPTION,
}

FIRST_USER_FULL_DICT_NO_DESC_NO_IMAG = {
    USERNAME_KEY: FIRST_USER_USERNAME,
    PASSWORD_KEY: FIRST_USER_PASSWORD,
    USER_DESCRIPTION_KEY: None,
    IMAGE_PATH_KEY: None
}

FIRST_USER_FULL_DICT_DESC_NO_IMAG = {
    USERNAME_KEY: FIRST_USER_USERNAME,
    PASSWORD_KEY: FIRST_USER_PASSWORD,
    USER_DESCRIPTION_KEY: FIRST_USER_NEW_USER_DESCRIPTION,
    IMAGE_PATH_KEY: None
}


FIRST_USER_FULL_DICT_NO_DESC_IMAG = {
    USERNAME_KEY: FIRST_USER_USERNAME,
    PASSWORD_KEY: FIRST_USER_PASSWORD,
    USER_DESCRIPTION_KEY: None,
    IMAGE_PATH_KEY: FIRST_USER_TEST_IMAGE_PATH,
}


SECOND_USER_USERID = 2
SECOND_USER_USERNAME = "threezinedinethirdusername"
SECOND_USER_PASSWORD = "threezinedinethirdpassword"
SECOND_USER_WRONG_USERNAME = "threezinedinethirdwrongusername"
SECOND_USER_WRONG_PASSWORD = "threezinedinethirdwrongpassword"

SECOND_USER_NEW_USER_DESCRIPTION = "This is the description for the second_testing_user"