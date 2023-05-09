from fastapi import HTTPException
from fastapi import status

from dependencies.db.client import Client


class FollowsDriver:
    """
    A class that provides methods for following and unfollowing users.

    Methods
    -------
    follow_user(follower_id: str, followed_id: str)
        Follows a user with the given `followed_id` by the user with the given `follower_id`.
    unfollow_user(follower_id: str, followed_id: str)
        Unfollows a user with the given `followed_id` by the user with the given `follower_id`.
    is_user_followed(follower_id: str, followed_id: str) -> bool
        Returns `True` if the user with the given `follower_id` follows the user with the given `followed_id`.
        Otherwise, returns `False`.
    get_followed_users(follower_id: str) -> list[str]
        Returns a list of IDs of users followed by the user with the given `follower_id`.
    """

    def __init__(self):
        """Initializes the FollowsDriver object."""
        self.db = Client().get_instance().get_db()
        self.collection = self.db["follow"]

    def follow_user(self, follower_id: str, followed_id: str):
        """
        Follows a user with the given `followed_id` by the user with the given `follower_id`.

        Parameters
        ----------
        follower_id : str
            The ID of the user who wants to follow another user.
        followed_id : str
            The ID of the user who is going to be followed.

        Raises
        ------
        HTTPException
            If the `follower_id` and `followed_id` are the same, or if the `follower_id` is already following the
            `followed_id`, the appropriate exception is raised.
        """
        if follower_id == followed_id:
            raise HTTPException(
                detail="Sorry, buddy. Following yourself isn't allowed. That's like trying to hug yourself – "
                       "it might feel nice, but it's not really the same as a hug from someone else!",
                status_code=status.HTTP_403_FORBIDDEN
            )
        if self.is_user_followed(follower_id, followed_id):
            raise HTTPException(detail="user is already followed", status_code=status.HTTP_400_BAD_REQUEST)
        self.collection.insert_one({"follower_id": follower_id, "followed_id": followed_id})

    def unfollow_user(self, follower_id: str, followed_id: str):
        """
        Unfollows a user with the given `followed_id` by the user with the given `follower_id`.

        Parameters
        ----------
        follower_id : str
            The ID of the user who wants to unfollow another user.
        followed_id : str
            The ID of the user who is going to be unfollowed.

        Raises
        ------
        HTTPException
            If the `follower_id` is not following the `followed_id`, an appropriate exception is raised.
        """
        if not self.is_user_followed(follower_id, followed_id):
            raise HTTPException(detail="user is not followed", status_code=status.HTTP_400_BAD_REQUEST)
        self.collection.delete_one({"follower_id": follower_id, "followed_id": followed_id})

    def is_user_followed(self, follower_id: str, followed_id: str):
        """
        Checks if the follower is following the followed user.

        Args:
            follower_id (str): The ID of the user that follows the other user
            followed_id (str): The ID of the user that is being followed

        Returns:
            bool: True if the follower is following the followed user, False otherwise
        """
        return self.collection.find_one({"follower_id": follower_id, "followed_id": followed_id}) is not None

    def get_followed_users(self, follower_id: str) -> list[str]:
        """
        Retrieves a list of user IDs that the follower is following.

        Args:
            follower_id (str): The ID of the user that is following other users

        Returns:
            list[str]: A list of user IDs that the follower is following
        """
        return [follow["followed_id"] for follow in self.collection.find({"follower_id": follower_id})]
