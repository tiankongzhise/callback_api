from .core import proxy_router,reload_proxy_settings
# from .oauth_proxy import proxy_oauth_router
from .proxy_common import proxy_common_router

# proxy_router.include_router(proxy_oauth_router)
proxy_router.include_router(proxy_common_router)

__all__ = [
    "proxy_router",
    "reload_proxy_settings",
]
