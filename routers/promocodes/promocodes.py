from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from dependencies.db.promocodes import PromocodeDriver
from dependencies.models.promocodes import PromoCode, PromocodeOut

from dependencies.db.users import UsersDriver
from dependencies.token_handler import TokenHandler
from fastapi.security import OAuth2PasswordBearer
from dependencies.models.users import UserToken
from fastapi import Depends


router = APIRouter(
    prefix="/promocodes",
    tags=["promocodes"],
)

db_handler = PromocodeDriver()

users_driver = UsersDriver()
token_handler = TokenHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# adding documentation using docstring


def unlimited(promocode_id):
    """
    Helper function that checks if the given promocode is unlimited or not.

    Args:
    - promocode_id (str): The ID of the promocode to be checked.

    Returns:
    - bool: True if the given promocode is unlimited, False otherwise.
    """
    code = db_handler.get_promocode_by_id(promocode_id)
    if code.is_limited is False:
        return True
    return False


def check_amount(promocode_id, amount):
    """
    Helper function that checks if the given promocode has enough amount to be updated or not.

    Args:
    - promocode_id (str): The ID of the promocode to be checked.
    - amount (int): The amount by which the promocode is to be updated.

    Raises:
    - HTTPException(400): If the given amount is negative and there are not enough promocodes available.
    - HTTPException(400): If the given amount is positive and the maximum number of promocodes have already been reached.

    Returns:
    - bool: True if the given promocode has enough amount to be updated, False otherwise.
    """
    code = db_handler.get_promocode_by_id(promocode_id)
    if amount < 0:
        if code.current_amount + amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough promocodes available",
            )
        return True
    if amount > 0:
        if code.current_amount + amount > code.limited_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Too many Promocodes",
            )
        return True


@router.post(
    "/event_id/{event_id}",
    summary="Create promocodes by event id",
    description="This endpoint allows you to create promocodes by event id.",
    tags=["promocodes"],
    responses={
        404: {"description": "Event ID is invalid"},
        500: {"description": "Promocodes creation failed"},
    },
)
async def create_promocodes_by_event_id(event_id: str,
                                        promocodes: List[PromoCode], token: Annotated[str, Depends(oauth2_scheme)]):
    """
    API endpoint that creates promocodes for the given event ID.

    Args:
    - event_id (str): The ID of the event for which the promocodes are to be created.
    - promocodes (List[PromoCode]): The list of promocodes to be created.
    - token (Annotated[str, Depends]): The authorization token for the API.

    Raises:
    - HTTPException: If the given event ID is invalid.
    - HTTPException: If the promocodes creation fails.

    Returns:
    - PromocodeOut: The details of the created promocodes.
    """
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if not db_handler.is_valid_event_id(event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event ID is invalid")

    for code in promocodes:
        if code.current_amount > code.limited_amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Current amount can't be more than limited amount for {code.name}")
        elif code.current_amount is None:
            code.current_amount = code.limited_amount
    insertion = db_handler.create_promocodes(event_id, promocodes)
    if insertion:
        return insertion
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Promocodes creation failed")


@router.put(
    "/promocode_id/{promocode_id}",
    summary="Update promocode by promocode id",
    description="This endpoint allows you to update promocode by promocode id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode updated successfully"},
        404: {"description": "Promocode ID is invalid"},
        500: {"description": "Promocode update failed"},
    },
)
async def update_promocode_by_id(promocode_id: str,
                                 updated_promocode: Annotated[dict, Body(
                                     title="Promocode",
                                     description="Promocode to be updated",
                                     example={
                                         "name": "SALE10",
                                         "is_limited": True,
                                         "limited_amount": 100,
                                         "is_percentage": True,
                                         "discount_amount": 0.1,
                                         "start_date_time": "2023-05-01T00:00:00",
                                         "end_date_time": "2023-05-31T23:59:59"
                                     }
                                 )], token: Annotated[str, Depends(oauth2_scheme)]):
    """
    API endpoint that updates the given promocode.

    Args:
        promocode_id (str): The ID of the promocode to be updated.
        updated_promocode (Annotated[dict, Body]): The updated promocode.
        token (Annotated[str, Depends]): The authorization token for the API.

    Raises:
        HTTPException: If the given promocode ID is invalid.
        HTTPException: If the promocode update fails.
    Returns:
        PlainTextResponse: The response of the API.
    """
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if not db_handler.is_valid_promocode_id(promocode_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promocode ID is invalid")

    if db_handler.update_promocode(promocode_id, updated_promocode):
        return PlainTextResponse("Promocode updated successfully", status_code=200)
    else:
        raise HTTPException(status_code=500, detail="Promocode update failed")


@router.put(
    "/promocode_id/{promocode_id}/quantity/{quantity}",
    summary="Update promocode amount by promocode id",
    description="This endpoint allows you to update promocode amount by promocode id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode amount updated successfully"},
        400: {"description": "Not enough promocodes available"},
        400: {"description": "Too many Promocodes"},
        404: {"description": "Promocode ID is invalid"},
        408: {"description": "Promocode amount update failed"},
    },
)
async def update_promocode_amount_by_id(promocode_id: str, amount: int, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    API endpoint that updates the given promocode amount.

    Args:
        promocode_id (str): The ID of the promocode to be updated.
        amount (int): The amount to be updated.
        token (Annotated[str, Depends]): The authorization token for the API.

    Raises:
        HTTPException: If the given promocode ID is invalid.
        HTTPException: If the promocode amount update fails.

    Returns:
        PlainTextResponse: The response of the API.
    """
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if not db_handler.is_valid_promocode_id(promocode_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promocode ID is invalid")

    if unlimited(promocode_id):
        return PlainTextResponse("Promocode is unlimited", status_code=200)

    check_amount(promocode_id, amount)
    if db_handler.update_promocode_amount(promocode_id, amount):
        return PlainTextResponse("Promocode amount updated successfully", status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Promocode amount update failed")


@router.get(
    "/event_id/{event_id}",
    summary="Get promocodes by event id",
    description="This endpoint allows you to get promocodes by event id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocodes retrieved successfully"},
        404: {"description": "Event ID not found"},
    },
)
async def get_promocodes_by_event_id(event_id: str) -> List[PromocodeOut]:
    """
    API endpoint that gets the promocodes of the given event.

    Args:
        event_id (str): The ID of the event.

    Raises:
        HTTPException: If the given event ID is invalid.

    Returns:
        List[PromocodeOut]: The list of promocodes of the given event.
    """
    if not db_handler.is_valid_event_id(event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event ID not found")

    return db_handler.get_promocodes(event_id)


@router.get(
    "/promocode_id/{promocode_id}",
    summary="Get promocode by id",
    description="This endpoint allows you to get promocode by id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode retrieved successfully"},
        404: {"description": "Promocode ID not found"},
    },
)
async def get_promocode_by_id(promocode_id: str):
    """
    API endpoint that gets the promocode of the given id.

    Args:
        promocode_id (str): The ID of the promocode.

    Raises:
        HTTPException: If the given promocode ID is invalid.

    Returns:
        PromocodeOut: The promocode of the given id.
    """
    if not db_handler.is_valid_promocode_id(promocode_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promocode ID not found")

    return db_handler.get_promocode_by_id(promocode_id)


@router.delete(
    "event_id/{event_id}",
    summary="Delete promocodes by event id",
    description="This endpoint allows you to delete promocodes by event id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocodes deleted successfully"},
        404: {"description": "Event ID is invalid"},
    },
)
async def delete_promocodes_by_event_id(event_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    API endpoint that deletes the promocodes of the given event.

    Args:
        event_id (str): The ID of the event.
        token (Annotated[str, Depends]): The authorization token for the API.

    Raises:
        HTTPException: If the given event ID is invalid.

    Returns (PlainTextResponse): The response of the API.

    """
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if not db_handler.is_valid_event_id(event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event ID is invalid")

    db_handler.delete_promocodes_by_event_id(event_id)
    return PlainTextResponse("Promocodes deleted successfully", status_code=200)


@router.delete(
    "/promocode_id/{promocode_id}",
    summary="Delete promocode by id",
    description="This endpoint allows you to delete promocode by id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode deleted successfully"},
        404: {"description": "Promocode ID is invalid"},
    },
)
async def delete_promocode_by_id(promocode_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    API endpoint that deletes the promocode of the given id.

    Args:
        promocode_id (str): The ID of the promocode.
        token (Annotated[str, Depends]): The authorization token for the API.

    Raises:
        HTTPException: If the given promocode ID is invalid.

    Returns:
        PlainTextResponse: The response of the API.
    """
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)
    if not db_handler.is_valid_promocode_id(promocode_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promocode ID is invalid")

    db_handler.delete_promocode_by_id(promocode_id)
    return PlainTextResponse("Promocode deleted successfully", status_code=200)
