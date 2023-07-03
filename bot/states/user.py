from aiogram.fsm.state import StatesGroup, State


class DialogSG(StatesGroup):
    SOME_STATE = State()
    SELECT_LANGUAGE = State()