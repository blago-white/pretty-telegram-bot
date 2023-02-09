import aiogram
from src.bot.telegram import handlers
from src.bot.callback import callbacks


def registrate_handlers(dispatcher: aiogram.dispatcher,
                        message_handlers_cls: handlers.MessageHandler,
                        callback_handlers_cls: callbacks.CallbackHandler):
    
    dispatcher.register_callback_query_handler(callback_handlers_cls.callback_handler, lambda call: call.data)

    dispatcher.register_message_handler(message_handlers_cls.change_language_handler, commands=['en', 'ru'])
    
    dispatcher.register_message_handler(message_handlers_cls.start_handler, commands=['start'])
    
    dispatcher.register_message_handler(message_handlers_cls.help_handler, commands=['help'])
    
    dispatcher.register_message_handler(message_handlers_cls.restart_bot_handler, commands=['restart'])
    
    dispatcher.register_message_handler(message_handlers_cls.handle_photo, content_types=['photo'])
    
    dispatcher.register_message_handler(message_handlers_cls.text_handler, content_types=['text'])
