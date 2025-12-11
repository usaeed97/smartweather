# models/db.py
from pymongo import MongoClient

mongo_client = None
db = None


def init_db(app):
    """
    Initialize MongoDB client and database using Flask app config.
    """
    global mongo_client, db
    uri = app.config["MONGO_URI"]
    mongo_client = MongoClient(uri)
    db_name = app.config.get("MONGO_DB_NAME", "smartweather")
    db = mongo_client[db_name]
