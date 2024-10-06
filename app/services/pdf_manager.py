
from app.services.pdf_file import PDFFile


class PDFManager:
    def __init__(self):
        self.pdf_store = {}

    def upload_pdf(self, file):
        pdf_file = PDFFile(file)
        pdf_file.validate()
        pdf_file.extract_text()

        self.pdf_store[pdf_file.pdf_id] = pdf_file
        return pdf_file.pdf_id

    def get_pdf(self, pdf_id):
        if pdf_id not in self.pdf_store:
            raise ValueError(f"PDF with id {pdf_id} not found.")
        return self.pdf_store[pdf_id]
