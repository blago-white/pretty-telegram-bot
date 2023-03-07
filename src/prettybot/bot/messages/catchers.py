import aiogram

from src.prettybot.bot.messages.handlers import msghandlers
from src.prettybot.bot.messages.handlers.prehandler import PreHandler


class CallbackCatcher:
    callback_handler: msghandlers.CallbackHandler

    def __init__(self, callback_handler):
        self.callback_handler = callback_handler

    async def callback(self, callback_query: aiogram.types.CallbackQuery):
        await self.callback_handler.inline_keyboard_callback(
            callback_query=callback_query
        )


class CommandsCatcher:
    commands_handler: msghandlers.CommandHandler
    prehandler: PreHandler

    def __init__(self, commands_handlers: msghandlers.CommandHandler, prehandler: PreHandler):
        self.commands_handler = commands_handlers
        self.prehandler = prehandler

    async def start(self, message: aiogram.types.Message):
        await self.prehandler.prehandle(self.commands_handler.start, message)

    async def help(self, message: aiogram.types.Message):
        await self.prehandler.prehandle(self.commands_handler.help, message)

    async def restart(self, message: aiogram.types.Message):
        await self.prehandler.prehandle(self.commands_handler.restart, message)

    async def change_lang(self, message: aiogram.types.Message):
        await self.prehandler.prehandle(self.commands_handler.change_lang, message)

    async def stop_chatting(self, message: aiogram.types.Message):
        await self.prehandler.prehandle(self.commands_handler.stop_chatting, message)


class ContentTypeCatcher:
    content_type_handler: msghandlers.ContentTypeHandler
    prehandler: PreHandler

    def __init__(self, content_type_handler: msghandlers.ContentTypeHandler, prehandler: PreHandler):
        self.content_type_handler = content_type_handler
        self.prehandler = prehandler

    async def text(self, message: aiogram.types.Message):
        await self.prehandler.prehandle(self.content_type_handler.text, message)

    async def photo(self, message: aiogram.types.Message):
        await self.prehandler.prehandle(self.content_type_handler.photo, message)
