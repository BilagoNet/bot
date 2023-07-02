from typing import Callable, Dict, Any, Awaitable

import traceback

from aiogram import BaseMiddleware
from aiogram.types import Update

from sqlalchemy.orm import sessionmaker


class RepoMiddleware(BaseMiddleware):
    def __init__(self, db: sessionmaker) -> None:
        self.db = db

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        async with self.db() as session:
            print("Creating session")
            # get 1+1 with session
            stmt = "SELECT 1 + 1"
            result = await session.execute(stmt)
            print(result.all())
            data["session"] = session
            try:
                await handler(event, data)
            except Exception as e:
                traceback.print_exc()

            await session.commit()
