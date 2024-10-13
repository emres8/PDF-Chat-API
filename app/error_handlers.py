from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_501_NOT_IMPLEMENTED

async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "message": "Invalid input",
            "status_code": HTTP_400_BAD_REQUEST,
            "detail": str(exc),
        }
    )

async def key_error_handler(request: Request, exc: KeyError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "message": "Missing key",
            "status_code": HTTP_400_BAD_REQUEST,
            "detail": f"Key {str(exc)} not found.",
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        f"Error at {' -> '.join(map(str, error['loc']))}: {error['msg']}"
        for error in exc.errors()
    ]
    
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation failed",
            "status_code": HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": errors,
        }
    )

async def not_implemented_error_handler(request: Request, exc: NotImplementedError):
    return JSONResponse(
        status_code=HTTP_501_NOT_IMPLEMENTED,
        content={
            "message": "Not Implemented",
            "status_code": 501,
            "detail": "This feature is not implemented yet.",
        }
    )