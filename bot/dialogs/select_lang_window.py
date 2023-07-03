from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog, DialogManager

from operator import itemgetter

from aiogram.types import CallbackQuery, Message
from aiogram.utils.text_decorations import html_decoration as fmt
from aiogram_dialog import Dialog, Window
from aiogram_dialog.manager.protocols import DialogManager, ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Next, Row, Select
from aiogram_dialog.widgets.managed import ManagedWidgetAdapter
from aiogram_dialog.widgets.text import Const, Format

from bot.services.database.models import User
from bot.states.user import DialogSG


async def selected_lang(
    query: CallbackQuery,
    select: ManagedWidgetAdapter[Select],
    manager: DialogManager,
    item_id: str,
    **kwargs):
    mw_d = manager.data
    user = mw_d.get('db_user')
    user.lang = item_id
    manager.current_context()
    await User.update(mw_d['session'], user)
    
    await manager.start(
        DialogSG.SOME_STATE
    )

# select language window when user not select language
select_language_window = Window(
    Const("Tilni tanlang"),
    Const("Select language"),
    Const("Выберите язык"),
    Select(
            Format("{item[0]}"),
            id="lang_buttons",
            item_id_getter=itemgetter(1),
            items=[
                ("🇺🇿 O'zbek", 'uz'),
                ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 English", 'en'),
                ("🇷🇺 Русский", 'ru'),
            ],
            on_click=selected_lang,
        ),
    state=DialogSG.SELECT_LANGUAGE,
    )
