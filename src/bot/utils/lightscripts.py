from typing import Union

from src.bot.keyboards.callback_keyboards import *
from src.bot.config.recording_stages import *


def convert_sex_type(obj: Union[bool, str]) -> Union[bool, str]:
    if type(obj) is bool:
        return 'man' if obj else 'woman'

    return True if obj == 'man' else False


def get_digits_from_string(string: str) -> int:
    return [int(letter) for letter in string if letter.isdigit()]


def get_inline_keyboard_by_stage(recordstage: str, recordtype: str, user_lang_code: str) -> dict:
    if recordtype == TYPE_RECORDING[0] and recordstage in STAGES_RECORDING[1:3]:
        return INLINE_SEX_KB[user_lang_code]

    elif recordtype == TYPE_RECORDING[2] and recordstage == STAGES_RECORDING[2]:
        return INLINE_SEX_KB[user_lang_code]

    return INLINE_EMPTY_KB


def get_shifted_recordstage_for_main_record_type(record_type: str,
                                                 record_stage: str,
                                                 user_answer_is_valid: bool) -> str:
    if record_type == MAIN_RECORDING_TYPE:
        return record_stage if user_answer_is_valid else STAGES_RECORDING[STAGES_RECORDING.index(record_stage) - 1]
    return record_stage
