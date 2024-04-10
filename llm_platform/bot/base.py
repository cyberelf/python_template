"""大模型机器人接口，定义机器人的基本行为"""

from abc import ABC
from typing import Self

from fastapi import FastAPI
from langchain_core.tools import Runnable
from langchain.callbacks.tracers.logging import LoggingCallbackHandler
from langserve import add_routes

from llm_platform.common.logger import get_logger

logger = get_logger()


class BotService(ABC):
    """机器人服务基类

    机器人服务基类，定义机器人服务的基本行为接口

    Attributes:
        name: 机器人名称
        chain: 链式服务
    """

    def __init__(self, name: str, config: dict):
        self.name = name
        self._chain = None
        self._config = config

    @classmethod
    def create(cls, name: str) -> Self:
        """创建机器人服务

        创建机器人服务

        Args:

        Returns:
            机器人服务对象
        """
        return cls(name, cls.get_config())

    @classmethod
    def get_config(cls) -> dict:
        """获取机器人配置

        获取机器人配置

        Args:

        Returns:
            机器人配置
        """
        handler = LoggingCallbackHandler(logger)

        config = {"callbacks": [handler]}
        return config

    def add_to_app(self, app: FastAPI) -> None:
        """把机器人添加到服务中

        启动机器人服务

        Args:
            app: FastAPI服务

        Raises:
            ValueError: 已经注册了同名的bot
        """
        # check if the name is already in the app
        path = f"/bot/{self.name}"
        if any(route.path == path for route in app.routes):
            raise ValueError(f"Bot with name {self.name} already exists")

        add_routes(app, self.get_chain(), path=path)
        # app.include_router(self.get_router(), prefix="/bot/basic")

    def get_chain(self) -> Runnable:
        """获取langchain对象

        获取langchain对象

        Args:

        Returns:
            链式服务
        """
        return self._chain


def run_bot(bot: BotService, host: str, port: int) -> None:
    """运行机器人服务

    运行独立的机器人服务，仅在机器人作为独立服务时使用。默认时使用`add_to_route`添加到现有FastAPI服务中

    Args:
        bot: 机器人服务

    Returns:
    """
    app = FastAPI()
    bot.add_to_app(app)
    import uvicorn

    uvicorn.run(app, host=host, port=port)
