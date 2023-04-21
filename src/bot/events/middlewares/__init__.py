from aiogram.dispatcher.dispatcher import Dispatcher

from .text_middleware import TextMiddleware
from src.bot.utils.chat_interactor import ChatMessagesInteractor


def setup(dispatcher: Dispatcher, message_interactor: ChatMessagesInteractor):
    dispatcher.middleware.setup(middleware=TextMiddleware(chat_interactor=message_interactor, dispatcher=dispatcher))
