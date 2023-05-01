from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from fastapi import status

from pymongo import errors as mongo_errors

from dependencies.models import users
from dependencies.db.client import Client


class UsersDriver:
    def __init__(self):
        self.db = Client.get_instance().get_db()
        self.collection = self.db["users"]

    def create_user(self, user: users.UserInSignup) -> users.UserOut:
        try:
            user_db = users.UserDB(last_password_update=datetime.utcnow(), **user.dict())
            inserted_id = self.collection.insert_one(user_db.dict()).inserted_id
            user_out = users.UserOut(**user_db.dict(), id=str(inserted_id))
            return user_out
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_is_verified(self, email):
        try:
            result = self.collection.update_one({"email": email}, {"$set": {"is_verified": True}})
            return result.matched_count == 1 or result.modified_count == 1
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_by_email(self, email) -> users.UserOut:
        try:
            user = self.collection.find_one({"email": email})
            return users.UserOut(**user, id=str(user["_id"]))
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def email_exists(self, email):
        try:
            return self.collection.find_one({"email": email}) is not None
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_password(self, email, password):
        try:
            return self.collection.update_one(
                {"email": email}, {"$set": {"password": password, "last_password_update": datetime.utcnow()}}
            )
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_by_id(self, user_id):
        try:
            try:
                user_id = ObjectId(user_id)
            except TypeError or InvalidId:
                raise HTTPException(detail="invalid user id", status_code=status.HTTP_400_BAD_REQUEST)
            return self.collection.find_one({"_id": ObjectId(user_id)})
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_last_password_update_time(self, user_id: str):
        try:
            try:
                user_id = ObjectId(user_id)
            except TypeError or InvalidId:
                raise HTTPException(detail="invalid user id", status_code=status.HTTP_400_BAD_REQUEST)
            return self.collection.find_one({"_id": ObjectId(user_id)})["last_password_update"]
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)