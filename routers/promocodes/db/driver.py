import os
from pymongo import MongoClient


class PromocodeDriver:
    """
    A class for handling CRUD operations related to promo codes in a MongoDB database.
    """

    def __init__(self):
        """
        Initializes a new instance of the PromoCodeDriver class.
        """
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client[os.environ.get("MONGO_DB")]
        self.collection = self.db['events']

    def insert(self, event_id, promo_codes):
        """
        Inserts a document into the MongoDB collection.
        Args:
            event_id: The ID of the event to create promo codes for.
            promo_codes: A list of promo codes to be created.
        Returns:
            The result of the insertion operation.
        """
        return self.collection.insert_one({"_id": event_id, "promo_codes": promo_codes})

    def find_by_event_id(self, query):
        """
        Finds a document in the MongoDB collection by a given query.
        Args:
            query: A dictionary containing the query criteria.
        Returns:
            The document that matches the query criteria, or None if no match is found.
        """
        return self.collection.find(query)

    def count(self, query):
        """
        Counts the number of documents in the MongoDB collection that match a given query.
        Args:
            query: A dictionary containing the query criteria.
        Returns:
            The number of documents that match the query criteria.
        """
        return self.collection.count_documents(query)

    def update_by_event_id(self, query, data):
        """
        Updates a document in the MongoDB collection.
        Args:
            query: A dictionary containing the query criteria.
            data: A dictionary containing the data to be updated.
        Returns:
            The result of the update operation.
        """
        return self.collection.update_many(query, {"$set": data})

    def delete_by_event_id(self, query):
        """
        Deletes a document in the MongoDB collection.
        Args:
            query: A dictionary containing the query criteria.
        Returns:
            The result of the delete operation.
        """
        return self.collection.delete_many(query)

    def delete_by_event_id_and_promocode_id(self, query, data):
        """
        Deletes a document in the MongoDB collection.
        Args:
            query: A dictionary containing the query criteria.
        Returns:
            The result of the delete operation.
        """
        return self.collection.delete_one(query, {"$set": data})

    def delete(self, query):
        """
        Deletes a document in the MongoDB collection.
        Args:
            query: A dictionary containing the query criteria.
        Returns:
            The result of the delete operation.
        """
        return self.collection.delete_many(query)

