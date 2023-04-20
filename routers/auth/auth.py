from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse

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


def handle_exists_email(email):
    if db.email_exists(email):
        raise HTTPException(detail={"email already exists"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)


def handle_not_exists_email(email):
    if not db.email_exists(email):
        raise HTTPException(detail={"email not found"}, status_code=status.HTTP_404_NOT_FOUND)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: models.UserInSignup):
    handle_exists_email(user.email)

    user.password = password_handler.get_password_hash(user.password)
    inserted_user: dict = db.create_user(**user.dict())

    token = token_handler.encode_token(**inserted_user)
    email_handler.send_email(user.email, token, EmailType.SIGNUP_VERIFICATION)

    return PlainTextResponse("please verify your email", status_code=status.HTTP_200_OK)


@router.get("/verify")
async def verify_email(token: str):
    user = token_handler.get_user(token)

    if not db.set_is_verified(user.email):
        raise HTTPException(detail="can't verify email", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return PlainTextResponse("email verified successfully", status_code=status.HTTP_201_CREATED)


@router.post("/login")
async def login(user_in: models.UserInLogin) -> models.UserOutLogin:
    handle_not_exists_email(user_in.email)

    user_db: models.UserDB = models.UserDB(**db.find_user(user_in.email))
    if not password_handler.verify_password(user_in.password, user_db.password):
        raise HTTPException(detail="wrong password", status_code=status.HTTP_401_UNAUTHORIZED)

    encoded_token = token_handler.encode_token(**user_db.dict())
    if not user_db.is_verified:
        email_handler.send_email(user_db.email, encoded_token, EmailType.SIGNUP_VERIFICATION)
        raise HTTPException(detail="email is not verified", status_code=status.HTTP_401_UNAUTHORIZED)

    return models.UserOutLogin(**user_db.dict(), token=encoded_token)


@router.post("/forgot-password")
async def forgot_password(email):
    handle_not_exists_email(email)

    encoded_token = token_handler.encode_token(**db.find_user(email).dict())
    email_handler.send_email(email, encoded_token, EmailType.FORGET_PASSWORD)
    return PlainTextResponse("sent a verification email", status_code=status.HTTP_200_OK)


@router.get("/reset-password")
async def reset_password(token: str):
    user = token_handler.get_user(token)

    handle_not_exists_email(user.email)

    return RedirectResponse(url=f"/auth/change-password?token={token}")


@router.put("/change-password")
async def change_password(token: str, request: models.UserInForgotPassword):
    user = token_handler.get_user(token)

    new_password = password_handler.get_password_hash(request.password)

    db.update_password(user.email, new_password)
    return PlainTextResponse("password updated successfully", status_code=status.HTTP_200_OK)


@router.post("/check-email")
async def check_email(email):
    handle_not_exists_email(email)

    return PlainTextResponse("email is available", status_code=status.HTTP_200_OK)
