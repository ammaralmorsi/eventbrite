from dependencies.models.tickets import TicketDB, TicketIn, TicketOut
from dependencies.db.client import Client
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id


class TicketDriver:
    """
    A class used to interact with the tickets collection in the database.

    Attributes
    ----------
    db : pymongo.database.Database
        an instance of the database
    collection : pymongo.collection.Collection
        the tickets collection in the database

    Methods
    -------
    create_tickets(event_id, tickets: list[TicketIn]) -> list[TicketOut]:
        Create new tickets for the given event_id.

    get_tickets(event_id) -> list[TicketOut]:
        Get all the tickets for a given event_id.

    get_ticket_by_id(ticket_id: str) -> TicketOut:
        Get the ticket with the given ticket_id.

    is_valid_event_id(event_id: str) -> int:
        Check if the given event_id is valid and exists in the database.

    is_valid_ticket_id(ticket_id: str) -> bool:
        Check if the given ticket_id is valid and exists in the database.

    is_free_event(event_id: str) -> bool:
        Check if the given event_id is a free event.

    get_minimum_price(event_id: str) -> int:
        Get the minimum price of the tickets for the given event_id.

    update_ticket(ticket_id: str, updated_attributes: dict) -> pymongo.results.UpdateResult:
        Update the given ticket with the given attributes.

    update_ticket_quantity(ticket_id: str, quantity: int) -> pymongo.results.UpdateResult:
        Increment the current quantity of the given ticket with the given quantity.

    delete_tickets_by_event_id(event_id: str) -> pymongo.results.DeleteResult:
        Delete all the tickets for a given event_id.

    delete_ticket_by_id(ticket_id: str) -> pymongo.results.DeleteResult:
        Delete the ticket with the given ticket_id.


    """
    def __init__(self):
        """
           Initializes a TicketDriver instance and sets up the database connection.
       """
        self.db = Client().get_instance().get_db()
        self.collection = self.db["tickets"]

    def create_tickets(self, event_id, tickets: list[TicketIn]):
        """
        Creates tickets for a given event in the database.

        Args:
            event_id (str): The ID of the event for which tickets are created.
            tickets (list[TicketIn]): A list of TicketIn objects representing the tickets to be created.

        Returns:
            list[TicketOut]: A list of TicketOut objects representing the created tickets.
        """
        tickets = [
            TicketDB(
                event_id=event_id, available_quantity=ticket.max_quantity, **ticket.dict()
            ).dict() for ticket in tickets
        ]
        inserted = self.collection.insert_many(tickets).inserted_ids
        inserted = [
            TicketOut(id=str(ticket), **self.collection.find_one({"_id": ticket})) for ticket in inserted
        ]
        return inserted

    def get_tickets(self, event_id) -> list[TicketOut]:
        """
        Retrieves all tickets for a given event from the database.

        Args:
            event_id (str): The ID of the event for which tickets are to be retrieved.

        Returns:
            list[TicketOut]: A list of TicketOut objects representing the retrieved tickets.
        """
        res = []
        for ticket in self.collection.find({"event_id": event_id}):
            res.append(TicketOut(id=str(ticket["_id"]), **ticket))
        return res

    def is_free_event(self, event_id):
        """
        Determines if a given event has any free tickets.

        Args:
            event_id (str): The ID of the event for which to check for free tickets.

        Returns:
            bool: True if the event has at least one free ticket, False otherwise.
        """
        tickets = self.collection.find({"event_id": event_id})
        for ticket in tickets:
            if ticket["price"] == 0:
                return True
        return False

    def get_minimum_price(self, event_id):
        """
        Retrieves the minimum price for tickets for a given event.

        Args:
            event_id (str): The ID of the event for which to retrieve the minimum ticket price.

        Returns:
            int: The minimum ticket price for the event, or -1 if no tickets for the event are found.
        """
        tickets = list(self.collection.find({"event_id": event_id}))
        if tickets:
            minimum_price = tickets[0]["price"]
        else:
            return -1
        for ticket in tickets:
            if ticket["price"] < minimum_price:
                minimum_price = ticket["price"]
        return minimum_price

    def is_valid_event_id(self, event_id):
        """
        Determines if a given event ID is valid.

        Args:
            event_id (str): The ID of the event to check for validity.

        Returns:
            bool: True if the event ID is valid, False otherwise.
        """
        return self.db["events"].count_documents({"_id": convert_to_object_id(event_id)}) > 0

    def is_valid_ticket_id(self, ticket_id):
        """
        Determines if a given ticket ID is valid.

        Args:
            ticket_id (str): The ID of the ticket to check for validity.

        Returns:
            bool: True if the ticket ID is valid, False otherwise
        """
        return self.collection.count_documents({"_id": ObjectId(ticket_id)}) > 0

    def get_ticket_by_id(self, ticket_id) -> TicketOut:
        """
        Retrieves a ticket from the database by its ID.

        Args:
            ticket_id (str): The ID of the ticket to retrieve.

        Returns:
            TicketOut: A TicketOut object representing the retrieved ticket.
        """
        return TicketOut(id=ticket_id, **self.collection.find_one({"_id": ObjectId(ticket_id)}))

    def update_ticket(self, ticket_id: str, updated_attributes: dict):
        """
        Updates a ticket in the database with the given attributes.

        Args:
            ticket_id (str): The ID of the ticket to update.
            updated_attributes (dict): A dictionary of attributes to update.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        return self.collection.update_one({"_id": ObjectId(ticket_id)}, {"$set": updated_attributes})

    def update_quantity(self, ticket_id, quantity):
        """
        Updates the quantity of a ticket in the database.

        Args:
            ticket_id (str): The ID of the ticket to update.
            quantity (int): The quantity to increment the ticket by.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        return self.collection.update_one({"_id": ObjectId(ticket_id)}, {"$inc": {"available_quantity": quantity}})

    def delete_tickets_by_event_id(self, event_id):
        """
        Deletes all tickets for a given event from the database.

        Args:
            event_id (str): The ID of the event for which to delete tickets.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        return self.collection.delete_many({"event_id": event_id})

    def delete_ticket_by_ticket_id(self, ticket_id):
        """
        Deletes a ticket from the database by its ID.

        Args:
            ticket_id (str): The ID of the ticket to delete.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        return self.collection.delete_one({"_id": ObjectId(ticket_id)})
