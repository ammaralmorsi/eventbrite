from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from .db_settings import get_db_conn, User, is_unique, get_password_hash, send_verification_email
import jwt
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/signup")
async def signup(user: User):
    db = get_db_conn()
    if not is_unique(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is already registered")
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user.is_verified = False # Set is_verified flag to False
    db["User"].insert_one(user.dict())
    send_verification_email(user.email, jwt.encode({"email": user.email, "exp": datetime.utcnow() + timedelta(hours=1)}, "secret_key", algorithm="HS256"))
    return JSONResponse(content={"message": "Please verify your email before logging in"}, status_code=status.HTTP_200_OK)

@router.get("/verify")
async def verify_email(token: str):
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        email = payload["email"]
        expiration_time = datetime.fromtimestamp(payload["exp"])
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

