from pymongo import MongoClient

def get_db_conn():
    client = MongoClient('mongodb://localhost:27017')
    db = client['EventBrite']
    return db
