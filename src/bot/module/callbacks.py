import aiogram

from src.etc.config import LANG_STATEMENTS, LANG_CODES, DEFAULT_LANG
from src.bot.bin import dataclass
from src.bot.db import dbscripts
from src.bot.module import message_manager
from src.bot.module.callback_keyboards import (inline_profile_kb_by_lang,
                                               inline_kb_change_prof_by_lang,
                                               inline_empty_kb,
                                               inline_markup_by_stage)


class CallbacksHandler:
    _db_scripts: dbscripts.Database
    _bot: aiogram.Bot
    _message_manager: message_manager.MessageManage

    def __init__(
            self,
            db_scripts: dbscripts.Database,
            bot: aiogram.Bot,
            message_manager_: message_manager.MessageManage):

        self._db_scripts = db_scripts
        self._bot = bot
        self._message_manager = message_manager_

    @staticmethod
    def unpack(payload_string: str) -> dict:
        return dict(type_request=payload_string.split('%')[0],
                    type_requested_operation=payload_string.split('%')[1])

    @staticmethod
    def get_inline_kb_by_stage(stage_logging: int):
        return inline_markup_by_stage[stage_logging]

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
        :param alert_text: string, alert text

        :retuens: Dataclasses.ResultOperation object

        """

        if alert_text:
            await self._bot.answer_callback_query(idquery, text=text, show_alert=True)

        else:
            await self._bot.answer_callback_query(idquery)

        type_request, type_requested_operation = payload.values()
        sending_response = None

        if type_request == 'main':
            if type_requested_operation == 'change_profile_data':
                await self.change_markup(ids=ids,
                                         messageid=message,
                                         markup=inline_kb_change_prof_by_lang[user_lang_code])

            elif type_requested_operation == 'del_annotations':
                self._db_scripts.del_user_annotations(ids=ids)
                await self._message_manager.message_scavenger(ids=ids, idmes=message)

        elif type_request == 'change':

            if type_requested_operation != 'back':
                await self.change_markup(ids=ids,
                                         messageid=message,
                                         markup=inline_empty_kb)

            if type_requested_operation == 'change_photo':
                sending_response = await self._message_manager.sender(ids,
                                                                      description=LANG_STATEMENTS[
                                                                          user_lang_code]['q_new_photo']
                                                                      )

            elif type_requested_operation == 'change_age':
                sending_response = await self._message_manager.sender(ids,
                                                                      description=LANG_STATEMENTS[
                                                                          user_lang_code]['q_new_age']
                                                                      )

            elif type_requested_operation == 'change_city':
                sending_response = await self._message_manager.sender(ids,
                                                                      description=LANG_STATEMENTS[
                                                                          user_lang_code]['q_new_city']
                                                                      )

            elif type_requested_operation == 'change_description':
                sending_response = await self._message_manager.sender(ids,
                                                                      description=LANG_STATEMENTS[
                                                                          user_lang_code]['q_new_desc']
                                                                      )

            elif type_requested_operation == 'back':
                await self.change_markup(ids=ids,
                                         messageid=message,
                                         markup=inline_profile_kb_by_lang[user_lang_code])

        elif type_request == 'sex':
            if not stage_logging:
                return

            self._db_scripts.record_user_data_by_stage(
                ids=ids,
                message_text=True if type_requested_operation == 'man' else False,
                logstage=stage_logging
            )

        if sending_response:
            if sending_response.object:
                self._db_scripts.add_main_message_to_db(ids=ids,
                                                        id_message=sending_response.object,
                                                        type_message=1)

    async def change_markup(self, ids: int, messageid: int, markup: aiogram.types.InlineKeyboardMarkup):
        await self._bot.edit_message_reply_markup(chat_id=ids, message_id=messageid, reply_markup=markup)
