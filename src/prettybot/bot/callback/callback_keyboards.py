from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.config.pbconfig import STATEMENTS_BY_LANG
from src.config.pbconfig import LANG_CODES

INLINE_PROFILE_KB = dict()
INLINE_CHANGE_PROF_DATA_KB = dict()
INLINE_SEX_KB = dict()
INLINE_CHANGE_PARAMS_FIND_KB = dict()
INLINE_MODE_FINDING_KB = dict()
INLINE_BUFFERING_QUESTION_KB = dict()
INLINE_EXIT_BUFFER_KB = dict()
INLINE_EMPTY_KB = dict()

KEYBOARDS = (INLINE_PROFILE_KB,
             INLINE_CHANGE_PROF_DATA_KB,
             INLINE_SEX_KB,
             INLINE_CHANGE_PARAMS_FIND_KB,
             INLINE_MODE_FINDING_KB,
             INLINE_BUFFERING_QUESTION_KB,
             INLINE_EXIT_BUFFER_KB,
             INLINE_EMPTY_KB)

KEYBOARD_INDEXES = {
    0: INLINE_PROFILE_KB,
    1: INLINE_CHANGE_PROF_DATA_KB,
    2: INLINE_SEX_KB,
    3: INLINE_CHANGE_PARAMS_FIND_KB,
    4: INLINE_MODE_FINDING_KB,
    5: INLINE_BUFFERING_QUESTION_KB,
    6: INLINE_EXIT_BUFFER_KB,
    7: INLINE_EMPTY_KB
}

KEYBOARD_ROWS = dict(
    INLINE_PROFILE_KB=1,
    INLINE_CHANGE_PROF_DATA_KB=2,
    INLINE_SEX_KB=2,
    INLINE_CHANGE_PARAMS_FIND_KB=3,
    INLINE_MODE_FINDING_KB=2,
    INLINE_BUFFERING_QUESTION_KB=2,
    INLINE_EXIT_BUFFER_KB=1,
    INLINE_EMPTY_KB=1)

KEYBOARD_NAMES = {
    0: 'INLINE_PROFILE_KB',
    1: 'INLINE_CHANGE_PROF_DATA_KB',
    2: 'INLINE_SEX_KB',
    3: 'INLINE_CHANGE_PARAMS_FIND_KB',
    4: 'INLINE_MODE_FINDING_KB',
    5: 'INLINE_BUFFERING_QUESTION_KB',
    6: 'INLINE_EXIT_BUFFER_KB',
    7: 'INLINE_EMPTY_KB'
}

KEYBOARD_VALUES = {
    0: (),
    1: ('change%change_photo',
        'change%change_age',
        'change%change_city',
        'change%change_description',
        'change%back'),
    2: ('sex%man', 'sex%woman'),
    3: ('changewish%change_age', 'changewish%change_city', 'changewish%change_sex', 'find%back'),
    4: ('find%start&fast', 'find%start&spec', 'main%back', 'find%clarify'),
    5: ('buffer%fast', 'buffer%specific', 'main%back'),
    6: ('buffer%back', ),
    7: ()
}

KEYBOARD_TEXT_VALUES = {
    0: (),
    1: {'ru': (STATEMENTS_BY_LANG['ru'].btn_change_photo,
               STATEMENTS_BY_LANG['ru'].btn_change_age,
               STATEMENTS_BY_LANG['ru'].btn_change_city,
               STATEMENTS_BY_LANG['ru'].btn_change_description,
               STATEMENTS_BY_LANG['ru'].btn_back),

        'en': (STATEMENTS_BY_LANG['en'].btn_change_photo,
               STATEMENTS_BY_LANG['en'].btn_change_age,
               STATEMENTS_BY_LANG['en'].btn_change_city,
               STATEMENTS_BY_LANG['en'].btn_change_description,
               STATEMENTS_BY_LANG['en'].btn_back)},

    2: {'en': (STATEMENTS_BY_LANG['en'].man,
               STATEMENTS_BY_LANG['en'].woman),
        'ru': (STATEMENTS_BY_LANG['ru'].man,
               STATEMENTS_BY_LANG['ru'].woman)},

    3: {'en': (STATEMENTS_BY_LANG['en'].btn_change_age,
               STATEMENTS_BY_LANG['en'].btn_change_city,
               STATEMENTS_BY_LANG['en'].btn_change_sex,
               STATEMENTS_BY_LANG['en'].btn_back),
        'ru': (STATEMENTS_BY_LANG['ru'].btn_change_age,
               STATEMENTS_BY_LANG['ru'].btn_change_city,
               STATEMENTS_BY_LANG['ru'].btn_change_sex,
               STATEMENTS_BY_LANG['ru'].btn_back)},

    4: {'en': (STATEMENTS_BY_LANG['en'].start_fast_find,
               STATEMENTS_BY_LANG['en'].start_find,
               STATEMENTS_BY_LANG['en'].btn_back,
               STATEMENTS_BY_LANG['en'].do_clairfy),
        'ru': (STATEMENTS_BY_LANG['ru'].start_fast_find,
               STATEMENTS_BY_LANG['ru'].start_find,
               STATEMENTS_BY_LANG['ru'].btn_back,
               STATEMENTS_BY_LANG['ru'].do_clairfy)},

    5: {'en': (STATEMENTS_BY_LANG['en'].btn_fast_buffering,
               STATEMENTS_BY_LANG['en'].btn_specific_buffering,
               STATEMENTS_BY_LANG['en'].btn_back),
        'ru': (STATEMENTS_BY_LANG['ru'].btn_fast_buffering,
               STATEMENTS_BY_LANG['ru'].btn_specific_buffering,
               STATEMENTS_BY_LANG['ru'].btn_back)},

    6: {'en': (STATEMENTS_BY_LANG['en'].btn_exit_buffer, ),
        'ru': (STATEMENTS_BY_LANG['ru'].btn_exit_buffer, )},

    7: {'en': (), 'ru': ()}
}


def _fill_keyboard(keyboard: dict, language: str, row_width: int, value_for_btns: dict, text_for_btns: dict):
    keyboard.update({language: InlineKeyboardMarkup(row_width=row_width)})

    buttons = [InlineKeyboardButton(text_for_btns[language][cycle], callback_data=value_for_btns[cycle])
               for cycle in range(len(value_for_btns))
               ]

    keyboard[language].add(*buttons)


def _create_keyboard(keyboard_index: dict):
    rows = KEYBOARD_ROWS[KEYBOARD_NAMES[keyboard_index]]
    value_for_btns = KEYBOARD_VALUES[keyboard_index]
    text_for_btns = KEYBOARD_TEXT_VALUES[keyboard_index]
    keyboard = KEYBOARD_INDEXES[keyboard_index]

    for index, language in enumerate(LANG_CODES.values()):
        _fill_keyboard(keyboard=keyboard,
                       language=language,
                       row_width=rows,
                       value_for_btns=value_for_btns,
                       text_for_btns=text_for_btns)


def _set_inline_profile_kb():
    global INLINE_PROFILE_KB

    INLINE_PROFILE_KB = {'en': InlineKeyboardMarkup(row_width=1), 'ru': InlineKeyboardMarkup(row_width=1)}
    value_for_buttons = ('main%change_profile_data',
                         'main%start_find',
                         'https://vk.com/l0ginoff')

    for lang in LANG_CODES.values():
        text_for_buttons = (STATEMENTS_BY_LANG[lang].btn_change,
                            STATEMENTS_BY_LANG[lang].btn_start_find,
                            STATEMENTS_BY_LANG[lang].btn_creator)

        INLINE_PROFILE_KB[lang].add(
            *[InlineKeyboardButton(
                text_for_buttons[cycle],
                callback_data=value_for_buttons[cycle]
            )
                for cycle in range(len(value_for_buttons) - 1)
            ]
        )

        INLINE_PROFILE_KB[lang].add(InlineKeyboardButton(
            text_for_buttons[-1],
            url=value_for_buttons[-1])
        )


def _main():
    for idx in range(1, len(KEYBOARDS)):
        _create_keyboard(keyboard_index=idx)

    _set_inline_profile_kb()


_main()
