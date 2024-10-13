import redis.asyncio as redis
from bson import ObjectId
from fastapi import Depends

from app.repositories.pdf_repository import PDFRepository
from app.services.pdf_service import PDFService
from app.services.chat_service import ChatService
from app.external_services.gemini import GeminiLanguageModel

redis_client = redis.Redis(host='localhost', port=6379)

def get_pdf_repository() -> PDFRepository:
    return PDFRepository()

def get_pdf_service(pdf_repository: PDFRepository = Depends(get_pdf_repository)) -> PDFService:
    return PDFService(repository=pdf_repository)


def get_chat_service() -> ChatService:
    gemini_model = GeminiLanguageModel()
    return ChatService(gemini_model, redis_client)


def validate_pdf_id(pdf_id: str) -> str:
    if not ObjectId.is_valid(pdf_id):
        raise ValueError("Invalid PDF ID format. Refer https://www.mongodb.com/docs/manual/reference/method/ObjectId/ for correct format")
    return pdf_id
