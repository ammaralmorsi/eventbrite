"""
This module contains the API router for user authentication.
"""

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
import jwt

from .commons import is_unique
from .commons import get_password_hash
from .commons import verify_password
from .commons import send_email
from .commons import encode_token
from .commons import decode_token
from .db.models import User, LoginUser, ChangePasswordRequest
from .db.driver import get_db_conn


from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signup")
async def signup(user: User):
    """
    Register a new user with the given user object and sends a verification email.

    Args:
        user (User): A user object representing the user to register.

    Returns:
        JSONResponse: A JSON response containing a success message or an error message if the email is already registered.
    """
    db = get_db_conn()
    if not is_unique(user.email):
        return JSONResponse(content={"message": "email is already registered"}, status_code=status.HTTP_400_BAD_REQUEST)
    token = encode_token(user.email)
    send_email_value, body = send_email(user.email, token, 1)
    if send_email_value == -1:
        return JSONResponse(content={"message": body}, status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    db["User"].insert_one(user.dict())
    return JSONResponse(content={"message": "Please verify your email before your login"},
                        status_code=status.HTTP_200_OK)

@router.get("/verify")
async def verify_email(token: str):
    """
    Verify a user's email address with the given verification token.

    Args:
        token (str): A string containing the verification token to use.

    Returns:
        JSONResponse: A JSON response containing a success message if the email is verified successfully, or an error message if the token is invalid or has expired.
    """
    try:
        email, expiration_time = decode_token(token)
        if datetime.utcnow() > expiration_time:
            return JSONResponse(content={"message": "Token has expired"}, status_code=status.HTTP_400_BAD_REQUEST)
        db = get_db_conn()
        result = db["User"].update_one({"email": email}, {"$set": {"is_verified": True}})
        if result.modified_count == 1:
            return JSONResponse(content={"message": "Email verified successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Email not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except jwt.exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid token"}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/login")
async def login(user: LoginUser):
    """
    Authenticate a user with the given login credentials and return an access token.

    Args:
        user (LoginUser): A login user object containing the email and password to authenticate.

    Returns:
        JSONResponse: A JSON response containing an access token or an error message if the credentials are invalid or the email is not verified.
    """
    if user.email == "" or user.password == "":
        return JSONResponse(content={"message": "please, provide both email and password"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    db = get_db_conn()
    logged_user = db["User"].find_one({"email": user.email})
    if not logged_user:
        return JSONResponse(content={"message": "email is not registered"}, status_code=status.HTTP_401_UNAUTHORIZED)

    if not verify_password(user.password, logged_user["password"]):
        return JSONResponse(content={"message": "wrong password"}, status_code=status.HTTP_401_UNAUTHORIZED)
    encoded_token = encode_token(user.email)
    if not logged_user["is_verified"]:
        send_email(logged_user["email"], encoded_token, 1)
        return JSONResponse(content={"message": "email is not verified"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return JSONResponse(content={"token": encoded_token, "email": logged_user["email"],
                                 "firstname": logged_user["firstname"], "lastname": logged_user["lastname"],
                                 "avatar": logged_user["avatar_url"]}, status_code=status.HTTP_200_OK)


@router.get("/forgot-password")
async def forgot_password(email):
    """
    Sends a forgot password email to the given email address.

    Args:
        email (str): A string containing the email address to send the forgot password email to.

    Returns:
        JSONResponse: A JSON response containing a success message or an error message if the email is not found.
    """
    if email == "":
        return JSONResponse(content={"message": "please, provide both email and password"}, status_code=status.HTTP_400_BAD_REQUEST)
    db = get_db_conn()
    logged_user = db["User"].find_one({"email": email})
    if not logged_user:
        return JSONResponse(content={"message": "Email is not found"}, status_code=status.HTTP_404_NOT_FOUND)
    encoded_token = encode_token(email)
    send_email(email, encoded_token, 2)
    return JSONResponse(content={"message": "Sent a verification email"}, status_code=status.HTTP_200_OK)


@router.get("/reset-password")
async def reset_password(token: str):
    """
    Verify a user's reset password token and redirect to the change password page.

    Args:
        token (str): A string containing the reset password token to use.

    Returns:
        RedirectResponse or JSONResponse: A redirect response to the change password page if the token is valid, or a JSON response containing an error message if the token is invalid or has expired.
    """
    try:
        email, expiration_time = decode_token(token)
        if datetime.utcnow() > expiration_time:
            return JSONResponse(content={"message": "Token has expired"}, status_code=status.HTTP_400_BAD_REQUEST)
        db = get_db_conn()
        logged_user = db["User"].find_one({"email": email})
        if not logged_user:
            return JSONResponse(content={"message": "Email not found"}, status_code=status.HTTP_404_NOT_FOUND)
        else:
            return RedirectResponse(url=f"/auth/change-password?token={token}")
    except jwt.exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid token"}, status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/change-password")
async def change_password(token: str, request: ChangePasswordRequest):
    """
    Update a user's password with the given reset password token and new password.

    Args:
        token (str): A string containing the reset password token to use.
        request (ChangePasswordRequest): A change password request object containing the new password to use.

    Returns:
        JSONResponse: A JSON response containing a success message or an error message if the token is invalid or has expired.
    """
    try:
        email, expiration_time = decode_token(token)
        if datetime.utcnow() > expiration_time:
            return JSONResponse(content={"message": "Token has expired"}, status_code=status.HTTP_400_BAD_REQUEST)
        db = get_db_conn()
        logged_user = db["User"].find_one({"email": email})
        if not logged_user:
            return JSONResponse(content={"message": "Email not found"}, status_code=status.HTTP_404_NOT_FOUND)
        # update user password in database
        new_password = get_password_hash(request.new_password)
        db["User"].update_one({"email": email}, {"$set": {"password": new_password}})
        # return success message
        return JSONResponse(content={"message": "Password updated successfully"}, status_code=status.HTTP_200_OK)
    except jwt.exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid token"}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/check-email")
async def check_email(email):
    db = get_db_conn()
    logged_user = db["User"].find_one({"email": email})
    if not logged_user:
        return False
    return True
