import os
from datetime import datetime
from datetime import timedelta
from bson import ObjectId

import jwt

from fastapi import HTTPException
from fastapi import status

from routers.auth.db import models


class TokenHandler:
    def __init__(self):
        self.secret_key = os.environ.get("JWT_SECRET_KEY")
        self.algorithm = "HS256"

    def encode_token(self, user: models.UserToken, duration=24):
        expiration_time = datetime.utcnow() + timedelta(hours=duration)

        payload = {"exp": expiration_time, "id": str(user.id), "email": user.email}

        try:
            return jwt.encode(payload, self.secret_key, self.algorithm)
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(detail="jwt error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except TypeError as e:
            raise HTTPException(detail="type error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user(self, token) -> models.UserToken:
        try:
            payload = jwt.decode(token, self.secret_key, self.algorithm)
            payload["id"] = ObjectId(payload["id"])    # Convert _id field to ObjectId
            user = models.UserToken(**payload)
            expiration_time = datetime.fromtimestamp(payload["exp"])
            if datetime.utcnow() > expiration_time:
                raise HTTPException(detail="invalid token", status_code=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError as e:
            raise HTTPException(detail="invalid token", status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(detail="jwt error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return user
