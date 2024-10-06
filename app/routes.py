from fastapi import APIRouter, UploadFile, File, HTTPException
from app.pdf_processor import process_pdf

pdf_router = APIRouter()

@pdf_router.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_id = process_pdf(file)
    if not pdf_id:
        raise HTTPException(status_code=400, detail="Invalid PDF format")
    return {"pdf_id": pdf_id}