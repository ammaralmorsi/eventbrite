from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from .commons import is_unique, get_password_hash, verify_password, send_verification_email,send_forgot_password_email, encode_token, decode_token
import jwt
from .db_settings import get_db_conn, User, LoginUser
from datetime import datetime

router = APIRouter(prefix="/auth")


@router.post("/signup")
async def signup(user: User):
    db = get_db_conn()
    if not is_unique(user.email):
        return JSONResponse(content={"message": "email is already registered"}, status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user.is_verified = False  # Set is_verified flag to False
    db["User"].insert_one(user.dict())
    token = encode_token(user.email)
    send_verification_email(user.email, token)
    return JSONResponse(content={"message": "Please verify your email before logging in"},
                        status_code=status.HTTP_200_OK)


@router.get("/verify")
async def verify_email(token: str):
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
    return JSONResponse(content={"token": encoded_token}, status_code=status.HTTP_200_OK)


# @router.post("/forgot-password")
# async def forgot_password(email):
#     if email == "":
#         return JSONResponse(content={"message": "please, provide both email and password"}, status_code=status.HTTP_400_BAD_REQUEST)
#     db = get_db_conn()
#     logged_user = db["User"].find_one({"email": email})
#     if not logged_user:
#         return JSONResponse(content={"message": "Email is not found"}, status_code=status.HTTP_404_NOT_FOUND)
#     send_forgot_password_email(email)
#
# @router.get("/reset-password")
# async def reset_password(token: str):
#     try:
#         email, expiration_time = decode_token(token)
#         if datetime.utcnow() > expiration_time:
#             return JSONResponse(content={"message": "Token has expired"}, status_code=status.HTTP_400_BAD_REQUEST)
#         db = get_db_conn()
#         result = db["User"].update_one({"email": email}, {"$set": {"is_verified": True}})
#         if result.modified_count == 1:
#             return JSONResponse(content={"message": "Email verified successfully"}, status_code=status.HTTP_200_OK)
#         else:
#             return JSONResponse(content={"message": "Email not found"}, status_code=status.HTTP_404_NOT_FOUND)
#     except jwt.exceptions.DecodeError:
#         return JSONResponse(content={"message": "Invalid token"}, status_code=status.HTTP_400_BAD_REQUEST)
