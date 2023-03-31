from typing import Union

from src.prettybot.bot.minorscripts import minor_scripts
from src.config.recording_stages import *


def reformat_text_to_db(text: str) -> str:
    return "'{}'".format(text.replace("'", "''").replace("/", ""))


def convert_user_param_value(user_value: Union[str, int], record_strage: str) -> Union[str, bool, str]:
    if record_strage == SEX_STAGE:
        return supportive.convert_sex_type(user_value)

    if type(user_value) == str and not minor_scripts.check_numbers_in_string(string=user_value):
        return reformat_text_to_db(text=user_value)

    return user_value
