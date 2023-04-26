import os
from pymongo import MongoClient
from bson.objectid import ObjectId


class TicketDriver:
    """
    The TicketDriver class provides methods to interact with a MongoDB database.
    It is specifically designed to interact with an 'events' collection, and provides
    methods to retrieve and update event documents by their ObjectId.

    sql_more
    Copy
    Attributes:
        client (MongoClient): MongoClient object used to connect to the MongoDB instance
        db (str): Name of the MongoDB database to use
        collection (Collection): Collection object representing the 'events' collection in the MongoDB database
    """
    def __init__(self):
        """
        Initializes a new TicketDriver object by connecting to the MongoDB instance
        specified in the MONGO_URI environmental variable, and setting the 'db' and 'collection'
        attributes to the values specified in the MONGO_DB and 'events' strings, respectively.
        """
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client[os.environ.get("MONGO_DB")]
        self.collection = self.db['events']

    def find_by_event_id(self, event_id):
        """
        Finds and returns an event document from the 'events' collection by its ObjectId.

        Args:
            event_id (str): The ObjectId of the event document to retrieve

        Returns:
            dict: The event document matching the specified ObjectId, or None if no document was found.
        """
        return self.collection.find_one({"_id": ObjectId(event_id)})

    def is_valid_event_id(self, event_id):
        """
        Checks if an event with the specified ObjectId exists in the 'events' collection.

        Args:
            event_id (str): The ObjectId of the event to check for existence

        Returns:
            bool: True if an event with the specified ObjectId exists in the 'events' collection, False otherwise.
        """
        return self.collection.count_documents({"_id": ObjectId(event_id)})

    def update_tickets(self, event_id, tickets):
        """
        Updates the 'tickets' field of an event document with the specified ObjectId.

        Args:
            event_id (str): The ObjectId of the event document to update
            tickets (list): The new list of tickets to set for the event document

        Returns:
            pymongo.results.UpdateResult: The result of the update operation, and the number of documents modified.
        """
        return self.collection.update_one({"_id": ObjectId(event_id)}, {"$set": {"tickets": tickets}})
