from dependencies.models.attendees import Attendee, AttendeeOut
from dependencies.db.client import Client
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id
from fastapi import HTTPException
from fastapi import status

class AttendeeDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["attendees"]#Attendees collection

    def handle_nonexistent_attendee(self, attendee_id):
        """
        Handles the case when an attendee does not exist.

        This method checks if an attendee with the given attendee_id exists in the collection.
        If the attendee does not exist, it raises an HTTPException with a 404 Not Found status code.

        Args:
            self: The instance of the class.
            attendee_id (str): The ID of the attendee to check.

        Raises:
            HTTPException: If the attendee with the given attendee_id does not exist.

        """
        if not self.collection.find_one({"_id": convert_to_object_id(attendee_id)}):
            raise HTTPException(
                detail="attendee not found", status_code=status.HTTP_404_NOT_FOUND
            )

    def add_attendee(self, event_id:str, attendee: Attendee):
        """
        Adds an attendee to the collection.

        This method adds the provided attendee to the collection, assigning the specified event_id to the attendee.
        It then returns the newly added attendee as an AttendeeOut object.

        Args:
            self: The instance of the class.
            event_id (str): The ID of the event to which the attendee is being added.
            attendee (Attendee): The Attendee object representing the attendee to be added.

        Returns:
            AttendeeOut: The newly added attendee as an AttendeeOut object.

        """
        attendee.event_id = event_id
        inserted_id=self.collection.insert_one(attendee.dict()).inserted_id
        return AttendeeOut(id=str(inserted_id), **attendee.dict())

    def get_attendee(self, attendee_id):
        """
        Retrieves an attendee from the collection.

        This method retrieves an attendee from the collection based on the provided attendee_id.
        It returns the attendee as an AttendeeOut object.

        Args:
            self: The instance of the class.
            attendee_id (str): The ID of the attendee to retrieve.

        Returns:
            AttendeeOut: The retrieved attendee as an AttendeeOut object.

        """
        attendee = self.collection.find_one({"_id": convert_to_object_id(attendee_id)})
        return AttendeeOut(id=str(attendee["_id"]), **attendee)

    def get_attendees(self, event_id):
        """
        Retrieves attendees from the collection for a specific event.

        This method retrieves all attendees from the collection that belong to the specified event_id.
        It returns a list of AttendeeOut objects representing the retrieved attendees.

        Args:
            self: The instance of the class.
            event_id (str): The ID of the event for which attendees are being retrieved.

        Returns:
            list[AttendeeOut]: A list of AttendeeOut objects representing the retrieved attendees.

        """
        res = []
        for attendee in self.collection.find({"event_id": event_id}):
            res.append(AttendeeOut(id=str(attendee["_id"]), **attendee))
        return res

    def get_attendees_by_order_id(self, order_id):
        """
        Retrieves attendees from the collection based on the order ID.

        Args:
            order_id (str): The ID of the order associated with the attendees.

        Returns:
            list[AttendeeOut]: A list of AttendeeOut objects representing the retrieved attendees.
        """
        res = []
        for attendee in self.collection.find({"order_id": order_id}):
            res.append(AttendeeOut(id=str(attendee["_id"]), **attendee))
        return res

    def update_attendee(self, attendee_id,updated_attributes):
        """
        Updates an attendee with the specified attributes.

        Args:
            attendee_id (str): The ID of the attendee to update.
            updated_attributes (dict): A dictionary containing the updated attributes of the attendee.

        """
        self.collection.update_one(
            {"_id": convert_to_object_id(attendee_id)},
            {"$set": updated_attributes},
        )

    def delete_attendee(self, attendee_id):
        """
        Deletes an attendee from the collection.

        Args:
            attendee_id (str): The ID of the attendee to delete.

        """
        self.collection.delete_one({"_id": convert_to_object_id(attendee_id)})

    def attendees_count(self, order_id):
        """
        Counts the number of attendees for a specific order.

        Args:
            order_id (str): The ID of the order for which to count the attendees.

        Returns:
            int: The number of attendees for the specified order.

        """
        return self.collection.count_documents({"order_id": order_id})
