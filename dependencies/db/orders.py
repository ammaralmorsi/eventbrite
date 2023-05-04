from dependencies.models.orders import Order, OrderOut
from dependencies.db.client import Client
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id


class OrderDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["orders"]

    def get_user_orders(self, user_id):
        res = []
        for order in self.collection.find({"user_id": user_id}):
            res.append(order)
        return res

    def get_event_orders(self, event_id):
        res = []
        for order in self.collection.find({"event_id": event_id}):
            res.append(order)
        return res

