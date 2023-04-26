import os
from pymongo import MongoClient
from bson.objectid import ObjectId


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

    def is_valid_event_id(self, event_id):
        return self.collection.count_documents({"_id": ObjectId(event_id)})

    def find_by_event_id(self, event_id):
        return self.collection.find_one({"_id": ObjectId(event_id)})

    def update_promocodes(self, event_id, promocodes):
        return self.collection.update_one({"_id": ObjectId(event_id)}, {"$set": {"promo_codes": promocodes}})
