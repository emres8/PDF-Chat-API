import google.generativeai as genai
from app.config import Config
from app.external_services.language_model import LanguageModel

class GeminiLanguageModel(LanguageModel):
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def generate_response(self, pdf_text: str, message: str) -> str:
        prompt = self.generate_context_aware_prompt(pdf_text, message)
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_context_aware_prompt(self, pdf_text: str, message: str) -> str:
        """
        Generates a context-aware prompt by combining the PDF content and the user's query,
        with additional improvements to handle large texts and give more precise instructions.

        :param pdf_text: Extracted text from the PDF document.
        :param message: The question or query asked by the user.
        :return: A context-aware prompt string.
        """

        prompt = f"""
        The user has provided the following question related to a PDF document:
        
        User's Question: "{message}"

        Please use the following content from the PDF document to provide a helpful, concise response:

        PDF Content: {pdf_text}

        Provide a direct, context-aware answer to the user's question based on the PDF content.
        """

        return prompt

