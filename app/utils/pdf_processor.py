import re
from PyPDF2 import PdfReader

class PDFProcessor:
    ALLOWED_FILE_TYPES = ["application/pdf"]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB size limit

    @staticmethod
    def validate(file):
        if file.content_type not in PDFProcessor.ALLOWED_FILE_TYPES:
            raise ValueError("Invalid file type. Only PDFs are allowed.")

        file_size = len(file.file.read())
        if file_size > PDFProcessor.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds the maximum limit of {PDFProcessor.MAX_FILE_SIZE / (1024*1024)} MB.")
        file.file.seek(0)

    @staticmethod
    def preprocess(text):
        text = re.sub(r'\s+', ' ', text).strip().lower()
        return text

    @staticmethod
    def extract_text(file):
        try:
            reader = PdfReader(file.file)
            text = "\n".join([page.extract_text() for page in reader.pages])
            if not text:
                raise Exception("No text extracted from PDF.")
            page_count = len(reader.pages)
            return text, page_count
        except Exception as e:
            raise ValueError(f"Failed to process the PDF: {e}")
