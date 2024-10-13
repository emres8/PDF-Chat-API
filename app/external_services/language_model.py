from abc import ABC, abstractmethod

class LanguageModel(ABC):
    @abstractmethod
    def generate_response(self, pdf_text: str, message: str) -> str:
        """Generates a response based on PDF text and user message."""
        pass