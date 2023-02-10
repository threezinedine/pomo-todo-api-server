from fastapi import (
    APIRouter,
    Depends,
)
from app.schemas.TaskSchema import TaskRequestModel, TaskResponseModel
from app.utils.auth import get_token
from app.utils.api import handleStatus
from app.controllers.TaskController import TaskController
from constants import HTTP_201_CREATED
from constants.database.user import USERID_KEY

from constants.routes import (
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
    print(task, task.taskId)

    return task
