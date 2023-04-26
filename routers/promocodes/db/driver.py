import os
from pymongo import MongoClient
from bson.objectid import ObjectId


class PromocodeDriver:
    """
    A class for handling CRUD operations related to promo codes in a MongoDB database.

    pgsql
    Copy
    ...

    Attributes
    ----------
    client : MongoClient
        The MongoClient instance created from the MONGO_URI environment variable
    db : Database
        The MongoDB database instance created from the MONGO_DB environment variable
    collection : Collection
        The MongoDB collection instance for the 'events' collection in the specified database

    Methods
    -------
    is_valid_event_id(event_id: str) -> bool:
        Checks if the provided event_id is valid by searching for the corresponding document in the 'events' collection.
        Returns True if the document exists, False otherwise.

    find_by_event_id(event_id: str) -> dict:
        Returns the document from the 'events' collection that matches the provided event_id.

    update_promocodes(event_id: str, promocodes: list) -> bool:
        Updates the 'promo_codes' field of the document in the 'events' collection that matches the provided event_id
        with the provided list of promo codes. Returns True if the update was successful, False otherwise.
    """

    def __init__(self):
        """
        Initializes a new instance of the PromoCodeDriver class.
        """
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client[os.environ.get("MONGO_DB")]
        self.collection = self.db['events']

    def is_valid_event_id(self, event_id: str):
        """
        Checks if the provided event_id is valid by searching for the corresponding document in the 'events' collection.
        Returns True if the document exists, False otherwise.

        Parameters
        ----------
        event_id : str
            The event ID to validate.

        Returns
        -------
        bool
            True if the document exists, False otherwise.
        """
        return self.collection.count_documents({"_id": ObjectId(event_id)})

    def find_by_event_id(self, event_id: str) -> dict:
        """
        Returns the document from the 'events' collection that matches the provided event_id.

        Parameters
        ----------
        event_id : str
            The event ID to search for.

        Returns
        -------
        dict
            The document from the 'events' collection that matches the provided event_id.
        """
        return self.collection.find_one({"_id": ObjectId(event_id)})

    def update_promocodes(self, event_id: str, promocodes: list):
        """
        Updates the 'promo_codes' field of the document in the 'events' collection that matches the provided event_id
        with the provided list of promo codes. Returns True if the update was successful, False otherwise.

        Parameters
        ----------
        event_id : str
            The event ID of the document to update.
        promocodes : list
            The list of promo codes to set as the value of the 'promo_codes' field.

        Returns
        -------
        bool
            True if the update was successful, False otherwise.
        """
        return self.collection.update_one({"_id": ObjectId(event_id)}, {"$set": {"promo_codes": promocodes}})
