import aiogram

from src.prettybot.bot.messages import chat_interaction
from src.prettybot.bot.messages.botmessages import botmessages
from src.prettybot.bot.messages.handlers.eventhandlers import event_handler

from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.dbassistant.registrations import registration_data_handler

from src.prettybot.bot.callback.callback_keyboards import *
from src.config.recording_stages import *


class CommandsHandler:
    database_operation_assistant: database_assistant.Database
    message_sender: chat_interaction.MessageSender
    message_deleter: chat_interaction.MessageDeleter
    large_message_renderer: botmessages.MainMessagesRenderer
    registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(self, bot_event_handler: event_handler.BotEventHandler):
        self.__dict__ = {param: bot_event_handler.__dict__[param]
                         for param in bot_event_handler.__dict__
                         if param in CommandsHandler.__annotations__}

    async def handle_start(self, message: aiogram.types.Message, user_id: int, user_lang_code: str):
        user_recording_condition = self.database_operation_assistant.get_recording_condition(user_id=user_id)
        if user_recording_condition.object:
            recording, record_type, record_stage = user_recording_condition.object

            if recording:
                if record_type in MAIN_REGISTRATION_TYPE:
                    await self.large_message_renderer.render_disappearing_message(
                        user_id=user_id,
                        retrievable_message_id=message.message_id,
                        description=STATEMENTS_BY_LANG[user_lang_code].help,
                        delay_before_deleting=LONG_DELAY
                    )

                else:
                    self.database_operation_assistant.stop_recording(user_id=user_id)
                    await self.large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)

            else:
                await self.large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)

        else:
            self.database_operation_assistant.add_new_user(user_id=user_id,
                                                           fname=message.from_user.first_name,
                                                           lname=message.from_user.last_name,
                                                           telegname=message.chat.username,
                                                           date_message=message.date
                                                           )

            await self.large_message_renderer.render_main_message(
                user_id=user_id,
                description=BASE_STATEMENTS.welcome.format(message.from_user.first_name))

    async def handle_help(self, message: aiogram.types.Message, user_id: int, user_lang_code: str):
        await self.large_message_renderer.render_disappearing_message(
            user_id=user_id,
            retrievable_message_id=message.message_id,
            description=STATEMENTS_BY_LANG[user_lang_code].help,
            delay_before_deleting=MEDIUM_DELAY)

    async def handle_restart(self, *args):
        await self.large_message_renderer.delete_main_message(user_id=args[1])
        self.database_operation_assistant.delete_user_records(user_id=args[1])

    async def handle_change_lang(self, message: aiogram.types.Message, user_id: int, _: str):
        self.database_operation_assistant.change_user_lang(user_id=user_id, lang_code=message.text[1:3])
        await self.large_message_renderer.render_disappearing_message(
            user_id=user_id,
            retrievable_message_id=message.message_id,
            description=STATEMENTS_BY_LANG[message.text[1:3]].change_lang_good,
            delay_before_deleting=DEFAULT_DELAY
        )

    async def handle_stop_chatting(self, message: aiogram.types.Message, user_id: int, user_lang_code: str):
        if self.database_operation_assistant.get_chatting_condition(user_id=user_id).object:
            self.database_operation_assistant.stop_chatting(user_id=user_id)
            await coroutine_executor.execute_coros(
                self.large_message_renderer.render_profile(
                    user_id=user_id,
                    user_lang_code=user_lang_code),
                self.large_message_renderer.render_disappearing_message(
                    user_id=user_id,
                    retrievable_message_id=message.message_id,
                    description=STATEMENTS_BY_LANG[user_lang_code].end_chatting,
                    delay_before_deleting=DEFAULT_DELAY
                ))
