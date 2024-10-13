from pydantic import BaseModel

class PDFMetadata(BaseModel):
    page_count: int
    file_name: str

class PDFDocument(BaseModel):
    file_name: str
    text: str
    metadata: PDFMetadata