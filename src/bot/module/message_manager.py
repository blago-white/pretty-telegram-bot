import aiogram
from aiogram.types import ParseMode
from src.etc.config import LANG_STATEMENTS
from src.bot.bin import dataclass

__all__ = ['send_reply_message', 'photo_sender', 'sender', 'send_except_message', 'message_scavenger']


class MessageManage:
    bot: aiogram.Bot

    def __init__(self, bot: aiogram.Bot):
        self.bot = bot

    @staticmethod
    async def send_reply_message(
            message: aiogram.types.Message,
            description: str = None,
            parse_mode: aiogram.types.ParseMode = ParseMode.HTML) -> dataclass.ResultOperation:
        """
        :param message: aiogram message instance
        :param description: string, sending with photo
        :param parse_mode: telegram parsemode, default = HTML

        :returns: Dataclass.ResultOperation
        """

        try:
            sending_response = await message.reply(description, parse_mode=parse_mode)
            return dataclass.ResultOperation(sending_response.message_id)

        except:
            return dataclass.ResultOperation(status=False, description='sending error')

    async def photo_sender(
            self,
            ids: int,
            photo: str,
            description: str = None,
            parse_mode: aiogram.types.ParseMode = ParseMode.HTML,
            keyboard: aiogram.types.InlineKeyboardMarkup = None) -> dataclass.ResultOperation:
        """
        :param ids: integer, user id
        :param photo: string, telegram id of file photo
        :param description: string, description to photo
        :param parse_mode: telegram parsemode, default = HTML
        :param keyboard: reply inline keyboard, sending with photo

        :returns: Dataclass.ResultOperation
        """

        try:
            if keyboard:
                sending_response = await self.bot.send_photo(chat_id=ids,
                                                             photo=photo,
                                                             caption=description,
                                                             reply_markup=keyboard,
                                                             parse_mode=parse_mode)

            else:
                sending_response = await self.bot.send_photo(chat_id=ids,
                                                             photo=photo,
                                                             caption=description,
                                                             parse_mode=parse_mode)

            return dataclass.ResultOperation(object=sending_response.message_id)

        except:
            return dataclass.ResultOperation(status=False, description='sending error')

    async def sender(
            self,
            ids: int,
            description: str = None,
            parse_mode: aiogram.types.ParseMode = ParseMode.HTML,
            markup: aiogram.types.InlineKeyboardMarkup = None
    ) -> dataclass.ResultOperation:
        """
        :param ids: integer, user id
        :param description: string, sending with photo
        :param parse_mode: telegram parsemode, default = HTML
        :param markup: telegram markup, sended with message

        :returns: Dataclass.ResultOperation
        """

        try:
            sending_response = await self.bot.send_message(chat_id=ids,
                                                           text=description,
                                                           parse_mode=parse_mode,
                                                           reply_markup=markup)

            return dataclass.ResultOperation(object=sending_response.message_id)

        except Exception as e:
            print(e, '---')
            return dataclass.ResultOperation(status=False, description='sender error')

    async def send_except_message(
            self,
            ids: int,
            description: str = None,
            markup: aiogram.types.InlineKeyboardMarkup = None,
            parse_mode: aiogram.types.ParseMode = ParseMode.HTML) -> dataclass.ResultOperation:
        """
        :param ids: integer, user id
        :param description: string, default = 'sorry, there was a problem, please try again later!'
        :param parse_mode: telegram parsemode, default = HTML

        :returns: Dataclass.ResultOperation
        """

        if description is None:
            description = LANG_STATEMENTS['en']['fatal_err']

        if markup:
            sending_response = await self.bot.send_message(ids,
                                                           LANG_STATEMENTS['en']['exception_templ'].format(description),
                                                           parse_mode=parse_mode,
                                                           reply_markup=markup)

        else:
            sending_response = await self.bot.send_message(ids,
                                                           LANG_STATEMENTS['en']['exception_templ'].format(description),
                                                           parse_mode=parse_mode)

        return dataclass.ResultOperation(object=sending_response.message_id)

    async def message_scavenger(
            self,
            ids: int,
            idmes: list[int]) -> dataclass.ResultOperation:
        """

        :param ids: telegram id of user
        :param idmes: id of the message you want to delete, integer or list of integers

        :returns: Dataclass.ResultOperation

        """

        try:
            if type(idmes) is not int:
                response = [await self.bot.delete_message(ids, idms) for idms in idmes]

                if None in response:
                    return dataclass.ResultOperation(status=False, description='deliting error')

                return dataclass.ResultOperation()

            response = await self.bot.delete_message(ids, idmes)
            if not response:
                return dataclass.ResultOperation(status=False, description='deliting error')

            return dataclass.ResultOperation()

        except Exception as e:
            print('! ' + str(e))
            return dataclass.ResultOperation(status=False, description=str(e))
