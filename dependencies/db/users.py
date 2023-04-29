from bson import ObjectId
from fastapi import HTTPException
from fastapi import status

from pymongo import errors as mongo_errors

from dependencies.models.users import UserDB
from dependencies.db.client import Client


class UsersDriver:
    def __init__(self):
        self.db = Client.get_instance().get_db()
        self.collection = self.db["users"]

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

    def get_user_by_id(self, user_id):
        try:
            id_as_ObjectId = ObjectId(user_id)
            return self.collection.find_one({"_id": id_as_ObjectId})
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)