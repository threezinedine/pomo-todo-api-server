from sqlalchemy.orm import Session


class TaskController:
    """
    Controller which interact with the task tables. 
    """

    def __init__(self, session: Session):
        self.session = session
