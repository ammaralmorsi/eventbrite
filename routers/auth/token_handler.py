import jwt
from datetime import datetime
from datetime import timedelta


class TokenHandler:
    def __init__(self):
        self.secret_key = "e97244b639a6fdfd242a282aea9e02acc49aed30fb45e889aec683ae56cf1fe8"
        self.token_duration = 24
        self.algorithm = "HS256"

    def encode_token(self, email):
        expiration_time = datetime.utcnow() + timedelta(hours=self.token_duration)
        payload = {"email": email, "exp": expiration_time}
        encoded_token = jwt.encode(payload, self.secret_key, self.algorithm)
        return encoded_token

    def decode_token(self, token):
        payload = jwt.decode(token, self.secret_key, self.algorithm)
        email = payload["email"]
        expiration_time = datetime.fromtimestamp(payload["exp"])
        return email, expiration_time

