from bson import ObjectId

from dependencies.db.client import Client
from dependencies.models.likes import LikeIn, LikeDB


class LikesDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["likes"]

    def like_event(self, like: LikeDB):
        self.collection.insert_one(like.dict())

    def unlike_event(self, like: LikeDB):
        self.collection.delete_one(like.dict())

    def is_event_liked(self, like: LikeDB):
        return self.collection.find_one(like.dict()) is not None

    def get_liked_events(self, user_id: str) -> list[str]:
        return [like["event_id"] for like in self.collection.find({"user_id": user_id})]
