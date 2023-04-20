from typing import Annotated

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import HttpUrl

from bson import ObjectId

password_type = Annotated[str, Field(
        example="password",
        title="New password",
        description="New password of the user",
    )]
email_type = Annotated[EmailStr, Field(
        example="user@gmail.com",
        title="Email",
        description="Email of the user",
    )]
firstname_type = Annotated[str, Field(
        example="John",
        title="First name",
        description="First name of the user",
    )]
lastname_type = Annotated[str, Field(
        example="Doe",
        title="Last name",
        description="Last name of the user",
    )]
avatar_url_type = Annotated[HttpUrl | None, Field(
        example="https://example.com/avatar.png",
        title="Avatar URL",
        description="URL of the user's avatar",
    )]
is_verified_type = Annotated[bool, Field(
        example=True,
        title="Is verified",
        description="Is the user verified",
    )]


class UserInSignup(BaseModel):
    email: email_type
    password: password_type
    firstname: firstname_type
    lastname: lastname_type


class UserInLogin(BaseModel):
    email: email_type
    password: password_type


class UserInForgotPassword(BaseModel):
    password: password_type


class UserDB(UserInSignup):
    is_verified: is_verified_type | bool = False
    avatar_url: avatar_url_type | str = ""


class UserOutLogin(BaseModel):
    token: str
    email: email_type
    firstname: firstname_type
    lastname: lastname_type
    avatar_url: avatar_url_type


class UserToken(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    email: email_type

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
