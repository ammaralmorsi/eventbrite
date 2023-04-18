from fastapi import APIRouter
from .db.models import Event, EventDB
from .db.driver import EventDriver
from fastapi.responses import PlainTextResponse
from bson import ObjectId
from typing import List
from fastapi_pagination import Page, paginate


router = APIRouter(
    prefix="/events",
    tags=["events"],
)

db_handler = EventDriver()


@router.post(
    "/create",
    summary="Create a new event",
    description="This endpoint allows you to create a new event in the database.",
    tags=["events"],
    responses={
        200: {"description": "Event created successfully"},
    },
)
async def create_event(event: Event):
    """
    Create a new event.

    Args:
        event (Event): The event object to be created.

    Returns:
        PlainTextResponse: The response indicating whether the event was created successfully or not.
    """
    if db_handler.insert(event.dict()):
        return PlainTextResponse("Event created successfully", status_code=201)
    else:
        return PlainTextResponse("Event creation failed", status_code=500)


@router.get(
    "/id/{event_id}",
    summary="Get an event by id",
    description="This endpoint allows you to get an event by id.",
    tags=["events"],
    responses={
        200: {"description": "Event retrieved successfully"},
    },
)
async def get_event(event_id: str):
    """
    Get an event by id.

    Args:
        event_id (str): The id of the event to be retrieved.

    Returns:
        EventDB or PlainTextResponse: The retrieved event or a response indicating that the event was not found.
    """
    event = db_handler.find_one({"_id": ObjectId(event_id)})
    if event:
        out_event = EventDB(**event)
        out_event.id = str(event["_id"])
        return out_event
    else:
        return PlainTextResponse("Event not found", status_code=404)


@router.get(
    "/title/{event_title}",
    summary="Get an event by title",
    description="This endpoint allows you to get an event by title.",
    tags=["events"],
    responses={
        200: {"description": "Event retrieved successfully"},
    },
)
async def get_event_by_title(event_title: str) -> List[EventDB]:
    """
    Get events by title.

    Args:
        event_title (str): The title of the events to be retrieved.

    Returns:
        List[EventDB]: A list of events that match the given title.
    """
    events = db_handler.find_by_title({"title": event_title})
    result = []
    for event in events:
        event_out = EventDB(**event)
        event_out.id = str(event["_id"])
        result.append(event_out)
    return result


@router.get(
    "/category/{category_name}",
    summary="Get events by category",
    description="This endpoint allows you to get events by category.",
    tags=["events"],
    responses={
        200: {"description": "Event retrieved successfully"},
    },
)
async def get_event_by_category(category_name: str) -> List[EventDB]:
    """
    Get events by category.

    Args:
        category_name (str): The category of the events to be retrieved.

    Returns:
        List[EventDB]: A list of events that match the given category.
    """
    events = db_handler.find_by_category({"category": category_name})
    result = []
    for event in events:
        event_out = EventDB(**event)
        event_out.id = str(event["_id"])
        result.append(event_out)
    return result


@router.delete(
    "/id/{event_id}",
    summary="Delete an event by id",
    description="This endpoint allows you to delete an event by id.",
    tags=["events"],
    responses={
        200: {"description": "Event deleted successfully"},
    },
)
async def delete_event_by_id(event_id: str):
    """
    Delete an event by id.

    Args:
        event_id (str): The id of the event to be deleted.

    Returns:
        PlainTextResponse: The response indicating whether the event was deleted successfully or not.
    """
    if db_handler.count({"_id": ObjectId(event_id)}) == 0:
        return PlainTextResponse("Event not found", status_code=404)

    if db_handler.delete({"_id": ObjectId(event_id)}):
        return PlainTextResponse("Event deleted successfully", status_code=200)
    else:
        return PlainTextResponse("Event deletion failed", status_code=500)


@router.get(
    "/location/{event_location}",
    summary="Get events by location",
    description="This endpoint allows you to get events by location.",
    tags=["events"],
    responses={
        200: {"description": "Events retrieved successfully"},
    },
)
async def get_event_by_location(event_location: str) -> List[EventDB]:
    """
    Get events by location.

    Args:
        event_location (str): The location of the events to be retrieved.

    Returns:
        List[EventDB]: A list of events that match the given location.
    """
    events = db_handler.find_by_location({"location": event_location})
    result = []
    for event in events:
        event_out = EventDB(**event)
        event_out.id = str(event["_id"])
        result.append(event_out)
    return result



@router.get(
    "/date",
    summary="Get events sorted by date",
    description="This endpoint allows you to get events sorted by date.",
    tags=["events"],
    responses={
        200: {"description": "Events retrieved successfully"},
    },
    response_model=Page[EventDB],
)
async def get_event_by_date():
    """
    Get events sorted by date.

    Returns:
        List[EventDB]: A list of events sorted by date.
    """
    events = db_handler.get_events_sorted_by_date()
    result = []
    for event in events:
        event_out = EventDB(**event)
        event_out.id = str(event["_id"])
        result.append(event_out)
    return paginate(result)
