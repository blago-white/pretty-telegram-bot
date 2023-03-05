import re
from typing import Union

from src.prettybot.dataclass import dataclass
from src.prettybot.scripts import auxiliary
from src.prettybot.bot.db import large_messages
from src.conf.recording_stages import TYPE_RECORDING, LENGHT_TYPE_RECORDING_VAL
from src.conf.dbconfig import AMOUNT_CITIES

from src.conf.pbconfig import *

__all__ = ['handle_message']


def handle_age(*args, message_text: str, user_lang_code: str) -> Union[str, dataclass.ResultOperation]:

    recordtype = [item for item in args if type(item) is str and len(item) == LENGHT_TYPE_RECORDING_VAL][0]

    if recordtype in TYPE_RECORDING[:2]:
        try:
            age = int(message_text)
            print(age, '----')
            if not LOWER_AGE_LIMIT <= age <= UPPER_AGE_LIMIT:
                return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[
                    user_lang_code].invalid_t_age)

            return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_city)

        except:
            return dataclass.ResultOperation(status=False,
                                             object=STATEMENTS_BY_LANG[user_lang_code].invalid_v_age)

    elif recordtype == TYPE_RECORDING[2]:
        if auxiliary.check_numbers_in_string(string=message_text) is not None:
            numbers = [i for i in message_text if i.isdigit()]

            if len(numbers) < 4:
                return dataclass.ResultOperation(status=False)

            return dataclass.ResultOperation(status=True)


def handle_city(*args, message_text: str, user_lang_code: str):

    cities = [item for item in args if type(item) is dict and len(item) == AMOUNT_CITIES][0]

    if str.lower(str(message_text)) not in cities:

        simular_cities = auxiliary.get_similar_cities(city=str.lower(message_text),
                                                      cities=cities)

        if simular_cities:
            return dataclass.ResultOperation(status=False,
                                             object=auxiliary.generate_drop_down_cities_list(
                                                 cities_list=simular_cities)
                                             )

        return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].invalid_citi)

    return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_sex)


def handle_description(*args, message_text: str, user_lang_code: str):
    if len(message_text) > MAX_LEN_DESCRIPTION:
        return dataclass.ResultOperation(status=False,
                                         object=STATEMENTS_BY_LANG[user_lang_code].invalid_l_desc.format(
                                             len(message_text)
                                         ))

    return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_photo)


def handle_photo(*args, message_text: str, user_lang_code: str):
    return dataclass.ResultOperation(status=True) \
        if message_text else \
        dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].invalid_t_photo)


def handle_message(
        *args,
        recordstage: str) -> dataclass.ResultOperation:

    """
    args values ---
    1. message text / file id {file id in handle photo}
    2. user lang code
    3. recordtype / cities {handle age, handle city}

    :param args:
    :param recordstage:
    :return: your statement
    """

    print(args[0], '-----666')

    return HANDLE_SCRIPT_BY_RECORDING_STAGE[recordstage](*args, message_text=args[0], user_lang_code=args[1])


HANDLE_SCRIPT_BY_RECORDING_STAGE = {
    'age': handle_age,
    'cty': handle_city,
    'dsc': handle_description,
    'pht': handle_photo,
}
