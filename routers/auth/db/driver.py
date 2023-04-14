from pymongo import MongoClient
import os

def get_db_conn():
    """
    Returns a connection to the EventBrite MongoDB database.

    Returns:
        pymongo.MongoClient: A MongoClient object representing the database connection.
    """
    client = MongoClient(os.environ.get("MONGO_URI"))
    db = client[os.environ.get("MONGO_DB")]
    return db


