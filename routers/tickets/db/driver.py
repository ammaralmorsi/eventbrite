import os
from pymongo import MongoClient


class TicketDriver:
    """
    A class for handling CRUD operations related to tickets in a MongoDB database.

    """
    def __init__(self):
        """
        Initializes a new instance of the TicketDriver class.

        """
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client[os.environ.get("MONGO_DB")]
        self.collection = self.db['events']

    def find_by_event_id(self, query):
        """
        Finds a document in the MongoDB collection by a given query.

        Args:
            query: A dictionary containing the query criteria.

        Returns:
            The document that matches the query criteria, or None if no match is found.

        """
        return self.collection.find_one(query)

    def count(self, query):
        """
        Counts the number of documents in the MongoDB collection that match a given query.

        Args:
            query: A dictionary containing the query criteria.

        Returns:
            The number of documents that match the query criteria.

        """
        return self.collection.count_documents(query)

    def update_tickets(self, query, data):
        """
        Updates the tickets for a given event ID in the MongoDB collection.

        Args:
            query: A dictionary containing the query criteria for the event ID.
            data: A dictionary containing the update data for the tickets.

        Returns:
            An instance of the UpdateResult class that contains information about the update operation.

        """
        return self.collection.update_one(query, data)
    