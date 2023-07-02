from aiogram.fsm.state import StatesGroup, State


class UserMain(StatesGroup):
    SOME_STATE = State()


class DialogSG(StatesGroup):
    SOME_STATE = State()