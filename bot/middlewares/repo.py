from typing import Callable, Dict, Any, Awaitable

import traceback

from aiogram import BaseMiddleware
from aiogram.types import Update, ChatMember, CallbackQuery

from sqlalchemy.orm import sessionmaker

from bot.services.database.models import User


class RepoMiddleware(BaseMiddleware):
    def __init__(self, db: sessionmaker) -> None:
        self.db: sessionmaker = db

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        session = self.db()
        try:
            my_chat_member: ChatMember = event.my_chat_member
        except AttributeError:
            my_chat_member = None
        if my_chat_member and my_chat_member.chat.type == 'private':
            if event.my_chat_member.new_chat_member and my_chat_member.new_chat_member.status in ['left', 'kicked']:
                await User.delete(session, my_chat_member.chat.id)
                return
        data["session"] = session
        
        try:
            await handler(event, data)
        except Exception as e:
            traceback.print_exc(300)
        # close session
        await session.close()
