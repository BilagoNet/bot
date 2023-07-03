from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog, DialogManager

from bot.services.integration import LocaleText
from bot.states.user import DialogSG
from .select_lang_window import select_language_window


async def get_data(dialog_manager: DialogManager, **kwargs):
    mw_d = dialog_manager.data

    data = dict()
    data['user'] = mw_d.get('db_user')
    # if lang selected lang true else false
    data['lang'] = True if data['user'].lang else False
    data['user_name'] = data['user'].id

    return data
    

main_window = Window(
    LocaleText('welcome', user='@{user_name}'),
    Button(Const("Useless button"), id="nothing"),
    state=DialogSG.SOME_STATE,
    getter=get_data
)


dialog = Dialog(
    select_language_window,
    main_window
    )
