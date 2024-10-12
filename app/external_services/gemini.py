import google.generativeai as genai
from app.config import Config
from app.services.chat_model import ChatModel

class GeminiChatModel(ChatModel):
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def generate_response(self, pdf_text: str, message: str) -> str:
        prompt = f"The PDF content is: {pdf_text}\nUser's question: {message}"
        response = self.model.generate_content(prompt)
        return response.text
