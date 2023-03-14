from typing import Union

from src.prettybot.bot.minorscripts import supportive
from src.config.recording_stages import *


def convert_user_param_value(user_value: Union[str, int], record_strage: str) -> Union[str, bool, str]:
    if record_strage == SEX_STAGE:
        return supportive.convert_sex_type(user_value)

    if type(user_value) == str and not supportive.check_numbers_in_string(string=user_value):
        return supportive.correct_text_to_db(text=user_value)

    return user_value
