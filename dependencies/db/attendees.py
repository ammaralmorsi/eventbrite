from dependencies.models.attendees import Attendee, AttendeeOut
from dependencies.db.client import Client
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id
from fastapi import HTTPException
from fastapi import status

class AttendeeDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["Attendees"]

    def handle_nonexistent_attendee(self, attendee_id):
        if not self.collection.find_one({"_id": convert_to_object_id(attendee_id)}):
            raise HTTPException(
                detail="attendee not found", status_code=status.HTTP_404_NOT_FOUND
            )

    def add_attendee(self, event_id:str, attendee: Attendee):
        attendee["event_id"] = event_id
        self.collection.insert_one(attendee)

    def get_Attendees(self, event_id):
        res = []
        for attendee in self.collection.find({"event_id": event_id}):
            res.append(attendee)
        return res

    def get_Attendees_by_order_id(self, order_id):
        res = []
        for attendee in self.collection.find({"order_id": order_id}):
            res.append(attendee)
        return res

    def update_attendee(self, attendee_id,updated_attributes):
        self.collection.update_one(
            {"_id": convert_to_object_id(attendee_id)},
            {"$set": updated_attributes},
        )

    def delete_attendee(self, attendee_id):
        self.collection.delete_one({"_id": convert_to_object_id(attendee_id)})
