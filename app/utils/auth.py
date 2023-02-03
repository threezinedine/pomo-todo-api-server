import jwt
import datetime
from fastapi import (
    HTTPException,
)


secret_key = "testing_secret_key"
algorithm = 'HS256'
DEFAULT_EXPIRED_TIME = datetime.timedelta(hours=1)
EXPIRED_TIME_KEY = "exp"

def generate_token(data: dict, 
                        password: str, 
                        algorithm: str = algorithm,
                        exp_time: datetime.timedelta = DEFAULT_EXPIRED_TIME):
    data[EXPIRED_TIME_KEY] = datetime.datetime.utcnow() + exp_time
    return jwt.encode(data, password, algorithm)

def verify_token(token: str, password: str, algorithm: str = algorithm):
    try: 
        decoded_data = jwt.decode(token, password, algorithm)
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=404, detail=)