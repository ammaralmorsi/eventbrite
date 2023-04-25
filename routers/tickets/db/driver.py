import os
from pymongo import MongoClient
from bson.objectid import ObjectId

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

    def insert(self, event_id, tickets):
        """
        Inserts a document into the MongoDB collection.

        Args:
            event_id: The ID of the event to create tickets for.
            tickets: A list of tickets to be created.

        Returns:
            The result of the insertion operation.

        """
        # event = self.collection.find_one({"_id": event_id})

        return self.collection.update_one({"_id": event_id}, {"$set": {"tickets": tickets}})

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

    def update_tickets(self, event_id, tickets):
        return self.collection.update_one({"_id": ObjectId(event_id)}, {"$set": {"tickets": tickets}})
