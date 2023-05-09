from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Body
from dependencies.db.tickets import TicketDriver
from dependencies.models.tickets import TicketIn, TicketOut

from dependencies.db.users import UsersDriver
from dependencies.token_handler import TokenHandler
from fastapi.security import OAuth2PasswordBearer
from dependencies.models.users import UserToken
from fastapi import Depends

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

db_handler = TicketDriver()

users_driver = UsersDriver()
token_handler = TokenHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def check_quantity(ticket_id, quantity):
    ticket = db_handler.get_ticket_by_id(ticket_id)
    if quantity < 0:
        if ticket.available_quantity + quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough tickets available",
            )
        return True
    if quantity > 0:
        if ticket.available_quantity + quantity > ticket.max_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Too many tickets",
            )
        return True


@router.post(
    "/event_id/{event_id}",
    summary="Create tickets by event id",
    description="This endpoint allows you to create tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets created successfully"},
        404: {"description": "Event not found"},
        400: {"description": "Error creating tickets"},
    },
)
async def create_tickets_by_event_id(event_id: str,
                                     tickets: List[TicketIn], token: Annotated[str, Depends(oauth2_scheme)]):
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if not db_handler.is_valid_event_id(event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    inserted = db_handler.create_tickets(event_id, tickets)
    if inserted:
        return inserted
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating tickets")


@router.get(
    "/event_id/{event_id}",
    summary="Get tickets by event id",
    description="This endpoint allows you to get tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets retrieved successfully"},
        404: {"description": "Event not found"},
    },
)
async def get_tickets_by_event_id(event_id: str) -> List[TicketOut]:
    if db_handler.is_valid_event_id(event_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return db_handler.get_tickets(event_id)


@router.get(
    "/ticket_id/{ticket_id}",
    summary="Get tickets by ticket id",
    description="This endpoint allows you to get tickets by ticket id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets retrieved successfully"},
        404: {"description": "Ticket not found"},
    },
)
async def get_tickets_by_ticket_id(ticket_id: str) -> TicketOut:
    if db_handler.is_valid_ticket_id(ticket_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return db_handler.get_ticket_by_id(ticket_id)


@router.put(
    "/ticket_id/{ticket_id}",
    summary="Update ticket by ticket id",
    description="This endpoint allows you to update ticket by ticket id.",
    tags=["tickets"],
    responses={
        200: {"description": "Ticket updated successfully"},
        404: {"description": "Ticket not found"},
    },
)
async def update_ticket_by_ticket_id(
        ticket_id: str,
        updated_attributes: Annotated[dict, Body(
            example={
                "name": "Regular Ticket",
                "price": 50,
                "sales_start_date_time": "2023-05-01T00:00:00",
                "sales_end_date_time": "2023-05-31T23:59:59",
            },
        )],
        token: Annotated[str, Depends(oauth2_scheme)]
):
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if db_handler.is_valid_ticket_id(ticket_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    if db_handler.update_ticket(ticket_id, updated_attributes):
        return PlainTextResponse("Ticket updated successfully", status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")


@router.put(
    "/ticket_id/{ticket_id}/quantity/{quantity}",
    summary="Update number of tickets in the given event id",
    description="This endpoint allows you to update number of tickets in the given event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets updated successfully"},
        404: {"description": "Ticket not found"},
        400: {"description": "Not enough tickets available"},
        400: {"description": "Too many tickets"},
    },
)
async def update_ticket_by_available_quantity(ticket_id: str,
                                              quantity: int, token: Annotated[str, Depends(oauth2_scheme)]):
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if db_handler.is_valid_ticket_id(ticket_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    check_quantity(ticket_id, quantity)

    if db_handler.update_quantity(ticket_id, quantity):
        return PlainTextResponse("Tickets updated successfully", status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")


@router.delete(
    "/event_id/{event_id}",
    summary="Delete tickets by event id",
    description="This endpoint allows you to delete tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets deleted successfully"},
        404: {"description": "Event not found"},
    },
)
async def delete_tickets_by_event_id(event_id: str,  token: Annotated[str, Depends(oauth2_scheme)]):
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if db_handler.is_valid_event_id(event_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if db_handler.delete_tickets_by_event_id(event_id):
        return PlainTextResponse("Tickets deleted successfully", status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")


@router.delete(
    "/ticket_id/{ticket_id}",
    summary="Delete tickets by ticket id",
    description="This endpoint allows you to delete tickets by ticket id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets deleted successfully"},
        404: {"description": "Ticket not found"},
    },
)
async def delete_tickets_by_ticket_id(ticket_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if db_handler.is_valid_ticket_id(ticket_id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    if db_handler.delete_ticket_by_ticket_id(ticket_id):
        return PlainTextResponse("Tickets deleted successfully", status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
