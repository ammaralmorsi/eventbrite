from fastapi import HTTPException, status
from dependencies.db.client import Client


class LikesDriver:
    """
    Driver for handling likes on events
    """

    def __init__(self):
        """
        Initializes LikesDriver
        """
        self.db = Client().get_instance().get_db()
        self.collection = self.db["likes"]

    def like_event(self, user_id: str, event_id: str):
        """
        Adds a like to the event for the user with the given user_id.

        :param user_id: The user ID
        :type user_id: str
        :param event_id: The event ID
        :type event_id: str
        :raises HTTPException: If the event is already liked
        """
        if self.is_event_liked(user_id, event_id):
            raise HTTPException(detail="event is already liked",
                                status_code=status.HTTP_400_BAD_REQUEST)
        self.collection.insert_one({"user_id": user_id, "event_id": event_id})

    def unlike_event(self, user_id: str, event_id: str):
        """
        Removes a like from the event for the user with the given user_id.

        :param user_id: The user ID
        :type user_id: str
        :param event_id: The event ID
        :type event_id: str
        :raises HTTPException: If the event is not liked
        """
        if not self.is_event_liked(user_id, event_id):
            raise HTTPException(detail="event is not liked", status_code=status.HTTP_400_BAD_REQUEST)
        self.collection.delete_one({"user_id": user_id, "event_id": event_id})

    def is_event_liked(self, user_id: str, event_id: str) -> bool:
        """
        Returns True if the event with the given event_id is liked by the user with the given user_id.

        :param user_id: The user ID
        :type user_id: str
        :param event_id: The event ID
        :type event_id: str
        :return: True if the event is liked by the user, False otherwise
        :rtype: bool
        """
        return self.collection.find_one({"user_id": user_id, "event_id": event_id}) is not None

    def get_liked_events(self, user_id: str) -> list[str]:
        """
        Returns a list of event IDs that are liked by the given user.

        Args:
            user_id: A string representing the ID of the user whose liked events are to be retrieved.

        Returns:
            A list of strings representing the event IDs that are liked by the given user.
        """
        return [like["event_id"] for like in self.collection.find({"user_id": user_id})]

    def delete_likes_by_event_id(self, event_id: str):
        """
        Deletes all likes associated with the given event ID.

        Args:
            event_id: A string representing the ID of the event whose associated likes are to be deleted.
        """
        self.collection.delete_many({"event_id": event_id})
