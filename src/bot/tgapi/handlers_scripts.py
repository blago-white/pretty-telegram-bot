"""
Main file of _bot with handlers
"""
import aiogram

from src.bot.module import message_manager
from src.bot.module import callbacks
from src.bot.db import dbscripts
from src.bot.tgapi import helper_bot_scripts
from src.etc.config import (STATEMENT_FOR_STAGE,
                            LANG_STATEMENTS,
                            STAGE_BY_PAYLOAD,
                            TYPES_MAIN_MESSAGES,
                            DEFAULT_LANG,
                            DEFAULT_DELAY,
                            STAGE_BLOCKED_TEXT_MESSAGES)

from src.bot.module import decorators


class MessageHandlers:
    database: dbscripts.Database
    callback_handler: callbacks
    message_manager_: message_manager.MessageManage
    bot_helper_scripts_: helper_bot_scripts.HelperScripts

    def __init__(self, scripts_class_instance: dbscripts.Database, bot: aiogram.Bot):
        self.database = scripts_class_instance

        self.message_manager_ = message_manager.MessageManage(bot=bot)

        self.callback_handler = callbacks.CallbacksHandler(db_scripts=self.database,
                                                           bot=bot,
                                                           message_manager_=self.message_manager_)

        self.bot_helper_scripts_ = helper_bot_scripts.HelperScripts(database_scripts=self.database)

    # juyhnjhgbhjhyhnhjhyhy87y676y677yu97887u8797878989u87yuty7gtygtt66y756tr]

    async def process_callback_button(self, callback_query: aiogram.types.CallbackQuery):
        """

        all callbacks handled by this function

        """

        payload = self.callback_handler.unpack(payload_string=callback_query.data)
        user_id = callback_query.from_user.id
        user_lang_code = self.database.get_user_lang_code(ids=user_id)

        stage_logging = None

        if payload.get('type_request') == 'sex':
            stage_logging = self.database.get_logging_info(ids=user_id).object[-1]

        await self.callback_handler.process_callback_by_id(payload=payload,
                                                           ids=user_id,
                                                           idquery=callback_query.id,
                                                           message=callback_query.message.message_id,
                                                           user_lang_code=user_lang_code,
                                                           stage_logging=stage_logging)

        if payload.get('type_request') == 'sex':
            await self.bot_helper_scripts_.delete_requirement_message(
                message_manager=self.message_manager_,
                user_id=user_id)

            response_sending = await self.message_manager_.sender(ids=user_id,
                                                                  description=LANG_STATEMENTS[
                                                                      user_lang_code
                                                                  ]['q_desc']
                                                                  )

            self.database.add_main_message_to_db(ids=user_id,
                                                 id_message=response_sending.object,
                                                 type_message=1)

            self.database.change_state_logging(ids=user_id,
                                               logtype=1,
                                               logstage=stage_logging + 1)

        if payload.get('type_requested_operation') in STAGE_BY_PAYLOAD.keys():
            stage = STAGE_BY_PAYLOAD[payload.get('type_requested_operation')]

            response = self.database.change_state_logging(ids=user_id,
                                                          logtype=2,
                                                          logstage=stage
                                                          )

            if not response.status:
                await self.message_manager_.send_except_message(ids=user_id)

        return

    @decorators.unpack_message
    async def send_welcome(self, message: aiogram.types.Message, user_id: int):
        user_logging_condition = self.database.get_logging_info(ids=user_id)

        if not user_logging_condition.status:
            await self.message_manager_.send_except_message(ids=user_id)
            return

        if not user_logging_condition.object:
            response = self.database.init_user(ids=user_id,
                                               fname=message.from_user.first_name,
                                               lname=message.from_user.last_name,
                                               telegname=message.chat.username,
                                               date_message=message.date
                                               )

            if not response.status:
                await self.message_manager_.send_except_message(ids=user_id)
                return

            welcome_sending_response = await self.message_manager_.sender(ids=user_id,
                                                                          description=LANG_STATEMENTS[DEFAULT_LANG][
                                                                              'welcome'].format(
                                                                              message.from_user.first_name),
                                                                          )

            entry_sending_response = await self.message_manager_.sender(ids=user_id,
                                                                        description=LANG_STATEMENTS[DEFAULT_LANG][
                                                                            'entry_registration']
                                                                        )

            self.database.add_main_message_to_db(ids=user_id,
                                                 id_message=welcome_sending_response.object,
                                                 type_message=2)

            self.database.add_main_message_to_db(ids=user_id,
                                                 id_message=entry_sending_response.object,
                                                 type_message=1)

        elif user_logging_condition.object:

            user_lang_code = self.database.get_user_lang_code(ids=user_id)
            await self.bot_helper_scripts_.delete_requirement_message(message_manager=self.message_manager_,
                                                                      user_id=user_id)

            if user_logging_condition.object[0]:

                markup = self.callback_handler.get_inline_kb_by_stage(stage_logging=user_logging_condition.object[-1] 
                                                                                    - 1)
                statement = LANG_STATEMENTS[user_lang_code]['continue_warn'].format(STATEMENT_FOR_STAGE[
                                                                                        user_logging_condition.object[2]]
                                                                                    )

                await self.message_manager_.message_scavenger(ids=user_id,
                                                              idmes=message.message_id - 1,
                                                              )

                sending_response = await self.message_manager_.send_except_message(ids=user_id,
                                                                                   description=statement,
                                                                                   markup=markup)

                self.database.add_main_message_to_db(ids=user_id,
                                                     id_message=sending_response.object,
                                                     type_message=1)

            else:
                await self.message_manager_.sender(ids=user_id,
                                                   description=LANG_STATEMENTS[user_lang_code][
                                                       'welcome_back'])

                await self.bot_helper_scripts_.render_profile(user_id=user_id,
                                                              user_lang_code=user_lang_code,
                                                              message_manager=self.message_manager_)

        await self.message_manager_.message_scavenger(ids=user_id,
                                                      idmes=message.message_id,
                                                      )

    @decorators.unpack_message
    async def handle_photo(self, message: aiogram.types.Message, user_id: int):
        user_loging_condition = self.database.get_logging_info(ids=user_id)

        if not user_loging_condition.status or len(user_loging_condition.object) < 2:
            await self.message_manager_.send_except_message(ids=user_id)
            return

        try:
            logging, type_logging, stage_logging = user_loging_condition.object

        except:
            await self.message_manager_.send_except_message(ids=user_id)
            return

        if logging:

            user_lang_code = self.database.get_user_lang_code(ids=user_id)

            if stage_logging == 5:
                photo_id = message.photo[0]['file_id']

                statement_response = self.bot_helper_scripts_.get_statement_by_stage(
                    message=message,
                    logstage=stage_logging,
                    user_lang_code=user_lang_code
                )

                if statement_response.status:
                    self.database.record_user_data_by_stage(ids=user_id,
                                                            message_text=photo_id,
                                                            logstage=stage_logging,
                                                            update=True if type_logging == 2 else False)

                    await self.bot_helper_scripts_.render_profile(user_id=user_id,
                                                                  user_lang_code=user_lang_code,
                                                                  message_manager=self.message_manager_)

                    self.database.change_state_logging(ids=user_id, stop_logging=True)

                await self.bot_helper_scripts_.delete_requirement_message(message_manager=self.message_manager_,
                                                                          user_id=user_id)

            else:

                user_logging_condition = self.database.get_logging_info(ids=user_id)

                await self.message_manager_.send_except_message(ids=user_id,
                                                                description=LANG_STATEMENTS[
                                                                    user_lang_code
                                                                ]['continue_warn'].format(
                                                                    STATEMENT_FOR_STAGE[
                                                                        user_logging_condition.object[2]
                                                                    ]
                                                                ))

                await self.bot_helper_scripts_.delete_requirement_message(message_manager=self.message_manager_,
                                                                          user_id=user_id)

        await self.message_manager_.message_scavenger(ids=message.from_user.id,
                                                      idmes=message.message_id)

    @decorators.unpack_message
    async def text_handler(self, message: aiogram.types.Message, user_id: int):

        user_logging_data = self.database.get_logging_info(ids=user_id)

        if not user_logging_data.status or len(user_logging_data.object) < 3:
            await self.message_manager_.send_except_message(ids=user_id)
            return

        if not user_logging_data.object:
            await self.message_manager_.send_except_message(ids=user_id,
                                                            description=LANG_STATEMENTS[DEFAULT_LANG]['start_warn'])

            return

        _, type_logging, stage_logging = user_logging_data.object
        sending_response = None

        if user_logging_data.object[0]:

            user_lang_code = self.database.get_user_lang_code(ids=user_id)

            statement = self.bot_helper_scripts_.get_statement_by_stage(message=message,
                                                                        logstage=stage_logging,
                                                                        user_lang_code=user_lang_code)

            markup = self.callback_handler.get_inline_kb_by_stage(stage_logging=stage_logging)

            if statement.status:

                self.database.record_user_data_by_stage(ids=user_id,
                                                        message_text=message.text,
                                                        logstage=stage_logging)

                if type_logging == 1:
                    if statement.object:
                        if stage_logging not in STAGE_BLOCKED_TEXT_MESSAGES:
                            sending_response = await self.message_manager_.sender(ids=user_id,
                                                                                  description=statement.object,
                                                                                  markup=markup
                                                                                  )

                            self.database.change_state_logging(ids=user_id,
                                                               logtype=type_logging,
                                                               logstage=stage_logging + 1)

                            await self.bot_helper_scripts_.delete_requirement_message(user_id=user_id,
                                                                                      message_manager=self.message_manager_)

                if type_logging == 2:
                    await self.bot_helper_scripts_.render_profile(user_id=user_id,
                                                                  user_lang_code=user_lang_code,
                                                                  message_manager=self.message_manager_)

                    self.database.change_state_logging(ids=user_id, stop_logging=True)

            else:
                if statement.object:
                    sending_response = await self.message_manager_.send_except_message(ids=user_id,
                                                                                       description=statement.object)

            await self.bot_helper_scripts_.delete_requirement_message(user_id=user_id,
                                                                      message_manager=self.message_manager_)

            if sending_response:
                self.database.add_main_message_to_db(ids=user_id,
                                                     id_message=sending_response.object,
                                                     type_message=1)

        await self.message_manager_.message_scavenger(ids=user_id,
                                                      idmes=message.message_id)

    @decorators.unpack_message
    async def handler_help(self, message: aiogram.types.Message, user_id: int):

        user_lang_code = self.database.get_user_lang_code(ids=user_id)

        await self.message_manager_.sender(ids=user_id,
                                           description=LANG_STATEMENTS[user_lang_code]['help'])

        await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id)

    @decorators.unpack_message
    async def restart(self, message: aiogram.types.Message, user_id: int):

        id_main_messages = [self.database.get_main_message(ids=user_id, type_message=type_message).object
                            for type_message in range(0, max(TYPES_MAIN_MESSAGES) + 1)]

        for id_ in id_main_messages:
            if id_:
                await self.message_manager_.message_scavenger(ids=user_id, idmes=id_)

        self.database.del_user_annotations(ids=user_id)

        await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id)

    @decorators.unpack_message
    async def change_language(self, message: aiogram.types.Message, user_id: int):

        self.database.change_user_lang(ids=user_id, lang_code=message.text[1:3])

        user_lang_code = self.database.get_user_lang_code(ids=user_id)

        await self.message_manager_.sender(ids=user_id,
                                           description=LANG_STATEMENTS[user_lang_code]['change_lang_good'])

        await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id)
        await self.bot_helper_scripts_.start_delay(delay=DEFAULT_DELAY)
        await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id + 1)
