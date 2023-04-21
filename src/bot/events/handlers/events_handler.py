import aiogram

from . import commands_handler, content_types_handler, callback_handler

from src.bot.utils import messages_renderer, chat_interactor, user_fast_finding_buffer

from src.bot.dbassistant import database_assistant
from src.bot.dbassistant.registrations.registration_data_handler import RegistrationParamsHandler


class EventsHandler:
    def __init__(
            self,
            database_operation_assistant: database_assistant.BotDatabase,
            bot: aiogram.Bot,
            message_interactor: chat_interactor.ChatMessagesInteractor,
            large_message_renderer: messages_renderer.MainMessagesRenderer,
            registration_data_handler: RegistrationParamsHandler,
            fast_users_buffer: user_fast_finding_buffer.UsersFastFindingBuffer,
            dispatcher: aiogram.Dispatcher):

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
            registration_data_handler=registration_data_handler,
            fast_users_buffer=fast_users_buffer,
            dispatcher=dispatcher
        )
