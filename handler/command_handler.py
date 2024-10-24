from copy import deepcopy
from random import randint

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message 

from database import users, TEMPLATE_USER
from lexicon import LEXICON
from buttons import process_create_yesno_options, process_buttons_change, procces_create_setting_options
from utils import process_make_new_game, get_random_number, procces_first_bot_move
from FSMdata import FSMGame


router = Router()


# на запуск бота
@router.message(CommandStart())
async def process_hello(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = deepcopy(TEMPLATE_USER)

    await message.answer(text=LEXICON["BOT_RESPONCE"]["HELLO"], reply_markup=process_create_yesno_options())


# ломается принцип DRY
@router.message(StateFilter(default_state), Command(commands="again"))
async def process_start_game(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await message.answer(text=LEXICON["BOT_RESPONCE"]["START_COMMAND"])
        return 
    
    process_make_new_game(users[message.from_user.id])

    if users[message.from_user.id]["isBot"]:
        procces_first_bot_move(users=users, user_id=message.from_user.id)

    await message.answer(text=LEXICON["BOT_RESPONCE"]["START_GAME"], reply_markup=process_buttons_change(users[message.from_user.id]))
    await state.get_state(FSMGame)


@router.message(StateFilter(FSMGame), Command(commands="again"))
async def process_start_game(message: Message, state: FSMContext):    
    process_make_new_game(users[message.from_user.id])

    if users[message.from_user.id]["isBot"]:
        procces_first_bot_move(users=users, user_id=message.from_user.id)

    await message.answer(text=LEXICON["BOT_RESPONCE"]["START_GAME"], reply_markup=process_buttons_change(users[message.from_user.id]))
    await state.get_state(FSMGame)


# Выбор настроик
@router.message(Command(commands="setting"))
async def process_setting(message: Message):
    await message.answer(text=LEXICON["BOT_SETTING"]["BOT_SETTING"], reply_markup=procces_create_setting_options())


# Если пользователь соглашается 
@router.message(StateFilter(default_state), F.text.in_({'Давай!', "Занова"}))
async def process_start_game(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await message.answer(text=LEXICON["BOT_RESPONCE"]["START_COMMAND"])
        return 
    
    process_make_new_game(users[message.from_user.id])

    if users[message.from_user.id]["isBot"]:
        procces_first_bot_move(users=users, user_id=message.from_user.id)

    await message.answer(text=LEXICON["BOT_RESPONCE"]["START_GAME"], reply_markup=process_buttons_change(users[message.from_user.id]))
    await state.set_state(FSMGame.game_start)


@router.message(~StateFilter(default_state), F.text.in_({"Занова"}))
async def process_start_game(message: Message, state: FSMContext):

    process_make_new_game(users[message.from_user.id])

    if users[message.from_user.id]["isBot"]:
        procces_first_bot_move(users=users, user_id=message.from_user.id)

    await message.answer(text=LEXICON["BOT_RESPONCE"]["START_GAME"], reply_markup=process_buttons_change(users[message.from_user.id]))
    await state.set_state(FSMGame.game_start)


# Если пользаватель отказывается 
@router.message(F.text=='Нет, не надо')
async def process_start_game(message: Message):
    process_make_new_game(users[message.from_user.id])
    await message.answer(text=LEXICON["BOT_RESPONCE"]["NOT_ACCEPT"][get_random_number(0, 2)], reply_markup=process_create_yesno_options())

