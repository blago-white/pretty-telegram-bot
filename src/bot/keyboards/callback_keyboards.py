from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import callback_factories
from ..config.pbconfig import LANG_CODES, STATEMENTS_BY_LANG

INLINE_PROFILE_KB = {lang: InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_change,
        callback_data=callback_factories.PROFILE_CALLS.new(called_operation='change_profile_data')
    )],
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_start_find,
        callback_data=callback_factories.PROFILE_CALLS.new(called_operation='start_find'))],
    [InlineKeyboardButton(text=STATEMENTS_BY_LANG[lang].btn_creator, url='https://vk.com/l0ginoff')]
]) for lang in LANG_CODES.values()
}

INLINE_CHANGE_PROF_DATA_KB = {lang: InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_change_photo,
        callback_data=callback_factories.CHANGING_CALLS.new(called_operation='change_photo')),
     InlineKeyboardButton(
            text=STATEMENTS_BY_LANG[lang].btn_change_age,
            callback_data=callback_factories.CHANGING_CALLS.new(called_operation='change_age'))],
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_change_city,
        callback_data=callback_factories.CHANGING_CALLS.new(called_operation='change_city')),
     InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_change_description,
        callback_data=callback_factories.CHANGING_CALLS.new(called_operation='change_description'))],
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_back,
        callback_data=callback_factories.CHANGING_CALLS.new(called_operation='back'))]
])
    for lang in LANG_CODES.values()
}

INLINE_SEX_KB = {lang: InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].man,
        callback_data=callback_factories.SEX_CALLS.new(called_operation='man')),
     InlineKeyboardButton(
         text=STATEMENTS_BY_LANG[lang].woman,
         callback_data=callback_factories.SEX_CALLS.new(called_operation='woman'))],
])
    for lang in LANG_CODES.values()
}

INLINE_CHANGE_PARAMS_FIND_KB = {lang: InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_change_age,
        callback_data=callback_factories.WISH_CHANGING_CALS.new(called_operation='change_age')),
     InlineKeyboardButton(
         text=STATEMENTS_BY_LANG[lang].btn_change_city,
         callback_data=callback_factories.WISH_CHANGING_CALS.new(called_operation='change_city')),
     InlineKeyboardButton(
         text=STATEMENTS_BY_LANG[lang].btn_change_sex,
         callback_data=callback_factories.WISH_CHANGING_CALS.new(called_operation='change_sex'))],
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_back,
        callback_data=callback_factories.FINDING_MENU_CALS.new(called_operation='back'))]
])
    for lang in LANG_CODES.values()
}

INLINE_MODE_FINDING_KB = {lang: InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].start_fast_find,
        callback_data=callback_factories.FINDING_CALS.new(finding_type='fast')),
     InlineKeyboardButton(
         text=STATEMENTS_BY_LANG[lang].start_find,
         callback_data=callback_factories.FINDING_CALS.new(finding_type='spec'))],
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_back,
        callback_data=callback_factories.PROFILE_CALLS.new(called_operation='back')),
     InlineKeyboardButton(
         text=STATEMENTS_BY_LANG[lang].do_clairfy,
         callback_data=callback_factories.FINDING_MENU_CALS.new(called_operation='clarify'))]
])
    for lang in LANG_CODES.values()
}

INLINE_BUFFERING_QUESTION_KB = {lang: InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_fast_buffering,
        callback_data=callback_factories.BUFFERING_CALLS.new(called_operation='fast')),
     InlineKeyboardButton(
         text=STATEMENTS_BY_LANG[lang].btn_specific_buffering,
         callback_data=callback_factories.BUFFERING_CALLS.new(called_operation='specific'))],
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_back,
        callback_data=callback_factories.FINDING_MENU_CALS.new(called_operation='back'))]
])
    for lang in LANG_CODES.values()
}

INLINE_EXIT_BUFFER_KB = {lang: InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text=STATEMENTS_BY_LANG[lang].btn_exit_buffer,
        callback_data=callback_factories.BUFFERING_CALLS.new(called_operation='back'))]
])
    for lang in LANG_CODES.values()
}

INLINE_EMPTY_KB = {lang: InlineKeyboardMarkup(inline_keyboard=[[]]) for lang in LANG_CODES.values()}
