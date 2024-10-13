from app.decorators import log_function
from app.utils.pdf_processor import PDFProcessor
from app.repositories.pdf_repository import PDFRepository
from app.models.pdf_model import PDFMetadata

class PDFService:
    def __init__(self, repository: PDFRepository):
        self.repository = repository

    @log_function(
        start_message="Initiating PDF Upload with name '{file.filename}'",
        end_message="PDF Upload with name '{file.filename}' is done with id '{result}'"
    )
    async def process_and_save_pdf(self, file):
        PDFProcessor.validate(file)
        raw_text, page_count = PDFProcessor.extract_text(file)
        #processed_text = PDFProcessor.preprocess(raw_text)

        metadata = PDFMetadata(page_count=page_count, file_name=file.filename)

        pdf_id = await self.repository.save_pdf(file_name=file.filename, text=raw_text, metadata=metadata.dict())
        return pdf_id

    @log_function(
        start_message="Initiating PDF fetch with id '{pdf_id}'",
        end_message="Fetched PDF with id '{pdf_id}'"
    )
    async def get_pdf(self, pdf_id):
        pdf = await self.repository.get_pdf_by_id(pdf_id)
        if not pdf:
            raise ValueError(f"PDF with id {pdf_id} not found.")
        return pdf
