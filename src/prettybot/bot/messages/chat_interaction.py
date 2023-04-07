import aiogram
from aiogram.types import ParseMode

from src.prettybot.dataclass import dataclass

from src.config.pbconfig import *

__all__ = ['ChatMessagesInteractor']


class ChatMessagesInteractor:
    bot: aiogram.Bot
    _INVALID_MESSAGE_ID = -1

    def __init__(self, bot: aiogram.Bot):
        self.bot = bot

    async def send_photo(
            self,
            user_id: int,
            photo_id: str,
            description: str = None,
            parse_mode: aiogram.types.ParseMode = ParseMode.HTML,
            keyboard: aiogram.types.InlineKeyboardMarkup = None) -> dataclass.ResultOperation:

        """
        :param user_id: integer, user id
        :param photo_id: string, bot id of file photo
        :param description: string, description to photo
        :param parse_mode: bot parsemode, default = HTML
        :param keyboard: reply inline keyboard, sending with photo

        :rtype ResultOperation class
        :returns: sended message id
        """
        try:
            if keyboard:
                sending_response = await self.bot.send_photo(chat_id=user_id,
                                                             photo=photo_id,
                                                             caption=description,
                                                             reply_markup=keyboard,
                                                             parse_mode=parse_mode)

            else:
                sending_response = await self.bot.send_photo(chat_id=user_id,
                                                             photo=photo_id,
                                                             caption=description,
                                                             parse_mode=parse_mode)

            return dataclass.ResultOperation(object=sending_response.message_id)

        except Exception as exception:
            return dataclass.ResultOperation(status=False,
                                             object=self._INVALID_MESSAGE_ID,
                                             description=f'sending error')

    async def send(
            self,
            user_id: int,
            description: str = None,
            parse_mode: aiogram.types.ParseMode = ParseMode.HTML,
            markup: aiogram.types.InlineKeyboardMarkup = None
    ) -> dataclass.ResultOperation:

        """
        :param user_id: integer, user id
        :param description: string, sending with photo_id
        :param parse_mode: bot parsemode, default = HTML
        :param markup: bot markup, sended with message

        :rtype ResultOperation class
        :returns: sended message id
        """

        try:
            sending_response = await self.bot.send_message(chat_id=user_id,
                                                           text=description,
                                                           parse_mode=parse_mode,
                                                           reply_markup=markup)

            return dataclass.ResultOperation(object=sending_response.message_id)

        except Exception as e:
            return dataclass.ResultOperation(status=False,
                                             object=self._INVALID_MESSAGE_ID,
                                             description=e)

    async def send_except_message(
            self,
            user_id: int,
            description: str = None,
            user_lang_code: str = DEFAULT_LANG,
            markup: aiogram.types.InlineKeyboardMarkup = None,
            parse_mode: aiogram.types.ParseMode = ParseMode.HTML) -> dataclass.ResultOperation:

        """
        :param user_id: integer, user id
        :param description: string, default = 'sorry, there was a problem, please try again later!'
        :param user_lang_code: lang code of user defaul - en
        :param markup: inline markup
        :param parse_mode: bot parsemode, default = HTML

        :rtype ResultOperation class
        :returns: sended message id
        """

        if description is None:
            description = STATEMENTS_BY_LANG[user_lang_code].fatal_err

        if markup:
            sending_response = await self.bot.send_message(user_id,
                                                           BASE_STATEMENTS.exception_templ.format(description),
                                                           parse_mode=parse_mode,
                                                           reply_markup=markup)

        else:
            sending_response = await self.bot.send_message(user_id,
                                                           BASE_STATEMENTS.exception_templ.format(description),
                                                           parse_mode=parse_mode)

        return dataclass.ResultOperation(object=sending_response.message_id)

    async def delete_message(
            self,
            user_id: int,
            message_id: list[int]) -> dataclass.ResultOperation:

        """

        :param user_id: bot id of user
        :param message_id: id of the message you want to delete, integer or list of integers

        :rtype ResultOperation class
        :returns: result of deleting

        """
        try:
            if type(message_id) is not int:
                response = [await self.bot.delete_message(user_id, msg_id) for msg_id in message_id]

                if None in response:
                    return dataclass.ResultOperation(status=False, description='deliting error')

                return dataclass.ResultOperation()

            response = await self.bot.delete_message(user_id, message_id)

            if not response:
                return dataclass.ResultOperation(status=False, description='deliting error')

            return dataclass.ResultOperation()

        except Exception as e:
            return dataclass.ResultOperation(status=False, description=str(e))

