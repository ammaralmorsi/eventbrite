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
    """
    This class provides methods for interacting with the events collection in MongoDB.
    """

    def __init__(self):
        """
        Initializes the EventDriver instance.
        """
        self.db = Client.get_instance().get_db()
        self.collection = self.db["events"]
        self.tickets_driver = TicketDriver()

    def handle_nonexistent_event(self, event_id: str):
        """
        Handles the case where an event with the given ID does not exist in the database.

        Parameters:
            - event_id (str): The ID of the event to check.

        Raises:
            - HTTPException: If the event does not exist, raises a 404 error with the message "event not found".
        """
        if not self.event_exists(event_id):
            raise HTTPException(detail="event not found", status_code=status.HTTP_404_NOT_FOUND)

    def event_exists(self, event_id: str) -> bool:
        """
        Checks whether an event with the given ID exists in the database.

        Parameters:
            - event_id (str): The ID of the event to check.

        Returns:
            - bool: True if an event with the given ID exists in the database, False otherwise.
        """
        event_id = convert_to_object_id(event_id)
        return self.collection.find_one({"_id": event_id}) is not None

    def create_new_event(self, event: models.EventDB):
        """
        Inserts a new event into the database.

        Parameters:
            - event (models.EventDB): The event object to insert into the database.

        Returns:
            - str: The ID of the newly inserted event.

        Raises:
            - HTTPException: If there is an error inserting the event into the database, raises a 500 error with the message "database error".
        """
        try:
            return str(self.collection.insert_one(event.dict()).inserted_id)
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_event_by_id(self, event_id: str) -> models.EventOut:
        """
        Retrieves an event from the database by its ID.

        Parameters:
            - event_id (str): The ID of the event to retrieve.

        Returns:
            - models.EventOut: An object representing the retrieved event.

        Raises:
            - HTTPException: If there is an error retrieving the event from the database, raises a 500 error with the message "database error".
        """
        self.handle_nonexistent_event(event_id)
        try:
            event = self.collection.find_one({"_id": convert_to_object_id(event_id)})
            return models.EventOut(
                price=self.tickets_driver.get_minimum_price(event_id),
                is_free=self.tickets_driver.is_free_event(event_id),
                id=str(event["_id"]),
                **event
            )
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_event_by_id(self, event_id: str):
        """
        Deletes the event with the given event ID.

        Args:
            event_id (str): The ID of the event to be deleted.

        Raises:
            HTTPException: If there is an error with the database.
        """
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
        """
        Searches for events in the database that match the specified criteria.

        Args:
            city (str): Name of the city where the event is taking place.
            online (bool, optional): Whether the event is online or not. Defaults to None.
            free (bool, optional): Whether the event is free or not. Defaults to None.
            title (str, optional): Title of the event. Defaults to None.
            start_date (str, optional): Start date of the event (format: YYYY-MM-DD). Defaults to None.
            end_date (str, optional): End date of the event (format: YYYY-MM-DD). Defaults to None.
            category (str, optional): Category of the event. Defaults to None.

        Returns:
            list[models.EventOut]: A list of events that match the specified criteria.

        Raises:
            HTTPException: If there is an error accessing the database.
        """

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

            events_out = [
                models.EventOut(
                    price=self.tickets_driver.get_minimum_price(str(event["_id"])),
                    is_free=self.tickets_driver.is_free_event(str(event["_id"])),
                    id=str(event["_id"]),
                    **event
                )
                for event in self.collection.find(query)
            ]

            if free is not None:
                events_out = [event for event in events_out if event.is_free == free]
            return events_out

        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_events_by_creator_id(self, creator_id):
        """
        Get events created by a specific creator.

        Args:
        - creator_id (str): ID of the creator.

        Returns:
        - list[models.EventOut]: A list of EventOut models representing the events created by the specified creator.

        Raises:
        - HTTPException: If a PyMongoError occurs while accessing the database.
        """
        try:
            events = self.collection.find({"creator_id": creator_id})
            return [
                models.EventOut(
                    price=self.tickets_driver.get_minimum_price(str(event["_id"])),
                    is_free=self.tickets_driver.is_free_event(str(event["_id"])),
                    id=str(event["_id"]),
                    **event
                )
                for event in events
            ]
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
