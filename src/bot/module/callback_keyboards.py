from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.etc.config import LANG_STATEMENTS


inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change'], callback_data='main%change_profile_data')
inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_creator'], url='https://vk.com/l0ginoff')
inline_btn3 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_start_find'], callback_data='main%btn_start_find')
inline_profile_kb_en = InlineKeyboardMarkup(row_width=1)
inline_profile_kb_en.add(inline_btn1, inline_btn3, inline_btn2)

inline_profile_kb_by_lang = {'en': inline_profile_kb_en}

inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_photo'],
                                   callback_data='change%change_photo')

inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_age'],
                                   callback_data='change%change_age')

inline_btn3 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_city'],
                                   callback_data='change%change_city')

inline_btn4 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_description'],
                                   callback_data='change%change_description')

inline_btn5 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_back'],
                                   callback_data='change%back')

inline_kb_change_prof_en = InlineKeyboardMarkup(row_width=2)
inline_kb_change_prof_en.add(inline_btn2, inline_btn3, inline_btn4, inline_btn1, inline_btn5)

inline_kb_change_prof_by_lang = {'en': inline_kb_change_prof_en}

inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['man'], callback_data='sex%man')
inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['woman'], callback_data='sex%woman')

inline_kb_set_sex_en = InlineKeyboardMarkup(row_width=2)
inline_kb_set_sex_en.add(inline_btn1, inline_btn2)

inline_kb_set_sex_by_lang = {'en': inline_kb_set_sex_en}

inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['start_find'], callback_data='find%start')
inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['do_clairfy'], callback_data='find%clarify')
inline_btn3 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_back'], callback_data='main%back')
inline_kb_mode_finding_en = InlineKeyboardMarkup(row_width=1)
inline_kb_mode_finding_en.add(inline_btn1, inline_btn2, inline_btn3)

inline_kb_mode_finding_by_lang = {'en': inline_kb_mode_finding_en}

inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_age'],
                                   callback_data='change_wish%change_age')

inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_city'],
                                   callback_data='change_wish%change_city')

inline_btn3 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change_sex'],
                                   callback_data='change_wish%change_sex')

inline_btn4 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_back'],
                                   callback_data='find%back')

inline_kb_change_params_en = InlineKeyboardMarkup(row_width=3)
inline_kb_change_params_en.add(inline_btn1, inline_btn2, inline_btn3, inline_btn4)

inline_kb_change_params_by_lang = {'en': inline_kb_change_params_en}

inline_empty_kb = InlineKeyboardMarkup()
