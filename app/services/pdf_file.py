import re

from PyPDF2 import PdfReader


class PDFFile:
    ALLOWED_FILE_TYPES = ["application/pdf"]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB size limit

    def __init__(self, file):
        self.file = file
        self.file_name = file.filename
        self.pdf_id = self._generate_unique_id()
        self.text = None
        self.page_count = None
        self.metadata = None

    def _generate_unique_id(self):
        import uuid
        return str(uuid.uuid4())

    def validate(self):
        if self.file.content_type not in self.ALLOWED_FILE_TYPES:
            raise ValueError("Invalid file type. Only PDFs are allowed.")


        file_size = len(self.file.file.read())
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds the maximum limit of {self.MAX_FILE_SIZE / (1024*1024)} MB.")
        self.file.file.seek(0)

    def preprocess(self, text):
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.lower()
        return text
    
    def extract_text(self):
        try:
            reader = PdfReader(self.file.file)
            self.text = "\n".join([page.extract_text() for page in reader.pages])
            self.page_count = len(reader.pages)
            if not self.text:
                raise Exception("No text extracted from PDF.")
            self.metadata = {
                "page_count": self.page_count,
                "file_name": self.file_name
            }
        except Exception as e:
            raise ValueError(f"Failed to process the PDF: {e}")
    
    def get_metadata(self):
        return self.metadata

    def get_text(self):
        return self.text
