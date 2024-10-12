from fastapi import FastAPI
from app.routes.pdf_routes import router as pdf_router
from app.routes.chat_routes import router as chat_router

app = FastAPI()

app.include_router(pdf_router, prefix="/v1", tags=["pdf"])
app.include_router(chat_router, prefix="/v1", tags=["chat"])