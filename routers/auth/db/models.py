from pydantic import BaseModel

class User(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    is_verified: bool = False

class LoginUser(BaseModel):
    email: str
    password: str