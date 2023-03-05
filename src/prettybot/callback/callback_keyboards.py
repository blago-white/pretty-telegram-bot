from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.conf.pbconfig import STATEMENTS_BY_LANG
from src.conf.pbconfig import LANG_CODES

INLINE_PROFILE_KB = dict()
INLINE_CHANGE_PROF_DATA_KB = dict()
INLINE_SEX_KB = dict()
INLINE_CHANGE_PARAMS_FIND_KB = dict()
INLINE_MODE_FINDING_KB = dict()
INLINE_EMPTY_KB = dict()

for lang_code in LANG_CODES.values():

    INLINE_EMPTY_KB.update({lang_code: InlineKeyboardMarkup(row_width=1)})

    INLINE_PROFILE_KB.update({lang_code: InlineKeyboardMarkup(row_width=1)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].btn_change,
                        STATEMENTS_BY_LANG[lang_code].btn_start_find,
                        STATEMENTS_BY_LANG[lang_code].btn_creator)

    value_for_buttons = ('main%change_profile_data',
                         'main%start_find',
                         'https://vk.com/l0ginoff')

    INLINE_PROFILE_KB[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons)-1)
        ]
    )

    INLINE_PROFILE_KB[lang_code].add(InlineKeyboardButton(
        text_for_buttons[-1],
        url=value_for_buttons[-1])
    )

    INLINE_CHANGE_PROF_DATA_KB.update({lang_code: InlineKeyboardMarkup(row_width=2)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].btn_change_photo,
                        STATEMENTS_BY_LANG[lang_code].btn_change_age,
                        STATEMENTS_BY_LANG[lang_code].btn_change_city,
                        STATEMENTS_BY_LANG[lang_code].btn_change_description,
                        STATEMENTS_BY_LANG[lang_code].btn_back)

    value_for_buttons = ('change%change_photo',
                         'change%change_age',
                         'change%change_city',
                         'change%change_description',
                         'change%back')

    INLINE_CHANGE_PROF_DATA_KB[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons))
        ]
    )

    INLINE_SEX_KB.update({lang_code: InlineKeyboardMarkup(row_width=2)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].man,
                        STATEMENTS_BY_LANG[lang_code].woman)

    value_for_buttons = ('sex%man',
                         'sex%woman')

    INLINE_SEX_KB[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons))
        ]
    )

    INLINE_MODE_FINDING_KB.update({lang_code: InlineKeyboardMarkup(row_width=1)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].start_find,
                        STATEMENTS_BY_LANG[lang_code].start_fast_find,
                        STATEMENTS_BY_LANG[lang_code].do_clairfy,
                        STATEMENTS_BY_LANG[lang_code].btn_back)

    value_for_buttons = ('find%start&spec',
                         'find%start&fast',
                         'find%clarify',
                         'main%back')

    INLINE_MODE_FINDING_KB[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons))
        ]
    )

    INLINE_CHANGE_PARAMS_FIND_KB.update({lang_code: InlineKeyboardMarkup(row_width=3)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].btn_change_age,
                        STATEMENTS_BY_LANG[lang_code].btn_change_city,
                        STATEMENTS_BY_LANG[lang_code].btn_change_sex,
                        STATEMENTS_BY_LANG[lang_code].btn_back)

    value_for_buttons = ('changewish%change_age',
                         'changewish%change_city',
                         'changewish%change_sex',
                         'find%back')

    INLINE_CHANGE_PARAMS_FIND_KB[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons))
        ]
    )
