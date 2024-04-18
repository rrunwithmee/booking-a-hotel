import jwt

from fastapi import Response
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="A")

SECRET_KEY = "B"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)

def create_jwt_token(data: dict):
    iat = datetime.utcnow()
    data.update({"iat": iat})
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None


def create_cookie(response: Response, jwt):
    response.set_cookie(key="test", value=jwt, max_age=3600)
    return {"message": "куки установлены"}


def get_cookie(response: Response):
    response.cookies
    return {"message": "куки установленыffff"}