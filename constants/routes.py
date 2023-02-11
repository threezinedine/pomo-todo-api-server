ROOT_ROUTE = "/"
USER_BASE_ROUTE = "/users"
USER_TAG = "users"

USER_REGISTER_ROUTE = "/register"
USER_REGISTER_FULL_ROUTE = f"{USER_BASE_ROUTE}{USER_REGISTER_ROUTE}"

USER_LOGIN_ROUTE = "/login"
USER_LOGIN_FULL_ROUTE = f"{USER_BASE_ROUTE}{USER_LOGIN_ROUTE}"

USER_CHANGE_DESCRIPTION_ROUTE = "/description"
USER_CHANGE_DESCRIPION_FULL_ROUTE = f"{USER_BASE_ROUTE}{USER_CHANGE_DESCRIPTION_ROUTE}"

USER_UPLOAD_IMAGE_ROUTE = '/upload-user-image'
USER_UPLOAD_IMAGE_FULL_ROUTE = f"{USER_BASE_ROUTE}{USER_UPLOAD_IMAGE_ROUTE}"

USER_GET_IMAGE_ROUTE = '/image'
USER_GET_IMAGE_FULL_ROUTE = f'{USER_BASE_ROUTE}{USER_GET_IMAGE_ROUTE}'

TASK_ROUTE_PREFIX = "/tasks"
TASK_TAG = "tasks"

TASK_CREATE_ROUTE = "/"
TASK_CREATE_FULL_ROUTE = f"{TASK_ROUTE_PREFIX}{TASK_CREATE_ROUTE}"

TASK_GET_ALL_ROUTE = "/"
TASK_GET_ROUTE = "/{taskId}"

TASK_CHANGE_TASK_NAME_ROUTE = "/task-name/{taskId}"
TASK_CHANGE_USERNAME_FULL_ROUTE = f"{TASK_ROUTE_PREFIX}{TASK_CHANGE_TASK_NAME_ROUTE}"

TASK_CHANGE_TASK_DESCRIPTION_ROUTE = "/task-description/{taskId}"

TASK_DELETE_ROUTE = "/{taskId}"

TASK_COMPLETE_ROUTE = "/complete"
TASK_COMPLETE_FULL_ROUTE = f"{TASK_ROUTE_PREFIX}{TASK_COMPLETE_ROUTE}"
