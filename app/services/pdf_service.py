from app.utils.pdf_processor import PDFProcessor
from app.repositories.pdf_repository import PDFRepository
from app.models.pdf_model import PDFMetadata

class PDFService:
    def __init__(self, repository: PDFRepository):
        self.repository = repository

    async def process_and_save_pdf(self, file):
        PDFProcessor.validate(file)
        text, page_count = PDFProcessor.extract_text(file)

        metadata = PDFMetadata(page_count=page_count, file_name=file.filename)

        pdf_id = await self.repository.save_pdf(file_name=file.filename, text=text, metadata=metadata.dict())
        return pdf_id

    async def get_pdf(self, pdf_id):
        pdf = await self.repository.get_pdf_by_id(pdf_id)
        if not pdf:
            raise ValueError(f"PDF with id {pdf_id} not found.")
        return pdf