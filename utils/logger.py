import inspect
import logging
import sys
import threading

from loguru import logger


class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # print(level)
        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


lock = threading.Lock()


def stop_logging() -> None:
    models = ["httpcore", "httpx", "apscheduler", "elastic_transport", "sqlalchemy"]
    for model in models:
        logger.disable(model)


def setup_logging():
    with lock:
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        # remove every other logger's handlers
        # and propagate to root logger
        for name in logging.root.manager.loggerDict.keys():
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = True
        logger.remove()  # Will remove all handlers already configured

        stop_logging()
        logger.add(
            sink=sys.stdout,
            format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
            " | <level>{level: <8}</level>"
            " | <cyan><b>{line}</b></cyan>"
            " - <white><b>{message}</b></white>",
        )

        logger.add(
            sink="./logs/app.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="10 days",
            compression="zip",
        )
        logger.opt(colors=True)
