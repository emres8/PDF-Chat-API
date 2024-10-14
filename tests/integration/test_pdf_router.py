from unittest.mock import AsyncMock
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.pdf_model import PDFDocument, PDFMetadata

client = TestClient(app)

# --- Integration Tests for PDF Routes ---

async def test_upload_pdf_valid(test_database):
    test_database.save_pdf.return_value = "670a8a39c8e846c029106fc1"

    with open("tests/assets/valid_test.pdf", "rb") as pdf_file:
        response = client.post("/v1/pdf", files={"file": ("valid_test.pdf", pdf_file, "application/pdf")})

    assert response.status_code == 200
    json_response = response.json()
    assert "pdf_id" in json_response


@pytest.mark.asyncio
async def test_upload_pdf_invalid_file_type():
    with open("tests/assets/invalid_test.txt", "rb") as txt_file:
        response = client.post("/v1/pdf", files={"file": ("invalid_test.txt", txt_file, "text/plain")})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type. Only PDFs are allowed."


@pytest.mark.asyncio
async def test_get_pdf_valid(test_database):
    valid_pdf_id = "670a7bc71cfea946c4531111"

    test_pdf_data = PDFDocument(
        file_name="test_pdf.pdf",
        text="This is a test PDF document.",
        metadata=PDFMetadata(page_count=2, file_name="test_pdf.pdf")
    )

    test_database.get_pdf_by_id.return_value = test_pdf_data

    response = client.get(f"/v1/pdf/{valid_pdf_id}")

    assert response.status_code == 200
    json_response = response.json()
    assert "file_name" in json_response
    assert "text" in json_response
    assert "metadata" in json_response


@pytest.mark.asyncio
async def test_get_pdf_invalid_id_format():
    invalid_pdf_id = "invalid_id"
    response = client.get(f"/v1/pdf/{invalid_pdf_id}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid PDF ID format. Refer https://www.mongodb.com/docs/manual/reference/method/ObjectId/ for correct format"


@pytest.mark.asyncio
async def test_get_pdf_not_found(test_database):
    test_database.get_pdf_by_id.return_value = None

    non_existent_pdf_id = "670a7bc71cfea946c4531111"
    response = client.get(f"/v1/pdf/{non_existent_pdf_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"PDF with id '{non_existent_pdf_id}' not found."

