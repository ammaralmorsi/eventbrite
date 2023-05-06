from dependencies.models.orders import Order, OrderOut,OrderDB, Attendee
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

    def get_attendees(self, order_id:str):
        order = self.collection.find_one({"_id": convert_to_object_id(order_id)})
        return order["attendees"]

    def get_order(self, order_id:str):
        order = self.collection.find_one({"_id": convert_to_object_id(order_id)})
        return OrderOut(id=str(order["_id"]), **order)

    def handle_nonexistent_attendee(self, order_id:str, attendee_id:str):
        order = self.collection.find_one({"_id": convert_to_object_id(order_id)})
        attendees = order["attendees"]
        for attendee in attendees:
            if attendee["attendee_id"] == attendee_id:
                return
        raise HTTPException(detail="attendee not found", status_code=status.HTTP_404_NOT_FOUND)

    def add_attendee(self, order_id:str, attendee:Attendee):
        self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$push": {"attendees": attendee.dict()}})
        self.upate_tickets_count(order_id, 1)

    # def add_attendee2(self, order_id:str, attendee:dict):#attendee:Attendee please change it
    #     self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$push": {"attendees": attendee}})
    #     self.upate_tickets_count(order_id, 1)

    def delete_attendee(self, order_id:str, attendee_id:str):
        self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$pull": {"attendees": {"attendee_id": attendee_id}}})
        self.upate_tickets_count(order_id, -1)

    def edit_attendee(self, order_id:str, attendee_id:str, updated_attributes:dict):
        self.collection.update_one({"_id": convert_to_object_id(order_id), "attendees.attendee_id": attendee_id}, {"$set": {"attendees.$": updated_attributes}})
