from src.prettybot.bot.messages.handlers import msghandlers
from src.config import pbconfig


def get_handlers_routes(
        bot_commands_handler: msghandlers.CommandsHandler,
        bot_content_types_handler: msghandlers.ContentTypesHandler):
    command_handlers_routes = {
        'start': bot_commands_handler.handle_start,
        'help': bot_commands_handler.handle_help,
        'restart': bot_commands_handler.handle_restart,
        'en': bot_commands_handler.handle_change_lang,
        'ru': bot_commands_handler.handle_change_lang,
        'end': bot_commands_handler.handle_stop_chatting}

    content_types_routes = {
        'photo': bot_content_types_handler.handle_photo,
        'text': bot_content_types_handler.handle_text
    }

    return dict(command_handlers_routes=command_handlers_routes,
                content_types_routes=content_types_routes)
