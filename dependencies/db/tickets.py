from dependencies.models.tickets import TicketDB, TicketIn, TicketOut
from dependencies.db.client import Client
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id


class TicketDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["tickets"]

    def create_tickets(self, event_id, tickets: list[TicketIn]):
        tickets = [
            TicketDB(
                event_id=event_id, available_quantity=ticket.max_quantity, **ticket.dict()
            ).dict() for ticket in tickets
        ]
        return self.collection.insert_many(tickets)

    def create_ticket(self, event_id: str, ticket: TicketIn):
        pass

    def get_tickets(self, event_id) -> list[TicketOut]:
        res = []
        for ticket in self.collection.find({"event_id": event_id}):
            res.append(TicketOut(id=str(ticket["_id"]), **ticket))
        return res

    def is_free_event(self, event_id):
        tickets = self.collection.find({"event_id": event_id})
        for ticket in tickets:
            if ticket["price"] == 0:
                return True
        return False

    def is_valid_event_id(self, event_id):
        return self.db["events"].count_documents({"_id": convert_to_object_id(event_id)}) > 0

    def is_valid_ticket_id(self, ticket_id):
        return self.collection.count_documents({"_id": ObjectId(ticket_id)}) > 0

    def get_ticket_by_id(self, ticket_id) -> TicketOut:
        return TicketOut(id=ticket_id, **self.collection.find_one({"_id": ObjectId(ticket_id)}))

    def update_ticket(self, ticket_id: str, updated_attributes: dict):
        return self.collection.update_one({"_id": ObjectId(ticket_id)}, {"$set": updated_attributes})

    def update_quantity(self, ticket_id, quantity):
        return self.collection.update_one({"_id": ObjectId(ticket_id)}, {"$inc": {"available_quantity": quantity}})

    def delete_tickets_by_event_id(self, event_id):
        return self.collection.delete_many({"event_id": event_id})

    def delete_ticket_by_ticket_id(self, ticket_id):
        return self.collection.delete_one({"_id": ObjectId(ticket_id)})
