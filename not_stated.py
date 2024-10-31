from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from pyasn1_modules.rfc2315 import data

import keyboards
import work_with_excel
from config import BOT_API
from aiogram.types import InputFile


router = Router()
bot = Bot(BOT_API)

@router.message(Command(commands="upload_data"))
async def upload_data(msg: Message):
    users_data = work_with_excel.read_from_csv()
    print(users_data)
    work_with_excel.save_to_xlsx(users_data)
    await msg.answer("Загружаю таблицу...")
    await bot.send_document(InputFile("output.xlsx"))


@router.message(Command(commands="help"))
async def help_handler(msg: Message):
    await msg.answer("Если у вас возникли какие либо трудности, то напишите администратору https://t.me/strng_dev")


@router.message()
async def any_message_handler(msg: Message):
    await msg.answer("Простите, не понимаю вас, но я ещё учусь и возможно, в будущем смогу вам ответить",
                     reply_markup=keyboards.main_reply_keyboard()
                     )