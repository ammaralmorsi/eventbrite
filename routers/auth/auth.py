from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from .db import models
from .db.driver import UsersDriver
from .password_handler import PasswordHandler
from .token_handler import TokenHandler
from .email_handler import EmailHandler
from .email_handler import EmailType

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

password_handler = PasswordHandler()
token_handler = TokenHandler()
email_handler = EmailHandler()
db = UsersDriver()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def handle_exists_email(email):
    if db.email_exists(email):
        raise HTTPException(detail="email already exists", status_code=status.HTTP_406_NOT_ACCEPTABLE)


def handle_not_exists_email(email):
    if not db.email_exists(email):
        raise HTTPException(detail="email not found", status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "/signup",
    description="add user to the database and send email to verify",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "email sent successfully to verify and user is added to the database",
            "content": {
                "text/plain": {
                    "example": "unverified user is created, please verify your email"
                },
            }
        },
        status.HTTP_406_NOT_ACCEPTABLE: {
            "description": "email already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "email already exists"
                    }
                }
            }
        }
    }
)
async def signup(user: models.UserInSignup) -> PlainTextResponse:
    handle_exists_email(user.email)

    user.password = password_handler.get_password_hash(user.password)
    inserted_user: dict = db.create_user(user.dict())

    token = token_handler.encode_token(models.UserToken(**inserted_user), 0.5)
    email_handler.send_email(user.email, token, EmailType.SIGNUP_VERIFICATION)

    return PlainTextResponse("unverified user is created, please verify your email", status_code=status.HTTP_200_OK)


@router.get(
    "/verify-email",
    description="given a token, verify the email",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "email verified successfully",
            "content": {
                "text/plain": {
                    "example": "email verified successfully"
                },
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid token"
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "email not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "email not found"
                    }
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "can't verify email",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "can't verify email"
                    }
                }
            }
        }
    }
)
async def verify_email(token: Annotated[str, Depends(oath2_scheme)]):
    user = token_handler.get_user(token)

    handle_not_exists_email(user.email)

    if not db.set_is_verified(user.email):
        raise HTTPException(detail="can't verify email", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return PlainTextResponse("email verified successfully", status_code=status.HTTP_200_OK)


@router.post(
    "/login",
    description="login and get access token",
    response_model=models.UserOutLogin,
    responses={
        status.HTTP_200_OK: {
            "description": "login successfully",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIiwiaWF0IjoxNjIyNjQyNjQyLCJleHAiOjE",
                        "token_type": "bearer"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "wrong password or email is not verified",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "wrong password or email is not verified"
                    }
                }
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "email not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "email not found"
                        }
                    }
                }
            }
        }
    }
)
async def login(user_in: Annotated[OAuth2PasswordRequestForm, Depends()]) -> models.UserOutLogin:
    user_in = models.UserInLogin(email=user_in.username, password=user_in.password)

    handle_not_exists_email(user_in.email)
    user_db: models.UserDB = models.UserDB(**db.find_user(user_in.email))
    if not password_handler.verify_password(user_in.password, user_db.password):
        raise HTTPException(detail="wrong password", status_code=status.HTTP_401_UNAUTHORIZED)

    encoded_token = token_handler.encode_token(models.UserToken(**user_db.dict()))
    if not user_db.is_verified:
        email_handler.send_email(user_db.email, encoded_token, EmailType.SIGNUP_VERIFICATION)
        raise HTTPException(detail="email is not verified", status_code=status.HTTP_401_UNAUTHORIZED)

    return models.UserOutLogin(access_token=encoded_token)


@router.post(
    "/forgot-password",
    description="given an email, send a verification email to reset password",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "sent a verification email",
            "content": {
                "text/plain": {
                    "example": "sent a verification email"
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "email not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "email not found"
                    }
                }
            }
        }
    }

)
async def forgot_password(email):
    handle_not_exists_email(email)

    encoded_token = token_handler.encode_token(models.UserToken(**db.find_user(email)), 0.5)
    email_handler.send_email(email, encoded_token, EmailType.FORGET_PASSWORD)
    return PlainTextResponse("sent a verification email", status_code=status.HTTP_200_OK)


@router.put(
    "/change-password",
    description="given a token, change the password",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "password updated successfully",
            "content": {
                "text/plain": {
                    "example": "password updated successfully"
                },
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid token"
                    }
                }
            }
        }
    }

)
async def change_password(token: Annotated[str, Depends(oath2_scheme)], request: models.UserInForgotPassword):
    user = token_handler.get_user(token)

    handle_not_exists_email(user.email)
    new_password = password_handler.get_password_hash(request.new_password)

    db.update_password(user.email, new_password)
    return PlainTextResponse("password updated successfully", status_code=status.HTTP_200_OK)


@router.post(
    "/check-email",
    description="check if email is available",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "email is available",
            "content": {
                "text/plain": {
                    "example": "email is available"
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "email not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "email not found"
                    }
                }
            }
        }
    }
)
async def check_email(email):
    handle_not_exists_email(email)

    return PlainTextResponse("email is available", status_code=status.HTTP_200_OK)
