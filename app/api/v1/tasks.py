from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
)
from app.schemas.TaskSchema import TaskCompleteRequestModel, TaskRequestModel, TaskResponseModel
from app.utils.auth import get_token
from app.utils.api import handleStatus
from app.controllers.TaskController import TaskController
from constants import HTTP_200_OK, HTTP_201_CREATED
from constants.database.user import USERID_KEY

from constants.routes import (
    TASK_COMPLETE_ROUTE,
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
    status, task = TaskController(session).complete_task_by_task_id(
        taskId=task.taskId,
        completedTime=task.completedTime,
    )

    handleStatus(status)

    return task
