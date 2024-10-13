import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.main import app

client = TestClient(app)

# --- Integration Tests for PDF Routes ---

async def test_upload_pdf_valid(test_database):
    # Mock the database save operation to return a valid PDF ID
    test_database.insert_one.return_value.inserted_id = "670a8a39c8e846c029106fc1"

    # Test uploading a valid PDF file
    with open("tests/assets/valid_test.pdf", "rb") as pdf_file:
        response = client.post("/v1/pdf", files={"file": ("valid_test.pdf", pdf_file, "application/pdf")})

    assert response.status_code == 200
    json_response = response.json()
    assert "pdf_id" in json_response


@pytest.mark.asyncio
async def test_upload_pdf_invalid_file_type(test_database):
    # Test uploading an invalid file type
    with open("tests/assets/invalid_test.txt", "rb") as txt_file:
        response = client.post("/v1/pdf", files={"file": ("invalid_test.txt", txt_file, "text/plain")})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type. Only PDFs are allowed."


@pytest.mark.asyncio
async def test_get_pdf_valid(test_database):
    # Mock a valid PDF document in the test database
    test_pdf_data = {
        "_id": "670a8a39c8e846c029106fc1",
        "file_name": "test_pdf.pdf",
        "text": "This is a test PDF document.",
        "metadata": {"page_count": 2, "file_name": "test_pdf.pdf"},
    }
    test_database.find_one.return_value = test_pdf_data

    # Make the GET request to fetch the PDF by ID
    response = client.get(f"/v1/pdf/{test_pdf_data['_id']}")

    assert response.status_code == 200
    json_response = response.json()
    assert "file_name" in json_response
    assert "text" in json_response
    assert "metadata" in json_response


@pytest.mark.asyncio
async def test_get_pdf_invalid_id_format():
    # Test invalid ObjectId format
    invalid_pdf_id = "invalid_id"
    response = client.get(f"/v1/pdf/{invalid_pdf_id}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid PDF ID format. Refer https://www.mongodb.com/docs/manual/reference/method/ObjectId/ for correct format"


@pytest.mark.asyncio
async def test_get_pdf_not_found(test_database):
    # Mock no PDF found in the database
    test_database.find_one.return_value = None

    non_existent_pdf_id = "670a7bc71cfea946c4531111"
    response = client.get(f"/v1/pdf/{non_existent_pdf_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"PDF with id '{non_existent_pdf_id}' not found."


# --- Integration Tests for Chat Routes ---

@pytest.mark.asyncio
async def test_chat_with_pdf_valid(test_database, mock_redis):
    # Mock a valid PDF document in the test database
    test_pdf_data = {
        "_id": "670a8a39c8e846c029106fc1",
        "file_name": "test_pdf.pdf",
        "text": "This is a test PDF document.",
        "metadata": {"page_count": 2, "file_name": "test_pdf.pdf"},
    }
    test_database.find_one.return_value = test_pdf_data

    chat_payload = {
        "message": "What does this document say?",
        "language_model_name": "gemini"
    }
    response = client.post(f"/v1/chat/{test_pdf_data['_id']}", json=chat_payload)

    assert response.status_code == 200
    assert "response" in response.json()


@pytest.mark.asyncio
async def test_chat_with_pdf_invalid_model(test_database):
    # Mock a valid PDF document in the test database
    valid_pdf_id = "670a8a39c8e846c029106fc1"
    chat_payload = {
        "message": "What does this document say?",
        "language_model_name": "invalid_model"
    }
    response = client.post(f"/v1/chat/{valid_pdf_id}", json=chat_payload)

    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_chat_with_missing_message(test_database):
    # Mock a valid PDF document in the test database
    valid_pdf_id = "670a8a39c8e846c029106fc1"
    chat_payload = {
        "language_model_name": "gemini"
    }
    response = client.post(f"/v1/chat/{valid_pdf_id}", json=chat_payload)

    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_chat_with_invalid_pdf_id():
    invalid_pdf_id = "invalid_pdf_id"
    chat_payload = {
        "message": "What does this document say?",
        "language_model_name": "gemini"
    }
    response = client.post(f"/v1/chat/{invalid_pdf_id}", json=chat_payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid PDF ID format. Refer https://www.mongodb.com/docs/manual/reference/method/ObjectId/ for correct format"


@pytest.mark.asyncio
async def test_chat_with_non_existent_pdf(test_database):
    # Mock no PDF found in the database
    test_database.find_one.return_value = None

    non_existent_pdf_id = "670a7bc71cfea946c4531111"
    chat_payload = {
        "message": "What does this document say?",
        "language_model_name": "gemini"
    }
    response = client.post(f"/v1/chat/{non_existent_pdf_id}", json=chat_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == f"PDF with id '{non_existent_pdf_id}' not found."
