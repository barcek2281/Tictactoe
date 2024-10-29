from aiogram import Bot
from aiogram.types import BotCommand
from lexicon import LEXICON

async def set_bot_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command='/start',
                   description=LEXICON["MENU"]["START"]),
        BotCommand(command='/again',
                   description=LEXICON["MENU"]["AGAIN"]),
        BotCommand(command="/setting",
                   description=LEXICON["MENU"]["SETTING"]),
    ]


    await bot.set_my_commands(main_menu_commands)