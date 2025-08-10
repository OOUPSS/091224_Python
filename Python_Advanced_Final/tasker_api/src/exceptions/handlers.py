from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Обработчик для HTTPException.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Обработчик для ошибок валидации запроса.
    """
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )