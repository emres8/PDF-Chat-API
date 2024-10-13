import redis.asyncio as redis
from bson import ObjectId
from fastapi import Depends

from app.configs.config import Config
from app.external_services.language_model_factory import LanguageModelFactory
from app.repositories.pdf_repository import PDFRepository
from app.services.pdf_service import PDFService
from app.services.chat_service import ChatService

redis_client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

def get_pdf_repository() -> PDFRepository:
    return PDFRepository()

def get_pdf_service(pdf_repository: PDFRepository = Depends(get_pdf_repository)) -> PDFService:
    return PDFService(repository=pdf_repository)

def get_redis_client():
    return redis_client

def get_chat_service(language_model_name: str, redis_client=Depends(get_redis_client)) -> ChatService:

    language_model = LanguageModelFactory.get_model(language_model_name)
    return ChatService(language_model, redis_client)

def validate_pdf_id(pdf_id: str) -> str:
    if not ObjectId.is_valid(pdf_id):
        raise ValueError("Invalid PDF ID format. Refer https://www.mongodb.com/docs/manual/reference/method/ObjectId/ for correct format")
    return pdf_id
