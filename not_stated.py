from aiogram import Router
from aiogram.types import Message

import keyboards

router = Router()
@router.message()
async def any_message_handler(msg: Message):
    await msg.answer("Простите, не понимаю вас, но я ещё учусь и возможно, в будущем смогу вам ответить",
                     reply_markup=keyboards.main_reply_keyboard()
                     )