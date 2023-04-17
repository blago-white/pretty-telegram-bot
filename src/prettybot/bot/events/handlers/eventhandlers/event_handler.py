import aiogram

from ... import chat_interactor
from ...botmessages import botmessages

from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.dbassistant.registrations import registration_data_handler


class EventHandlersFields:
    _database_operation_assistant: database_assistant.Database
    _bot: aiogram.Bot
    _message_interactor: chat_interactor.ChatMessagesInteractor
    _large_message_renderer: botmessages.MainMessagesRenderer
    _registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(
            self,
            database_operation_assistant: database_assistant.Database,
            bot: aiogram.Bot,
            message_interactor: chat_interactor.ChatMessagesInteractor,
            large_message_renderer: botmessages.MainMessagesRenderer,
            registration_data_handler_: registration_data_handler.RegistrationParamsHandler):
        self._database_operation_assistant = database_operation_assistant
        self._bot = bot
        self._message_interactor = message_interactor
        self._large_message_renderer = large_message_renderer
        self._registration_data_handler = registration_data_handler_

