import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.etc.config import LANG_STATEMENTS, LANG_CODES
from src.bot.bin import dataclass
from src.bot.db import dbscripts
from src.bot.module import message_manager

inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change'], callback_data='main%change_profile_data')
inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_creator'], url='https://vk.com/l0ginoff')
inline_btn3 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_del_acc'], callback_data='main%del_annotations')
inline_profile_kb = InlineKeyboardMarkup(row_width=1)

inline_profile_kb.add(inline_btn1, inline_btn3, inline_btn2)

inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_photo'],
                                   callback_data='change%change_photo')

inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_age'],
                                   callback_data='change%change_age')

inline_btn3 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_city'],
                                   callback_data='change%change_city')

inline_btn4 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_description'],
                                   callback_data='change%change_description')

inline_btn5 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_back'],
                                   callback_data='change%back')

inline_kb_change_prof = InlineKeyboardMarkup(row_width=2)
inline_kb_change_prof.add(inline_btn2, inline_btn3, inline_btn4, inline_btn1, inline_btn5)

inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_en_lang'], callback_data='lang%en_lang_select')
inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_ru_lang'], callback_data='lang%ru_lang_select')
inline_lang_kb = InlineKeyboardMarkup(row_width=2)
inline_lang_kb.add(inline_btn1, inline_btn2)

inline_empty_kb = InlineKeyboardMarkup()


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

    async def process_callback_by_id(
            self,
            payload: dict,
            ids: int,
            idquery: int,
            message: int,
            alert_text=None) -> dataclass.ResultOperation:
        """

        :param payload: payload from callback query
        :param ids: integer id tg
        :param idquery: integer id query
        :param message: aiogram message
        :param alert_text: string, alert text

        :retuens: Dataclasses.ResultOperation object

        """
        if alert_text:
            await self._bot.answer_callback_query(idquery, text=text, show_alert=True)

        else:
            await self._bot.answer_callback_query(idquery)

        type_request, type_requested_operation = payload.values()

        if type_request == 'main':
            if type_requested_operation == 'change_profile_data':
                await self.change_markup(ids=ids, messageid=message, markup=inline_kb_change_prof)

            elif type_requested_operation == 'del_annotations':
                self._db_scripts.del_user_annotations(ids=ids)

        elif type_request == 'change':

            if type_requested_operation != 'back':
                await self.change_markup(ids=ids,
                                         messageid=message,
                                         markup=inline_empty_kb)

            if type_requested_operation == 'change_photo':
                await self._message_manager.sender(ids, description=LANG_STATEMENTS['en']['q_new_photo'])

            elif type_requested_operation == 'change_age':
                await self._message_manager.sender(ids, description=LANG_STATEMENTS['en']['q_new_age'])

            elif type_requested_operation == 'change_city':
                await self._message_manager.sender(ids, description=LANG_STATEMENTS['en']['q_new_city'])

            elif type_requested_operation == 'change_description':
                await self._message_manager.sender(ids, description=LANG_STATEMENTS['en']['q_new_desc'])

            elif type_requested_operation == 'back':
                await self.change_markup(ids=ids,
                                         messageid=message,
                                         markup=inline_profile_kb)

        elif type_request == 'lang':

            lang_code = LANG_CODES[type_requested_operation]

            self._db_scripts.set_user_lang(ids=ids, lang_code=lang_code)

            select_lang_msg_id = int(self._db_scripts.get_main_message(ids=ids, type_message=1).object)

            self._db_scripts.del_main_message_from_db(ids=ids, type_message=1)

            await self._message_manager.message_scavenger(ids=ids, idmes=select_lang_msg_id)
            await self._message_manager.sender(ids=ids,
                                               description=LANG_STATEMENTS[lang_code]['entry_registration']
                                               )

    async def render_profile(
            self,
            ids: int,
            name: str,
            age: int,
            city: str,
            desc: str,
            photo: str,
            keyboard: aiogram.types.InlineKeyboardMarkup) -> dataclass.ResultOperation:
        """

        :param ids: integer id tg
        :param name:
        :param age:
        :param city:
        :param desc:
        :param photo:
        :param keyboard: aiogram inline keyboard

        :retuens: Dataclasses.ResultOperation object

        """

        declination = 'лет'

        if age % 10 == 1:
            declination = 'год'

        elif 1 < age % 10 < 5:
            declination = 'года'

        text = LANG_STATEMENTS['en']['profile_templ'].format(name=name,
                                                             age=age,
                                                             declination=declination,
                                                             city=city.capitalize(),
                                                             desc=desc
                                                             )

        await self._message_manager.photo_sender(ids=ids,
                                                 photo=photo,
                                                 description=text,
                                                 keyboard=keyboard)

        return dataclass.ResultOperation()

    async def change_markup(self, ids: int, messageid: int, markup: InlineKeyboardMarkup):
        await self._bot.edit_message_reply_markup(chat_id=ids, message_id=messageid, reply_markup=markup)
