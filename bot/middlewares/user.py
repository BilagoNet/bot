from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode


from bot.services.database.models import User
from bot.states.user import DialogSG


class RegisterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        session = data["session"]
        
        _u = User(
            id=event.from_user.id
        )
        
        if not await User.is_exists(session, _u):
            await User.create(session, _u)  # create user
        else:
            _u = await User.get(session, _u.id)
        data['db_user'] = _u

        return await handler(event, data)
