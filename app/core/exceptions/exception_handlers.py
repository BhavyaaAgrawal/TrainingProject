import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions.domain import AppError
from app.core.exceptions import error_codes, error_messages

logger = logging.getLogger(__name__)

def __err(code:str, message:str, *, details:dict | None= None):
    return {"code":code, "message":message, "details":details or {}}

# we dont need to handle below generic exceptions, they are handled automatically by fastapi whenever it
# seems issue like for eg validation erro in request payload etc, the lower ones inheriting AppError are
# explicitly defined are will be called on demand
def register_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        payload = __err(
            error_codes.VALIDATION_ERROR,
            error_messages.VALIDATION_ERROR,
            details={"errors":exc.errors()}
        )
        return JSONResponse(status_code=422, content=payload)

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_handler(request: Request, exc: StarletteHTTPException):
        # Normalize FastAPI/Starlette HTTP exceptions into your schema
        detail = exc.detail if isinstance(exc.detail, (str, int, float, dict, list)) else str(exc.detail)
        payload = __err(error_codes.HTTP_ERROR,
                        error_messages.HTTP_ERROR,
                        details={"details":detail})

        return JSONResponse(status_code=exc.status_code, content=payload)

    # If you prefer: handle fastapi.HTTPException separately (optional, Starlette handler usually covers it)
    @app.exception_handler(HTTPException)
    async def fastapi_http_handler(request: Request, exc: HTTPException):
        detail = exc.detail if isinstance(exc.detail, (str, int, float, dict, list)) else str(exc.detail)
        payload = __err("HTTP_ERROR", "Request failed", details={"detail": detail})
        return JSONResponse(status_code=exc.status_code, content=payload)


    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        status = 400
        if exc.__class__.__name__ == "NotFoundError":
            status = 400
        if exc.__class__.__name__ == "ConflictError":
            status = 409
        if exc.__class__.__name__ == "AuthError":
            status = 401

        payload = __err(exc.code, exc.message, details=exc.details)
        return JSONResponse(status_code=status, content=payload)

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception", extra={"path": str(request.url), "method": request.method})
        payload = __err(error_codes.INTERNAL_ERROR, error_messages.INTERNAL_ERROR)
        return JSONResponse(status_code=500, content=payload)


