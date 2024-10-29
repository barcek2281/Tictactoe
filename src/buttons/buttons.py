from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import cbdata as cbdata
from lexicon import LEXICON

yes_or_no = ReplyKeyboardBuilder()
pg = ReplyKeyboardBuilder()

yn: list[KeyboardButton] = [
    KeyboardButton(text="Давай!"),
    KeyboardButton(text="Нет, не надо")
]

playground: list[KeyboardButton] = [
    KeyboardButton(text="ᅠ"*i) for i in range(1, 10)
]


yes_or_no.row(*yn)
pg.row(*playground, width=3)


def process_create_yesno_options() -> ReplyKeyboardMarkup:
    yn: list[KeyboardButton] = [
        KeyboardButton(text="Давай!"),
        KeyboardButton(text="Нет, не надо")
    ]

    return ReplyKeyboardBuilder().row(*yn).as_markup(resize_keyboard=True)


def add_yn_options(kb: ReplyKeyboardBuilder) -> None:
    kb.row(*yn)


# -------------------------
def _process_buttons_change(pg: list[int]) -> ReplyKeyboardBuilder:
    temp = [0] * len(pg)
    for i in range(len(pg)):
        if pg[i] == 0:
            temp[i] = (KeyboardButton(text="ᅠ"*(i+1)))
        elif pg[i] == 1:
            temp[i] = (KeyboardButton(text="❌"))
        elif pg[i] == 2:
            temp[i] = (KeyboardButton(text="⭕"))
        else:
            raise ValueError("Почему-то появилось другое значение!!!")

    return ReplyKeyboardBuilder().row(*temp, width=3)


def process_buttons_change(user: dict, isFinish: bool=False) -> ReplyKeyboardMarkup:
    pg = user["pg"]
    pg = user["pg"]
    stack = user["stack"]
    rStack = user["rStack"]

    kb = _process_buttons_change(pg)
    keyboard_list_temp = []

    if stack:
        keyboard_list_temp.append(KeyboardButton(text="<<"))
    if rStack:
        keyboard_list_temp.append(KeyboardButton(text=">>"))

    if not isFinish:
        keyboard_list_temp.append(KeyboardButton(text="Занова"))

    kb.row(*keyboard_list_temp)

    if isFinish:
        add_yn_options(kb)

    return kb.as_markup()


# --------------------------------
# ---------INLINE BUTTONS----------------------------------------------------
# --------------------------------

def exit_button(inline_kb: InlineKeyboardBuilder):
    inline_kb.row(
        InlineKeyboardButton(
            text="Выход",
            callback_data="exit"
        )
    )

def procces_create_setting_options() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()

    inline_kb.row(
        InlineKeyboardButton(
            text="Выбрать уровень сложности",
            callback_data="level_choose"
        )
    )

    inline_kb.row(
        InlineKeyboardButton(
            text="Кто должен начать игру?",
            callback_data="who_is_first"
        )
    )
    return inline_kb.as_markup()

def procces_choose_level() ->InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()

    _buttons = [
        InlineKeyboardButton(text=str(ind),
                             callback_data=cbdata.ChooseLevel(level=ind).pack())
        for ind in range(1, 4)
    ]
    

    inline_kb.add(*_buttons)
    exit_button(inline_kb=inline_kb)

    return inline_kb.as_markup()

def procces_who_is_first() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()

    _buttons = [
        InlineKeyboardButton(text="BOT", callback_data=cbdata.WhoIsFirst(isBot=True).pack()),
        InlineKeyboardButton(text="USER", callback_data=cbdata.WhoIsFirst(isBot=False).pack())
    ]

    inline_kb.add(*_buttons)
    exit_button(inline_kb=inline_kb)

    return inline_kb.as_markup()


    