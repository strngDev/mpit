import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import config
import asyncio

import fsm_dont_know
import fsm_know
import keyboards
import not_stated

# bot init
bot = Bot(token=config.BOT_API)
dp = Dispatcher()
dp.include_router(fsm_know.router)
dp.include_router(fsm_dont_know.router)
dp.include_router(not_stated.router)




@dp.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(f"Добро пожаловать, {msg.from_user.full_name}!", reply_markup=keyboards.main_reply_keyboard())


@dp.message(F.text == "📨 Подать заявку 📨")
async def personal_data_agreement(msg: Message):
    await msg.answer("Для продолжения необходимо принять соглашение на обработку персональных данных",
                     reply_markup=keyboards.personal_data_agreement_keyboard()
                     )


@dp.callback_query(F.data == "personal_data_agreement")
async def submit_application_handler(callback: CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await bot.send_message(callback.message.chat.id, "Отлично! Пожалуйста укажите, есть ли у вас опыт или вы впервые в it",
                     reply_markup=keyboards.know_or_dont_keyboard())


@dp.message(F.text == "❓ Часто задаваемые вопросы ❓")
async def faq_handler(msg: Message):
    await msg.answer(open("faq.txt", "r").read())


@dp.message(F.text == "🗓️ мероприятия 🗓️")
async def events_handler(msg: Message):
    await msg.answer("На данный момент, нет ни одного активного мероприятия, возвращайтесь позже!")


async def main():
    await dp.start_polling(bot)


logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
asyncio.run(main())