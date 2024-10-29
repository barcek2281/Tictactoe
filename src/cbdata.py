from aiogram.filters.callback_data import CallbackData


class ChooseLevel(CallbackData, prefix="level"):
    level: int


class WhoIsFirst(CallbackData, prefix="first"):
    isBot: bool
