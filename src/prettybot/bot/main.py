import aiogram

from src.prettybot.bot import routes
from src.prettybot.bot.messages import handlers, catchers, tgmessages

from src.prettybot.bot.db import registration_data_handler
from src.prettybot.bot.db import large_messages
from src.prettybot.bot.messages import prehandler

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

    prehandler_ = prehandler.PreHandler(database_assistant=db_scripts)

    message_sender = tgmessages.MessageSender(bot=bot)
    message_deleter = tgmessages.MessageDeleter(aiogram_bot=bot)

    large_message_renderer = large_messages.LargeMessageRenderer(
        database_operation_assistant=db_scripts,
        message_deleter=message_deleter,
        message_sender=message_sender
    )

    large_message_generator = large_messages.LargeMessageTextGenerator(
        database_operation_assistant=db_scripts
    )

    registration_data_handler_ = registration_data_handler.RegistrationDataHandler(
        database_operation_assistant=db_scripts
    )

    event_handler = handlers.BotEventHandler(database_operation_assistant=db_scripts,
                                             bot=bot,
                                             message_sender=message_sender,
                                             message_deleter=message_deleter,
                                             large_message_renderer=large_message_renderer,
                                             large_message_generator=large_message_generator,
                                             registration_data_handler_=registration_data_handler_)

    command_handler = handlers.CommandHandler(bot_event_handler=event_handler)
    content_type_handler = handlers.ContentTypeHandler(bot_event_handler=event_handler)
    callback_handler = handlers.CallbackHandler(bot_event_handler=event_handler)

    commands_catcher = catchers.CommandsCatcher(
        commands_handlers=command_handler,
        prehandler=prehandler_
    )

    content_type_catcher = catchers.ContentTypeCatcher(
        content_type_handler=content_type_handler,
        prehandler=prehandler_
    )

    callback_catcher = catchers.CallbackCatcher(
        callback_handler=callback_handler
    )

    routes.registrate_handlers(dispatcher=dp,
                               commands_catcher=commands_catcher,
                               content_types_catcher=content_type_catcher,
                               callback_catcher=callback_catcher)

    start_dispatcher(dp=dp)
