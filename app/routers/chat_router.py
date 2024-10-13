from fastapi import APIRouter, Depends, HTTPException

from app.external_services.language_model_factory import LanguageModelFactory
from app.services.pdf_service import PDFService
from app.services.chat_service import ChatService
from app.schemas.chat_schema import ChatRequest
from app.utils.dependencies import get_pdf_service, validate_pdf_id, get_redis_client

router = APIRouter()

@router.post("/chat/{pdf_id}")
async def chat_with_pdf(
        chat_request: ChatRequest,
        pdf_id: str = Depends(validate_pdf_id),
        pdf_service: PDFService = Depends(get_pdf_service),
        redis_client = Depends(get_redis_client),
        ):

    pdf_document = await pdf_service.get_pdf(pdf_id)

    if not pdf_document:
            raise HTTPException(status_code=404, detail=f"PDF with id '{pdf_id}' not found.")

    language_model = LanguageModelFactory.get_model(chat_request.language_model_name)
    chat_service = ChatService(language_model, redis_client)

    response = await chat_service.chat_with_pdf(
            language_model_name=chat_request.language_model_name,
            pdf_id=pdf_id,
            pdf_text=pdf_document.text,
            message=chat_request.message
        )
    return {"response": response}

