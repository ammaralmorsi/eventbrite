import datetime
import re
from typing import Optional

from fastapi import status
from fastapi import HTTPException

from pymongo import errors as mongo_errors

from dependencies.db.client import Client
import dependencies.models.events as models
from dependencies.db.tickets import TicketDriver
from dependencies.utils.bson import convert_to_object_id


class EventDriver:
    def __init__(self):
        self.db = Client.get_instance().get_db()
        self.collection = self.db["events"]
        self.tickets_driver = TicketDriver()

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

    def search_events(
            self,
            city: str,
            online: Optional[bool] = None,
            free: Optional[bool] = None,
            title: Optional[str] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            category: Optional[str] = None,
    ) -> list[models.EventOut]:
        def get_pattern(str_in: str):
            return re.compile(".*{}.*".format(re.escape(str_in)), re.IGNORECASE)

        try:
            city_pattern = get_pattern(city)
            query = {
                "state.is_public": True,
                "location.city": {"$regex": city_pattern},
            }

            if online is not None:
                query["location.is_online"] = online

            if title is not None:
                title_pattern = get_pattern(title)
                query["basic_info.title"] = {"$regex": title_pattern}

            if start_date is not None:
                inner_start_date = start_date
            else:
                inner_start_date = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)

            if end_date is not None:
                inner_end_date = end_date
            else:
                inner_end_date = datetime.datetime(3000, 1, 1, 0, 0, 0, 0)

            query["date_and_time.start_date_time"] = {"$gte": inner_start_date, "$lte": inner_end_date}

            if category is not None:
                category_pattern = get_pattern(category)
                query["basic_info.category"] = {"$regex": category_pattern}

            events_out = [models.EventOut(id=str(event["_id"]), **event) for event in self.collection.find(query)]

            if free is not None:
                events_out = [event for event in events_out if self.tickets_driver.is_free_event(event.id) == free]
            return events_out

        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
