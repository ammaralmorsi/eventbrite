import os

from pymongo import MongoClient

from .models import UserDB


class UsersDriver:
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client[os.environ.get("MONGO_DB")]
        self.collection = self.db["users"]

    def create_user(self, user: UserDB):
        inserted_id = self.collection.insert_one(user.dict()).inserted_id
        return user.dict().update({"_id": inserted_id})

    def set_is_verified(self, email):
        result = self.collection.update_one({"email": email}, {"$set": {"is_verified": True}})
        return result.modified_count == 1

    def find_user(self, email):
        return self.collection.find_one({"email": email})

    def email_exists(self, email):
        return self.collection.find_one({"email": email}) is None

    def update_password(self, email, password):
        return self.collection.update_one({"email": email}, {"$set": {"password": password}})
