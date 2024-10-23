from copy import deepcopy
from collections import deque

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from buttons import process_buttons_change
from utils import make_next_move, check_winners, move_position, is_full
from lexicon import LEXICON
from database import users, TEMPLATE_USER
from myfilter import isCells

# Router - for user responce
router = Router()


# Самый главные хендлер,  по шаблонным кнопком
@router.message(isCells())
async def process_gaming(message: Message):
    user = users[message.from_user.id]
    pos:int = len(message.text)-1
    pg = users[message.from_user.id]["pg"]
    stack = users[message.from_user.id]["stack"]
    rStack = users[message.from_user.id]["rStack"]
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

    # победа за игрока
    if result:
        await message.answer(text=LEXICON["BOT_GAME"]["USER_WIN"], reply_markup=process_buttons_change(user=user,  isFinish=True))
        return
    
    # если все клетки полны
    if not isBot and is_full(pg):
        await message.answer(text=LEXICON["BOT_GAME"]["DRAW"], reply_markup=process_buttons_change(user=user, isFinish=True))
        return 
    
    text = text=move_position(pos=pos, is_human=True)

    # бот делает свой хоd
    bot_answer = make_next_move(pg)
    users[message.from_user.id]["pg"][bot_answer] = 2
    stack.append(bot_answer)

    result = check_winners(playground=pg, player=2)

    await message.answer(text=text + '\n' + move_position(pos=bot_answer, is_human=False), reply_markup=process_buttons_change(user=user))
    if result:
        await message.answer(text=LEXICON["BOT_GAME"]["BOT_WIN"], reply_markup=process_buttons_change(user=user, isFinish=True))
    
    if isBot and is_full(pg):
        await message.answer(text=LEXICON["BOT_GAME"]["DRAW"],reply_markup=process_buttons_change(user=user, isFinish=True))
        return 
    
        

@router.message(F.text == "<<")
async def process_back_move(message: Message):
    user = users[message.from_user.id]
    pg = users[message.from_user.id]["pg"]
    stack, rStack = users[message.from_user.id]["stack"], users[message.from_user.id]["rStack"]

    element = stack.pop()
    pg[element] = 0
    rStack.appendleft(element)

    await message.answer(text=LEXICON["BOT_GAME"]["BACKWARD"], reply_markup=process_buttons_change(user=user))


@router.message(F.text == ">>")
async def process_back_move(message: Message):
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
