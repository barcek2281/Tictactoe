from aiogram.fsm.state import StatesGroup, State

class FSMGame(StatesGroup):
    game_start = State()