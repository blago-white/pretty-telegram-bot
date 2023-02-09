import aiogram

from src.conf.config import STAGE_BY_PAYLOAD, STATEMENTS_BY_LANG
from src.bot.simple import dataclass
from src.bot.db import database_assistant
from src.bot.telegram.script import message_manager
from src.bot.telegram.script.helper_bot_scripts import HelperScripts
from src.bot.callback.callback_keyboards import (inline_profile_kb_by_lang,
                                                 inline_kb_change_prof_by_lang,
                                                 inline_kb_set_sex_by_lang,
                                                 inline_empty_kb,
                                                 inline_kb_mode_finding_by_lang,
                                                 inline_kb_change_params_by_lang)


def unpack_playload(payload_string: str) -> dict:
    return dict(type_request=payload_string.split('%')[0],
                type_requested_operation=payload_string.split('%')[1])


def get_inline_keyboard_by_stage(stage: int):
    if stage == 2:
        return inline_kb_set_sex_by_lang

    else:
        return inline_empty_kb


class CallbackHandler:
    _database_operation_assistant: database_assistant.Database
    bot: aiogram.Bot
    _message_sender: message_manager.MessageSender
    _bot_helper_scripts: HelperScripts

    def __init__(
            self,
            database_operation_assistant: database_assistant.Database,
            bot: aiogram.Bot,
            message_sender: message_manager.MessageSender,
            bot_helper_scripts: HelperScripts
    ):

        if not (type(database_operation_assistant) == database_assistant.Database
                and type(bot) == aiogram.Bot
                and type(message_sender) == message_manager.MessageSender
                and type(bot_helper_scripts) == HelperScripts):
            raise ValueError('Not correct type of given to __init__ arguments check type hints')

        self._database_operation_assistant = database_operation_assistant
        self.bot = bot
        self._message_sender = message_sender
        self._bot_helper_scripts = bot_helper_scripts

    async def process_callback_by_id(
            self,
            payload: dict,
            ids: int,
            idquery: int,
            message: int,
            user_lang_code: str,
            stage_logging: int = None,
            type_logging: int = None,
            alert_text=None) -> dataclass.ResultOperation:

        """

        :param payload: payload from callback query
        :param ids: integer id tg
        :param idquery: integer id query
        :param message: aiogram message
        :param user_lang_code: user-language
        :param stage_logging: stage of logging user
        :param type_logging: type of logging user
        :param alert_text: string, alert text

        :retuens: Dataclasses.ResultOperation object

        """

        print(payload)

        if alert_text:
            await self.bot.answer_callback_query(idquery, text=text, show_alert=True)

        else:
            await self.bot.answer_callback_query(idquery)

        type_request, type_requested_operation = payload.values()
        sending_response = None

        if type_request == 'main':
            if type_requested_operation == 'change_profile_data':
                await self.bot.edit_message_reply_markup(chat_id=ids,
                                                         message_id=message,
                                                         reply_markup=inline_kb_change_prof_by_lang[user_lang_code])

            elif type_requested_operation == 'start_find':
                response_sending = await self._message_sender.send(
                    user_id=ids,
                    description=STATEMENTS_BY_LANG[user_lang_code].clarify,
                    markup=inline_kb_mode_finding_by_lang[user_lang_code]
                )
                print('----', response_sending.__dict__)

                self._database_operation_assistant.add_main_message_to_db(ids=ids,
                                                                          id_message=response_sending.object,
                                                                          type_message=1
                                                                          )

                await self._bot_helper_scripts.delete_main_message(user_id=ids,
                                                                   type_message=0)

            elif type_requested_operation == 'back':
                await self._bot_helper_scripts.render_profile(user_id=ids,
                                                              user_lang_code=user_lang_code)

                await self._bot_helper_scripts.delete_main_message(user_id=ids,
                                                                   type_message=1)

        elif type_request in ('change', 'changewish'):

            if type_requested_operation != 'back':
                await self.bot.edit_message_reply_markup(chat_id=ids,
                                                         message_id=message,
                                                         reply_markup=inline_empty_kb)

            if type_requested_operation == 'change_photo':
                sending_response = await self._message_sender.send(user_id=ids,
                                                                   description=STATEMENTS_BY_LANG[
                                                                       user_lang_code
                                                                   ].q_new_photo
                                                                   )

            elif type_requested_operation == 'change_age':
                sending_response = await self._message_sender.send(user_id=ids,
                                                                   description=STATEMENTS_BY_LANG[
                                                                       user_lang_code
                                                                   ].q_new_age
                                                                   )

            elif type_requested_operation == 'change_city':
                sending_response = await self._message_sender.send(user_id=ids,
                                                                   description=STATEMENTS_BY_LANG[
                                                                       user_lang_code
                                                                   ].q_new_city
                                                                   )

            elif type_requested_operation == 'change_description':
                sending_response = await self._message_sender.send(ids,
                                                                   description=STATEMENTS_BY_LANG[
                                                                       user_lang_code
                                                                   ].q_new_desc
                                                                   )

            elif type_requested_operation == 'back':
                await self.bot.edit_message_reply_markup(chat_id=ids,
                                                         message_id=message,
                                                         reply_markup=inline_profile_kb_by_lang[user_lang_code])

            if type_requested_operation in STAGE_BY_PAYLOAD.keys():
                stage = STAGE_BY_PAYLOAD[payload.get('type_requested_operation')]

                self._database_operation_assistant.change_state_logging(ids=ids,
                                                                        logtype=2 if type_request == 'change' else 3,
                                                                        logstage=stage
                                                                        )

        elif type_request == 'sex':
            if not stage_logging:
                return

            self._database_operation_assistant.record_user_data_by_stage(
                ids=ids,
                message_text=self._bot_helper_scripts.convert_sex_type(message),
                logstage=stage_logging,
                logtype=type_logging
            )

            await self._bot_helper_scripts.delete_main_message(user_id=ids,
                                                               type_message=1)

            response_sending = await self._message_sender.send(user_id=ids,
                                                               description=STATEMENTS_BY_LANG[
                                                                   user_lang_code
                                                               ].q_desc
                                                               )

            self._database_operation_assistant.add_main_message_to_db(ids=ids,
                                                                      id_message=response_sending.object,
                                                                      type_message=1)

            self._database_operation_assistant.change_state_logging(ids=ids,
                                                                    logtype=1,
                                                                    logstage=stage_logging + 1)

        elif type_request == 'find':
            if type_requested_operation == 'start':
                searching_settings = self._database_operation_assistant.get_user_wishes(ids=ids)
                finded_people = self._database_operation_assistant.get_users_by_params(age_range=searching_settings[0],
                                                                                       city=searching_settings[1],
                                                                                       sex=searching_settings[2])

                print(finded_people)

            if type_requested_operation == 'clarify':
                sending_response = await self._message_sender.send(user_id=ids,
                                                                   description=self._bot_helper_scripts.get_change_params(
                                                                       user_id=ids,
                                                                       user_lang_code=user_lang_code
                                                                   ),
                                                                   markup=inline_kb_change_params_by_lang[
                                                                       user_lang_code])

            if type_requested_operation == 'back':
                await self._bot_helper_scripts.delete_main_message(user_id=ids,
                                                                   type_message=1)

                await self.process_callback_by_id(payload=unpack_playload('main%start_find'),
                                                  ids=ids,
                                                  idquery=idquery,
                                                  message=message,
                                                  user_lang_code=user_lang_code,
                                                  stage_logging=stage_logging
                                                  )

                return

            await self._bot_helper_scripts.delete_main_message(user_id=ids, type_message=1)

        if sending_response:
            if sending_response.object:
                self._database_operation_assistant.add_main_message_to_db(ids=ids,
                                                                          id_message=sending_response.object,
                                                                          type_message=1)
