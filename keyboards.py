from typing import Optional

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from values import trainings


def main_reply_keyboard(msg: Optional[Message]=None) -> ReplyKeyboardMarkup:
    lay = [
        [
            KeyboardButton(text="📨 Подать заявку 📨"),
            KeyboardButton(text="🗓️ мероприятия 🗓️")
        ],
        [
            KeyboardButton(text="❓ Часто задаваемые вопросы ❓")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=lay, resize_keyboard=True)
    return keyboard


def know_or_dont_keyboard(msg: Optional[Message]=None) -> InlineKeyboardMarkup:
    lay = [
        [
            InlineKeyboardButton(text="У меня есть опыт в IT", callback_data="pro_talent"),
            InlineKeyboardButton(text="Я новичок", callback_data="new_talent")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lay)
    return keyboard


def interrupt_keyboard(msg: Optional[Message]=None) -> InlineKeyboardMarkup:
    lay = [[InlineKeyboardButton(text="Прервать форму", callback_data="interrupt")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lay)
    return keyboard\


def personal_data_agreement_keyboard(msg: Optional[Message]=None) -> InlineKeyboardMarkup:
    lay = [[InlineKeyboardButton(text="Согласиться", callback_data="personal_data_agreement")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lay)
    return keyboard


def spec_keyboard(msg: Optional[Message]=None) -> InlineKeyboardMarkup:
    lay = [
    [InlineKeyboardButton(text='Тестировщик', callback_data='spec_test')],
    [InlineKeyboardButton(text='Project-менеджер', callback_data='spec_proj')],
    [InlineKeyboardButton(text='Дизайнер', callback_data='speс_design')],
    [InlineKeyboardButton(text='Android разработчик', callback_data='spec_a_prog')],
    [InlineKeyboardButton(text='Ios разработчик', callback_data='spec_i_prog')],
    [InlineKeyboardButton(text='Аналитик', callback_data='spec_anal')],
    [InlineKeyboardButton(text='Backend Разработчик', callback_data='spec_backend')],
    [InlineKeyboardButton(text='Разговорный дизайн', callback_data='spec_talk_design')]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=lay)
    return keyboard


def prof_orient_keyboard(msg: Optional[Message]=None) -> InlineKeyboardMarkup:
    lay = [
        [InlineKeyboardButton(text="A", callback_data="tech")],
        [InlineKeyboardButton(text="B", callback_data="desi")],
        [InlineKeyboardButton(text="C", callback_data="mngr")],
        [InlineKeyboardButton(text="Прервать форму", callback_data="interrupt")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lay)
    return keyboard
