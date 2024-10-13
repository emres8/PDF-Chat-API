from llama_index.core import VectorStoreIndex, Document
from app.external_services.language_model import LanguageModel
from app.utils.decorators import log_function

class LlamaIndexLanguageModel(LanguageModel):
    def __init__(self):
        self.index = None
        self.query_engine = None

    def initialize_index_if_needed(self, pdf_text: str) -> None:
        """
        Initialize the LlamaIndex with the PDF text if it hasn't been initialized yet.
        """
        if not self.index:
            try:
                document = Document(text=pdf_text)
                self.index = VectorStoreIndex.from_documents([document])
                self.query_engine = self.index.as_query_engine()
            except Exception as e:
                raise ValueError(f"Failed to initialize the index: {e}")

    @log_function(
        start_message="Generating response with LlamaIndex for message '{message}'",
        end_message="LlamaIndex response generated for message '{message}'"
    )
    def generate_response(self, pdf_text: str, message: str) -> str:
        """
        Generates a response to the user's question by querying the indexed PDF content.
        """
        self.initialize_index_if_needed(pdf_text)

        try:
            response = self.query_engine.query(message)
            return str(response)
        except Exception as e:
            raise ValueError(f"Failed to generate response: {e}")

    def generate_context_aware_prompt(self, pdf_text: str, message: str) -> str:
        """
        Generates a context-aware prompt for LlamaIndex based on the user's question.
        """
        prompt = f"""
        The user has asked the following question related to a PDF document:

        User's Question: "{message}"

        Please provide a detailed and accurate response based on the following PDF content:

        PDF Content: {pdf_text}
        """
        return prompt
