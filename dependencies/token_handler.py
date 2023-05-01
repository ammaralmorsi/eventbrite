import os
from datetime import datetime
from datetime import timedelta

import jwt

from fastapi import HTTPException
from fastapi import status

from dependencies.models import users
from dependencies.db import users as users_db


users_driver = users_db.UsersDriver()


class TokenHandler:
    def __init__(self):
        self.secret_key = os.environ.get("JWT_SECRET_KEY")
        self.algorithm = "HS256"

    def encode_token(self, user: users.UserToken, duration=24):
        expiration_time = datetime.utcnow() + timedelta(hours=duration)
        start_time = datetime.utcnow().timestamp()
        payload = {"start": start_time, "exp": expiration_time, "id": user.id, "email": user.email}

        try:
            return jwt.encode(payload, self.secret_key, self.algorithm)
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(detail="jwt error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except TypeError as e:
            raise HTTPException(detail="type error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user(self, token) -> users.UserToken:
        try:
            payload = jwt.decode(token, self.secret_key, self.algorithm)
            last_updated_time = users_driver.get_last_password_update_time(payload["id"])
            user = users.UserToken(**payload)
            expiration_time = datetime.fromtimestamp(payload["exp"])
            start_time = datetime.fromtimestamp(payload["start"])
            if datetime.utcnow() > expiration_time or start_time < last_updated_time:
                raise HTTPException(detail="invalid token", status_code=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError as e:
            raise HTTPException(detail="invalid token", status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(detail="jwt error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return user
