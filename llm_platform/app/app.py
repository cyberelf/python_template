from typing import Annotated, Dict, Optional
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from llm_platform.bot.base_tool.app import router as bot_router


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Optional[Dict[str, str]]:
    return {"token": token}


app.include_router(bot_router, prefix="/bot/basic")
