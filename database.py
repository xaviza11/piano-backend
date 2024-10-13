from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['piano_app'] 


users_collection = db.users
users_collection.create_index([("email", ASCENDING)], unique=True)