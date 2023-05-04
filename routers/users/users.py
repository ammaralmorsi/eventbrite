from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer

from dependencies.models import events
from dependencies.db.users import UsersDriver
from dependencies.db.events import EventDriver
from dependencies.db.likes import LikesDriver
from dependencies.db.follow import FollowsDriver
from dependencies.models import users
from dependencies.token_handler import TokenHandler

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

users_driver = UsersDriver()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
token_handler = TokenHandler()
likes_driver = LikesDriver()
event_driver = EventDriver()
follows_driver = FollowsDriver()


def get_user_info(user_id: str) -> users.UserInfo:
    return users_driver.get_user_by_id(user_id)


@router.get(
    "/emails/check",
    summary="check if email is available",
    description="check if email is available",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "email is available",
            "content": {
                "text/plain": {
                    "example": "email is available"
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "email not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "email not found"
                    }
                }
            }
        }
    }
)
async def check_email(email: str):
    users_driver.handle_nonexistent_email(email)

    return PlainTextResponse("email is available", status_code=status.HTTP_200_OK)


@router.get(
    "/email/info/avatar",
    summary="get the the avatar of the email sent whether it is verified or not",
    responses={
        status.HTTP_200_OK: {
            "description": "login successfully",
            "content": {
                "application/json": {
                    "example": {
                        "avatar_url": "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200",
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "wrong password or email is not verified",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "wrong email",
                    }
                }
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "email not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "email not found"
                        }
                    }
                }
            }
        }
    }
)
async def get_avatar(email: str) -> users.UserAvatar:
    users_driver.handle_nonexistent_email(email)
    return users.UserAvatar(**users_driver.get_user_by_email(email).dict())


@router.get(
    "/id/{user_id}/info",
    summary="get user information by id",
    description="get user information by id",
    responses={
        status.HTTP_200_OK: {
            "description": "get user information by id successfully",
            "content": {
                "application/json": {
                    "example": {
                        "email": "user@gmail.com",
                        "firstname": "user",
                        "lastname": "user",
                        "avatar_url": "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200",
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "user not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user not found"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "invalid user id",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid user id"
                    }
                }
            }
        }
    }
)
async def get_user_by_id(user_id) -> users.UserInfo:
    return get_user_info(user_id)


@router.get(
    "/me/info",
    summary="get user information",
    description="get the user firstname, lastname and avatar",
)
async def get_info(token: Annotated[str, Depends(oauth2_scheme)]) -> users.UserInfo:
    user = token_handler.get_user(token)
    return get_user_info(user.id)


@router.post(
    "/me/event/{event_id}/like",
    summary="like an event",
    description="like an event",
    responses={
        status.HTTP_200_OK: {
            "description": "event liked",
            "content": {
                "text/plain": {
                    "example": "event liked"
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "event not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event not found"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "event is already liked",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event is already liked"
                    }
                }
            }
        }
    }
)
async def like_event(event_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)
    event_driver.handle_nonexistent_event(event_id)

    likes_driver.like_event(user.id, event_id)
    return PlainTextResponse("event liked", status_code=status.HTTP_200_OK)


@router.delete(
    "/me/event/{event_id}/unlike",
    summary="unlike an event",
    description="unlike an event",
    responses={
        status.HTTP_200_OK: {
            "description": "event unliked",
            "content": {
                "text/plain": {
                    "example": "event unliked"
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "event not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event not found"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "event is not liked",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event is not liked"
                    }
                }
            }
        }
    }
)
async def unlike_event(event_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)
    event_driver.handle_nonexistent_event(event_id)

    likes_driver.unlike_event(user.id, event_id)
    return PlainTextResponse("event unliked", status_code=status.HTTP_200_OK)


@router.get(
    "/me/event/liked",
    summary="get liked events",
    description="get liked events",
    responses={
        status.HTTP_200_OK: {
            "description": "liked events",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "event_id",
                            "title": "event title",
                            "start_date_time": "2021-10-10T10:10:10",
                            "image_link": "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200",
                            "is_online": True
                        },
                        {
                            "id": "event_id",
                            "title": "event title",
                            "start_date_time": "2021-10-10T10:10:10",
                            "image_link": "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200",
                            "is_online": False
                        }
                    ]
                },
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        }
    }
)
async def get_liked_events(token: Annotated[str, Depends(oauth2_scheme)]) -> list[events.EventCard]:
    user = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)

    return [
        events.EventCard(
            id=event_out.id,
            title=event_out.basic_info.title,
            start_date_time=event_out.date_and_time.start_date_time,
            image_link=event_out.image_link,
            is_online=event_out.location.is_online
        )
        for event_out in [
            event_driver.get_event_by_id(event_id) for event_id in likes_driver.get_liked_events(user.id)
        ]
    ]


@router.get(
    "/me/event/{event_id}/is_liked",
    summary="check if event is liked",
    description="check if event is liked",
    responses={
        status.HTTP_200_OK: {
            "description": "event is liked",
            "content": {
                "application/json": {
                    "example": True
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "event not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event not found"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        }
    }
)
async def is_liked(event_id: str, token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    user = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)
    event_driver.handle_nonexistent_event(event_id)

    return likes_driver.is_event_liked(user.id, event_id)


@router.post(
    "/me/user/{user_id}/follow",
    summary="follow a user",
    description="follow a user",
    responses={
        status.HTTP_200_OK: {
            "description": "user followed",
            "content": {
                "text/plain": {
                    "example": "user followed"
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "user not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user not found"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "user is already followed",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user is already followed"
                    }
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "user is trying to follow himself",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sorry, buddy. Following yourself isn't allowed. That's like trying to hug yourself –"
                                  " it might feel nice, but it's not really the same as a hug from someone else!"
                    }
                }
            }
        }
    }
)
async def follow_user(user_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)
    users_driver.handle_nonexistent_user(user_id)

    follows_driver.follow_user(user.id, user_id)
    return PlainTextResponse("user followed", status_code=status.HTTP_200_OK)


@router.delete(
    "/me/user/{user_id}/unfollow",
    summary="unfollow a user",
    description="unfollow a user",
    responses={
        status.HTTP_200_OK: {
            "description": "user unfollowed",
            "content": {
                "text/plain": {
                    "example": "user unfollowed"
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "user not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user not found"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "user is not followed",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user is not followed"
                    }
                }
            }
        }
    }
)
async def unfollow_user(user_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)
    users_driver.handle_nonexistent_user(user_id)

    follows_driver.unfollow_user(user.id, user_id)
    return PlainTextResponse("user unfollowed", status_code=status.HTTP_200_OK)


@router.get(
    "/me/user/following",
    summary="get all followed users",
    description="get all followed users",
    responses={
        status.HTTP_200_OK: {
            "description": "list of followed users",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "email": "user@gmail.com",
                            "firstname": "user",
                            "lastname": "user",
                            "avatar": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngwing.com%2Fen%2Ffree-"
                        },
                        {
                            "email": "hi@gmail.com",
                            "firstname": "hi",
                            "lastname": "hi",
                            "avatar": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngwing.com%2Fen%2Ffree-"
                        }
                    ]
                },
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        }
    }
)
async def get_followed_users(token: Annotated[str, Depends(oauth2_scheme)]) -> list[users.UserInfo]:
    user = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)

    return [users_driver.get_user_by_id(user_id) for user_id in follows_driver.get_followed_users(user.id)]


@router.put(
    "/me/edit",
    summary="edit user firstname, lastname, avatar",
    description="edit user information",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "list of followed users",
            "content": {
                "text/plain": {
                    "example": "User information updated successfully"
                },
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "text/plain": {
                    "example": {
                        "detail": "invalid token"
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "user not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user not found"
                    }
                }
            }
        }
    })
async def edit_info(
        token: Annotated[str, Depends(oauth2_scheme)],
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        avatar_url: Optional[str] = None,
) -> PlainTextResponse:
    user = token_handler.get_user(token)
    users_driver.handle_nonexistent_user(user.id)
    users_driver.edit_info(user.id, firstname, lastname, avatar_url)
    return PlainTextResponse("User information updated successfully", status_code=status.HTTP_200_OK)
