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


def interupt_keyboard(msg: Optional[Message]=None) -> InlineKeyboardMarkup:
    lay = [[InlineKeyboardButton(text="Прервать форму", callback_data="interrupt")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lay)
    return keyboard


def spec_keyboard(msg: Optional[Message]=None) -> InlineKeyboardMarkup:
    lay = [[InlineKeyboardButton(text=j, callback_data=i)] for i,j in trainings.items()]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lay)
    return keyboard


def personal_data_agreement_keyboard(msg: Optional[Message]=None) -> InlineKeyboardMarkup:
    lay = [[InlineKeyboardButton(text="Согласиться", callback_data="personal_data_agreement")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lay)
    return keyboard

