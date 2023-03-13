import aiogram

from src.prettybot.bot.messages.handlers import msghandlers
from src.prettybot.bot.messages.handlers.prehandler import MessagePreHandler


class CallbackCatcher:
    callback_handler: msghandlers.CallbackHandler

    def __init__(self, callback_handler):
        self.callback_handler = callback_handler

    async def callback(self, callback_query: aiogram.types.CallbackQuery):
        await self.callback_handler.handle_callback(
            callback_query=callback_query
        )


class MessageCatcher:
    content_type_handler: msghandlers.ContentTypesHandler
    commands_handler: msghandlers.CommandsHandler
    prehandler: MessagePreHandler
    command_handlers_routes: dict
    content_type_handlers_routes: dict

    def __init__(
            self, content_type_handler: msghandlers.ContentTypesHandler,
            commands_handler: msghandlers.CommandsHandler,
            prehandler: MessagePreHandler,
            command_handlers_routes: dict,
            content_type_handlers_routes=dict):
        self.content_type_handler = content_type_handler
        self.commands_handler = commands_handler
        self.prehandler = prehandler
        self.command_handlers_routes = command_handlers_routes
        self.content_type_handlers_routes = content_type_handlers_routes

    async def _start_handling_command(self, message: aiogram.types.Message, command_name: str):
        try:
            await self.prehandler.prehandle(
                handler_func=self.command_handlers_routes[message.text[1:]],
                message=message
            )
        except KeyError:
            await self._start_handling_by_content_type(message=message)

    async def _start_handling_by_content_type(self, message: aiogram.types.Message):
        await self.prehandler.prehandle(
                handler_func=self.content_type_handlers_routes[message.content_type],
                message=message
            )

    async def catche_message(self, message: aiogram.types.Message):
        if message.entities and message.entities[0].type == 'bot_command':
            command_name = message.text[1:]
            await self._start_handling_command(message=message, command_name=command_name)

        else:
            await self._start_handling_by_content_type(message=message)
