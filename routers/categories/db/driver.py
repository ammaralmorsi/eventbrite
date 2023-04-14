import re
import os

from pymongo import MongoClient


class CategoriesDriver:
    """
    A class for interacting with a MongoDB collection that stores categories data.

    Attributes:
        client (MongoClient): The MongoDB client instance.
        db (MongoDatabase): The MongoDB database instance.
        collection (MongoCollection): The MongoDB collection instance for 'categories'.
    """

    def __init__(self):
        """
        Initializes a new instance of the CategoriesDriver class.

        The constructor connects to the MongoDB server using the MONGO_URI environment
        variable, selects the specified database using the MONGO_DB environment variable,
        and initializes the MongoDB collection instance for 'categories'.
        """
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client[os.environ.get("MONGO_DB")]
        self.collection = self.db['categories']

    def insert(self, data):
        """
        Inserts a single document into the 'categories' collection.

        Args:
            data (dict): The document to be inserted as a dictionary.

        Returns:
            None
        """
        self.collection.insert_one(data)

    def find_all(self):
        """
        Retrieves all documents from the 'categories' collection.

        Returns:
            cursor: A cursor to the result of the find operation.
        """
        return self.collection.find()

    def find(self, query):
        """
        Retrieves documents from the 'categories' collection that match a given query.

        Args:
            query (dict): A dictionary containing the query criteria.
                The dictionary should have a 'name' key with the value to be matched as
                a regular expression pattern.

        Returns:
            cursor: A cursor to the result of the find operation.
        """
        pattern = re.compile(".*{}.*".format(re.escape(query["name"])), re.IGNORECASE)
        query = {"name": {"$regex": pattern}}
        return self.collection.find(query)

    def count(self, query):
        """
        Returns the count of documents in the 'categories' collection that match a given query.

        Args:
            query (dict): A dictionary containing the query criteria.
                The dictionary should have a 'name' key with the value to be matched as
                a regular expression pattern.

        Returns:
            int: The count of documents that match the query.
        """
        pattern = re.compile(".*{}.*".format(re.escape(query["name"])), re.IGNORECASE)
        query = {"name": {"$regex": pattern}}
        return self.collection.count_documents(query)
