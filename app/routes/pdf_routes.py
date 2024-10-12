from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.pdf_manager import PDFManager

router = APIRouter()

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        pdf_manager = PDFManager()

        pdf_id = await pdf_manager.upload_pdf(file)
        return {"pdf_id": pdf_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload PDF: {str(e)}")


@router.get("/pdf/{pdf_id}")
async def get_pdf_by_id(pdf_id: str):
    pdf_manager = PDFManager()
    pdf = await pdf_manager.get_pdf(pdf_id)

    return {
        "pdf_id": pdf_id,
        "file_name": pdf["file_name"],
        "metadata": pdf["metadata"],
        "extracted_text": pdf["text"]
    }
