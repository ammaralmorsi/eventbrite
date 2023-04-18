from pydantic import BaseModel

class User(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    is_verified: bool = False
    avatar_url: str

class LoginUser(BaseModel):
    email: str
    password: str


class ChangePasswordRequest(BaseModel):
    new_password: str
