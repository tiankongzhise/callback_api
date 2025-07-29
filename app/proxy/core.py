from ..log import create_logger

logger = create_logger(__name__)

class ProxyCore:
    def __init__(self):
        logger.debug("初始化代理核心")
    
    def run(self):
        logger.debug("启动代理核心")
