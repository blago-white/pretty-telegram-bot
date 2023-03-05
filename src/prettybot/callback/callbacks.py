from src.prettybot.callback.callback_keyboards import *
from src.conf.recording_stages import *


def unpack_playload(payload_string: str) -> dict:
    return dict(type_request=payload_string.split('%')[0],
                type_requested_operation=payload_string.split('%')[1])


def get_inline_keyboard_by_stage(stage: int) -> dict:
    if stage == STAGES_RECORDING[1]:
        return INLINE_SEX_KB

    return INLINE_EMPTY_KB
