import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, Depends

from app.services.pdf_service import PDFService
from app.repositories.pdf_repository import PDFRepository
from app.services.chat_service import ChatService
from app.schemas.chat_schema import ChatRequest
from app.external_services.gemini import GeminiChatModel


router = APIRouter()

redis_client = redis.Redis(host='localhost', port=6379)

chat_service = ChatService(GeminiChatModel(), redis_client)

def get_pdf_service():
    repository = PDFRepository() 
    return PDFService(repository)

@router.post("/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, chat_request: ChatRequest, pdf_service: PDFService = Depends(get_pdf_service)):
    try:
        pdf_document = await pdf_service.get_pdf(pdf_id)

        if not pdf_document:
            raise HTTPException(status_code=404, detail=f"PDF with id {pdf_id} not found.")

        response = await chat_service.chat_with_pdf(pdf_id, pdf_document.text, chat_request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")
