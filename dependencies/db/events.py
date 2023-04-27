from fastapi import status
from fastapi import HTTPException

from bson import ObjectId
from pymongo import errors as mongo_errors

from dependencies.db.client import Client
import dependencies.models.events as models


class EventDriver:
    def __init__(self):
        self.db = Client.get_instance().get_db()
        self.collection = self.db["events"]

    def create_new_event(self, event: models.EventDB) -> models.EventOut:
        try:
            inserted_id = self.collection.insert_one(event.dict()).inserted_id
            return models.EventOut(id=str(inserted_id), **event.dict())
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_event_by_id(self, event_id: str) -> models.EventOut:
        try:
            event = self.collection.find_one({"_id": ObjectId(event_id)})
            if event:
                return models.EventOut(id=str(event["_id"]), **event)
            else:
                raise HTTPException(detail="event not found", status_code=status.HTTP_404_NOT_FOUND)
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_event_by_id(self, event_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(event_id)})
            if result.deleted_count == 0:
                raise HTTPException(detail="event not found", status_code=status.HTTP_404_NOT_FOUND)
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
