import jwt
import datetime
from fastapi import (
    HTTPException,
)

from constants.utils.auth import (
    EXPIRED_TIME_KEY,
    DEFAULT_EXPIRED_TIME,
    ALGORITHM,
)
from constants import (
    HTTP_401_UNAUTHORIZED,
)
from constants.message import (
    TOKEN_IS_EXPIRED_MESSAGE,
    TOKEN_IS_NOT_VALID_MESSAGE,
)



def generate_token(data: dict, 
                        password: str, 
                        algorithm: str = ALGORITHM,
                        exp_time: datetime.timedelta = DEFAULT_EXPIRED_TIME):
    data[EXPIRED_TIME_KEY] = datetime.datetime.utcnow() + exp_time
    return jwt.encode(data, password, algorithm)

def verify_token(token: str, password: str, algorithm: str = ALGORITHM):
    try: 
        return jwt.decode(token, password, algorithm)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=TOKEN_IS_EXPIRED_MESSAGE)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=TOKEN_IS_NOT_VALID_MESSAGE)