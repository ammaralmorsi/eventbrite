from typing import List
from bson import ObjectId
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from .db.driver import TicketDriver
from ..events.db.embeded_models.ticket import Ticket


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

db_handler = TicketDriver()


@router.post(
    "/{event_id}",
    summary="Create tickets by event id",
    description="This endpoint allows you to create tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets created successfully"},
    },
)
async def create_tickets_by_event_id(event_id: str, tickets: List[Ticket]):
    """
    Create tickets for a given event ID.

    Args:
        event_id (str): The ID of the event to create tickets for.
        tickets (List[Ticket]): A list of tickets to be created.

    Returns:
        PlainTextResponse: The response indicating whether the tickets were created successfully or not.
    """
    tickets_in_event = db_handler.find_by_event_id({"_id": ObjectId(event_id)})
    result = []
    result.append(tickets_in_event)
    result.append(tickets)

    if db_handler.update_tickets({"_id": ObjectId(event_id)}, {"tickets": result}):
        return PlainTextResponse("Tickets created successfully", status_code=201)
    else:
        return PlainTextResponse("Tickets creation failed", status_code=500)


@router.get(
    "/{event_id}",
    summary="Get tickets by event id",
    description="This endpoint allows you to get tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets retrieved successfully"},
    },
)
async def get_tickets_by_event_id(event_id: str) -> List[Ticket]:
    """
    Retrieve a list of tickets for a given event ID.

    Args:
        event_id (str): The ID of the event to get tickets for.

    Returns:
        List[Ticket]: A list of tickets for the given event ID.
    """
    if db_handler.count({"_id": ObjectId(event_id)}) == 0:
        return []
    tickets = db_handler.find_by_event_id({"_id": ObjectId(event_id)})
    result = []
    tickets = tickets["tickets"]
    for ticket in tickets:
        ticket_out = Ticket(**ticket)
        result.append(ticket_out)
    return result


@router.put(
    "/{event_id}",
    summary="Update tickets by event id",
    description="This endpoint allows you to update tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets updated successfully"},
    },
)
async def update_tickets_by_event_id(event_id: str, tickets: List[Ticket]):
    """
    Update the tickets for a given event ID.

    Args:
        event_id (str): The ID of the event to update tickets for.
        tickets (List[Ticket]): The tickets to update.

    Returns:
        List[Ticket]: The updated list of tickets for the given event ID.
    """
    if db_handler.count({"_id": ObjectId(event_id)}) == 0:
        return PlainTextResponse("Event not found", status_code=404)

    tickets_as_dicts = [ticket.dict() for ticket in tickets]
    for ticket in tickets_as_dicts:
        ticket["type"] = ticket["type"].value
    db_handler.update_tickets({"_id": ObjectId(event_id)}, {"tickets": tickets_as_dicts})
    return PlainTextResponse("Tickets updated successfully", status_code=200)


# @router.get(
#     "/{event_id}/type/{ticket_type}",
#     summary="Get tickets by event id and ticket type",
#     description="This endpoint allows you to get tickets by event id and ticket type.",
#     tags=["tickets"],
#     responses={
#         200: {"description": "Tickets retrieved successfully"},
#     },
# )
# async def get_tickets_by_event_id_and_ticket_type(event_id: str, ticket_type: type) -> List[Ticket]:
#
#     """
#     Retrieve a list of tickets for a given event ID and ticket type.
#     :param event_id:
#     :param ticket_type:
#     :return: Tickets for the given event ID and ticket type.
#     """
#     if db_handler.count({"_id": ObjectId(event_id)}) == 0:
#         return []
#     tickets = db_handler.find_by_event_id_and_ticket_type({"_id": ObjectId(event_id)}, ticket_type)
#     result = []
#     tickets = tickets["tickets"]
#     for ticket in tickets:
#         ticket_out = Ticket(**ticket)
#         result.append(ticket_out)
#     return result

@router.delete(
    "/{event_id}",
    summary="Delete tickets by event id",
    description="This endpoint allows you to delete tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets deleted successfully"},
    },
)
async def delete_tickets_by_event_id(event_id: str):
    """
    Delete the tickets for a given event ID.

    Args:
        event_id (str): The ID of the event to delete tickets for.

    Returns:
        List[Ticket]: The deleted list of tickets for the given event ID.
    """
    if db_handler.count({"_id": ObjectId(event_id)}) == 0:
        return PlainTextResponse("Event not found", status_code=404)

    db_handler.update_tickets({"_id": ObjectId(event_id)}, {"$set": {"tickets": []}})
    # if deleted_tickets.raw_result['n'] > 0:
    #     return []
    return PlainTextResponse("Tickets deleted successfully", status_code=200)
