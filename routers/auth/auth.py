from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
import jwt

from .commons import is_unique
from .db import models
from .db.driver import get_db_conn
from .password_handler import PasswordHandler
from .token_handler import TokenHandler
from .email_handler import EmailHandler
from .email_handler import EmailType

from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

password_handler = PasswordHandler()
token_handler = TokenHandler()
email_handler = EmailHandler()
db = get_db_conn()


@router.post("/signup")
async def signup(user: models.UserInSignup):
    if not is_unique(user.email):
        return JSONResponse(content={"message": "email is already registered"}, status_code=status.HTTP_400_BAD_REQUEST)
    token = token_handler.encode_token(user.email)
    send_email_value, body = email_handler.send_email(user.email, token, EmailType.SIGNUP_VERIFICATION)
    if send_email_value == -1:
        return JSONResponse(content={"message": body}, status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = password_handler.get_password_hash(user.password)
    user.password = hashed_password
    db["User"].insert_one(models.UserDB(**user.dict()))
    return JSONResponse(content={"message": "Please verify your email before your login"},
                        status_code=status.HTTP_200_OK)


@router.get("/verify")
async def verify_email(token: str):
    try:
        email, expiration_time = token_handler.decode_token(token)
        if datetime.utcnow() > expiration_time:
            return JSONResponse(content={"message": "Token has expired"}, status_code=status.HTTP_400_BAD_REQUEST)
        result = db["User"].update_one({"email": email}, {"$set": {"is_verified": True}})
        if result.modified_count == 1:
            return JSONResponse(content={"message": "Email verified successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Email not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except jwt.exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid token"}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/login")
async def login(user: models.UserInLogin):
    logged_user = db["User"].find_one({"email": user.email})
    if not logged_user:
        return JSONResponse(content={"message": "email is not registered"}, status_code=status.HTTP_401_UNAUTHORIZED)

    if not password_handler.verify_password(user.password, logged_user["password"]):
        return JSONResponse(content={"message": "wrong password"}, status_code=status.HTTP_401_UNAUTHORIZED)
    encoded_token = token_handler.encode_token(user.email)
    if not logged_user["is_verified"]:
        email_handler.send_email(logged_user["email"], encoded_token, EmailType.SIGNUP_VERIFICATION)
        return JSONResponse(content={"message": "email is not verified"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return models.UserOutLogin(**logged_user, token=encoded_token)


@router.post("/forgot-password")
async def forgot_password(email):
    logged_user = db["User"].find_one({"email": email})
    if not logged_user:
        return JSONResponse(content={"message": "Email is not found"}, status_code=status.HTTP_404_NOT_FOUND)
    encoded_token = token_handler.encode_token(email)
    email_handler.send_email(email, encoded_token, EmailType.FORGET_PASSWORD)
    return JSONResponse(content={"message": "Sent a verification email"}, status_code=status.HTTP_200_OK)


@router.get("/reset-password")
async def reset_password(token: str):
    try:
        email, expiration_time = token_handler.decode_token(token)
        if datetime.utcnow() > expiration_time:
            return JSONResponse(content={"message": "Token has expired"}, status_code=status.HTTP_400_BAD_REQUEST)
        logged_user = db["User"].find_one({"email": email})
        if not logged_user:
            return JSONResponse(content={"message": "Email not found"}, status_code=status.HTTP_404_NOT_FOUND)
        else:
            return RedirectResponse(url=f"/auth/change-password?token={token}")
    except jwt.exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid token"}, status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/change-password")
async def change_password(token: str, request: models.UserInForgotPassword):
    try:
        email, expiration_time = token_handler.decode_token(token)
        new_password = password_handler.get_password_hash(request.password)
        db["User"].update_one({"email": email}, {"$set": {"password": new_password}})
        return JSONResponse(content={"message": "Password updated successfully"}, status_code=status.HTTP_200_OK)
    except jwt.exceptions.DecodeError:
        return JSONResponse(content={"message": "Change password failed"}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/check-email")
async def check_email(email):
    logged_user = db["User"].find_one({"email": email})
    if not logged_user:
        return False
    return True
