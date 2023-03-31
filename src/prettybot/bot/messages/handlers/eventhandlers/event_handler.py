"""
Main file of _bot with handlers
"""

import aiogram

from src.prettybot.bot.messages import chat_interaction
from src.prettybot.bot.messages.handlers import user_answer_handlers
from src.prettybot.bot.minorscripts import minor_scripts
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.dbassistant.registrations import registration_data_handler
from src.prettybot.bot.messages.botmessages import botmessages
from src.prettybot.bot.asyncioscripts import coroutine_executor

from src.prettybot.bot.callback.callback_keyboards import *
from src.config.recording_stages import *


class EventHandlersFields:
    _database_operation_assistant: database_assistant.Database
    _bot: aiogram.Bot
    _message_sender: chat_interaction.MessageSender
    _message_deleter: chat_interaction.MessageDeleter
    _large_message_renderer: botmessages.MainMessagesRenderer
    _registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(
            self,
            database_operation_assistant: database_assistant.Database,
            bot: aiogram.Bot,
            message_sender: chat_interaction.MessageSender,
            message_deleter: chat_interaction.MessageDeleter,
            large_message_renderer: botmessages.MainMessagesRenderer,
            registration_data_handler_: registration_data_handler.RegistrationParamsHandler):
        if not (type(database_operation_assistant) == database_assistant.Database
                and type(bot) == aiogram.Bot
                and type(message_sender) == chat_interaction.MessageSender
                and type(message_deleter) == chat_interaction.MessageDeleter
                and type(large_message_renderer) == botmessages.MainMessagesRenderer
                and type(registration_data_handler_) == registration_data_handler.RegistrationParamsHandler):
            raise ValueError('Not correct type of given to __init__ arguments check type hints')

        self._database_operation_assistant = database_operation_assistant
        self._bot = bot
        self._message_sender = message_sender
        self._message_deleter = message_deleter
        self._large_message_renderer = large_message_renderer
        self._registration_data_handler = registration_data_handler_

