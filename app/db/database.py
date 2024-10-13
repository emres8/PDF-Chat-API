
from app.configs.config import Config
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_CONNECTION_STRING)
db = client[Config.MONGO_DATABASE_NAME]

def connect_to_collection(collection_name): 
    return db[collection_name]

pdf_collection = connect_to_collection("pdfs")
chat_collection = connect_to_collection("chats")
