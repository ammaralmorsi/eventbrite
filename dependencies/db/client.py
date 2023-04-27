import os

from pymongo import MongoClient
from pymongo import errors as mongo_errors

from fastapi import HTTPException
from fastapi import status


class Client:
    _instance = None

    @staticmethod
    def get_instance():
        if not Client._instance:
            Client()
        return Client._instance

    def __init__(self):
        if not Client._instance:
            try:
                Client._instance = self
                self.client = MongoClient(os.environ.get("MONGO_URI"))
                self.db = self.client[os.environ.get("MONGO_DB")]
            except mongo_errors.PyMongoError:
                raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_db(self):
        return self.db
