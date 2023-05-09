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
        """
        Handles the case when an order does not exist.

        This method checks if an order with the given order_id exists in the collection.
        If the order does not exist, it raises an HTTPException with a 404 Not Found status code.

        Args:
            order_id (str): The ID of the order to check.

        Raises:
            HTTPException: If the order with the given order_id does not exist.

        """
        if not self.collection.find_one({"_id": convert_to_object_id(order_id)}):
            raise HTTPException(detail="order not found", status_code=status.HTTP_404_NOT_FOUND)

    def get_user_orders(self, user_id):
        """
        Retrieves orders for a specific user.

        This method retrieves all orders from the collection that belong to the specified user_id.
        It also calculates the count of attendees associated with each order using the AttendeeDriver's attendees_count method.
        The retrieved orders, along with their attendee counts, are returned as a list of OrderOut objects.

        Args:
            user_id (str): The ID of the user for which orders are being retrieved.

        Returns:
            list[OrderOut]: A list of OrderOut objects representing the retrieved orders with attendee counts.

        """
        res = []
        for order in self.collection.find({"user_id": user_id}):
            count = AttendeeDriver().attendees_count(str(order["_id"]))
            res.append(OrderOut(id=str(order["_id"]),tickets_count=count ,**order))
        return res

    def get_event_orders(self, event_id):
        """
        Retrieves orders for a specific event.

        This method retrieves all orders from the collection that belong to the specified event_id.
        It also calculates the count of attendees associated with each order using the AttendeeDriver's attendees_count method.
        The retrieved orders, along with their attendee counts, are returned as a list of OrderOut objects.

        Args:
            event_id (str): The ID of the event for which orders are being retrieved.

        Returns:
            list[OrderOut]: A list of OrderOut objects representing the retrieved orders with attendee counts.

        """
        res = []
        for order in self.collection.find({"event_id": event_id}):
            count = AttendeeDriver().attendees_count(str(order["_id"]))
            res.append(OrderOut(id=str(order["_id"]),tickets_count=count, **order))
        return res

    def get_order(self, order_id):
        """
        Retrieves an order by its ID.

        This method retrieves an order from the collection based on the provided order_id.
        It first checks if the order exists by calling the handle_nonexistent_order method.
        If the order exists, it calculates the count of attendees associated with the order using the AttendeeDriver's attendees_count method.
        The retrieved order, along with its attendee count, is returned as an OrderOut object.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            OrderOut: An OrderOut object representing the retrieved order with attendee count.

        """
        self.handle_nonexistent_order(order_id)
        count = AttendeeDriver().attendees_count(order_id)
        order= self.collection.find_one({"_id": convert_to_object_id(order_id)})
        return OrderOut(id=str(order["_id"]),tickets_count=count, **order)

    def add_order(self, event_id, order):
        """
        Adds an order to the collection.

        This method adds a new order to the collection with the provided event_id.
        It assigns the event_id to the order and inserts the order as a dictionary into the collection.
        After inserting the order, it calculates the count of attendees associated with the order using the AttendeeDriver's attendees_count method.
        The inserted order, along with its attendee count, is returned as an OrderOut object.

        Args:
            event_id (str): The ID of the event associated with the order.
            order (Order): The order to add to the collection.

        Returns:
            OrderOut: An OrderOut object representing the inserted order with attendee count.

        """
        order.event_id = event_id
        inserted_id=self.collection.insert_one(order.dict()).inserted_id
        count = AttendeeDriver().attendees_count(str(inserted_id))
        return OrderOut(id=str(inserted_id),tickets_count=count ,**order.dict())

    def edit_order(self, order_id, updated_attributes):
        """
        Edits an order with the specified updated attributes.

        This method updates an order in the collection based on the provided order_id.
        It uses the updated_attributes dictionary to update the corresponding fields of the order.
        The order is updated using the update_one method of the collection.

        Args:
            order_id (str): The ID of the order to edit.
            updated_attributes (dict): A dictionary containing the updated attributes of the order.

        """
        self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$set": updated_attributes})

    def delete_order(self, order_id):
        """
        Deletes an order from the collection.

        This method deletes an order from the collection based on the provided order_id.
        It uses the delete_one method of the collection to remove the order.

        Args:
            order_id (str): The ID of the order to delete.

        """
        self.collection.delete_one({"_id": convert_to_object_id(order_id)})

    # def upate_tickets_count(self, order_id, increment:int):
    #     order = self.collection.find_one({"_id": convert_to_object_id(order_id)})
    #     tickets_count = order["tickets_count"] + increment
    #     self.collection.update_one({"_id": convert_to_object_id(order_id)}, {"$set": {"tickets_count": tickets_count}})
