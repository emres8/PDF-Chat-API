from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.middlewares.error_handler_middleware import ErrorHandlerMiddleware
from app.utils.error_handlers import (
    value_error_handler,
    validation_exception_handler,
    key_error_handler,
    not_implemented_error_handler
)

from app.routers.pdf_router import router as pdf_router
from app.routers.chat_router import router as chat_router

app = FastAPI()

app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(KeyError, key_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(NotImplementedError, not_implemented_error_handler)


app.add_middleware(ErrorHandlerMiddleware)

app.include_router(pdf_router, prefix="/v1", tags=["pdf"])
app.include_router(chat_router, prefix="/v1", tags=["chat"])
