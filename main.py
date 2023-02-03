import os
from fastapi import (
    FastAPI,
    Depends,
)
from dotenv import load_dotenv

from constants.env import (
    HOST_ENV_VARIABLE_KEY,
    PORT_ENV_VARIABLE_KEY,
    HOST_DEFAULT,
    PORT_DEFAULT,
    WELCOM_MESSAGE_ENV_VARIABLE_KEY,
)
from constants import (
    MAIN_KEY,
    EMPTY_STRING,
)
from constants.routes import (
    ROOT_ROUTE,
)
from app.api.v1 import users
from databases.base import get_session


load_dotenv()
app = FastAPI()

app.include_router(users.router)


@app.get(ROOT_ROUTE)
def home_url(session = Depends(get_session)):
    return dict(message=os.getenv(WELCOM_MESSAGE_ENV_VARIABLE_KEY, EMPTY_STRING))


if __name__ == "__main__":
    import uvicorn

    host = os.getenv(HOST_ENV_VARIABLE_KEY, HOST_DEFAULT)
    port = int(os.getenv(PORT_ENV_VARIABLE_KEY, PORT_DEFAULT))

    uvicorn.run(MAIN_KEY, host=host, port=port, reload=True)
