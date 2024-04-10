""" """

from langchain_core.tools import tool
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import JsonOutputKeyToolsParser

from llm_platform.bot.base import BotService


@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int


class BaseToolBotService(BotService):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.model = ChatOpenAI(model="gpt-3.5-turbo-1106")
        model_with_tools = self.model.bind_tools([multiply], tool_choice="multiply")
        self._chain = (
            model_with_tools
            | JsonOutputKeyToolsParser(key_name="multiply", first_tool_only=True)
            | multiply
        ).with_config(config)
