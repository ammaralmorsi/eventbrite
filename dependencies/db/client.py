import os

from pymongo import MongoClient
from pymongo import errors as mongo_errors

from fastapi import HTTPException
from fastapi import status


class Client:
    _instance = None

    def __init__(self):
        if not Client._instance:
            try:
                Client._instance = MongoClient(os.environ.get("MONGO_URI"))
                self.client = Client._instance
                self.db = self.client[os.environ.get("MONGO_DB")]
            except mongo_errors.PyMongoError:
                raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_db(self):
        return self.db
