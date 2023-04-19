import aiogram

from .handling_routes import routes_registrator, handlers_routes
from .dbassistant.database_assistant import BotDatabase
from .events import catchers, chat_interactor
from .events.botmessages import botmessages
from .events.handlers import prehandler
from .events.handlers.eventhandlers import events_handler, commands_handler, content_types_handler, callback_handler
from .dbassistant.registrations import registration_data_handler

from ...config import pbconfig

__all__ = ['start_bot']


def start_bot(bot_database_assistant: BotDatabase, bot_token: str) -> None:
    bot = _get_bot_instance(token=bot_token)
    dp = _get_dispatcher(bot=bot)

    message_interactor = chat_interactor.ChatMessagesInteractor(bot=bot)
    prehandler_ = prehandler.MessagePreHandler(database_assistant_=bot_database_assistant,
                                               message_interactor=message_interactor)

    large_message_renderer = botmessages.MainMessagesRenderer(
        database_operation_assistant=bot_database_assistant,
        message_interactor=message_interactor
    )

    registration_data_handler_ = registration_data_handler.RegistrationParamsHandler(
        database_operation_assistant=bot_database_assistant
    )

    events_handler_ = events_handler.EventsHandler(database_operation_assistant=bot_database_assistant,
                                                   bot=bot,
                                                   message_interactor=message_interactor,
                                                   large_message_renderer=large_message_renderer,
                                                   registration_data_handler=registration_data_handler_)

    routes = handlers_routes.get_handlers_routes(
        bot_commands_handler=events_handler_.command_handler,
        bot_content_types_handler=events_handler_.content_types_handler
    )

    message_catcher = catchers.MessageCatcher(
        prehandler=prehandler_,
        command_handlers_routes=routes['command_handlers_routes'],
        content_type_handlers_routes=routes['content_types_routes']
    )

    routes_registrator.registrate_handlers(dispatcher=dp,
                                           message_catcher=message_catcher,
                                           callback_handler=events_handler_.callback_handler,
                                           tracked_commands=pbconfig.BOT_COMMANDS,
                                           tracked_content_types=pbconfig.BOT_CONTENT_TYPES)

    _start_dispatcher(dp=dp)


def _get_dispatcher(bot: aiogram.Bot) -> aiogram.Dispatcher:
    try:
        return aiogram.Dispatcher(bot=bot)
    except Exception as exception:
        raise exception


def _get_bot_instance(token: str) -> aiogram.Bot:
    try:
        return aiogram.Bot(token=token)
    except Exception as exception:
        raise exception


def _start_dispatcher(dp: aiogram.Dispatcher) -> None:
    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)
