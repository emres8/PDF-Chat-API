from unittest.mock import AsyncMock
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- Integration Tests for Chat Routes ---

@pytest.mark.asyncio
async def test_chat_with_pdf_valid(test_database):

    test_pdf_data = {
        "_id": "670a8a39c8e846c029106fc2",
        "file_name": "test_pdf.pdf",
        "text": "This is a test PDF document.",
        "metadata": {"page_count": 2, "file_name": "test_pdf.pdf"},
    }
    test_database.get_pdf_by_id.return_value = AsyncMock(return_value=test_pdf_data)

    chat_payload = {
        "message": "What does this document say?",
        "language_model_name": "gemini"
    }
    response = client.post(f"/v1/chat/{test_pdf_data['_id']}", json=chat_payload)

    assert response.status_code == 200
    assert "response" in response.json()


@pytest.mark.asyncio
async def test_chat_with_pdf_invalid_model():

    valid_pdf_id = "670a8a39c8e846c029106fc1"
    chat_payload = {
        "message": "What does this document say?",
        "language_model_name": "invalid_model"
    }
    response = client.post(f"/v1/chat/{valid_pdf_id}", json=chat_payload)

    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_chat_with_missing_message():

    valid_pdf_id = "670a8a39c8e846c029106fc1"
    chat_payload = {
        "language_model_name": "gemini"
    }
    response = client.post(f"/v1/chat/{valid_pdf_id}", json=chat_payload)
    assert response.status_code == 422
    assert response.json()['detail'] == ['Error at body -> message: Field required']


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
    test_database.get_pdf_by_id.return_value = None

    non_existent_pdf_id = "670a7bc71cfea946c4531111"
    chat_payload = {
        "message": "What does this document say?",
        "language_model_name": "gemini"
    }
    response = client.post(f"/v1/chat/{non_existent_pdf_id}", json=chat_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == f"PDF with id '{non_existent_pdf_id}' not found."
