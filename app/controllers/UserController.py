from sqlalchemy.orm import Session

from constants.status import (
    OK_STATUS,
    USERNAME_DOES_NOT_EXIST_STATUS,
    USERNAME_EXIST_STATUS,
    PASSWORD_IS_INCORRECT_STATUS,
)
from constants.database.user import (
    USER_IMAGE_DEFAULT,
)
from databases.models.User import (
    User,
)


class UserController:
    """
    The controller class for all users' operations.

    Parameters
    ----------
        session: Session
            The database session which can handle inside
    """

    def __init__(self, session: Session):
        self.session = session

    def get_all_users(self):
        """
        Get all users from the database

        Returns
        -------
            status: status_code, detail_message 
                The result status

            users: list 
                The list of all users inside the project
        """
        return OK_STATUS, self.session.query(User).all()

    def create_new_user(self, username: str, password: str):
        """
        Create a new user.

        Parameters
        ----------
            username: str 
                The username information

            password: str 
                The password information

        Returns
        -------
            status: status_code, detail_message 
                The result status

            user: User 
                The user which is created
        """
        new_user = None
        status = USERNAME_EXIST_STATUS
        user = self._get_user_by_username(username=username)

        if user is None:
            new_user = User(username=username, password=password)
            status = OK_STATUS
            self.session.add(new_user)
            self.session.commit()

        return status, new_user

    def get_user_by_username_and_password(self, username: str, password: str):
        """
        Get a user from the database by username and password 

        Parameters
        ----------
            username: str
                The username
            password: str 
                The password

        Returns
        -------
            status: status_code, detail_message 
                The result status

            user: User 
                The user which is created
        """
        status = OK_STATUS
        user = self._get_user_by_username(username=username)

        if user is None:
            status = USERNAME_DOES_NOT_EXIST_STATUS
        else:
            if not user.match_password(password):
                status = PASSWORD_IS_INCORRECT_STATUS
                user = None

        return status, user

    def change_description_by_username(self, username: str, description: str):
        """
        Change the description by username

        Parameters
        ----------
            username: str
                The username
            description: str 
                The description

        Returns
        -------
            status: status_code, detail_message 
                The result status

            user: User 
                The user which is modified.
        """
        user = self._get_user_by_username(username)
        user.description = description
        self.session.commit()
        return OK_STATUS, user

    def change_user_image_path_by_username(self, username: str, imagePath: str):
        """
        Change the imagePath by username

        Parameters
        ----------
            username: str
                The username
            imagePath: str 
                The imagePath

        Returns
        -------
            status: status_code, detail_message 
                The result status

            user: User 
                The user which is modified.
        """
        user = self._get_user_by_username(username)
        user.imagePath = imagePath
        self.session.commit()

        return OK_STATUS, user

    def get_user_image_path_by_username(self, username: str):
        user = self._get_user_by_username(username=username)
        result = USER_IMAGE_DEFAULT

        if user.imagePath is not None:
            result = user.imagePath

        return OK_STATUS, result

    def _get_user_by_username(self, username: str):
        return self.session.query(User).filter(
            User.username == username).first()

    def __repr__(self) -> str:
        return f"<UserController session={self.session} />"
