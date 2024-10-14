from unittest.mock import MagicMock
import pytest
from app.utils.pdf_processor import PDFProcessor
from fastapi import UploadFile
from io import BytesIO

# --- Fixtures for Valid and Invalid Files ---


@pytest.fixture
def valid_pdf_file():
    with open("tests/assets/valid_test.pdf", "rb") as f:
        file_data = f.read()

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "valid_test.pdf"
    mock_file.file = BytesIO(file_data)
    mock_file.content_type = "application/pdf"

    return mock_file

@pytest.fixture
def no_text_pdf_file():
    with open("tests/assets/no_text_test.pdf", "rb") as f:
        file_data = f.read()

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "no_text_test.pdf"
    mock_file.file = ""
    mock_file.content_type = "application/pdf"

@pytest.fixture
def invalid_pdf_file():
    with open("tests/assets/invalid_test.txt", "rb") as f:
        file_data = f.read()
    
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "invalid_test.txt"
    mock_file.file = BytesIO(file_data)
    mock_file.content_type = "text/plain"
    return mock_file

@pytest.fixture
def large_size_pdf_file():
    with open("tests/assets/large_test.pdf", "rb") as f:
        file_data = f.read()
    
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "large_test.pdf"
    mock_file.file = BytesIO(file_data)
    mock_file.content_type = "application/pdf"
    return mock_file


# --- Tests for `preprocess` Method ---

@pytest.mark.parametrize("input_text, expected_output", [
    # Test removal of stopwords and alphanumeric filtering
    ("I'm happy", "happy"), 
    ("You're awesome", "awesome"),  
    ("I've seen this", "seen"), 
    ("She'll arrive soon", "arrive soon"), 
    ("He doesn't like it", "like"), 
    ("It's a test", "test"),  
    
    # Test stop words removal
    ("This is a simple test", "simple test"),  
    
    # Test handling of contractions combined with stop words removal
    ("I'm going to the store, and I've bought some things.", "going store bought things"),  
    
    # Test special characters removal
    ("Hello! This should remove #hashtags and @mentions.", "Hello remove hashtags mentions"),
])

def test_preprocess(input_text, expected_output):
    processed_text = PDFProcessor.preprocess(input_text)
    assert processed_text == expected_output

# --- Tests for `validate` Method ---

def test_validate_valid_pdf(valid_pdf_file):
    # Test if a valid PDF passes validation
    PDFProcessor.validate(valid_pdf_file)

def test_validate_invalid_file_type(invalid_pdf_file):
    with pytest.raises(ValueError, match="Invalid file type. Only PDFs are allowed."):
        PDFProcessor.validate(invalid_pdf_file)

def test_validate_file_size_exceeds_limit(large_size_pdf_file):
    # Test if a file exceeding the size limit raises ValueError
    with pytest.raises(ValueError, match="File size exceeds the maximum limit"):
        PDFProcessor.validate(large_size_pdf_file)


# --- Tests for `extract_text` Method ---

def test_extract_text_valid_pdf(valid_pdf_file):
    text, page_count = PDFProcessor.extract_text(valid_pdf_file)

    assert text is not None
    assert page_count > 0

# def test_extract_text_no_text_pdf(no_text_pdf_file):
#     # Test a PDF with no extractable text
#     with pytest.raises(ValueError, match="No text extracted from PDF."):
#         PDFProcessor.extract_text(no_text_pdf_file)

def test_extract_text_error_handling(invalid_pdf_file):
    # Test an invalid PDF file
    with pytest.raises(ValueError, match="Failed to process the PDF"):
        PDFProcessor.extract_text(invalid_pdf_file)
