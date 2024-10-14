import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.models.pdf_model import PDFMetadata
from app.services.pdf_service import PDFService
from app.repositories.pdf_repository import PDFRepository
from app.utils.pdf_processor import PDFProcessor

# --- Fixtures for Mock PDF Files and Repository ---

@pytest.fixture
def mock_pdf_repository():
    return AsyncMock(spec=PDFRepository)

@pytest.fixture
def valid_pdf_file():
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.file = MagicMock()
    return mock_file

@pytest.fixture
def invalid_pdf_file():
    mock_file = MagicMock()
    mock_file.filename = "invalid_test.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.file = MagicMock()
    return mock_file

# --- Tests for process_and_save_pdf Method ---

@pytest.mark.asyncio
async def test_process_and_save_pdf_valid(mock_pdf_repository, valid_pdf_file):
    with patch.object(PDFProcessor, 'validate') as mock_validate, \
         patch.object(PDFProcessor, 'extract_text', return_value=("Sample PDF text", 5)) as mock_extract_text, \
         patch.object(PDFProcessor, 'preprocess', return_value="Sample PDF text") as mock_preprocess:
        
        pdf_service = PDFService(mock_pdf_repository)
        
        mock_pdf_repository.save_pdf.return_value = "mock_pdf_id"

        result = await pdf_service.process_and_save_pdf(valid_pdf_file)

        mock_validate.assert_called_once_with(valid_pdf_file)
        
        mock_extract_text.assert_called_once_with(valid_pdf_file)
        
        mock_preprocess.assert_called_once_with("Sample PDF text")

        expected_metadata = PDFMetadata(page_count=5, file_name="test.pdf").model_dump()
        mock_pdf_repository.save_pdf.assert_called_once_with(
            file_name="test.pdf",
            text="Sample PDF text",
            metadata=expected_metadata
        )
        assert result == "mock_pdf_id"

@pytest.mark.asyncio
async def test_process_and_save_pdf_invalid(mock_pdf_repository, invalid_pdf_file):

    with patch.object(PDFProcessor, 'validate', side_effect=ValueError("Invalid PDF")) as mock_validate:

        pdf_service = PDFService(mock_pdf_repository)

        with pytest.raises(ValueError, match="Invalid PDF"):
            await pdf_service.process_and_save_pdf(invalid_pdf_file)

        mock_validate.assert_called_once_with(invalid_pdf_file)
        mock_pdf_repository.save_pdf.assert_not_called()

# --- Tests for get_pdf Method ---

@pytest.mark.asyncio
async def test_get_pdf_valid(mock_pdf_repository):

    mock_pdf_repository.get_pdf_by_id.return_value = {
        "file_name": "test.pdf",
        "text": "Sample PDF text",
        "metadata": {"page_count": 5, "file_name": "test.pdf"}
    }
    
    pdf_service = PDFService(mock_pdf_repository)

    result = await pdf_service.get_pdf("valid_pdf_id")

    mock_pdf_repository.get_pdf_by_id.assert_called_once_with("valid_pdf_id")
    assert result["file_name"] == "test.pdf"
    assert result["text"] == "Sample PDF text"
    assert result["metadata"]["page_count"] == 5