from typing import Callable, Dict, Any, Awaitable

import traceback

from aiogram import BaseMiddleware
from aiogram.types import Update

from sqlalchemy.orm import sessionmaker


class RepoMiddleware(BaseMiddleware):
    def __init__(self, db: sessionmaker) -> None:
        self.db: sessionmaker = db
        print("RepoMiddleware init")

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        session = self.db()
        print("Creating session")
        # get 1+1 with session
        data["session"] = session
        try:
            await handler(event, data)
        except Exception as e:
            traceback.print_exc(1)
        # close session
        await session.close()
