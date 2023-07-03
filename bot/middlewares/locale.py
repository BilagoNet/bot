from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery
from bot.services.database.models import User

from bot.services.locale import (
    Localizator,
    Locale
)


class LocaleMiddleware(BaseMiddleware):
    def __init__(self, localizator: Localizator):
        self._loc: Localizator = localizator

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, CallbackQuery) and "lang_buttons" in event.data:
            user_lang = event.data.split(":")[1]
        else:
            user: User = data["db_user"]
            user_lang = user.lang

        _locale: Locale = self._loc.get_by_locale(user_lang)
        data["locale"] = _locale

        return await handler(event, data)
