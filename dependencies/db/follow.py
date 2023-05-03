from fastapi import HTTPException
from fastapi import status

from dependencies.db.client import Client


class FollowsDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["follow"]

    def follow_user(self, follower_id: str, followed_id: str):
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
        if not self.is_user_followed(follower_id, followed_id):
            raise HTTPException(detail="user is not followed", status_code=status.HTTP_400_BAD_REQUEST)
        self.collection.delete_one({"follower_id": follower_id, "followed_id": followed_id})

    def is_user_followed(self, follower_id: str, followed_id: str):
        return self.collection.find_one({"follower_id": follower_id, "followed_id": followed_id}) is not None

    def get_followed_users(self, follower_id: str) -> list[str]:
        return [follow["followed_id"] for follow in self.collection.find({"follower_id": follower_id})]
