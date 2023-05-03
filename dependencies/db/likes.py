from fastapi import HTTPException
from fastapi import status

from dependencies.db.client import Client


class LikesDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["likes"]

    def like_event(self, user_id: str, event_id: str):
        if self.is_event_liked(user_id, event_id):
            raise HTTPException(detail="event is already liked",
                                status_code=status.HTTP_400_BAD_REQUEST)  # check if event exists
        self.collection.insert_one({"user_id": user_id, "event_id": event_id})

    def unlike_event(self, user_id: str, event_id: str):
        if not self.is_event_liked(user_id, event_id):
            raise HTTPException(detail="event is not liked", status_code=status.HTTP_400_BAD_REQUEST)
        self.collection.delete_one({"user_id": user_id, "event_id": event_id})

    def is_event_liked(self, user_id: str, event_id: str):
        return self.collection.find_one({"user_id": user_id, "event_id": event_id}) is not None

    def get_liked_events(self, user_id: str) -> list[str]:
        return [like["event_id"] for like in self.collection.find({"user_id": user_id})]

    def delete_likes_by_event_id(self, event_id: str):
        self.collection.delete_many({"event_id": event_id})
