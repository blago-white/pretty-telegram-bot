from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.etc.config import LANG_STATEMENTS


inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_change'], callback_data='main%change_profile_data')
inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_creator'], url='https://vk.com/l0ginoff')
inline_btn3 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_del_acc'], callback_data='main%del_annotations')
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

inline_btn1 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_en_lang'], callback_data='lang%en_lang_select')
inline_btn2 = InlineKeyboardButton(LANG_STATEMENTS['en']['btn_ru_lang'], callback_data='lang%ru_lang_select')
inline_lang_kb = InlineKeyboardMarkup(row_width=2)
inline_lang_kb.add(inline_btn1, inline_btn2)

inline_empty_kb = InlineKeyboardMarkup()