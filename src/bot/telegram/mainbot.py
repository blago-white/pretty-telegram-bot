import aiogram

from src.bot.telegram import handlers
from src.bot.telegram import routes

"""

1. create back button
2. add functionality button delete acc
3. renaming
3. commit push & tagging
4. add wishes form 
5. add simple mode (without deleting messages)

""" 


def start_dispatcher(dp: aiogram.Dispatcher):
    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)


def start_bot(db_scripts, bot_token: str):
    try:
        bot = aiogram.Bot(token=bot_token)
        dp = aiogram.Dispatcher(bot)

    except Exception as exeption:
        raise exeption

    handlers_ = handlers.EventHandler(scripts_class_instance=db_scripts, aiogram_bot=bot)
    routes.registrate_handlers(dispatcher=dp, bot=handlers_)
    start_dispatcher(dp=dp)

