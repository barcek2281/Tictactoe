from aiogram import Router, F
from aiogram.types import CallbackQuery

from buttons import buttons
from database import users
from lexicon import LEXICON
import cbdata as cbdata

router = Router()


@router.callback_query(F.data == "level_choose")
async def procces_level_choose(callback: CallbackQuery):

    await callback.message.edit_text(
        text=LEXICON["BOT_SETTING"]["LEVEL"],
        reply_markup=buttons.procces_choose_level()
    )

    await callback.answer()


@router.callback_query(F.data == "who_is_first")
async def procces_whoIsFirst(callback: CallbackQuery):

    await callback.message.edit_text(
        text=LEXICON["BOT_SETTING"]["WHO_FIRST"],
        reply_markup=buttons.procces_who_is_first()
    )

    await callback.answer()


@router.callback_query(cbdata.WhoIsFirst.filter())
async def procces_whoWillMove(callback: CallbackQuery, callback_data: cbdata.WhoIsFirst):
    if callback_data.isBot:
        users[callback.from_user.id]["isBot"] = True
        await callback.message.edit_text(text=LEXICON["BOT_SETTING"]["BOT_FIRST"])
    else:
        users[callback.from_user.id]["isBot"] = False
        await callback.message.edit_text(text=LEXICON["BOT_SETTING"]["USER_FIRST"])
    
    await callback.answer()


@router.callback_query(cbdata.ChooseLevel.filter())
async def process_choose_level(callback: CallbackQuery, callback_data: cbdata.ChooseLevel):

    await callback.answer()


@router.callback_query(F.data == "exit")
async def procces_delete_message(callback: CallbackQuery):
    await callback.message.delete()
