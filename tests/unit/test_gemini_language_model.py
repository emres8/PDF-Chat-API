from unittest.mock import MagicMock, patch
from app.external_services.gemini import GeminiLanguageModel

@patch('app.external_services.gemini.genai.GenerativeModel.generate_content')
def test_generate_response(mock_generate_content):
    # Mock the Gemini API response
    mock_generate_content.return_value = MagicMock(text="Test response from Gemini")
    
    gemini_model = GeminiLanguageModel()
    pdf_text = "Sample text from PDF"
    message = "What is this about?"

    response = gemini_model.generate_response(pdf_text, message)
    
    assert response == "Test response from Gemini"
    mock_generate_content.assert_called_once()  # Ensure Gemini API is called
