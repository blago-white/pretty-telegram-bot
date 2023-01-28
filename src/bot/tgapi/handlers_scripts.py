"""
Main file of _bot with handlers
"""

import aiogram

from src.bot.module import message_manager
from src.bot.module import callbacks
from src.bot.db import dbscripts
from src.bot.tgapi import bot_scripts
from src.etc.config import STATEMENT_FOR_STAGE, LANG_STATEMENTS, STAGE_BY_PAYLOAD


class MessageHandlers:
    _db_scripts: dbscripts.Database
    _callback_handler: callbacks
    _message_manager: message_manager.MessageManage
    _bot: aiogram.Bot = None

    def __init__(self, scripts_class_instance: dbscripts.Database, bot: aiogram.Bot):
        self._bot = bot
        self._db_scripts = scripts_class_instance

        self._message_manager = message_manager.MessageManage(bot=self._bot)

        self._callback_handler = callbacks.CallbacksHandler(db_scripts=self._db_scripts,
                                                            bot=self._bot,
                                                            message_manager_=self._message_manager)

    # juyhnjhgbhjhyhnhjhyhy87y676y677yu97887u8797878989u87yuty7gtygtt66y756tr]

    async def process_callback_button(self, callback_query: aiogram.types.CallbackQuery):
        """

        all callbacks handled by this func

        """

        payload = self._callback_handler.unpack(payload_string=callback_query.data)
        user_id = callback_query.from_user.id

        await self._callback_handler.process_callback_by_id(payload=payload,
                                                            ids=user_id,
                                                            idquery=callback_query.id,
                                                            message=callback_query.message.message_id)

        if payload.get('type_request') == 'lang':
            self._db_scripts.change_state_logging(ids=user_id, logtype=1, logstage=1)

        elif payload.get('type_requested_operation') in STAGE_BY_PAYLOAD.keys():
            stage = STAGE_BY_PAYLOAD[payload.get('type_requested_operation')]

            response = self._db_scripts.change_state_logging(ids=user_id,
                                                             logtype=2,
                                                             logstage=stage
                                                             )

            if not response.status:
                await self._message_manager.send_except_message(ids=user_id)

        return

    async def send_sex_messages(self, message: aiogram.types.Message):
        if message.chat.type == 'private':

            user_id = message.from_user.id

            data = self._db_scripts.get_logging_info(ids=user_id)

            if data.object[0]:

                data = data.object

                if len(data) != 3:
                    await self._message_manager.send_except_message(ids=user_id,
                                                                    description=LANG_STATEMENTS['en'][
                                                                        'start_warn'])

                    return

                _, type_logging, stage_logging = data

                if data[0] and type_logging == 1 and stage_logging == 3:
                    response = bot_scripts.get_statement_by_stage(message=message,
                                                                  logstage=stage_logging,
                                                                  db_scripts=self._db_scripts)

                    if response.status:
                        dbresponse = self._db_scripts.record_user_data_by_stage(
                            ids=user_id,
                            message_text=True if message.text == '/man' else False,
                            logstage=stage_logging
                        )

                        if not dbresponse.status:
                            await self._message_manager.send_except_message(ids=user_id)

                        self._db_scripts.change_state_logging(ids=user_id,
                                                              logtype=type_logging,
                                                              logstage=stage_logging + 1)

                    if response.object:
                        await self._message_manager.sender(ids=user_id,
                                                           description=response.object)

                await self._message_manager.message_scavenger(ids=user_id,
                                                              idmes=message.message_id - 1)

            else:
                await self._message_manager.send_except_message(ids=user_id,
                                                                description=LANG_STATEMENTS['en'][
                                                                    'start_warn'])

            await self._message_manager.message_scavenger(ids=user_id,
                                                          idmes=message.message_id)

    async def send_welcome(self, message: aiogram.types.Message):
        if message.chat.type == 'private':

            user_id = message.from_user.id
            states = self._db_scripts.get_logging_info(ids=user_id)

            if not states.status:
                await self._message_manager.send_except_message(ids=user_id)
                return

            if not states.object:
                response = self._db_scripts.init_user(ids=user_id,
                                                      fname=message.from_user.first_name,
                                                      lname=message.from_user.last_name,
                                                      telegname=message.chat.username,
                                                      date_message=message.date
                                                      )

                if not response.status:
                    await self._message_manager.send_except_message(ids=user_id)
                    return

                self._db_scripts.add_main_message_to_db(ids=user_id, id_message=message.message_id + 2, type_message=1)

                await self._message_manager.sender(ids=user_id,
                                                   description=LANG_STATEMENTS['en']['welcome'].format(
                                                       message.from_user.first_name),
                                                   )

                print('---1')

                await self._message_manager.sender(ids=user_id,
                                                   description=LANG_STATEMENTS['en']['select_lang'],
                                                   markup=callbacks.inline_lang_kb,
                                                   )

                print('---2')

            elif states.object:
                if states.object[0]:

                    await self._message_manager.message_scavenger(ids=user_id,
                                                                  idmes=message.message_id - 1,
                                                                  )

                    await self._message_manager.send_except_message(ids=user_id,
                                                                    description=LANG_STATEMENTS['en'][
                                                                        'continue_warn'].format(
                                                                        STATEMENT_FOR_STAGE[
                                                                            states.object[2]])
                                                                    )

                else:
                    await self._message_manager.sender(ids=user_id,
                                                       description=LANG_STATEMENTS['en'][
                                                           'welcome_back'])

                    await self.render_profile(user_id=user_id, id_profile_message=message.message_id + 1)

            await self._message_manager.message_scavenger(ids=user_id,
                                                          idmes=message.message_id,
                                                          )

    async def handle_photo(self, message: aiogram.types.Message):
        if message.chat.type == 'private':

            user_id = message.from_user.id
            data = self._db_scripts.get_logging_info(ids=user_id)

            if not data.status or len(data.object) < 2:
                await self._message_manager.send_except_message(ids=user_id)
                return

            try:
                logging, type_logging, stage_logging = data.object

            except:
                await self._message_manager.send_except_message(ids=user_id)
                return

            if logging:
                if stage_logging == 5:
                    photo_id = message.photo[0]['file_id']

                    statement_response = bot_scripts.get_statement_by_stage(
                        db_scripts=self._db_scripts,
                        message=message,
                        logstage=stage_logging,
                    )

                    if statement_response.status:
                        self._db_scripts.record_user_data_by_stage(ids=user_id,
                                                                   message_text=photo_id,
                                                                   logstage=stage_logging,
                                                                   update=True if type_logging == 2 else False)

                        await self.render_profile(user_id=user_id, id_profile_message=message.message_id + 1)
                        self._db_scripts.change_state_logging(ids=user_id, stop_logging=True)

                    await self._message_manager.message_scavenger(ids=user_id,
                                                                  idmes=message.message_id - 1)

                else:

                    states = self._db_scripts.get_logging_info(ids=user_id)

                    await self._message_manager.sender(ids=user_id,
                                                       description=LANG_STATEMENTS['en'][
                                                           'continue_warn'].format(
                                                           STATEMENT_FOR_STAGE[states.object[2]]
                                                       ))

                    await self._message_manager.message_scavenger(ids=user_id,
                                                                  idmes=message.message_id - 1,
                                                                  )

            await self._message_manager.message_scavenger(ids=message.from_user.id,
                                                          idmes=message.message_id)

    async def text_handler(self, message: aiogram.types.Message):
        if message.chat.type == 'private':

            user_id = message.from_user.id
            user_logging_data = self._db_scripts.get_logging_info(ids=user_id)

            if not user_logging_data.status or len(user_logging_data.object) < 3:
                await self._message_manager.send_except_message(ids=user_id)
                return

            if not user_logging_data.object:
                await self._message_manager.send_except_message(ids=user_id,
                                                                description=LANG_STATEMENTS['en']['start_warn'])

                return

            _, type_logging, stage_logging = user_logging_data.object

            if user_logging_data.object[0] and stage_logging != 0:

                statement = bot_scripts.get_statement_by_stage(message=message,
                                                               logstage=stage_logging,
                                                               db_scripts=self._db_scripts)

                if statement.status:

                    self._db_scripts.record_user_data_by_stage(ids=user_id,
                                                               message_text=message.text,
                                                               logstage=stage_logging)

                    if type_logging == 1:
                        if statement.object:
                            await self._message_manager.sender(ids=user_id,
                                                               description=statement.object
                                                               )

                            self._db_scripts.change_state_logging(ids=user_id,
                                                                  logtype=type_logging,
                                                                  logstage=stage_logging + 1)

                    if type_logging == 2:
                        await self.render_profile(user_id=user_id, id_profile_message=message.message_id + 1)
                        self._db_scripts.change_state_logging(ids=user_id, stop_logging=True)

                else:
                    if statement.object:
                        await self._message_manager.send_except_message(ids=user_id,
                                                                        description=statement.object)

                await self._message_manager.message_scavenger(ids=user_id,
                                                              idmes=message.message_id - 1)

            await self._message_manager.message_scavenger(ids=user_id,
                                                          idmes=message.message_id)

    async def render_profile(self, user_id: int, id_profile_message: int):

        user_data: dict = self._db_scripts.get_user_entry(ids=user_id).object
        user, photo, first_name = user_data.get('info_users'), user_data.get('photos'), user_data.get('users')
        first_name = first_name[1]
        photo = photo[1]

        main_msg_id = self._db_scripts.get_main_message(ids=user_id, type_message=0)

        if main_msg_id.object:
            self._db_scripts.del_main_message_from_db(ids=user_id, type_message=0)
            await self._message_manager.message_scavenger(ids=user_id,
                                                          idmes=main_msg_id.object,
                                                          )

        account_body = bot_scripts.get_profile_body(name=first_name,
                                                    age=user[1],
                                                    city=user[3],
                                                    desc=user[-1]).object

        sending_result = await self._message_manager.photo_sender(ids=user_id,
                                                                  photo=photo,
                                                                  description=account_body,
                                                                  keyboard=callbacks.inline_profile_kb)

        if not sending_result.status:
            return

        else:
            self._db_scripts.add_main_message_to_db(ids=user_id,
                                                    id_message=id_profile_message,
                                                    type_message=0)
