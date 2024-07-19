import hashlib

import jwt

from datetime import datetime, timedelta


SECRET_KEY = "B"
JWT_ALGORITHM = "HS256"

PASSWORD_HASH_ALGORITHM = "sha256"


def hash_password(password: str):
    sha256 = hashlib.sha256()
    sha256.update(password.encode())
    return sha256.hexdigest()


def create_jwt_token(data: dict):
    now = datetime.utcnow()
    payload = {
        'iat': now,
        'exp': now + timedelta(hours=1)
    } | data

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt





def decode_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is invalid


