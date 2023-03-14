import aiogram

from src.prettybot.bot.messages import chat_interaction
from src.prettybot.bot.messages.handlers import user_answer_handlers
from src.prettybot.bot.messages.botmessages import botmessages
from src.prettybot.bot.messages.handlers.eventhandlers import event_handler

from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.dbassistant.registrations import registration_data_handler

from src.prettybot.bot.minorscripts import supportive

from src.config.recording_stages import *


class ContentTypesHandler:
    database_operation_assistant: database_assistant.Database
    message_sender: chat_interaction.MessageSender
    message_deleter: chat_interaction.MessageDeleter
    large_message_renderer: botmessages.MainMessagesRenderer
    registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(self, bot_event_handler: event_handler.BotEventHandler):
        self.__dict__ = {param: bot_event_handler.__dict__[param]
                         for param in bot_event_handler.__dict__
                         if param in ContentTypesHandler.__annotations__}

    async def handle_photo(self, message: aiogram.types.Message, user_id: int, user_lang_code: str) -> None:
        recording, record_type, record_stage = self.database_operation_assistant.get_recording_condition(
            user_id=user_id
        ).object

        file_id = message.photo[0]['file_id']
        if recording and record_stage == STAGES_RECORDING[4]:
            self.registration_data_handler.record_user_param(
                user_id=user_id,
                message_payload=file_id,
                record_stage=record_stage,
                record_type=record_type)

            await self.large_message_renderer.render_profile(
                user_id=user_id,
                user_lang_code=user_lang_code,
            )

            self.database_operation_assistant.stop_recording(user_id=user_id)

    async def handle_text(self, message: aiogram.types.Message, user_id: int, user_lang_code: str) -> None:
        if self.database_operation_assistant.get_chatting_condition(user_id=user_id).object:
            """in future on this place be methods to re-send message to friend of user"""

            await self.message_sender.send(user_id=message.from_user.id,
                                           description=message.text)

            return

        user_recording_data = self.database_operation_assistant.get_recording_condition(user_id=user_id)

        if not user_recording_data.object:
            return

        recording, record_type, record_stage = user_recording_data.object
        if recording:
            statement_for_stage = user_answer_handlers.handle_message(message_text=message.text,
                                                                      user_lang_code=user_lang_code,
                                                                      record_type=record_type,
                                                                      cities=self.database_operation_assistant.all_cities,
                                                                      record_stage=record_stage)

            inline_markup_for_stage = supportive.get_inline_keyboard_by_stage(recordstage=record_stage,
                                                                              recordtype=record_type)

            if statement_for_stage.status:
                self.registration_data_handler.record_user_param(user_id=user_id,
                                                                 message_payload=message.text,
                                                                 record_stage=record_stage,
                                                                 record_type=record_type)

                if record_type == TYPE_RECORDING[0] and record_stage:
                    await self.large_message_renderer.render_main_message(user_id=user_id,
                                                                          description=statement_for_stage.object,
                                                                          markup=inline_markup_for_stage[user_lang_code]
                                                                          )

                    self.database_operation_assistant.increase_recording_stage(user_id=user_id)

                elif record_type == TYPE_RECORDING[1]:
                    await self.large_message_renderer.render_profile(
                        user_id=user_id,
                        user_lang_code=user_lang_code)

                    self.database_operation_assistant.stop_recording(user_id=user_id)

                elif record_type == TYPE_RECORDING[2]:
                    await self.large_message_renderer.render_finding_message(
                        user_id=user_id,
                        user_lang_code=user_lang_code)

            elif not statement_for_stage.status and statement_for_stage.object:
                await self.large_message_renderer.render_main_message(
                    user_id=user_id,
                    description=statement_for_stage.object,
                    markup=inline_markup_for_stage[user_lang_code],
                    with_warn=True
                )
