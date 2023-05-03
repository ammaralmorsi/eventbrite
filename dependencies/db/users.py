from datetime import datetime

from fastapi import HTTPException
from fastapi import status

from pymongo import errors as mongo_errors

from dependencies.models import users
from dependencies.db.client import Client
from dependencies.utils.bson import convert_to_object_id


class UsersDriver:
    def __init__(self):
        self.db = Client.get_instance().get_db()
        self.collection = self.db["users"]

    def handle_existing_email(self, email: str):
        if self.email_exists(email):
            raise HTTPException(detail="email already exists", status_code=status.HTTP_400_BAD_REQUEST)

    def handle_nonexistent_email(self, email: str):
        if not self.email_exists(email):
            raise HTTPException(detail="email not found", status_code=status.HTTP_404_NOT_FOUND)

    def handle_existing_user(self, user_id: str):
        if self.user_exists(user_id):
            raise HTTPException(detail="user already exists", status_code=status.HTTP_400_BAD_REQUEST)

    def handle_nonexistent_user(self, user_id: str):
        if not self.user_exists(user_id):
            raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)

    def user_exists(self, user_id: str) -> bool:
        user_id = convert_to_object_id(user_id)
        return self.collection.find_one({"_id": user_id}) is not None

    def create_user(self, user: users.UserInSignup) -> users.UserOut:
        try:
            user_db = users.UserDB(last_password_update=datetime.utcnow(), **user.dict())
            inserted_id = self.collection.insert_one(user_db.dict()).inserted_id
            user_out = users.UserOut(**user_db.dict(), id=str(inserted_id))
            return user_out
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_is_verified(self, email: str):
        try:
            result = self.collection.update_one({"email": email}, {"$set": {"is_verified": True}})
            return result.matched_count == 1 or result.modified_count == 1
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_by_email(self, email: str) -> users.UserOut:
        try:
            user = self.collection.find_one({"email": email})
            return users.UserOut(**user, id=str(user["_id"]))
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def email_exists(self, email: str):
        try:
            return self.collection.find_one({"email": email}) is not None
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_password(self, email: str, password: str):
        try:
            return self.collection.update_one(
                {"email": email}, {"$set": {"password": password, "last_password_update": datetime.utcnow()}}
            )
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_by_id(self, user_id: str) -> users.UserInfo:
        self.handle_nonexistent_user(user_id)
        try:
            return users.UserInfo(**self.collection.find_one({"_id": convert_to_object_id(user_id)}))
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_last_password_update_time(self, user_id: str) -> datetime:
        self.handle_nonexistent_user(user_id)
        try:
            return self.collection.find_one({"_id": convert_to_object_id(user_id)})["last_password_update"]
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
