from bson import ObjectId

from dependencies.db.client import Client
from dependencies.models.promocodes import PromocodeDB, PromoCode, PromocodeOut


class PromocodeDriver:
    """
    A class used to interact with the promocode collection in the database.

    Attributes
    ----------
    db : pymongo.database.Database
        an instance of the database
    collection : pymongo.collection.Collection
        the promocode collection in the database

    Methods
    -------
    is_valid_event_id(event_id: str) -> int:
        Check if the given event_id is valid and exists in the database.

    update_promocode(promocode_id: str, updated_attributes: dict) -> pymongo.results.UpdateResult:
        Update the given promocode with the given attributes.

    update_promocode_amount(promocode_id: str, amount: int) -> pymongo.results.UpdateResult:
        Increment the current amount of the given promocode with the given amount.

    is_valid_promocode_id(promocode_id: str) -> bool:
        Check if the given promocode_id is valid and exists in the database.

    get_promocodes(event_id: str) -> list[PromocodeOut]:
        Get all the promocodes for a given event_id.

    get_promocode_by_id(promocode_id: str) -> PromocodeOut:
        Get the promocode with the given promocode_id.

    create_promocodes(event_id, promocodes: list[PromoCode]) -> list[PromocodeOut]:
        Create new promocodes for the given event_id.

    delete_promocodes_by_event_id(event_id: str) -> pymongo.results.DeleteResult:
        Delete all the promocodes for a given event_id.

    delete_promocode_by_id(promocode_id: str) -> pymongo.results.DeleteResult:
        Delete the promocode with the given promocode_id.

    """
    def __init__(self):
        """
            Initialize a new instance of the PromocodeDriver class.
        """
        self.db = Client().get_instance().get_db()
        self.collection = self.db["promocodes"]

    def is_valid_event_id(self, event_id: str):
        """
        Check if the given event_id is valid and exists in the database.

        Parameters
        ----------
        event_id : str
            The id of the event.

        Returns
        -------
        int: 0 if the event_id is invalid, 1 otherwise.
        """
        return self.db["events"].count_documents({"_id": ObjectId(event_id)})

    def update_promocode(self, promocode_id: str, updated_attributes: dict):
        """
        Update the given promocode with the given attributes.

        Parameters
        ----------
        promocode_id : str
            The id of the promocode to update.
        updated_attributes : dict
            A dictionary of attributes to update.

        Returns
        -------
        pymongo.results.UpdateResult
            The result of the update operation.
        """
        return self.collection.update_one({"_id": ObjectId(promocode_id)}, {"$set": updated_attributes})

    def update_promocode_amount(self, promocode_id: str, amount: int):
        """
        Increment the current amount of the given promocode with the given amount.

        Parameters
        ----------
        promocode_id : str
            The id of the promocode to update.
        amount : int
            The amount to increment the current amount with.

        Returns
        -------
        pymongo.results.UpdateResult
            The result of the update operation.
        """
        return self.collection.update_one({"_id": ObjectId(promocode_id)}, {"$inc": {"current_amount": amount}})

    def is_valid_promocode_id(self, promocode_id: str):
        """
        Check if the given promocode_id is valid and exists in the database.

        Parameters
        ----------
        promocode_id : str
            The id of the promocode.

        Returns
        -------
        bool: True if the promocode_id is valid, False otherwise.

        """
        return self.collection.count_documents({"_id": ObjectId(promocode_id)}) > 0

    def get_promocodes(self, event_id: str) -> list[PromocodeOut]:
        """
         Retrieves all the promocodes associated with the given event_id.

         Args:
             event_id (str): The ID of the event to retrieve promocodes for.

         Returns:
             list[PromocodeOut]: A list of PromocodeOut objects representing the retrieved promocodes.
         """
        res = []
        for promocode in self.collection.find({"event_id": event_id}):
            res.append(PromocodeOut(id=str(promocode["_id"]), **promocode))
        return res

    def get_promocode_by_id(self, promocode_id: str) -> PromocodeOut:
        """
        Retrieves the promocode with the given ID.

        Args:
            promocode_id (str): The ID of the promocode to retrieve.

        Returns:
            PromocodeOut: A PromocodeOut object representing the retrieved promocode.
        """
        return PromocodeOut(id=promocode_id, **self.collection.find_one({"_id": ObjectId(promocode_id)}))

    def create_promocodes(self, event_id, promocodes: list[PromoCode]):
        """
        Creates new promocodes for the given event.

        Args:
            event_id (str): The ID of the event to create promocodes for.
            promocodes (list[PromoCode]): A list of PromoCode objects representing the promocodes to create.

        Returns:
            list[PromocodeOut]: A list of PromocodeOut objects representing the created promocodes.
        """
        promocodes = [
            PromocodeDB(
                event_id=event_id, **promocode.dict()
                ).dict() for promocode in promocodes
            ]
        inserted = self.collection.insert_many(promocodes).inserted_ids
        inserted = [
            PromocodeOut(id=str(code), **self.collection.find_one({"_id": code})) for code in inserted
        ]
        return inserted

    def delete_promocodes_by_event_id(self, event_id: str):
        """
        Deletes all the promocodes associated with the given event_id.

        Args:
            event_id (str): The ID of the event to delete promocodes for.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.

        """
        return self.collection.delete_many({"event_id": event_id})

    def delete_promocode_by_id(self, promocode_id: str):
        """
        Deletes the promocode with the given ID.

        Args:
            promocode_id (str): The ID of the promocode to delete.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.

        """
        return self.collection.delete_one({"_id": ObjectId(promocode_id)})
