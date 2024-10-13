from fastapi import APIRouter, UploadFile, Depends

from app.services.pdf_service import PDFService
from app.dependencies import get_pdf_service, validate_pdf_id

router = APIRouter()

@router.post("/pdf")
async def upload_pdf(file: UploadFile, pdf_service: PDFService = Depends(get_pdf_service)):
    pdf_id = await pdf_service.process_and_save_pdf(file)
    return {"pdf_id": pdf_id} 

@router.get("/pdf/{pdf_id}")
async def get_pdf_by_id(
    pdf_id: str = Depends(validate_pdf_id),
    pdf_service: PDFService = Depends(get_pdf_service)
    ):
    pdf = await pdf_service.get_pdf(pdf_id)
    return pdf.dict()
