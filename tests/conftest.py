import pytest
from unittest.mock import AsyncMock, patch
import redis.asyncio as redis
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
async def mock_redis():
    """
    Mock Redis instance for testing.
    """
    mock_redis_client = AsyncMock(redis.Redis)
    
    # Mock Redis methods
    mock_redis_client.get.return_value = None
    mock_redis_client.set.return_value = None

    with patch("app.utils.dependencies.get_redis_client", return_value=mock_redis_client):
        yield mock_redis_client

@pytest.fixture(scope="function")
async def test_database():
    """
    Mock the PDFRepository's methods for testing purposes.
    """
    test_db = AsyncMock()

    # Mock the methods used in the PDFRepository
    with patch("app.repositories.pdf_repository.PDFRepository.get_pdf_by_id", test_db.get_pdf_by_id), \
         patch("app.repositories.pdf_repository.PDFRepository.save_pdf", test_db.save_pdf):
        yield test_db