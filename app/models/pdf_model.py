from pydantic import BaseModel, Field
from typing import Optional

class PDFMetadata(BaseModel):
    page_count: int
    file_name: str

class PDFDocument(BaseModel):
    file_name: str
    text: str
    metadata: PDFMetadata

    class Config:
        populate_by_name = True