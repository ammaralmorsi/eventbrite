import os

from pymongo import MongoClient
from pymongo import errors as mongo_errors

from fastapi import HTTPException
from fastapi import status


class Client:
    """
    A class for connecting to a MongoDB database.

    This class provides a single instance of the database connection that can be accessed by calling the
    `get_instance()` method.
    """

    _instance = None

    @staticmethod
    def get_instance():
        """
        Returns the single instance of the `Client` class that connects to the MongoDB database.

        If an instance does not yet exist, this method creates one.

        Returns:
            Client: The `Client` instance used to connect to the database.
        """
        if not Client._instance:
            Client()
        return Client._instance

    def __init__(self):
        """
        Initializes the `Client` instance by connecting to the MongoDB database.

        Raises:
            HTTPException: If there is an error connecting to the database.
        """
        if not Client._instance:
            try:
                Client._instance = self
                self.client = MongoClient(os.environ.get("MONGO_URI"))
                self.db = self.client[os.environ.get("MONGO_DB")]
            except mongo_errors.PyMongoError:
                raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_db(self):
        """
        Returns the MongoDB database instance.

        Returns:
            Database: The `Database` instance used to interact with the MongoDB database.
        """
        return self.db
