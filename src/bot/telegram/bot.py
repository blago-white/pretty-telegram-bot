import aiogram

from src.bot.telegram import handlers
from src.bot.telegram import routes
from src.bot.telegram.script import message_manager
from src.bot.telegram.script import helper_bot_scripts
from src.bot.callback import callbacks

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

    message_sender = message_manager.MessageSender(bot=bot)
    message_deleter = message_manager.MessageDeleter(aiogram_bot=bot)

    helper_scripts = helper_bot_scripts.HelperScripts(database_scripts=db_scripts,
                                                      message_deleter=message_deleter,
                                                      message_sender=message_sender)

    message_handlers = handlers.MessageHandler(database_operation_assistant=db_scripts,
                                               message_sender=message_sender,
                                               message_deleter=message_deleter,
                                               bot_helper_scripts_=helper_scripts)

    callback_handler = callbacks.CallbackHandler(database_operation_assistant=db_scripts,
                                                 bot=bot,
                                                 message_sender=message_sender,
                                                 bot_helper_scripts=helper_scripts)

    callback_handlers = handlers.CallbackHandler(database_operation_assistant=db_scripts,
                                                 callback_handler=callback_handler)

    routes.registrate_handlers(dispatcher=dp,
                               message_handlers_cls=message_handlers,
                               callback_handlers_cls=callback_handlers)

    start_dispatcher(dp=dp)
