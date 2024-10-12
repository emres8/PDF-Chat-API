from fastapi import APIRouter, HTTPException, UploadFile, Depends

from app.services.pdf_service import PDFService
from app.dependencies import get_pdf_service

router = APIRouter()

@router.post("/pdf")
async def upload_pdf(file: UploadFile, pdf_service: PDFService = Depends(get_pdf_service)):
    try:
        pdf_id = await pdf_service.process_and_save_pdf(file)
        return {"pdf_id": pdf_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload PDF: {str(e)}")

@router.get("/pdf/{pdf_id}")
async def get_pdf_by_id(pdf_id: str, pdf_service: PDFService = Depends(get_pdf_service)):
    try:
        pdf = await pdf_service.get_pdf(pdf_id)
        return pdf.dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
