from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import keyboards

router = Router()

@router.message(Command(commands="help"))
async def help_handler(msg: Message):
    await msg.answer("Если у вас возникли какие либо трудности, то напишите администратору https://t.me/strng_dev")


@router.message()
async def any_message_handler(msg: Message):
    await msg.answer("Простите, не понимаю вас, но я ещё учусь и возможно, в будущем смогу вам ответить",
                     reply_markup=keyboards.main_reply_keyboard()
                     )