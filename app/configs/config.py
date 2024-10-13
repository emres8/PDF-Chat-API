from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')
    MONGO_DATABASE_NAME = os.getenv('MONGO_DATABASE_NAME')