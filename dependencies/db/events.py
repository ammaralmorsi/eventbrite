from fastapi import status
from fastapi import HTTPException

from pymongo import errors as mongo_errors

from dependencies.db.client import Client
import dependencies.models.events as models
from dependencies.utils.bson import convert_to_object_id


class EventDriver:
    def __init__(self):
        self.db = Client.get_instance().get_db()
        self.collection = self.db["events"]

    def handle_nonexistent_event(self, event_id: str):
        if not self.event_exists(event_id):
            raise HTTPException(detail="event not found", status_code=status.HTTP_404_NOT_FOUND)

    def event_exists(self, event_id: str) -> bool:
        event_id = convert_to_object_id(event_id)
        return self.collection.find_one({"_id": event_id}) is not None

    def create_new_event(self, event: models.EventDB) -> models.EventOut:
        try:
            inserted_id = self.collection.insert_one(event.dict()).inserted_id
            return models.EventOut(id=str(inserted_id), **event.dict())
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_event_by_id(self, event_id: str) -> models.EventOut:
        self.handle_nonexistent_event(event_id)
        try:
            event = self.collection.find_one({"_id": convert_to_object_id(event_id)})
            return models.EventOut(id=str(event["_id"]), **event)
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_event_by_id(self, event_id: str):
        self.handle_nonexistent_event(event_id)
        try:
            self.collection.delete_one({"_id": convert_to_object_id(event_id)})
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
