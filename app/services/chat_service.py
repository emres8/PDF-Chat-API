import redis.asyncio as redis
from app.services.chat_model import ChatModel
class ChatService:
    def __init__(self, chat_model: ChatModel, redis_client: redis.Redis):
        self.chat_model = chat_model
        self.redis_client = redis_client

    async def chat_with_pdf(self, pdf_id: str, pdf_text: str, message: str):
      
        cache_key = f"faq:{pdf_id}:{message.lower()}"

        cached_response = await self.redis_client.get(cache_key)
        if cached_response:
            return cached_response.decode("utf-8")

        response = self.chat_model.generate_response(pdf_text, message)

        await self.redis_client.set(cache_key, response, ex=3600)

        return response
