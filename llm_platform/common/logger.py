import inspect
import logging
import os
from typing import Optional


def get_caller_name() -> Optional[str]:
    """获取调用者的名称"""
    caller_frame = inspect.currentframe().f_back.f_back
    module = inspect.getmodule(caller_frame)
    if module:
        return module.__name__
    else:
        return None


def setup_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_directory = os.getenv("LOG_LEVEL", "log")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(f"{log_directory}/app.log"),
            logging.StreamHandler(),
        ],
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """返回命名logger，如果没有提供名称，则自动获取当前的模块名"""
    if not name:
        name = get_caller_name() or "root"

    return logging.getLogger(name)


setup_logging()
