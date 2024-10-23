from aiogram import Bot
from aiogram.types import BotCommand

async def set_bot_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запуск бота'),
        BotCommand(command='/again',
                   description='Начать занова бота'),
        BotCommand(command="/setting",
                   description="Настройки бота"),
        BotCommand(command='/help',
                   description='Руководство по пониманию игры')
    ]


    await bot.set_my_commands(main_menu_commands)