"""基本工具机器人的测试代码"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
import dotenv
from llm_platform.bot.base_tool.bot import BaseToolBotService

dotenv.load_dotenv()


@pytest.fixture
def app():
    app = FastAPI()
    yield app


@pytest.fixture
def client(app):
    client = TestClient(app)
    yield client


@pytest.fixture
def bot():
    bot = BaseToolBotService.create("test")
    yield bot


def test_base_tool(bot):
    assert bot.get_chain().invoke("3 times seven equals to?") == 21


def test_base_tool_service(bot, app):
    bot.add_to_app(app)
    client = TestClient(app)

    response = client.post(
        "/bot/test/invoke", json={"input": [{"content": "3 times 5", "type": "human"}]}
    )
    assert response.status_code == 200
    assert response.json()["output"] == 15
