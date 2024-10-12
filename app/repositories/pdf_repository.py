from app.database import pdf_collection
from app.models.pdf_model import PDFDocument
from bson import ObjectId

class PDFRepository:
    def __init__(self):
        self.collection = pdf_collection

    async def save_pdf(self, file_name: str, text: str, metadata: dict):
        pdf_data = PDFDocument(
            file_name=file_name,
            text=text,
            metadata=metadata
        )

        result = await self.collection.insert_one(pdf_data.dict(by_alias=True))
        return str(result.inserted_id)

    async def get_pdf_by_id(self, pdf_id: str):
        pdf = await self.collection.find_one({"_id": ObjectId(pdf_id)})
        if pdf:
            return PDFDocument(**pdf)
        return None
