from app.services.chat_model import ChatModel

class ChatService:
    def __init__(self, model: ChatModel):
        self.model = model
    
    def chat_with_pdf(self, pdf, message: str) -> str:
        if not pdf['text']:
            raise ValueError("No text available for the specified PDF.")
        
        pdf_text = pdf['text']
        return self.model.generate_response(pdf_text, message)