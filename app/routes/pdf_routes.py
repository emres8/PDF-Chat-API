from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.pdf_manager import PDFManager
from app.services.chat_service import ChatService
from app.models.chat_model import ChatRequest

router = APIRouter()
pdf_manager = PDFManager()
chat_service = ChatService()

@router.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_id = pdf_manager.upload_pdf(file)
    return {"pdf_id": pdf_id}

@router.get("/v1/pdf/{pdf_id}")
async def get_pdf_by_id(pdf_id: str):
    try:
        pdf_file = pdf_manager.get_pdf(pdf_id)
        return {
            "pdf_id": pdf_id,
            "file_name": pdf_file.file_name,
            "metadata": pdf_file.get_metadata(),
            "text": pdf_file.get_text()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/v1/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, chat_request: ChatRequest):
    print(pdf_id, chat_request.message)
    pdf_file = pdf_manager.get_pdf(pdf_id)
    response = chat_service.chat_with_pdf(pdf_file, chat_request.message)
    return {"response": response}
