import os

from fastapi import HTTPException
from fastapi import status

from pymongo import MongoClient
from pymongo import errors as mongo_errors

from .models import UserDB


class UsersDriver:
    def __init__(self):
        try:
            self.client = MongoClient(os.environ.get("MONGO_URI"))
            self.db = self.client[os.environ.get("MONGO_DB")]
            self.collection = self.db["users"]
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_user(self, user):
        try:
            inserted_id = self.collection.insert_one(UserDB(**user).dict()).inserted_id
            user.update({"_id": inserted_id})
            return user
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_is_verified(self, email):
        try:
            result = self.collection.update_one({"email": email}, {"$set": {"is_verified": True}})
            return result.matched_count == 1 or result.modified_count == 1
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def find_user(self, email):
        try:
            return self.collection.find_one({"email": email})
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def email_exists(self, email):
        try:
            return self.collection.find_one({"email": email}) is not None
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_password(self, email, password):
        try:
            return self.collection.update_one({"email": email}, {"$set": {"password": password}})
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
