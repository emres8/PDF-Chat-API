from fastapi import APIRouter, Depends

from app.services.pdf_service import PDFService
from app.services.chat_service import ChatService
from app.schemas.chat_schema import ChatRequest
from app.utils.dependencies import get_chat_service, get_pdf_service, validate_pdf_id

router = APIRouter()

@router.post("/chat/{pdf_id}")
async def chat_with_pdf(
        chat_request: ChatRequest,
        pdf_id: str = Depends(validate_pdf_id),
        pdf_service: PDFService = Depends(get_pdf_service), 
        chat_service: ChatService = Depends(get_chat_service)
        ):

    pdf_document = await pdf_service.get_pdf(pdf_id)
    response = await chat_service.chat_with_pdf(pdf_id, pdf_document.text, chat_request.message)

    return {"response": response}

