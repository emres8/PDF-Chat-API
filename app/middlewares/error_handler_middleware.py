from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware



class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except Exception as exc:

            return JSONResponse(
                status_code=500,
                content={
                    "message": "Internal Server Error",
                    "status_code": 500,
                    "detail": "An unexpected error occurred. Please try again later."
                }
            )
