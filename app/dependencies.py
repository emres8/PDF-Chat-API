from fastapi import Depends
from app.repositories.pdf_repository import PDFRepository
from app.services.pdf_service import PDFService
from app.services.chat_service import ChatService
from app.external_services.gemini import GeminiChatModel
import redis.asyncio as redis

redis_client = redis.Redis(host='localhost', port=6379)

def get_pdf_repository() -> PDFRepository:
    return PDFRepository()

def get_pdf_service(pdf_repository: PDFRepository = Depends(get_pdf_repository)) -> PDFService:
    return PDFService(repository=pdf_repository)


def get_chat_service() -> ChatService:
    gemini_model = GeminiChatModel()
    return ChatService(gemini_model, redis_client)
