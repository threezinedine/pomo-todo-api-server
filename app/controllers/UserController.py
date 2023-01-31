from sqlalchemy.orm import Session

from app.constants import (
    OK_STATUS,
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
        pass

    def get_all_users(self):
        """
        Get all users from the database
        """
        return OK_STATUS, []
