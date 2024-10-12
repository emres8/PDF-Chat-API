from fastapi import APIRouter, HTTPException, Depends
from app.services.pdf_manager import PDFManager
from app.services.chat_service import ChatService
from app.schemas.chat_schema import ChatRequest
from app.external_services.gemini_chat_model import GeminiChatModel

router = APIRouter()

chat_service = ChatService(GeminiChatModel())

@router.post("/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, chat_request: ChatRequest, pdf_manager: PDFManager = Depends()):
    try:
        pdf_file = await pdf_manager.get_pdf(pdf_id)
        
        if not pdf_file:
            raise HTTPException(status_code=404, detail=f"PDF with id {pdf_id} not found.")
        
        response = chat_service.chat_with_pdf(pdf_file, chat_request.message)
        
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
