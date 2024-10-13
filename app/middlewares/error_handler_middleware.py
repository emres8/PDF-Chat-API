from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.configs.logging_config import logger

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
   
        except Exception as exc:
            logger.error(f"Unhandled Exception: {str(exc)}")
            return JSONResponse(
                status_code=500,
                content={
                    "message": "Internal Server Error",
                    "status_code": 500,
                    "detail": "An unexpected error occurred. Please try again later."
                }
            )
