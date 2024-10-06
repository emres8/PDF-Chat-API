import google.generativeai as genai
import os

class ChatService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def chat_with_pdf(self, pdf, message: str):
        if not pdf.get_text():
            raise ValueError("No text available for the specified PDF.")
        
        prompt = f"The PDF content is: {pdf.get_text()}\nUser's question: {message}"

        response = self.model.generate_content(prompt)
        print(response)
        return response.text
