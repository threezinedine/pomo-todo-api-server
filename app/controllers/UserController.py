from sqlalchemy.orm import Session

from app.constants import (
    OK_STATUS,
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
        user = User(username=username, password=password)
        session = self.session.add(user)
        self.session.commit()

        return OK_STATUS, user
