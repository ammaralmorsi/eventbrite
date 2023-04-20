import jwt
from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException
from fastapi import status

from .db import models


class TokenHandler:
    def __init__(self):
        self.secret_key = "e97244b639a6fdfd242a282aea9e02acc49aed30fb45e889aec683ae56cf1fe8"
        self.token_duration = 24
        self.algorithm = "HS256"

    def encode_token(self, user: models.UserToken):
        expiration_time = datetime.utcnow() + timedelta(hours=self.token_duration)

        payload = {"exp": expiration_time, "id": str(user.id), "email": user.email}

        return jwt.encode(payload, self.secret_key, self.algorithm)

    def get_user(self, token) -> models.UserToken:
        try:
            payload = jwt.decode(token, self.secret_key, self.algorithm)
            user = models.UserToken(**payload)
            expiration_time = datetime.fromtimestamp(payload["exp"])
            if datetime.utcnow() > expiration_time:
                raise HTTPException(detail="invalid token", status_code=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError as e:
            raise HTTPException(detail="invalid token", status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(detail="jwt error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return user
