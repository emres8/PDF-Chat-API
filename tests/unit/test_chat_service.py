from unittest.mock import AsyncMock, patch
import pytest
from app.services.chat_service import ChatService
from app.external_services.gemini import GeminiLanguageModel

@pytest.mark.asyncio
async def test_chat_with_pdf_cache_hit():
    mock_redis_client = AsyncMock()
    mock_redis_client.get.return_value = b"Cached response"

    chat_service = ChatService(GeminiLanguageModel(), mock_redis_client)
    
    response = await chat_service.chat_with_pdf("gemini", "pdf_id", "pdf_text", "User message")
    assert response == "Cached response"
    mock_redis_client.get.assert_called_once()

@pytest.mark.asyncio
async def test_chat_with_pdf_cache_miss():

    mock_redis_client = AsyncMock()
    mock_redis_client.get.return_value = None

    chat_service = ChatService(GeminiLanguageModel(), mock_redis_client)
    
    with patch.object(GeminiLanguageModel, 'generate_response', return_value="Generated response"):
        response = await chat_service.chat_with_pdf("gemini", "pdf_id", "pdf_text", "User message")
    
    assert response == "Generated response"
    mock_redis_client.get.assert_called_once()
