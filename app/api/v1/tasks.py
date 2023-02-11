from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
)
from app.schemas.TaskSchema import TaskChangeTaskDescriptionRequestModel, TaskChangeTaskNameRequestModel, TaskCompleteRequestModel, TaskRequestModel, TaskResponseModel
from app.utils.auth import get_token
from app.utils.api import handleStatus
from app.controllers.TaskController import TaskController
from constants import HTTP_200_OK, HTTP_201_CREATED
from constants.database.user import USERID_KEY

from constants.routes import (
    TASK_CHANGE_TASK_DESCRIPTION_ROUTE,
    TASK_CHANGE_TASK_NAME_ROUTE,
    TASK_COMPLETE_ROUTE,
    TASK_DELETE_ALL_ROUTE,
    TASK_DELETE_ROUTE,
    TASK_GET_ALL_ROUTE,
    TASK_GET_ROUTE,
    TASK_ROUTE_PREFIX,
    TASK_TAG,
    TASK_CREATE_ROUTE,
)
from databases.base import get_session


router = APIRouter(prefix=TASK_ROUTE_PREFIX, tags=[TASK_TAG])


@router.post(
    TASK_CREATE_ROUTE,
    status_code=HTTP_201_CREATED,
    response_model=TaskResponseModel,
)
def create_task(task: TaskRequestModel,
                session=Depends(get_session),
                userInfo: dict = Depends(get_token)):
    status, task = TaskController(session).create_new_task(
        userId=userInfo[USERID_KEY],
        taskName=task.taskName,
        taskDescription=task.taskDescription,
        plannedDate=task.plannedDate,
    )

    handleStatus(status)

    return task


@router.put(
    TASK_COMPLETE_ROUTE,
    status_code=HTTP_200_OK,
    response_model=TaskResponseModel,
)
def complete_task(task: TaskCompleteRequestModel,
                  session=Depends(get_session),
                  userInfo: dict = Depends(get_token)):
    status, task = TaskController(session).complete_task_by_task_id_and_user_id(
        userId=userInfo[USERID_KEY],
        taskId=task.taskId,
        completedTime=task.completedTime,
    )

    handleStatus(status)

    return task


# Getting a task with task id route which is obtain from url path.
@router.get(
    TASK_GET_ROUTE,
    status_code=HTTP_200_OK,
    response_model=TaskResponseModel,
)
def get_task(taskId: int,
             session=Depends(get_session),
             userInfo: dict = Depends(get_token)):
    status, task = TaskController(session).get_task_by_task_id_and_user_id(
        userId=userInfo[USERID_KEY],
        taskId=taskId,
    )

    handleStatus(status)

    return task


@router.get(
    TASK_GET_ALL_ROUTE,
    status_code=HTTP_200_OK,
    response_model=list[TaskResponseModel],
)
def get_all_tasks(session=Depends(get_session),
                  userInfo: dict = Depends(get_token)):
    status, tasks = TaskController(session).get_all_tasks()

    handleStatus(status)

    return tasks


@router.put(
    TASK_CHANGE_TASK_NAME_ROUTE,
    status_code=HTTP_200_OK,
    response_model=TaskResponseModel,
)
def change_task_name(task: TaskChangeTaskNameRequestModel,
                     session=Depends(get_session),
                     userInfo: dict = Depends(get_token)):
    status, task = TaskController(session).change_task_name_by_task_id_and_user_id(
        userId=userInfo[USERID_KEY],
        taskId=task.taskId,
        newTaskName=task.taskName,
    )

    handleStatus(status)

    return task


@router.put(
    TASK_CHANGE_TASK_DESCRIPTION_ROUTE,
    status_code=HTTP_200_OK,
    response_model=TaskResponseModel,
)
def change_task_description(task: TaskChangeTaskDescriptionRequestModel,
                            session=Depends(get_session),
                            userInfo: dict = Depends(get_token)):
    status, task = TaskController(session).change_task_description_by_task_id_and_user_id(
        userId=userInfo[USERID_KEY],
        taskId=task.taskId,
        newTaskDescription=task.taskDescription,
    )

    handleStatus(status)

    return task


@router.delete(
    TASK_DELETE_ROUTE,
    status_code=HTTP_200_OK,
)
def delete_task(taskId: int,
                session=Depends(get_session),
                userInfo: dict = Depends(get_token)):
    status, task = TaskController(session).delete_task_by_task_id_and_user_id(
        userId=userInfo[USERID_KEY],
        taskId=taskId,
    )

    handleStatus(status)

    return None


@router.delete(
    TASK_DELETE_ALL_ROUTE,
    status_code=HTTP_200_OK,
)
def delete_all_tasks(session=Depends(get_session),
                     userInfo: dict = Depends(get_token)):
    status, _ = TaskController(session).delete_all_tasks_by_user_id(
        userId=userInfo[USERID_KEY],
    )

    handleStatus(status)

    return None
