from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.conf.config import STATEMENTS_BY_LANG
from src.conf.config import LANG_CODES

inline_profile_kb_by_lang = dict()
inline_kb_change_prof_by_lang = dict()
inline_kb_set_sex_by_lang = dict()
inline_kb_change_params_by_lang = dict()
inline_kb_mode_finding_by_lang = dict()
inline_empty_kb = dict()

for lang_code in LANG_CODES.values():

    inline_empty_kb.update({lang_code: InlineKeyboardMarkup(row_width=1)})

    inline_profile_kb_by_lang.update({lang_code: InlineKeyboardMarkup(row_width=1)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].btn_change,
                        STATEMENTS_BY_LANG[lang_code].btn_start_find,
                        STATEMENTS_BY_LANG[lang_code].btn_creator)

    value_for_buttons = ('main%change_profile_data',
                         'main%start_find',
                         'https://vk.com/l0ginoff')

    inline_profile_kb_by_lang[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons)-1)
        ]
    )

    inline_profile_kb_by_lang[lang_code].add(InlineKeyboardButton(
        text_for_buttons[-1],
        url=value_for_buttons[-1])
    )

    inline_kb_change_prof_by_lang.update({lang_code: InlineKeyboardMarkup(row_width=2)})
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

    inline_kb_change_prof_by_lang[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons))
        ]
    )

    inline_kb_set_sex_by_lang.update({lang_code: InlineKeyboardMarkup(row_width=2)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].man,
                        STATEMENTS_BY_LANG[lang_code].woman)

    value_for_buttons = ('sex%man',
                         'sex%woman')

    inline_kb_set_sex_by_lang[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons))
        ]
    )

    inline_kb_mode_finding_by_lang.update({lang_code: InlineKeyboardMarkup(row_width=1)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].start_find,
                        STATEMENTS_BY_LANG[lang_code].start_fast_find,
                        STATEMENTS_BY_LANG[lang_code].do_clairfy,
                        STATEMENTS_BY_LANG[lang_code].btn_back)

    value_for_buttons = ('find%start&spec',
                         'find%start&fast',
                         'find%clarify',
                         'main%back')

    inline_kb_mode_finding_by_lang[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons))
        ]
    )

    inline_kb_change_params_by_lang.update({lang_code: InlineKeyboardMarkup(row_width=3)})
    text_for_buttons = (STATEMENTS_BY_LANG[lang_code].btn_change_age,
                        STATEMENTS_BY_LANG[lang_code].btn_change_city,
                        STATEMENTS_BY_LANG[lang_code].btn_change_sex,
                        STATEMENTS_BY_LANG[lang_code].btn_back)

    value_for_buttons = ('changewish%change_age',
                         'changewish%change_city',
                         'changewish%change_sex',
                         'find%back')

    inline_kb_change_params_by_lang[lang_code].add(
        *[InlineKeyboardButton(
            text_for_buttons[cycle],
            callback_data=value_for_buttons[cycle]
        )
            for cycle in range(len(value_for_buttons))
        ]
    )
