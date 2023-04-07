from src.config import pbconfig
from ..messages.handlers.eventhandlers import command_handlers, content_type_handlers


def get_handlers_routes(
        bot_commands_handler: command_handlers.CommandsHandler,
        bot_content_types_handler: content_type_handlers.ContentTypesHandler):
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
