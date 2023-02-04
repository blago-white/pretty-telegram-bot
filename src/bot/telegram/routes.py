import aiogram
from src.bot.telegram import handlers


def registrate_handlers(dispatcher: aiogram.dispatcher, bot: handlers.EventHandler):
    
    dispatcher.register_callback_query_handler(bot.process_callback_button, lambda call: call.data)

    dispatcher.register_message_handler(bot.change_language, commands=['en', 'ru'])
    
    dispatcher.register_message_handler(bot.send_welcome, commands=['start'])
    
    dispatcher.register_message_handler(bot.handler_help, commands=['help'])
    
    dispatcher.register_message_handler(bot.restart, commands=['restart'])
    
    dispatcher.register_message_handler(bot.handle_photo, content_types=['photo'])
    
    dispatcher.register_message_handler(bot.text_handler, content_types=['text'])
