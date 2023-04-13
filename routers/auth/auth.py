from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from .db_settings import get_db_conn, User, is_unique, get_password_hash, send_verification

router = APIRouter()
@router.post("/signup")
async def signup(user: User):
    db = get_db_conn()
    if not is_unique(user.email):
        return {"message": "email is already signed"}
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    db["User"].insert_one(user.dict())
    send_verification(user)
    raise HTTPException(status_code=200, detail="user signed up successfully")

