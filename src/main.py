from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config import load_config
from handler import user, command_handler, callbacks
from start_menu import set_bot_menu


import logging

# Логгер
logger = logging.getLogger(__name__)

# TODO:
# 1) menu commands DONE
# 2) add more lexicon DONE
# 3) level choose
#    TODO:
#        1) who will move first DONE
#        2) inteleggent for bot
# 4) seprate handlers DONE
# 5) logger for handlers
# 6) made normal form for database IMPOSSIBLE


if __name__ == '__main__':
    # получение конфигурация
    config = load_config(".env")

    # базывые конфиги для логгера
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Хранилище 
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    # сам бот и корневый дистпечер
    bot = Bot(config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    

    logger.info("Bot is starting")

    # Установка меню
    dp.startup.register(set_bot_menu)

    # добавление дочерних роутеров
    dp.include_router(router=command_handler.router)
    dp.include_router(router=user.router)
    dp.include_router(router=callbacks.router)
    

    # удаление прошлых апдейтов и запуск бота
    bot.delete_webhook(drop_pending_updates=True)
    dp.run_polling(bot)