from dependencies.models.orders import Order, OrderOut,OrderDB
from dependencies.db.client import Client
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id
from fastapi import HTTPException
from fastapi import status


class OrderDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["orders"]

    def handle_nonexistent_order(self, order_id:str):
        if not self.collection.find_one({"_id": convert_to_object_id(order_id)}):
            raise HTTPException(detail="order not found", status_code=status.HTTP_404_NOT_FOUND)

    def upate_tickets_count(self, order_id, increment:int):
        order = self.collection.find_one({"_id": convert_to_object_id(order_id)})
        tickets_count = order["tickets_count"] + increment
        self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$set": {"tickets_count": tickets_count}})

    def get_user_orders(self, user_id:str):
        res = []
        for order in self.collection.find({"user_id": user_id}):
            res.append(OrderOut(id=str(order["_id"]), **order))
        return res

    def get_event_orders(self, event_id:str):
        res = []
        for order in self.collection.find({"event_id": event_id}):
            res.append(OrderOut(id=str(order["_id"]), **order))
        return res

    def add_order(self, event_id:str, order:Order):
        order.event_id = event_id
        order_db = OrderDB(**order.dict())
        order_db.tickets_count = len(order.attendees)
        self.collection.insert_one(order_db.dict())

    def edit_order(self, order_id:str, updated_attributes: dict):
        self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$set": updated_attributes})
        order = self.collection.find_one({"_id": convert_to_object_id(order_id)})

        self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$set": {"tickets_count": len(order["attendees"])}})

    def delete_order(self, order_id:str):
        self.collection.delete_one({"_id": convert_to_object_id(order_id)})
