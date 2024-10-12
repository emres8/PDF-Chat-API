from pydantic import BaseModel

class PDFSchema(BaseModel):
    title: str
    author: str
    page_count: int
    content: str

class PDFCreateSchema(BaseModel):
    title: str
    author: str
    content: str

class PDFResponseSchema(BaseModel):
    id: int
    title: str
    author: str
    page_count: int
    content: str