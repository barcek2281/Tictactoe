from copy import deepcopy
from collections import deque

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from buttons import process_buttons_change
from utils import make_next_move, check_winners, move_position, is_full
from lexicon import LEXICON
from database import users
from myfilter import isCells
from FSMdata import FSMGame

# Router - for user responce
router = Router()


# Самый главные хендлер,  по шаблонным кнопком
@router.message(StateFilter(FSMGame.game_start), isCells())
async def process_gaming(message: Message, state: FSMContext):
    user: dict = users[message.from_user.id]
    pos: int = len(message.text)-1
    pg: list[int] = users[message.from_user.id]["pg"]
    stack: deque = users[message.from_user.id]["stack"]
    rStack: deque = users[message.from_user.id]["rStack"]
    isBot: bool = users[message.from_user.id]["isBot"]
    
    # ход бота
    if len(stack)%2 != isBot:
        await message.answer(text=LEXICON["BOT_GAME"]["BOT_TURN"])
        return

    # если произошел ход, но при этом были прошлые ходы, то прошлые следущие, удаляются
    if len(rStack) > 0:
        users[message.from_user.id]["rStack"] = deque()
    rStack = users[message.from_user.id]["rStack"]

    # занятая клетка
    if pg[pos]:
        await message.answer(text=LEXICON["BOT_GAME"]["NOT_EMPTY"])
        return


    pg[pos] = 1
    stack.append(pos)
    result = check_winners(playground=pg, player=1)

    # победа за игроком
    if result:
        await message.answer(text=LEXICON["BOT_GAME"]["USER_WIN"], reply_markup=process_buttons_change(user=user,  isFinish=True))
        await state.clear()
        return
    
    # если все клетки полны
    if not isBot and is_full(pg):
        await message.answer(text=LEXICON["BOT_GAME"]["DRAW"], reply_markup=process_buttons_change(user=user, isFinish=True))
        await state.clear()
        return 
    
    text = text=move_position(pos=pos, is_human=True)

    # бот делает свой хоd
    bot_answer = make_next_move(pg)
    users[message.from_user.id]["pg"][bot_answer] = 2
    stack.append(bot_answer)

    result = check_winners(playground=pg, player=2)

    await message.answer(text=text + '\n' + move_position(pos=bot_answer, is_human=False), reply_markup=process_buttons_change(user=user))
    # Победа за ботом
    if result:
        await message.answer(text=LEXICON["BOT_GAME"]["BOT_WIN"], reply_markup=process_buttons_change(user=user, isFinish=True))
        await state.clear()
        return 
    
    if isBot and is_full(pg):
        await message.answer(text=LEXICON["BOT_GAME"]["DRAW"],reply_markup=process_buttons_change(user=user, isFinish=True))
        await state.clear()
        return 
    
        
@router.message(StateFilter(FSMGame.game_start), F.text == "<<")
async def process_back_move(message: Message, state: FSMContext):
    user = users[message.from_user.id]
    pg = users[message.from_user.id]["pg"]
    stack, rStack = users[message.from_user.id]["stack"], users[message.from_user.id]["rStack"]

    element = stack.pop()
    pg[element] = 0
    rStack.appendleft(element)

    await message.answer(text=LEXICON["BOT_GAME"]["BACKWARD"], reply_markup=process_buttons_change(user=user))


@router.message(~StateFilter(FSMGame.game_start), F.text == "<<")
async def process_back_move(message: Message, state: FSMContext):
    state.set_state(FSMGame.game_start)

    user = users[message.from_user.id]
    pg = users[message.from_user.id]["pg"]
    stack, rStack = users[message.from_user.id]["stack"], users[message.from_user.id]["rStack"]

    element = stack.pop()
    pg[element] = 0
    rStack.appendleft(element)

    await message.answer(text=LEXICON["BOT_GAME"]["BACKWARD"], reply_markup=process_buttons_change(user=user))


@router.message(StateFilter(FSMGame.game_start), F.text == ">>")
async def process_back_move(message: Message, state: FSMContext):
    user = users[message.from_user.id]
    pg = users[message.from_user.id]["pg"]
    stack, rStack = users[message.from_user.id]["stack"], users[message.from_user.id]["rStack"]
    isBot = users[message.from_user.id]["isBot"]

    element = rStack.popleft()

    if len(stack)%2 != isBot:
        pg[element] = 1
    else:
        pg[element] = 2

    stack.append(element)

    await message.answer(text=LEXICON["BOT_GAME"]["FORWARD"], reply_markup=process_buttons_change(user=user))


# Неизвестное сообщение
@router.message()
async def process_misunderstand(message: Message):
    await message.answer(text=LEXICON["BOT_RESPONCE"]["WTF"])
