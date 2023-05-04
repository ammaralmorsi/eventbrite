from dependencies.models.attendees import Attendees, AttendeesOut
from dependencies.db.client import Client
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id


class AttendeesDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["attendees"]

    def add_attendee(self, event_id, attendee):
        attendee["event_id"] = event_id
        self.collection.insert_one(attendee)

    def get_attendees(self, event_id):
        res = []
        for attendee in self.collection.find({"event_id": event_id}):
            res.append(attendee)
        return res

    def get_attendees_by_order_id(self, order_id):
        res = []
        for attendee in self.collection.find({"order_id": order_id}):
            res.append(attendee)
        return res
