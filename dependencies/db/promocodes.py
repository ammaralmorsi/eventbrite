from bson import ObjectId

from dependencies.db.client import Client
from dependencies.models.promocodes import PromocodeDB, PromoCode


class PromocodeDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["promocodes"]

    def is_valid_event_id(self, event_id: str):
        return self.db["events"].count_documents({"_id": ObjectId(event_id)})

    def update_promocode(self, promocode_id: str, updated_attributes: dict):
        return self.collection.update_one({"_id": ObjectId(promocode_id)}, {"$set": updated_attributes})

    def update_promocode_amount(self, promocode_id: str, amount: int):
        return self.collection.update_one({"_id": ObjectId(promocode_id)}, {"$inc": {"current_amount": amount}})

    def is_valid_promocode_id(self, promocode_id: str):
        return self.collection.count_documents({"_id": ObjectId(promocode_id)}) > 0

    def get_promocodes(self, event_id: str) -> list[PromocodeDB]:
        res = []
        for promocode in self.collection.find({"event_id": event_id}):
            res.append(PromocodeDB(**promocode))
        return res

    def get_promocode_by_id(self, promocode_id: str) -> PromocodeDB:
        return PromocodeDB(**self.collection.find_one({"_id": ObjectId(promocode_id)}))

    def create_promocodes(self, event_id,promocodes: list[PromoCode]):
        promocodes = [
            PromocodeDB(
                event_id=event_id, **promocode.dict()
                ).dict() for promocode in promocodes
            ]
        return self.collection.insert_many(promocodes)

    def delete_promocodes_by_event_id(self, event_id: str):
        return self.collection.delete_many({"event_id": event_id})

    def delete_promocode_by_id(self, promocode_id: str):
        return self.collection.delete_one({"_id": ObjectId(promocode_id)})
