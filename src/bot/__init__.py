import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . import _routes_registrator

from .dbassistant.database_assistant import BotDatabase
from .utils import messages_renderer, chat_interactor, user_fast_finding_buffer
from .events import middlewares
from .events.handlers import events_handler
from .dbassistant.registrations import registration_data_handler
from .events import filters

from .config import pbconfig

__all__ = ['start_bot']


def start_bot(bot_database_assistant: BotDatabase, bot_token: str) -> None:
    tg_bot = _get_bot_instance(token=bot_token)
    dp = _get_dispatcher(bot=tg_bot)

    message_interactor = chat_interactor.ChatMessagesInteractor(bot=tg_bot)

    large_message_renderer = messages_renderer.MainMessagesRenderer(
        database_operation_assistant=bot_database_assistant,
        message_interactor=message_interactor,
        bot=tg_bot
    )

    registration_data_handler_ = registration_data_handler.RegistrationParamsHandler(
        database_operation_assistant=bot_database_assistant
    )

    fast_users_buffer = user_fast_finding_buffer.UsersFastFindingBuffer()

    events_handler_ = events_handler.EventsHandler(database_operation_assistant=bot_database_assistant,
                                                   bot=tg_bot,
                                                   message_interactor=message_interactor,
                                                   large_message_renderer=large_message_renderer,
                                                   registration_data_handler=registration_data_handler_,
                                                   fast_users_buffer=fast_users_buffer,
                                                   dispatcher=dp)

    middlewares.setup(dispatcher=dp, message_interactor=message_interactor)
    filters.setup(dispatcher=dp)

    _routes_registrator.registrate_handlers(dispatcher=dp,
                                            commands_handler=events_handler_.command_handler,
                                            content_types_handler=events_handler_.content_types_handler,
                                            callback_handler=events_handler_.callback_handler)

    _start_dispatcher(dp=dp)


def _get_dispatcher(bot: aiogram.Bot) -> aiogram.Dispatcher:
    try:
        return aiogram.Dispatcher(bot=bot, storage=MemoryStorage())
    except Exception as exception:
        raise exception


def _get_bot_instance(token: str) -> aiogram.Bot:
    try:
        return aiogram.Bot(token=token)
    except Exception as exception:
        raise exception


def _start_dispatcher(dp: aiogram.Dispatcher) -> None:
    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)
