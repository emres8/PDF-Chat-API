from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.external_services.language_model import LanguageModel
from app.utils.decorators import log_function
from app.configs.config import Config

class LangchainLanguageModel(LanguageModel):
    def __init__(self):
        # Get the OpenAI API key from the environment or config
        self.api_key = Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.model = ChatOpenAI(model="gpt-4")
        self.parser = StrOutputParser()

    @log_function(
        start_message="Generating response with Langchain LLM for message '{message}'",
        end_message="Langchain LLM Response generated for message '{message}'"
    )
    def generate_response(self, pdf_text: str, message: str) -> str:
        prompt_template = self.create_prompt_template()
        chain = prompt_template | self.model | self.parser
        
        input_data = {
            "pdf_text": pdf_text,
            "message": message
        }
        
        # Invoke the chain with the input data
        response = chain.invoke(input_data)
        return response

    def create_prompt_template(self) -> ChatPromptTemplate:
        """
        Creates a prompt template for the Langchain LLM. The template includes a system message
        with PDF content and a user message with the user's query.
        """
        system_template = (
            "You are a helpful assistant. Use the provided content from a PDF to answer the user's question.\n\n"
            "PDF Content:\n{pdf_text}\n\n"
            "Now answer the user's question based on the PDF content."
        )

        return ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{message}")]
        )

    def generate_context_aware_prompt(self, pdf_text: str, message: str) -> str:
        """
        Generates a context-aware prompt by combining the PDF content and the user's question.
        This prompt will be passed to the LLM to generate a relevant response.
        """

        prompt = f"""
        The user has asked a question related to a PDF document:

        User's Question: "{message}"

        Please use the following content from the PDF document to provide a direct, context-aware answer:

        PDF Content: {pdf_text}
        """
        return prompt
