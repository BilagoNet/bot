from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode

from bot.services.locale import Locale
from bot.services.database.models import User
from bot.states.user import DialogSG

router = Router()

# F contains lang_buttons

@router.callback_query(~F.data.contains("lang_buttons"))
@router.message(content_types=['any'])
async def cmd_start(
    message: Message | CallbackQuery,
    db_user: User,
    dialog_manager: DialogManager,
    locale: Locale,
):
    if db_user.lang is None:
        await dialog_manager.start(
            DialogSG.SELECT_LANGUAGE,
            mode=StartMode.RESET_STACK
        )
    else:
        await dialog_manager.start(
            DialogSG.SOME_STATE,
            mode=StartMode.RESET_STACK
        )
