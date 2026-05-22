import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        
        logger.info("Requête entrante", extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path
        })
        
        response = await call_next(request)
        
        logger.info("Réponse envoyée", extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "path": request.url.path
        })
        
        response.headers["X-Request-ID"] = request_id
        return response