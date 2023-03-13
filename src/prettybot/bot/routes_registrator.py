import aiogram
from src.prettybot.bot.messages import catchers


def registrate_handlers(dispatcher: aiogram.dispatcher,
                        message_catcher: catchers.MessageCatcher,
                        callback_catcher: catchers.CallbackCatcher,
                        tracked_commands: dict,
                        tracked_content_types: dict) -> None:

    dispatcher.register_callback_query_handler(callback_catcher.callback, lambda call: call.data)

    for command in tracked_commands.values():
        dispatcher.register_message_handler(message_catcher.catche_message, commands=[*command])

    for content_type in tracked_content_types.values():
        dispatcher.register_message_handler(message_catcher.catche_message, content_types=[*content_type])
