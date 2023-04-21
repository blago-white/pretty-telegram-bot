import aiogram

from .events.handlers.commands_handler import CommandsHandler
from .events.handlers.content_types_handler import ContentTypesHandler
from .keyboards import callback_factories
from .events.handlers.callback_handler import CallbackHandler
from .events.states.registrations import InitialRegistration, AccountRegistration, WishesRegistration
from .events.states.chatting import Chatting
from .events.filters.chat_type import UserChatTypeFilter
from .events.filters.state import UserNotChattingFilter


def registrate_handlers(dispatcher: aiogram.Dispatcher,
                        commands_handler: CommandsHandler,
                        content_types_handler: ContentTypesHandler,
                        callback_handler: CallbackHandler) -> None:

    dispatcher.register_callback_query_handler(
        callback_handler.handle_profile_calls, callback_factories.PROFILE_CALLS.filter(), state='*'
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_change_calls, callback_factories.CHANGING_CALLS.filter(), state='*'
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_change_calls, callback_factories.WISH_CHANGING_CALS.filter(), state='*'
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_finding_cals, callback_factories.FINDING_CALS.filter(), state='*'
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_finding_cals, callback_factories.FINDING_MENU_CALS.filter(), state='*'
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_sex_call, callback_factories.SEX_CALLS.filter(), state='*'
    )
    dispatcher.register_callback_query_handler(
        callback_handler.handle_buffering_call, callback_factories.BUFFERING_CALLS.filter(), state='*'
    )

    dispatcher.register_message_handler(commands_handler.handle_start,
                                        UserChatTypeFilter(chat_type='private'),
                                        commands=['start'],
                                        state=[None, *AccountRegistration.states, *AccountRegistration.states])

    dispatcher.register_message_handler(commands_handler.handle_help,
                                        UserChatTypeFilter(chat_type='private'),
                                        UserNotChattingFilter(dispatcher=dispatcher, state=Chatting.ischatting),
                                        commands=['help'], state='*')
    dispatcher.register_message_handler(commands_handler.handle_restart,
                                        UserChatTypeFilter(chat_type='private'),
                                        UserNotChattingFilter(dispatcher=dispatcher, state=Chatting.ischatting),
                                        commands=['restart'], state='*')
    dispatcher.register_message_handler(commands_handler.handle_change_lang,
                                        UserChatTypeFilter(chat_type='private'),
                                        UserNotChattingFilter(dispatcher=dispatcher, state=Chatting.ischatting),
                                        commands=['ru', 'en'], state='*')
    dispatcher.register_message_handler(commands_handler.handle_stop_chatting,
                                        UserChatTypeFilter(chat_type='private'),
                                        commands=['end'], state='*')

    dispatcher.register_message_handler(content_types_handler.handle_photo,
                                        UserChatTypeFilter(chat_type='private'),
                                        content_types=['photo'],
                                        state=[InitialRegistration.pht,
                                               AccountRegistration.pht])

    dispatcher.register_message_handler(content_types_handler.handle_text,
                                        UserChatTypeFilter(chat_type='private'),
                                        content_types=['text'],
                                        state=[*InitialRegistration.states[:-1],
                                               *AccountRegistration.states[:-1],
                                               *WishesRegistration.states])

    dispatcher.register_message_handler(content_types_handler.handle_conversation_text,
                                        UserChatTypeFilter(chat_type='private'),
                                        state=Chatting.ischatting,
                                        content_types=['text'],
                                        )

    dispatcher.register_message_handler(content_types_handler.handle_useless_message,
                                        UserChatTypeFilter(chat_type='private'),
                                        content_types=['photo'],
                                        state=[None,
                                               *InitialRegistration.states[:-1],
                                               *AccountRegistration.states[:-1],
                                               *WishesRegistration.states])

    dispatcher.register_message_handler(content_types_handler.handle_useless_message,
                                        UserChatTypeFilter(chat_type='private'),
                                        content_types=['text'],
                                        state=[None, InitialRegistration.pht, AccountRegistration.pht])
