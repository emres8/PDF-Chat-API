import redis.asyncio as redis
from app.utils.decorators import log_function
from app.external_services.language_model import LanguageModel
class ChatService:
    def __init__(self, language_model: LanguageModel, redis_client: redis.Redis):
        self.language_model = language_model
        self.redis_client = redis_client

    @log_function(
        start_message="Initiating chat with PDF '{pdf_id}' for message '{message}'",
        end_message="Chat with PDF '{pdf_id}' completed."
    )
    async def chat_with_pdf(self, language_model_name: str, pdf_id: str, pdf_text: str, message: str):
      
        cache_key = f"{language_model_name}:faq:{pdf_id}:{message.lower()}"

        cached_response = await self.redis_client.get(cache_key)
        if cached_response:
            return cached_response.decode("utf-8")

        response = self.language_model.generate_response(pdf_text, message)

        await self.redis_client.set(cache_key, response, ex=3600)

        return response
