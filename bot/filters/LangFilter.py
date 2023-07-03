from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from pydantic import validator
from sqlalchemy.orm import Session

from bot.services.database.models import User


class LangFilter(BaseFilter):
    lang: bool

    @validator("lang")
    def _validate_lang(
        cls, value: bool
    ) -> bool:
        return value

    async def __call__(self, obj: TelegramObject, db_user: User, session: Session) -> bool:
        if not db_user.lang:
            return False
        return True
