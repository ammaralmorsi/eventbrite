import os
import re
from pymongo import MongoClient


class EventDriver:
    """
    EventDriver class provides methods to interact with an events collection in MongoDB.

    Attributes:
        client (MongoClient): MongoDB client instance.
        db (pymongo.database.Database): MongoDB database instance.
        collection (pymongo.collection.Collection): MongoDB collection instance.

    Methods:
        insert(data): Insert a document into the events collection.
        find(query): Find documents in the events collection based on a query.
        find_one(query): Find one document in the events collection based on a query.
        find_by_title(query): Find documents in the events collection based on a title query.
        find_by_category(query): Find documents in the events collection based on a category query.
        count(query): Count the number of documents in the events collection based on a query.
        delete(query): Delete a document from the events collection based on a query.
    """

    def __init__(self):
        """
        Initialize EventDriver instance with a MongoDB client, database, and collection.
        """
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client[os.environ.get("MONGO_DB")]
        self.collection = self.db['events']

    def insert(self, data):
        """
        Insert a document into the events collection.

        Args:
            data (dict): Data to be inserted as a document in the events collection.

        Returns:
            pymongo.results.InsertOneResult: Result of the insertion operation.
        """
        return self.collection.insert_one(data)

    def find(self, query):
        """
        Find documents in the events collection based on a query.

        Args:
            query (dict): Query to filter documents in the events collection.

        Returns:
            pymongo.cursor.Cursor: Cursor to iterate over the documents returned by the query.
        """
        return self.collection.find(query)

    def find_one(self, query):
        """
        Find one document in the events collection based on a query.

        Args:
            query (dict): Query to filter documents in the events collection.

        Returns:
            dict: Document that matches the query, or None if no document is found.
        """
        return self.collection.find_one(query)

    def find_by_title(self, query):
        """
        Find documents in the events collection based on a title query.

        Args:
            query (dict): Query containing the title to filter documents in the events collection.

        Returns:
            pymongo.cursor.Cursor: Cursor to iterate over the documents returned by the title query.
        """
        pattern = re.compile(".*{}.*".format(re.escape(query["title"])), re.IGNORECASE)
        query = {"basic_info.title": {"$regex": pattern}}
        return self.find(query)

    def find_by_category(self, query):
        """
        Find documents in the events collection based on a category query.

        Args:
            query (dict): Query containing the category to filter documents in the events collection.

        Returns:
            pymongo.cursor.Cursor: Cursor to iterate over the documents returned by the category query.
        """
        pattern = re.compile(".*{}.*".format(re.escape(query["category"])), re.IGNORECASE)
        query = {"basic_info.category": {"$regex": pattern}}
        return self.find(query)

    def count(self, query):
        """
        Count the number of documents in the events collection based on a query.

        Args:
            query (dict): Query to filter documents in the events collection.

        Returns:
            int: Number of documents that match the query.
        """
        return self.collection.count_documents(query)

    def delete(self, query):
        """
        Delete a document from the events collection based on a query.

        Args:
            query (dict): Query to identify the document to be deleted.

        Returns:
            pymongo.results.DeleteResult: Result of the deletion operation.
        """
        return self.collection.delete_one(query)

