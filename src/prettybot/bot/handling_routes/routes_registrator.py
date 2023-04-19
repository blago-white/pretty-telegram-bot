import aiogram
from aiogram.dispatcher.filters.builtin import CommandStart
from ..callback import callback_factories
from ..events.handlers.eventhandlers.callback_handler import CallbackHandler
from ..events import catchers


def registrate_handlers(dispatcher: aiogram.Dispatcher,
                        message_catcher: catchers.MessageCatcher,
                        callback_handler: CallbackHandler,
                        tracked_commands: dict,
                        tracked_content_types: dict) -> None:

    dispatcher.register_callback_query_handler(
        callback_handler.handle_profile_calls, callback_factories.PROFILE_CALLS.filter()
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_change_calls, callback_factories.CHANGING_CALLS.filter()
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_change_calls, callback_factories.WISH_CHANGING_CALS.filter()
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_finding_cals, callback_factories.FINDING_CALS.filter()
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_finding_cals, callback_factories.FINDING_MENU_CALS.filter()
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_sex_call, callback_factories.SEX_CALLS.filter()
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_buffering_call, callback_factories.BUFFERING_CALLS.filter()
    )

    for command in tracked_commands.values():
        dispatcher.register_message_handler(message_catcher.catche_message, commands=[*command])

    for content_type in tracked_content_types.values():
        dispatcher.register_message_handler(message_catcher.catche_message, content_types=[*content_type])

