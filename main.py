from app.log import create_logger, reload_logger_level
from app.proxy import reload_proxy_settings,proxy_router
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

logger = create_logger(__name__)

app = FastAPI(
    title="callback API Gateway",
    description="A gateway to forward requests to different channels.",
    version="1.0.0",
)

origins = [
    "http://api2.hnzzzsw.com",
    "https://api2.hnzzzsw.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

app.include_router(proxy_router)

@app.get("/")
async def read_root():
    logger.info('测试日志记录是否正常')
    return {"message": "API Gateway is running."}

@app.get("/reload")
async def reload():
    reload_logger_level(logger)
    reload_proxy_settings()
    return {"message": "日志级别和代理配置已重载"}
    
