from datetime import datetime
from sqlalchemy.orm import Session

from constants.status import CREATED_STATUS, NO_PERMISSION_STATUS, OK_STATUS, TASK_NOT_FOUND_STATUS
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

    def complete_task_by_task_id_and_user_id(self,
                                             userId: int,
                                             taskId: int,
                                             completedTime: datetime):
        """
        Complete the task by the given taskId.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

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
        # TODO: If the userId does not match the userId of the task,
        # return NO_PERMISSION_STATUS and None.

        status = OK_STATUS

        task = self.session.query(Task).filter(Task.taskId == taskId).first()

        if task is None:
            status = TASK_NOT_FOUND_STATUS
        elif task.userId != userId:
            status = NO_PERMISSION_STATUS
            task = None
        else:
            task.taskComplete = True
            task.completedTime = completedTime

            self.session.commit()

        return status, task

    def get_task_by_task_id_and_user_id(self, userId: int, taskId: int):
        """
        Get the task by the given taskId.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

            taskId : int
                The id of the task.

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
        # TODO: Get the task by the given taskId, and return HTTP_200_OK and the task object.
        # TODO: If the task is not found, return TASK_NOT_FOUND_STATUS and None.
        # TODO: If the userId does not match the userId of the task, return NO_PERMISSION_STATUS and None.

        status = OK_STATUS

        task = self.session.query(Task).filter(Task.taskId == taskId).first()

        if task is None:
            status = TASK_NOT_FOUND_STATUS
        elif task.userId != userId:
            status = NO_PERMISSION_STATUS
            task = None

        return status, task

    def get_all_tasks_of_user(self, userId: int):
        """
        Get all the tasks of the given user.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

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
        # TODO: Get all the tasks of the given user, and return HTTP_200_OK and the list of tasks.
        status = OK_STATUS

        tasks = self.session.query(Task).filter(Task.userId == userId).all()

        return status, tasks

    def change_task_name_by_task_id_and_user_id(self,
                                                userId: int,
                                                taskId: int,
                                                newTaskName: str):
        """
        Change the task name by the given taskId.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

            taskId : int
                The id of the task.

            newTaskName : str
                The name of the task.

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
        # TODO: Get the task by the given taskId, change the taskName to newTaskName
        # and return HTTP_200_OK and the task object.
        # TODO: If the task is not found, return TASK_NOT_FOUND_STATUS and None.
        # TODO: If the userId does not match the userId of the task, return NO_PERMISSION_STATUS and None.

        status = OK_STATUS

        task = self.session.query(Task).filter(Task.taskId == taskId).first()

        if task is None:
            status = TASK_NOT_FOUND_STATUS
        elif task.userId != userId:
            status = NO_PERMISSION_STATUS
            task = None
        else:
            task.taskName = newTaskName

        self.session.commit()

        return status, task

    def change_task_description_by_task_id_and_user_id(self,
                                                       userId: int,
                                                       taskId: int,
                                                       newTaskDescription: str):
        """
        Change the task description by the given taskId.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

            taskId : int
                The id of the task.

            newTaskDescription : str
                The description of the task.

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
        # TODO: Get the task by the given taskId, change the taskDescription to newTaskDescription
        # and return HTTP_200_OK and the task object.
        # TODO: If the task is not found, return TASK_NOT_FOUND_STATUS and None.
        # TODO: If the userId does not match the userId of the task, return NO_PERMISSION_STATUS and None.

        status = OK_STATUS

        task = self.session.query(Task).filter(Task.taskId == taskId).first()

        if task is None:
            status = TASK_NOT_FOUND_STATUS
        elif task.userId != userId:
            status = NO_PERMISSION_STATUS
            task = None
        else:
            task.taskDescription = newTaskDescription

        self.session.commit()

        return status, task

    def delete_task_by_task_id_and_user_id(self, userId: int, taskId: int):
        """
        Delete the task by the given taskId.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

            taskId : int
                The id of the task.

        Returns
        -------
            status : dict
                The status of the request.

                status_code: int
                    The status code of the request.
                message: str
                    The message of the request.
        """
        # TODO: Get the task by the given taskId, delete the task and return HTTP_200_OK.
        # TODO: If the task is not found, return TASK_NOT_FOUND_STATUS and None.
        # TODO: If the userId does not match the userId of the task, return NO_PERMISSION_STATUS and None.

        status = OK_STATUS

        task = self.session.query(Task).filter(Task.taskId == taskId).first()

        if task is None:
            status = TASK_NOT_FOUND_STATUS
        elif task.userId != userId:
            status = NO_PERMISSION_STATUS
            task = None
        else:
            self.session.delete(task)
            self.session.commit()

        return status, None

    def delete_all_tasks_by_user_id(self, userId: int):
        """
        Delete all the tasks of the given user.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

        Returns
        -------
            status : dict
                The status of the request.

                status_code: int
                    The status code of the request.
                message: str
                    The message of the request.
        """
        # TODO: Get all the tasks of the given user, delete all the tasks and return HTTP_200_OK.

        status = OK_STATUS

        self.session.query(Task).filter(Task.userId == userId).delete()

        self.session.commit()

        return status, None

    def change_task_planned_date_by_task_id_and_user_id(self,
                                                        userId: int,
                                                        taskId: int,
                                                        newTaskPlannedDate: str):
        """
        Change the task planned date by the given taskId.

        Parameters
        ----------
            userId : int
                The id of the user who create the task.

            taskId : int
                The id of the task.

            newTaskPlannedDate : str
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
        # TODO: Get the task by the given taskId, change the taskPlannedDate to newTaskPlannedDate
        # and return HTTP_200_OK and the task object.
        # TODO: If the task is not found, return TASK_NOT_FOUND_STATUS and None.

        status = OK_STATUS

        task = self.session.query(Task).filter(Task.taskId == taskId).first()
        if task is None:
            status = TASK_NOT_FOUND_STATUS
        elif task.userId != userId:
            status = NO_PERMISSION_STATUS
            task = None
        else:
            task.plannedDate = newTaskPlannedDate

        return status, task
