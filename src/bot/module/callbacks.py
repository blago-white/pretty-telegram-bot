import aiogram

from src.etc.config import LANG_STATEMENTS, LANG_CODES, DEFAULT_LANG, STAGE_BY_PAYLOAD
from src.bot.bin import dataclass
from src.bot.db import dbscripts
from src.bot.module import message_manager
from src.bot.tgapi.helper_bot_scripts import HelperScripts
from src.bot.module.callback_keyboards import (inline_profile_kb_by_lang,
                                               inline_kb_change_prof_by_lang,
                                               inline_empty_kb,
                                               inline_kb_set_sex_by_lang,
                                               inline_kb_mode_finding_by_lang,
                                               inline_kb_change_params_by_lang)


class CallbacksHandler:
    db_scripts: dbscripts.Database
    bot: aiogram.Bot
    message_manager_: message_manager.MessageManage
    helper_scripts: HelperScripts

    def __init__(
            self,
            db_scripts: dbscripts.Database,
            bot: aiogram.Bot,
            message_manager_: message_manager.MessageManage,
            bot_helper_scripts
    ):

        self.db_scripts = db_scripts
        self.bot = bot
        self.message_manager_ = message_manager_
        self.helper_scripts = bot_helper_scripts

    @staticmethod
    def unpack(payload_string: str) -> dict:
        return dict(type_request=payload_string.split('%')[0],
                    type_requested_operation=payload_string.split('%')[1])

    async def process_callback_by_id(
            self,
            payload: dict,
            ids: int,
            idquery: int,
            message: int,
            user_lang_code: str,
            stage_logging: int = None,
            alert_text=None) -> dataclass.ResultOperation:
        """

        :param payload: payload from callback query
        :param ids: integer id tg
        :param idquery: integer id query
        :param message: aiogram message
        :param user_lang_code: user-language
        :param stage_logging: stage of logging user
        :param alert_text: string, alert text

        :retuens: Dataclasses.ResultOperation object

        """

        if alert_text:
            await self.bot.answer_callback_query(idquery, text=text, show_alert=True)

        else:
            await self.bot.answer_callback_query(idquery)

        type_request, type_requested_operation = payload.values()
        sending_response = None

        if type_request == 'main':
            if type_requested_operation == 'change_profile_data':
                await self.change_markup(ids=ids,
                                         messageid=message,
                                         markup=inline_kb_change_prof_by_lang[user_lang_code])

            elif type_requested_operation == 'btn_start_find':
                response_sending = await self.message_manager_.sender(ids=ids,
                                                                      description=LANG_STATEMENTS[user_lang_code][
                                                                          'clarify'],
                                                                      markup=inline_kb_mode_finding_by_lang[
                                                                          user_lang_code]
                                                                      )

                self.db_scripts.add_main_message_to_db(ids=ids,
                                                       id_message=response_sending.object,
                                                       type_message=1
                                                       )
                self.db_scripts.del_main_message_from_db(ids=ids,
                                                         type_message=0)

                await self.message_manager_.message_scavenger(ids=ids, idmes=message)

            elif type_requested_operation == 'back':
                await self.helper_scripts.render_profile(message_manager=self.message_manager_,
                                                         user_id=ids,
                                                         user_lang_code=user_lang_code)

                await self.helper_scripts.delete_requirement_message(message_manager=self.message_manager_,
                                                                     user_id=ids)

        elif type_request == 'change':

            if type_requested_operation != 'back':
                await self.change_markup(ids=ids,
                                         messageid=message,
                                         markup=inline_empty_kb)

            if type_requested_operation == 'change_photo':
                sending_response = await self.message_manager_.sender(ids,
                                                                      description=LANG_STATEMENTS[
                                                                          user_lang_code]['q_new_photo']
                                                                      )

            elif type_requested_operation == 'change_age':
                sending_response = await self.message_manager_.sender(ids,
                                                                      description=LANG_STATEMENTS[
                                                                          user_lang_code]['q_new_age']
                                                                      )

            elif type_requested_operation == 'change_city':
                sending_response = await self.message_manager_.sender(ids,
                                                                      description=LANG_STATEMENTS[
                                                                          user_lang_code]['q_new_city']
                                                                      )

            elif type_requested_operation == 'change_description':
                sending_response = await self.message_manager_.sender(ids,
                                                                      description=LANG_STATEMENTS[
                                                                          user_lang_code]['q_new_desc']
                                                                      )

            elif type_requested_operation == 'back':
                await self.change_markup(ids=ids,
                                         messageid=message,
                                         markup=inline_profile_kb_by_lang[user_lang_code])

            if type_requested_operation in STAGE_BY_PAYLOAD.keys():
                stage = STAGE_BY_PAYLOAD[payload.get('type_requested_operation')]

                self.db_scripts.change_state_logging(ids=ids,
                                                     logtype=2,
                                                     logstage=stage
                                                     )

        elif type_request == 'sex':
            if not stage_logging:
                return

            self.db_scripts.record_user_data_by_stage(
                ids=ids,
                message_text=self.helper_scripts.convert_sex_type(message),
                logstage=stage_logging
            )

            await self.helper_scripts.delete_requirement_message(message_manager=self.message_manager_,
                                                                 user_id=ids)

            response_sending = await self.message_manager_.sender(ids=ids,
                                                                  description=LANG_STATEMENTS[
                                                                      user_lang_code
                                                                  ]['q_desc']
                                                                  )

            self.db_scripts.add_main_message_to_db(ids=ids,
                                                   id_message=response_sending.object,
                                                   type_message=1)

            self.db_scripts.change_state_logging(ids=ids,
                                                 logtype=1,
                                                 logstage=stage_logging + 1)

        elif type_request == 'find':
            if type_requested_operation == 'start':
                await self.message_manager_.sender(ids=ids, description='later!')

            if type_requested_operation == 'clarify':
                await self.message_manager_.sender(ids=ids,
                                                   description=self.helper_scripts.get_change_params(
                                                       user_id=ids,
                                                       user_lang_code=user_lang_code
                                                   ),
                                                   markup=inline_kb_change_params_by_lang[user_lang_code])

            if type_requested_operation == 'back':
                await self.helper_scripts.delete_requirement_message(message_manager=self.message_manager_,
                                                                     user_id=ids
                                                                     )

                await self.process_callback_by_id(payload=self.unpack('main%btn_start_find'),
                                                  ids=ids,
                                                  idquery=idquery,
                                                  message=message,
                                                  user_lang_code=user_lang_code,
                                                  stage_logging=stage_logging
                                                  )

                return

            await self.helper_scripts.delete_requirement_message(message_manager=self.message_manager_,
                                                                 user_id=ids)

        if sending_response:
            if sending_response.object:
                self.db_scripts.add_main_message_to_db(ids=ids,
                                                       id_message=sending_response.object,
                                                       type_message=1)

    async def change_markup(self, ids: int, messageid: int, markup: aiogram.types.InlineKeyboardMarkup):
        await self.bot.edit_message_reply_markup(chat_id=ids, message_id=messageid, reply_markup=markup)
