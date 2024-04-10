import dotenv

from llm_platform.bot.base_tool.bot import BaseToolBotService
from llm_platform.bot.base import run_bot


dotenv.load_dotenv()


bot = BaseToolBotService.create("test")
run_bot(bot, "localhost", 8000)
