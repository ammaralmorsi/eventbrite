from bson import ObjectId

from dependencies.db.client import Client
from dependencies.models.follow import FollowIn, FollowDB


class LikesDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["follow"]

    def follow_user(self, follow: FollowDB):
        self.collection.insert_one(follow.dict())

    def unfollow_user(self, follow: FollowDB):
        self.collection.delete_one(follow.dict())

    def is_user_followed(self, follow: FollowDB):
        return self.collection.find_one(follow.dict()) is not None

    def get_followed_users(self, user_id: str) -> list[str]:
        return [follow["followed_user_id"] for follow in self.collection.find({"user_id": user_id})]
