import aiogram

from .handling_routes import routes_registrator, handlers_routes
from .events import catchers, chat_interactor
from .events.botmessages import botmessages
from .events.handlers import prehandler
from .events.handlers.eventhandlers import event_handler, command_handlers, content_type_handlers, callback_handler
from .dbassistant.registrations import registration_data_handler

from src.config import pbconfig


def start_bot(db_scripts, bot_token: str):
    try:
        bot = aiogram.Bot(token=bot_token)
        dp = aiogram.Dispatcher(bot)

    except Exception as exeption:
        raise exeption

    message_interactor = chat_interactor.ChatMessagesInteractor(bot=bot)

    prehandler_ = prehandler.MessagePreHandler(database_assistant_=db_scripts, message_interactor=message_interactor)

    large_message_renderer = botmessages.MainMessagesRenderer(
        database_operation_assistant=db_scripts,
        main_message_text_generator=botmessages.MainMessageTextGenerator(database_operation_assistant=db_scripts),
        message_interactor=message_interactor
    )

    registration_data_handler_ = registration_data_handler.RegistrationParamsHandler(
        database_operation_assistant=db_scripts
    )

    handlers_fields = event_handler.EventHandlersFields(database_operation_assistant=db_scripts,
                                                        bot=bot,
                                                        message_interactor=message_interactor,
                                                        large_message_renderer=large_message_renderer,
                                                        registration_data_handler_=registration_data_handler_)

    command_handler = command_handlers.CommandsHandler(bot_handlers_fields=handlers_fields)
    content_type_handler = content_type_handlers.ContentTypesHandler(bot_handlers_fields=handlers_fields)
    callback_handler_ = callback_handler.CallbackHandler(bot_handlers_fields=handlers_fields)

    routes = handlers_routes.get_handlers_routes(
        bot_commands_handler=command_handler,
        bot_content_types_handler=content_type_handler
    )

    message_catcher = catchers.MessageCatcher(
        content_type_handler=content_type_handler,
        prehandler=prehandler_,
        command_handlers_routes=routes['command_handlers_routes'],
        content_type_handlers_routes=routes['content_types_routes']
    )

    callback_catcher = catchers.CallbackCatcher(
        callback_handler_=callback_handler_
    )

    routes_registrator.registrate_handlers(dispatcher=dp,
                                           message_catcher=message_catcher,
                                           callback_catcher=callback_catcher,
                                           tracked_commands=pbconfig.BOT_COMMANDS,
                                           tracked_content_types=pbconfig.BOT_CONTENT_TYPES)

    _start_dispatcher(dp=dp)


def _start_dispatcher(dp: aiogram.Dispatcher):
    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)
