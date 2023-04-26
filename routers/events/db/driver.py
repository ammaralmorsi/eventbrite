import os
import re
from pymongo import MongoClient
from datetime import datetime


class EventDriver:
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client[os.environ.get("MONGO_DB")]
        self.collection = self.db['events']

    def insert(self, data):
        return self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)

    def find_one(self, query):
        return self.collection.find_one(query)

    def find_by_title(self, query):
        pattern = re.compile(".*{}.*".format(re.escape(query["title"])), re.IGNORECASE)
        query = {"basic_info.title": {"$regex": pattern}}
        return self.find(query)

    def find_by_category(self, query):
        pattern = re.compile(".*{}.*".format(re.escape(query["category"])), re.IGNORECASE)
        query = {"basic_info.category": {"$regex": pattern}}
        return self.find(query)

    def count(self, query):
        return self.collection.count_documents(query)

    def delete(self, query):
        return self.collection.delete_one(query)

    def find_by_location(self, query):
        pattern = re.compile(".*{}.*".format(re.escape(query["location"])), re.IGNORECASE)
        query = {"location.location": {"$regex": pattern}, "location.type": "venue"}
        return self.find(query)


    def get_events_sorted_by_date(self):
        query = {"date_and_time.start_date_time": {"$gte": datetime.now()}}
        return self.collection.find(query).sort("date_and_time.start_date_time", 1)
