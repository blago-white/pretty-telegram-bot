import aiogram

from src.prettybot.bot import routes_registrator
from src.prettybot.bot.messages import catchers, chat_interaction
from src.prettybot.bot.dbassistant.registrations import registration_data_handler
from src.prettybot.bot.messages.botmessages import botmessages
from src.prettybot.bot.messages.handlers.eventhandlers import event_handler
from src.prettybot.bot.messages.handlers.eventhandlers import callback_handler
from src.prettybot.bot.messages.handlers.eventhandlers import command_handlers
from src.prettybot.bot.messages.handlers.eventhandlers import content_type_handlers
from src.prettybot.bot.messages.handlers import prehandler
from src.prettybot.bot import handlers_routes
from src.config import pbconfig

"""

1. create back button
2. add functionality button delete acc
3. renaming
3. commit push & tagging
4. add wishes form 
5. add simple mode (without deleting messages)

"""


def start_dispatcher(dp: aiogram.Dispatcher):
    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)


def start_bot(db_scripts, bot_token: str):
    try:
        bot = aiogram.Bot(token=bot_token)
        dp = aiogram.Dispatcher(bot)

    except Exception as exeption:
        raise exeption

    message_sender = chat_interaction.MessageSender(bot=bot)
    message_deleter = chat_interaction.MessageDeleter(aiogram_bot=bot)

    prehandler_ = prehandler.MessagePreHandler(database_assistant_=db_scripts,
                                               message_sender=message_sender,
                                               message_deleter=message_deleter)

    large_message_renderer = botmessages.MainMessagesRenderer(
        database_operation_assistant=db_scripts,
        message_deleter=message_deleter,
        main_message_text_generator=botmessages.MainMessageTextGenerator(database_operation_assistant=db_scripts),
        message_sender=message_sender
    )

    registration_data_handler_ = registration_data_handler.RegistrationParamsHandler(
        database_operation_assistant=db_scripts
    )

    event_handler_ = event_handler.BotEventHandler(database_operation_assistant=db_scripts,
                                                   bot=bot,
                                                   message_sender=message_sender,
                                                   message_deleter=message_deleter,
                                                   large_message_renderer=large_message_renderer,
                                                   registration_data_handler_=registration_data_handler_)

    command_handler = command_handlers.CommandsHandler(bot_event_handler=event_handler_)
    content_type_handler = content_type_handlers.ContentTypesHandler(bot_event_handler=event_handler_)
    callback_handler_ = callback_handler.CallbackHandler(bot_event_handler=event_handler_)

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

    start_dispatcher(dp=dp)
