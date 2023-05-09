from dependencies.models.orders import Order, OrderOut
#import attendeedriver
from dependencies.db.attendees import AttendeeDriver
from dependencies.db.client import Client
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id
from fastapi import HTTPException
from fastapi import status


class OrderDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["orders"]
        # self.atteendee_collection = self.db["attendees"]

    def handle_nonexistent_order(self, order_id:str):
        if not self.collection.find_one({"_id": convert_to_object_id(order_id)}):
            raise HTTPException(detail="order not found", status_code=status.HTTP_404_NOT_FOUND)

    def get_user_orders(self, user_id):
        res = []
        for order in self.collection.find({"user_id": user_id}):
            count = AttendeeDriver().attendees_count(str(order["_id"]))
            res.append(OrderOut(id=str(order["_id"]),tickets_count=count ,**order))
        return res

    def get_event_orders(self, event_id):
        res = []
        for order in self.collection.find({"event_id": event_id}):
            count = AttendeeDriver().attendees_count(str(order["_id"]))
            res.append(OrderOut(id=str(order["_id"]),tickets_count=count, **order))
        return res

    def get_order(self, order_id):
        self.handle_nonexistent_order(order_id)
        count = AttendeeDriver().attendees_count(order_id)
        order= self.collection.find_one({"_id": convert_to_object_id(order_id)})
        return OrderOut(id=str(order["_id"]),tickets_count=count, **order)

    def add_order(self, event_id, order):
        order.event_id = event_id
        inserted_id=self.collection.insert_one(order.dict()).inserted_id
        count = AttendeeDriver().attendees_count(str(inserted_id))
        return OrderOut(id=str(inserted_id),tickets_count=count ,**order.dict())

    def edit_order(self, order_id, updated_attributes):
        self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$set": updated_attributes})

    def delete_order(self, order_id):
        self.collection.delete_one({"_id": convert_to_object_id(order_id)})

    # def upate_tickets_count(self, order_id, increment:int):
    #     order = self.collection.find_one({"_id": convert_to_object_id(order_id)})
    #     tickets_count = order["tickets_count"] + increment
    #     self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$set": {"tickets_count": tickets_count}})
