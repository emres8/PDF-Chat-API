
from pymongo import MongoClient
from app.config import Config

client = MongoClient(Config.MONGO_CONNECTION_STRING)
database = Config.MONGO_DATABASE_NAME
db = client[database]

def connect_to_collection(collection_name): 
    return db[collection_name]

pdf_collection = connect_to_collection("pdfs")
chat_collection = connect_to_collection("chats")
