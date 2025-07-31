from .core import forward_request,create_logger
from fastapi import APIRouter,Request,Response
logger = create_logger(__name__)

proxy_common_router = APIRouter()


@proxy_common_router.api_route("/{proxy_router}/{api_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_with_path(proxy_router: str, api_path: str, request: Request) -> Response:
    logger.info(f'proxy转发记录,来源:{request.client.host},router:{proxy_router},path:{api_path},request:{request}')
    return await forward_request(proxy_router, api_path, request)
