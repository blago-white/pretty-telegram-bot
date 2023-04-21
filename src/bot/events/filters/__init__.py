from aiogram.dispatcher.dispatcher import Dispatcher
from .chat_type import UserChatTypeFilter
from .state import UserNotChattingFilter
from ...events.handlers.commands_handler import CommandsHandler


def setup(dispatcher: Dispatcher):
    dispatcher.filters_factory.bind(UserChatTypeFilter)
    dispatcher.filters_factory.bind(UserNotChattingFilter,
                                    event_handlers=[CommandsHandler.handle_help,
                                                    CommandsHandler.handle_start,
                                                    CommandsHandler.handle_restart,
                                                    CommandsHandler.handle_change_lang])
