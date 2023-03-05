import aiogram
from src.prettybot.bot.messages import catchers
from src.prettybot.bot.messages.prehandler import PreHandler


def registrate_handlers(dispatcher: aiogram.dispatcher,
                        commands_catcher: catchers.CommandsCatcher,
                        content_types_catcher: catchers.ContentTypeCatcher,
                        callback_catcher: catchers.CallbackCatcher) -> None:
    
    dispatcher.register_callback_query_handler(callback_catcher.callback, lambda call: call.data)

    dispatcher.register_message_handler(commands_catcher.change_lang, commands=['en', 'ru'])
    dispatcher.register_message_handler(commands_catcher.start, commands=['start'])
    dispatcher.register_message_handler(commands_catcher.help, commands=['help'])
    dispatcher.register_message_handler(commands_catcher.restart, commands=['restart'])
    dispatcher.register_message_handler(commands_catcher.stop_chatting, commands=['end'])

    dispatcher.register_message_handler(content_types_catcher.photo, content_types=['photo'])
    dispatcher.register_message_handler(content_types_catcher.text, content_types=['text'])
