import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
            duration = (time.perf_counter() - start_time)*1000
            logger.info(f"time taken:{duration} ms,"
                        f" Request url:{request.url},"
                        f" Request method:{request.method}")
            return response
        except Exception as e:
            logger.error(e)
            raise e


