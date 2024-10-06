from PyPDF2 import PdfReader
import uuid

from fastapi import UploadFile

def process_pdf(file: UploadFile):
    try:
        reader = PdfReader(file.file)
        text = "\n".join([page.extract_text() for page in reader.pages])
        pdf_id = str(uuid.uuid4())

        #save_pdf_to_store(pdf_id, text)
        return pdf_id
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None
