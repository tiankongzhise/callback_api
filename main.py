from app import proxy
from app.log import create_logger, reload_logger_level
from app.proxy import ProxyCore
def main():
    logger = create_logger(__name__)
    logger.info("启动回调 API 服务")
    logger.debug(f"调试模式已启用")
    
    # 创建并启动控制台监听线程
    import threading
    def listen_console():
        while True:
            try:
                cmd = input().strip().lower()
                if cmd == "reload":
                    reload_logger_level(logger)
                    logger.info("日志级别已重载")
                elif cmd == "exit":
                    logger.info("接收到退出指令，准备退出程序")
                    break
            except EOFError:  # 处理 Ctrl+D/Z
                logger.info("控制台输入结束，退出监听")
                break
            except Exception as e:
                logger.error(f"控制台监听错误: {str(e)}")
    
    # 使用事件控制线程生命周期
    stop_event = threading.Event()
    thread = threading.Thread(
        target=listen_console,
        name="ConsoleListener"
    )
    thread.daemon = True
    thread.start()
    
    logger.info("控制台监听线程已启动，输入 'reload' 重载配置或 'exit' 退出")
    
    try:
        # 主线程工作逻辑（示例）
        while not stop_event.is_set():
            # 这里是主程序的实际业务逻辑
            proxy_core = ProxyCore()
            proxy_core.run()
            logger.debug("主程序正常运行中...")
            
            # 模拟工作，实际替换为您的业务代码
            threading.Event().wait(5)  # 每5秒执行一次
    except KeyboardInterrupt:
        logger.info("接收到 Ctrl+C 中断信号")
    finally:
        logger.info("程序清理中...")
        # 执行清理操作（关闭网络连接、保存状态等）
        
        # 等待控制台线程结束（最多等待1秒）
        thread.join(timeout=1.0)
        
        if thread.is_alive():
            logger.warning("控制台线程未在时限内退出")
        
        logger.info("程序退出")

if __name__ == "__main__":
    main()



    
    
    
