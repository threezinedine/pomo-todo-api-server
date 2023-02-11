from datetime import datetime
from sqlalchemy.orm import Session

from constants.status import CREATED_STATUS, OK_STATUS, TASK_NOT_FOUND_STATUS
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

        self.session.add(task)
        self.session.commit()

        return status, task

    def get_all_tasks(self):
        """
        Get all the tasks.

        Returns
        -------
            status : dict
                The status of the request.

                status_code: int
                    The status code of the request.
                message: str
                    The message of the request.

            tasks : list
                The list of tasks.
        """
        # TODO: Get all the tasks, and return HTTP_200_OK and the list of tasks.
        status = OK_STATUS

        tasks = self.session.query(Task).all()

        return status, tasks

    def complete_task_by_task_id(self,
                                 taskId: int,
                                 completedTime: datetime):
        """
        Complete the task by the given taskId.

        Parameters
        ----------
            taskId : int
                The id of the task.

            completedTime : datetime
                The time when the task is completed.

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
        # TODO: Get the task by the given taskId,
        # udpate the taskComplete to True and the current time to completedTime
        # and return HTTP_200_OK and the task object.
        # TODO: If the task is not found, return TASK_NOT_FOUND_STATUS and None.

        status = OK_STATUS

        task = self.session.query(Task).filter(Task.taskId == taskId).first()

        if task is None:
            status = TASK_NOT_FOUND_STATUS
        else:
            task.taskComplete = True
            task.completedTime = completedTime

            self.session.commit()

        return status, task
