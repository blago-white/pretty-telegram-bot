import aiogram

from . import commands_handler, content_types_handler, callback_handler

from ... import chat_interactor
from ...botmessages import botmessages

from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.dbassistant.registrations.registration_data_handler import RegistrationParamsHandler


class EventsHandler:
    def __init__(
            self,
            database_operation_assistant: database_assistant.BotDatabase,
            bot: aiogram.Bot,
            message_interactor: chat_interactor.ChatMessagesInteractor,
            large_message_renderer: botmessages.MainMessagesRenderer,
            registration_data_handler: RegistrationParamsHandler):

        self.command_handler = commands_handler.CommandsHandler(
            database_operation_assistant=database_operation_assistant,
            large_message_renderer=large_message_renderer
        )
        self.content_types_handler = content_types_handler.ContentTypesHandler(
            database_operation_assistant=database_operation_assistant,
            message_interactor=message_interactor,
            large_message_renderer=large_message_renderer,
            registration_data_handler=registration_data_handler
        )
        self.callback_handler = callback_handler.CallbackHandler(
            database_operation_assistant=database_operation_assistant,
            bot=bot,
            large_message_renderer=large_message_renderer,
            registration_data_handler=registration_data_handler
        )
