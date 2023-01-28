import aiogram

from src.bot.tgapi import handlers_scripts
from src.bot.bin.jsons import json_getters


"""

1. create back button
2. add functionality button delete acc
3. renaming
3. commit push & tagging
4. add wishes form 
5. add simple mode (without deleting messages)

"""


def registrate_handlers(dp: aiogram.dispatcher, bot: handlers_scripts.MessageHandlers):

    dp.register_callback_query_handler(bot.process_callback_button, lambda c: c.data)

    dp.register_message_handler(bot.send_sex_messages, commands=['man', 'woman'])
    dp.register_message_handler(bot.send_welcome, commands=['start', 'help'])
    dp.register_message_handler(bot.handle_photo, content_types=['photo'])
    dp.register_message_handler(bot.text_handler, content_types=['text'])


def _starting(dp: aiogram.Dispatcher):
    aiogram.executor.start_polling(dp, skip_updates=True)


def start_bot(backend_scripts, bot_token: str):
    try:
        bot = aiogram.Bot(token=bot_token)
        dp = aiogram.Dispatcher(bot)

    except:
        raise BaseException('Error with init _bot')

    handlers_ = handlers_scripts.MessageHandlers(scripts_class_instance=backend_scripts, bot=bot)
    registrate_handlers(dp=dp, bot=handlers_)
    _starting(dp=dp)

