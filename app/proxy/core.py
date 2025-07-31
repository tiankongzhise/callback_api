import httpx
from fastapi import Request, Response,APIRouter
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from tk_base_utils import load_toml
from ..log import create_logger
logger = create_logger(__name__)

def get_settings():
    config = load_toml("config.toml")
    return config

proxy_settings = get_settings()

def reload_proxy_settings():
    proxy_settings = get_settings()
    logger.info(f"Reloaded proxy_settings: {proxy_settings}")

proxy_router = APIRouter()


@retry(
    stop=stop_after_attempt(proxy_settings['retry']['max_retry']),
    wait=wait_fixed(proxy_settings['retry']['retry_delay']),
    retry=retry_if_exception_type(httpx.RequestError),
    before_sleep=lambda retry_state: logger.warning(f"Retrying request, attempt {retry_state.attempt_number}")
)
async def forward_request(router: str, api_path: str, request: Request) -> Response:
    logger.info(f'forward is running,router:{router},api_path:{api_path},request:{request}')
    router_info = proxy_settings['proxy'].get(router,{})
    api_url = router_info.get(api_path)
    if not router_info:
        logger.error(f"Unknown router: {router}")
        logger.debug(f"Available routers: {proxy_settings['proxy'].keys()}")
        return Response(content=f"Unknown router: {router}", status_code=400)
    if not api_url:
        logger.error(f"Unknown api_path: {api_path}")
        logger.debug(f"Available api_paths: {router_info.keys()}")
        return Response(content=f"Unknown api_path: {api_path}", status_code=400)

    async with httpx.AsyncClient() as client:
        url = f"{api_url}"
        headers = dict(request.headers)
        headers.pop("host", None)

        logger.info(f"Forwarding request to {url}")

        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                params=request.query_params,
                content=await request.body(),
                timeout=30.0,
            )

            logger.info(f"Received response with status code {response.status_code}")
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
        except httpx.RequestError as e:
            logger.error(f"Request to {url} failed: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise e
        




