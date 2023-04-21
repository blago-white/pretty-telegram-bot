import asyncio

import aiogram

from src.bot.utils.messages_renderer import MainMessagesRenderer

from src.bot.dbassistant.database_assistant import BotDatabase
from src.bot.events.states import registrations, chatting
from src.bot.config.recording_stages import *


class CommandsHandler:
    def __init__(self, database_operation_assistant: BotDatabase, large_message_renderer: MainMessagesRenderer):
        self._database_operation_assistant = database_operation_assistant
        self._large_message_renderer = large_message_renderer

    async def handle_start(
            self, message: aiogram.types.Message,
            state: aiogram.dispatcher.FSMContext):
        user_id = message.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

        user_recording_condition = await state.get_state()

        if self._database_operation_assistant.user_exist(user_id=user_id):
            recording = bool(user_recording_condition)
            record_type, record_stage = None, None
            if recording:
                record_type, record_stage = (
                    TYPE_RECORDING_BY_STATE_GROUP[user_recording_condition.split(':')[0]],
                    user_recording_condition.split(':')[-1]
                )

            if recording and record_type == MAIN_RECORDING_TYPE:
                await self._large_message_renderer.render_disappearing_message(
                    user_id=user_id,
                    description=STATEMENTS_BY_LANG[user_lang_code].help,
                    delay_before_deleting=LONG_DELAY
                )
            else:
                if recording:
                    await state.finish()

                await self._large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)

        else:
            self._database_operation_assistant.add_new_user(
                user_id=user_id,
                fname=message.from_user.first_name,
                lname=message.from_user.last_name,
                telegname=message.chat.username,
                date_message=message.date
            )

            await self._large_message_renderer.render_main_message(
                user_id=user_id,
                description=BASE_STATEMENTS.welcome.format(message.from_user.first_name)
            )
            await state.set_state(state=registrations.InitialRegistration.age)

    async def handle_help(self, message: aiogram.types.Message, **_):
        user_id = message.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)
        await self._large_message_renderer.render_disappearing_message(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[user_lang_code].help,
            delay_before_deleting=MEDIUM_DELAY)

    async def handle_restart(self, message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
        user_id = message.from_user.id
        await self._large_message_renderer.delete_main_message_from_all(user_id=user_id)
        self._database_operation_assistant.delete_user_records(user_id=user_id)
        await state.reset_state()

    async def handle_change_lang(
            self, message: aiogram.types.Message,
            state: aiogram.dispatcher.FSMContext):
        user_id = message.from_user.id
        lang_code = message.text[1:3]
        self._database_operation_assistant.change_user_lang(user_id=user_id, lang_code=lang_code)
        await self._large_message_renderer.render_disappearing_message(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[lang_code].change_lang_good,
            delay_before_deleting=DEFAULT_DELAY
        )

    async def handle_stop_chatting(
            self, message: aiogram.types.Message,
            state: aiogram.dispatcher.FSMContext):
        user_id = message.from_user.id
        interlocutor_id = (await state.get_data())['interlocutor_id']
        message_send_tasks = list()

        for telegram_id in (user_id, interlocutor_id):
            await chatting.Chatting.ischatting.finish(user_id=telegram_id)
            lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=interlocutor_id)
            message_send_tasks.append(
                asyncio.create_task(
                    self._large_message_renderer.render_profile(user_id=telegram_id, user_lang_code=lang_code)
                ))
            message_send_tasks.append(
                asyncio.create_task(
                    self._large_message_renderer.render_disappearing_message(
                        user_id=telegram_id,
                        description=STATEMENTS_BY_LANG[lang_code].end_chatting,
                        delay_before_deleting=DEFAULT_DELAY)
                ))

        await asyncio.gather(*message_send_tasks)
