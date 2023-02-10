from sqlalchemy.orm import Session

from constants.status import CREATED_STATUS
from databases.models import Task


class TaskController:
    """
    Controller which interact with the task tables. 
    """

    def __init__(self, session: Session):
        self.session = session

    def create_new_task(self,
                        userId: int,
                        taskName: str,
                        taskDescription: str,
                        plannedDate: str):
        """
        Create a new task for the given user.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

            taskName : str
                The name of the task.

            taskDescription : str
                The description of the task.

            plannedDate : str
                The planned date of the task.

        Returns
        -------
            status : dict
                The status of the request.

                status_code: int
                    The status code of the request.
                message: str
                    The message of the request.

            task : SqlAlchemy object
                The task object.
        """
        # TODO: Create a new task for the given userId, and return CREATED_STATUS and the task object.
        status = CREATED_STATUS

        task = Task(
            userId=userId,
            taskName=taskName,
            taskDescription=taskDescription,
            plannedDate=plannedDate,
        )

        return status, task
