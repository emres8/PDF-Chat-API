from app.services.pdf_file import PDFFile
from app.database import pdf_collection
from bson import ObjectId
from fastapi import HTTPException

class PDFManager:
    def __init__(self):
        self.pdf_collection = pdf_collection

    async def upload_pdf(self, file):
        pdf_file = PDFFile(file)
        pdf_file.validate()
        pdf_file.extract_text()

        pdf_document = {
            "pdf_id": pdf_file.pdf_id,
            "file_name": pdf_file.file_name,
            "text": pdf_file.get_text(),
            "metadata": pdf_file.get_metadata()
        }

        result = self.pdf_collection.insert_one(pdf_document)
        return str(result.inserted_id)

    async def get_pdf(self, pdf_id):
        pdf = self.pdf_collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            raise HTTPException(status_code=404, detail=f"PDF with id {pdf_id} not found.")
        return pdf
